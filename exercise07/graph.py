from collections.abc import Iterable
from enum import Enum, auto, unique
from typing import NamedTuple

import networkx as nx


class OpType(Enum):
    """Supported operations types for the DSES synthesis flow"""

    Constant = auto()
    And = auto()
    Xor = auto()
    Or = auto()
    Nor = auto()
    Invert = auto()
    Nand = auto()
    Add = auto()
    Sub = auto()
    Mult = auto()
    LShift = auto()
    RShift = auto()
    Eq = auto()
    NotEq = auto()
    Lt = auto()
    LtE = auto()
    Gt = auto()
    GtE = auto()

    def __str__(self):
        return self.name


# Node Attribute
class Attr(NamedTuple):
    """Attributes for an operation node of the DSES synthesis flow"""

    op_type: OpType
    exec_time: int
    area: float
    scheduled_time: int


class DSESGraph:
    """Wrapper around a networkx graph, tuned for VLSI algorithms"""

    def __init__(self):
        # Control Flow Graph
        self._GRAPH = nx.DiGraph()
        self._GRAPH.graph["splines"] = "false"
        # Node Attribute Map: dict[int, attribute]
        self._node_attributes = dict()

    @property
    def GRAPH(self):
        return self._GRAPH

    @property
    def node_attributes(self):
        return self._node_attributes

    # Helper functions returns id of new node or 0 if no nodes exist
    def get_new_node_id(self):
        if len(self._node_attributes):
            return max(self._node_attributes.keys()) + 1
        else:
            return 0

    def get_total_area(self):
        return sum([n.area for n in self._node_attributes.values()])

    # gets new node id, creates node and adds it to Graph
    def add_node(self, op_type: OpType, exec_time: int = 1, area: float = 0.0, children=None):
        node_id = self.get_new_node_id()
        self._node_attributes[node_id] = Attr(op_type, exec_time, area, -1)
        self._GRAPH.add_node(node_id)
        self._GRAPH.nodes[node_id]["label"] = str(self._node_attributes[node_id].op_type)
        if children is not None:
            if isinstance(children, Iterable):
                for v in children:
                    self.add_edge(node_id, v)
            else:
                self.add_edge(node_id, children)
        return node_id

    # adds edge from node u to node v
    def add_edge(self, u: int, v: int):
        if not (self._node_attributes.get(u, False) and self._node_attributes.get(v, False)):
            RuntimeWarning(f'Node "{u}" or Node "{v}" does not exist')
        self._GRAPH.add_edge(u, v)
        self._GRAPH[u][v]["parent_type"] = self._GRAPH.nodes[u]["label"]
        self._GRAPH[u][v]["child_type"] = self._GRAPH.nodes[v]["label"]

    def reset_graph(self):
        for n in self._GRAPH.nodes:
            self._GRAPH.nodes[n]["fillcolor"] = "white"
            self._GRAPH.nodes[n]["label"] = str(self._node_attributes[n].op_type)
            if n not in self._node_attributes:
                self._GRAPH.delte_node(n)
        for n, v in self._node_attributes.items():
            self._node_attributes[n] = self._node_attributes[n]._replace(scheduled_time=-1)
        for e in self._GRAPH.edges:
            self._GRAPH.edges[e]["label"] = ""

    # transforms the graph to dot Graph and creates pdf of graph
    def graph_to_dot(self, fn="graph"):
        import pathlib
        from subprocess import check_call

        fp = pathlib.Path(__file__).parent.absolute() / f"{fn}.dot"
        nx.drawing.nx_agraph.write_dot(self._GRAPH, fp)
        check_call(["dot", "-Tpdf", fp, "-o", f"{fn}.pdf"])
        if fp.exists():
            fp.unlink()

    # transforms the graph to dot Graph and creates pdf of graph
    def schedule_to_dot(self, fn):
        import graphviz as gv

        levels = dict()
        for n, v in self._node_attributes.items():
            levels[v.scheduled_time] = [n] + levels.get(v.scheduled_time, list())

        hidden = list()
        for i in range(max(levels.keys())):
            if i not in levels:
                # Create hidden node
                node_id = f"hidden{i}"
                levels[i] = [node_id]
                hidden += [i]

        # Define Graph
        dot = gv.Digraph("schedule")
        dot.attr(splines="false")
        dot.attr(outputorder="edgesfirst")

        # Define Subgraphs
        for i, ns in sorted(levels.items(), key=lambda x: x[0]):
            sg = gv.Digraph(f"level{i}")
            sg.attr(rank="same")
            # Define number node
            numbernode = f"numbernode{i}"
            sg.node(numbernode, label=str(i), shape="plaintext", group="left")
            sg.edge(numbernode, str(ns[0]), style="invis")
            # Define anker node
            ankernode = f"ankernode{i}"
            sg.node(ankernode, style="invis", group="right")
            sg.edge(str(ns[-1]), ankernode, style="invis")
            for n in ns:
                if i in hidden:
                    sg.node(
                        str(n),
                        style="invis",
                    )
                else:
                    sg.node(
                        str(n),
                        label=str(self._node_attributes[n].op_type) + ":" + str(n),
                        style="filled",
                        fillcolor=self._GRAPH.nodes[n]["fillcolor"],
                    )
            # Force Ordering
            for u, v in zip(ns[:-1], [ns[(j + 1) % len(ns)] for j, x in enumerate(ns)][:-1]):
                sg.edge(str(u), str(v), style="invis")

            dot.subgraph(sg)

        # Define Edges
        for u, v in self._GRAPH.edges:
            e = self._GRAPH.get_edge_data(u, v, None)
            if e:
                dot.edge(str(u), str(v), label=e["label"])

        # Define Hidden Edges
        for i in range(max(levels.keys()) + 1):
            if levels.get(i + 1, None) is not None:
                dot.edge(
                    str(levels[i][0]),
                    str(levels[i + 1][0]),
                    ltail=f"level{i + 1}",
                    style="invis",
                )
                dot.edge(f"numbernode{i}", f"numbernode{i + 1}", style="invis")
                dot.edge(f"ankernode{i}", f"ankernode{i + 1}", style="invis")
            dot.edge(f"numbernode{i}", f"ankernode{i}", style="dotted", dir="none")

        import pathlib

        dot_file = pathlib.Path(fn).absolute()
        dot.render(pathlib.Path(__file__).parent.absolute() / dot_file, format="pdf")
        if dot_file.exists():
            dot_file.unlink()

    # applies asap Algorithm on the Graph
    def asap(self):
        self.reset_graph()
        for n in nx.topological_sort(self._GRAPH):
            if len(list(self._GRAPH.predecessors(n))):
                self._node_attributes[n] = self._node_attributes[n]._replace(
                    scheduled_time=(
                        # finds slowest predecessor node and calculate schedule time of current node
                        # by adding exec_time and schedule_time
                        self._node_attributes[
                            max(
                                self._GRAPH.predecessors(n),
                                key=lambda x: self._node_attributes[x].scheduled_time
                                + self._node_attributes[x].exec_time,
                            )
                        ].scheduled_time
                        + self._node_attributes[
                            max(
                                self._GRAPH.predecessors(n),
                                key=lambda x: self._node_attributes[x].scheduled_time
                                + self._node_attributes[x].exec_time,
                            )
                        ].exec_time
                    )
                )
            else:
                # if no predecessors default to scheduling at time 0
                self._node_attributes[n] = self._node_attributes[n]._replace(scheduled_time=0)

    # applies alap Algorithm on the Graph
    def alap(self, goal: int):
        self.reset_graph()
        for n in reversed(list(nx.topological_sort(self._GRAPH))):
            if len(list(self._GRAPH.successors(n))):
                self._node_attributes[n] = self._node_attributes[n]._replace(
                    # finds fastest succsessor node and calculate schedule time of current node
                    # by subtracting schedule time of succsessor with exec_time of current node
                    scheduled_time=(
                        self._node_attributes[
                            min(
                                self._GRAPH.successors(n),
                                key=lambda x: self._node_attributes[x].scheduled_time,
                            )
                        ].scheduled_time
                        - self._node_attributes[n].exec_time
                    )
                )
            else:
                # if no predecessors default to schedule node at goal-1
                self._node_attributes[n] = self._node_attributes[n]._replace(
                    scheduled_time=goal - 1
                )
        for n, v in self._node_attributes.items():
            # if schedule is not possible
            if v.scheduled_time < 0:
                raise RuntimeError(f'Cannot schedule with ALAP goal "{goal}"')

    # Assign each node to a ressource
    def ressource_binding(self, hls_lib):
        # For simplicity reasons, our setup does not allow that multiple function units can execute the same operation type
        for i, c0 in hls_lib:
            for j, c1 in hls_lib:
                if (i != j) and any([(o in c1) for o in c0]):
                    raise RuntimeError(
                        "HLS Lib operations can only be execution by single computational unit"
                    )

        # Check that each nodes can be assigned to a function unit
        for n, t in self._node_attributes.items():
            if not any([t.op_type in c for _, c in hls_lib]):
                raise RuntimeError(f'HLS Lib does not contain op type "{t.op_type}"')

        # Each function unit gets its own color
        def random_color():
            import random

            def rand():
                return random.randint(100, 255)

            return "#%02X%02X%02X" % (rand(), rand(), rand())

        # Undirected Graph
        comp_graph = nx.Graph()

        # Add all nodes
        for n in self._node_attributes.keys():
            comp_graph.add_node(n)
            comp_graph.nodes[n]["label"] = str(self._node_attributes[n].op_type) + ":" + str(n)

        # TODO START
        # 1. Add edges
        node_ids = list(self._GRAPH.nodes)
        for i in range(len(node_ids)):
            for j in range(i + 1, len(node_ids)):
                u = node_ids[i]
                v = node_ids[j]
                u_attr = self._node_attributes[u]
                v_attr = self._node_attributes[v]

                # Same Type?
                if u_attr.op_type != v_attr.op_type:
                    continue

                u_start = u_attr.scheduled_time
                u_end = u_start + u_attr.exec_time
                v_start = v_attr.scheduled_time
                v_end = v_start + v_attr.exec_time

                # Not scheduled at the same time?
                if (u_end <= v_start) or (v_end <= u_start):
                    comp_graph.add_edge(u, v)

        # 2. Make cliques
        comp_graph_complement = nx.complement(comp_graph)
        coloring = nx.coloring.greedy_color(comp_graph_complement, strategy='largest_first')
        color_to_nodes = dict()
        for node, color in coloring.items():
            color_to_nodes.setdefault(color, []).append(node)

        unique_cliques = list(color_to_nodes.values())
        # TODO END

        # Get the clique coverage number
        k = max(unique_cliques, key=lambda x: len(x))

        # Color each opertion with the color of the clique it gets assigned to.
        for l in unique_cliques:
            rc = random_color()
            for n in l:
                self._GRAPH.nodes[n]["fillcolor"] = rc
                comp_graph.nodes[n]["fillcolor"] = rc
                comp_graph.nodes[n]["style"] = "filled"

        # Annotate function unit types and return
        return [
            (
                [i for i, comp_unit in hls_lib if self._node_attributes[c[0]].op_type in comp_unit][
                    0
                ],
                c,
            )
            for c in unique_cliques
        ], k

    # resource binding end

    # This function perform a register allocation using the left edge algorithm on the graphs' edges
    def register_allocation(self):
        # TODO START
        # 1. Create intervals based on edges
        intervals = []
        for i, (u, v) in enumerate(self._GRAPH.edges):
            start = self._node_attributes[u].scheduled_time
            end = self._node_attributes[v].scheduled_time
            intervals.append((i, start, end))

        # sort intervals by start time (index 1)
        intervals.sort(key=lambda x: (x[1], -(x[2] - x[1])))
    

        # 2. LEA algorithm ``push all intervals to the left``

        # This the intervals similar to the LEA algorithm in the lecture
        LEA_bins = [[intervals[0]]]

        # Sort the intervals into bins, if they do not overlap with an interval that is already in the bin
        for i, b, e in intervals[1:]:
            added = False
            for k, l in enumerate(LEA_bins):
                # Check if the intervals overlap, if so move to new bin
                if all(not (b < e2 and e > b2) for _, b2, e2 in l):
                    l.append((i, b, e))
                    added = True
                    break

            # Create new bin as no bin was found
            if not added:
                LEA_bins += [[(i, b, e)]]

        # TODO END

        # Assign labels to each edge that show the associated bin, i.e., which register they get assigned to.
        for i, e in enumerate(self._GRAPH.edges):
            self._GRAPH.edges[e]["label"] = (
                "edge: "
                + str(i)
                + ", reg: "
                + str([j for j, l in enumerate(LEA_bins) for (k, _, _) in l if i == k][0])
            )

        return {i: [j for (j, _, _) in l] for i, l in enumerate(LEA_bins)}

    def apply_resource_binding(self):
        rb, k = self.ressource_binding(HLS_LIB)
        print(f"Ressource Binding (k = {k}), requires {len(rb)} units, with node mapping:")
        for i, l in rb:
            print(f"Function unit instance {i} computes nodes: {l}")
        print()

    def apply_register_allocation(self):
        ra = self.register_allocation()
        print(f"Register Binding, requires {len(ra)} register, with edge mapping:")
        for i, l in ra.items():
            print(f"Register {i} stores values of edges: {l}")
        print()





if __name__ == "__main__":
    # HLS Lib example from lecture
    HLS_LIB = list(
        enumerate(
            [
                [  # FU 0
                    OpType.Mult,
                ],
                [  # FU 1
                    OpType.Add,
                    OpType.Gt,
                    OpType.Sub,
                ],
            ]
        )
    )

    # Graph example from lecture
    G1 = DSESGraph()
    g1_n0 = G1.add_node(OpType.Sub)
    g1_n1 = G1.add_node(OpType.Sub, children=g1_n0)
    g1_n2 = G1.add_node(OpType.Gt)
    g1_n3 = G1.add_node(OpType.Add)
    g1_n4 = G1.add_node(OpType.Mult, children=g1_n0)
    g1_n5 = G1.add_node(OpType.Mult, children=g1_n1)
    g1_n6 = G1.add_node(OpType.Add, children=g1_n2)
    g1_n7 = G1.add_node(OpType.Mult, children=g1_n3)
    g1_n8 = G1.add_node(OpType.Mult, children=g1_n4)
    g1_n9 = G1.add_node(OpType.Mult, children=g1_n5)
    g1_n10 = G1.add_node(OpType.Mult, children=g1_n5)
    G1.graph_to_dot("g1")

    G2 = DSESGraph()
    g2_n0 = G2.add_node(OpType.Mult)
    g2_n1 = G2.add_node(OpType.Add, children=g2_n0)
    g2_n2 = G2.add_node(OpType.Mult, children=g2_n0)
    g2_n3 = G2.add_node(OpType.Add, children=[g2_n1, g2_n2])
    G2.graph_to_dot("g2")

    G3 = DSESGraph()
    g3_n0 = G3.add_node(OpType.Sub)
    g3_n1 = G3.add_node(OpType.Add, children=g3_n0)
    g3_n2 = G3.add_node(OpType.Gt, children=g3_n1)
    g3_n3 = G3.add_node(OpType.Add, children=g3_n2)
    g3_n4 = G3.add_node(OpType.Mult, children=g3_n2)
    g3_n5 = G3.add_node(OpType.Mult, children=[g3_n3, g3_n4])
    G3.graph_to_dot("g3")




    # Schedule (use either)
    G1.asap()
    G2.asap()
    G3.asap()
    G3.alap(goal=max(attr.scheduled_time + attr.exec_time for attr in G3.node_attributes.values()))

    G1.schedule_to_dot("g1_scheduled_graph")
    G2.schedule_to_dot("g2_scheduled_graph")
    G3.schedule_to_dot("g3_scheduled_graph")

    if True:  # Enable me when implemented
        # Ressource binding
        G1.apply_resource_binding()
        G2.apply_resource_binding()
        G3.apply_resource_binding()

    G1.schedule_to_dot("g1_bound_graph")
    G2.schedule_to_dot("g2_bound_graph")
    G3.schedule_to_dot("g3_bound_graph")

    if True:  # Enable me when implemented
        # Register Allocation
        G1.apply_register_allocation()
        G2.apply_register_allocation()
        G3.apply_register_allocation()

    # Print schedule, with coloring and edgle labeling (when implemented)
    G1.schedule_to_dot("g1_bound_and_allocated_graph")
    G2.schedule_to_dot("g2_bound_and_allocated_graph")
    G3.schedule_to_dot("g3_bound_and_allocated_graph")