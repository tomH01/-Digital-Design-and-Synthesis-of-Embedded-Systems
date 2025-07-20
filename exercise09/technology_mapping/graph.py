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

    def compute_Nv(self, v):
        reversed_graph = self._GRAPH.reverse()
        return set(nx.descendants(reversed_graph, v)).union({v})

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

        # Built compatability graph. Each node is compatible to another node when they can be executed on the same ressource but are not scheduled in the same timestep.
        for n, t in self._node_attributes.items():
            i, cu = [
                (i, comp_unit)
                for i, comp_unit in hls_lib
                if self._node_attributes[n].op_type in comp_unit
            ][0]

            for m, tt in self._node_attributes.items():
                j, cuu = [
                    (i, comp_unit)
                    for i, comp_unit in hls_lib
                    if self._node_attributes[m].op_type in comp_unit
                ][0]

                # We constrain that for each function unit, only a single instance is allowed.
                if (i == j) and (t.scheduled_time != tt.scheduled_time):
                    comp_graph.add_edge(n, m)

        # Get all cliques of comp. graph
        # Sort from largest to smallest.
        cliques = sorted(
            list(nx.enumerate_all_cliques(comp_graph)),
            key=lambda x: len(x),
            reverse=True,
        )

        # Find minimal amount of cliques required to
        acc = set()
        unique_cliques = list()
        for c in cliques:
            if len(set(c).intersection(acc)):
                continue
            else:
                unique_cliques += [c]
            acc = acc.union(set(c))

        # Get the clique coverage numbeor
        k = len(unique_cliques)

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
        # Create intervals based on edges, we don't use backedges
        intervals = sorted(
            [
                (
                    i,
                    self._node_attributes[u].scheduled_time,
                    self._node_attributes[v].scheduled_time,
                )
                for i, (u, v) in enumerate(self._GRAPH.edges())
            ],
            key=lambda x: x[0],
        )

        # This the intervals similar to the LEA algorithm in the lecture
        LEA_bins = [[intervals[0]]]

        # Sort the intervals into bins, if they do not overlap with an interval that is already in the bin
        for i, b, e in intervals[1:]:
            added = False
            for k, l in enumerate(LEA_bins):
                # Check if the intervals overlap, if so move to new bin
                if any([(b < bb) and (e > bb) or (b >= bb) and (ee > b) for (j, bb, ee) in l]):
                    continue
                else:
                    LEA_bins[k] += [(i, b, e)]
                    added = True
                    break

            # Create new bin as no bin was found
            if not added:
                LEA_bins += [[(i, b, e)]]

        # Assign labels to each edge that show the associated bin, i.e., which register they get assigned to.
        for i, e in enumerate(self._GRAPH.edges):
            self._GRAPH.edges[e]["label"] = (
                "edge: "
                + str(i)
                + ", reg: "
                + str([j for j, l in enumerate(LEA_bins) for (k, _, _) in l if i == k][0])
            )

        return {i: [j for (j, _, _) in l] for i, l in enumerate(LEA_bins)}

    # flowmap algorithm
    def flow_map(self, K):
        import itertools

        Nv = {n: self.compute_Nv(n) for n in self._node_attributes.keys()}
        PI = [n for n in self._node_attributes.keys() if self._GRAPH.in_degree(n) == 0]
        PO = [n for n in self._node_attributes.keys() if self._GRAPH.out_degree(n) == 0]
        GATES = [n for n in self._node_attributes.keys() if n not in PI and n not in PO]

        # Labels
        l = {n: 0 for n in self._node_attributes.keys() if self._GRAPH.in_degree(n) == 0}

        # Compute all K-Cones
        K_cones = {}
        for v in GATES + PO:
            subgraph = self._GRAPH.subgraph(Nv[v])

            all_connected_subgraphs = []
            for nb_nodes in range(1, subgraph.number_of_nodes() + 1):
                for sg_seg in itertools.combinations(subgraph, nb_nodes):
                    # Make subgraph of all nodes in Nv combination, without primary nodes
                    sg_seg = list(set(sg_seg).difference(set(PI)).union({v}))
                    sg = subgraph.subgraph(sg_seg)

                    # Gather all incoming edges
                    incoming_edges = [
                        (n, m)
                        for n in set(self._GRAPH.nodes).difference(set(sg.nodes))
                        for m in sg.nodes
                        if self._GRAPH.has_edge(n, m)
                    ]

                    # Count unique edges
                    edges = 0
                    while len(incoming_edges):
                        n, m = incoming_edges.pop(0)
                        if n in [nn for nn, mm in incoming_edges]:
                            continue
                        else:
                            edges += 1

                    if nx.is_connected(sg.to_undirected()) and edges <= K:
                        if sg_seg not in all_connected_subgraphs:
                            all_connected_subgraphs.append(sg_seg)
            K_cones[v] = (
                list(max(all_connected_subgraphs, key=len)) if len(all_connected_subgraphs) else [v]
            )

        # Compute Labels
        l = {n: 0 for n in PI}
        for n in nx.topological_sort(self._GRAPH):
            if self._GRAPH.in_degree(n) != 0:
                # Get partition of current node
                opt_cone = K_cones[n]
                # Get Nn
                Nn = Nv[n]
                # Find max length
                l[n] = max(l[v] for v in Nn if v not in opt_cone) + 1

        # Uncomment to print node labels
        # print(
        #     "Node Labels: "
        #     + " ".join([f"{i}:{d}" for i, d, in sorted(l.items(), key=lambda x: x[0])])
        # )

        # Compute LUTs
        luts = list()
        L = PO.copy()
        while any([g not in PI for g in L]):
            # Get non PI node
            n = L.pop(0)
            if n in PI:
                L += [n]
                continue

            luts = list(set(luts).union({n}))
            sg = self._GRAPH.subgraph(K_cones[n])
            lut_inputs = [
                v
                for v in self._GRAPH.nodes
                if v not in sg.nodes and any([self._GRAPH.has_edge(v, u) for u in sg.nodes])
            ]
            L = list(set(lut_inputs).union(set(L)))
        print(
            "LUTS:\n",
            "\n".join([f"\t{k} = {K_cones[k]} with depth of {l[k]}" for k in luts]),
        )

    # technology mapping with library stdc_lib
    def tech_map(self, stdc_lib):
        import itertools

        # All predecessor nodes of node
        Nv = {n: self.compute_Nv(n) for n in self._node_attributes.keys()}

        # Enumerate all mappings
        node_mapping = dict()
        for n in list(nx.topological_sort(self._GRAPH)):
            mappings = list()
            subgraph = self._GRAPH.subgraph(Nv[n])
            for nb_nodes in range(1, subgraph.number_of_nodes() + 1):
                for sg_seg in itertools.combinations(subgraph, nb_nodes):
                    # Make subgraph of all nodes in Nv combination, without primary nodes
                    sg_seg = list(set(sg_seg).union({n}))
                    sg = subgraph.subgraph(sg_seg)

                    # add labels to subgraph
                    for v in sg.nodes:
                        sg.nodes[v]["label"] = str(self._node_attributes[v].op_type)
                    for e in sg.edges:
                        sg.edges[e]["parent_type"] = str(self._node_attributes[e[0]].op_type)
                        sg.edges[e]["child_type"] = str(self._node_attributes[e[1]].op_type)

                    if nx.is_connected(sg.to_undirected()):
                        for i, g in enumerate(stdc_lib):

                            def edge_same(x, y):
                                return (x["parent_type"] == y["parent_type"]) and (
                                    x["child_type"] == y["child_type"]
                                )

                            def node_same(x, y):
                                return x["label"] == y["label"]

                            if nx.is_isomorphic(
                                sg, g.GRAPH, node_match=node_same, edge_match=edge_same
                            ):
                                # Gather all incoming edges
                                total_weight = [g.get_total_area()] + [
                                    node_mapping[u][1] if u in node_mapping else 0
                                    for u in set(self._GRAPH.nodes).difference(set(sg.nodes))
                                    for v in sg.nodes
                                    if self._GRAPH.has_edge(u, v)
                                ]

                                mappings.append((i, sum(total_weight), sg))
            node_mapping[n] = min(mappings, key=lambda x: x[1])

        min_cover = dict()
        total_size = node_mapping[
            [n for n in self._node_attributes.keys() if self._GRAPH.out_degree(n) == 0][0]
        ][1]
        working_list = [n for n in self._node_attributes.keys() if self._GRAPH.out_degree(n) == 0]
        while len(working_list):
            n = working_list.pop(0)
            # Get STDC map and area
            min_cover[n] = node_mapping[n]

            # Append to working_list all inputs of cover
            working_list += [
                v
                for v in self._GRAPH.nodes
                if v not in node_mapping[n][2]
                and any([self._GRAPH.has_edge(v, u) for u in node_mapping[n][2]])
            ]

        return min_cover, total_size

    def test_resource_binding(self):
        self.asap()
        HLS_LIB = list(
            enumerate(
                [
                    [
                        OpType.Constant,
                    ],
                    [
                        OpType.Mult,
                        OpType.Sub,
                        OpType.Add,
                    ],
                    [
                        OpType.Gt,
                        OpType.Or,
                        OpType.And,
                        OpType.Nor,
                        OpType.Nand,
                    ],
                ]
            )
        )
        rb, k = self.ressource_binding(HLS_LIB)
        print(f"Resource Binding (k = {k}) node mapping:")
        for i, l in rb:
            print(f"Function unit instance {i} computes nodes: {l}")
        print()

    def test_register_allocation(self):
        ra = self.register_allocation()
        print(f"Register Binding, requires {len(ra)} register, with edge mapping:")
        for i, l in ra.items():
            print(f"Register {i} stores values of edges: {l}")
        print()

    def test_tech_map(self, STDC_LIB):
        tm, ts = self.tech_map(STDC_LIB)
        print(f"\nTechnology mapping, has size of {ts}, with node mapping:")
        for i, l in tm.items():
            print(f"Node {i} matches subgraph (complex gate): {l[0]}. Covered nodes: {l[2].nodes}")
        print()


if __name__ == "__main__":
    # Graph Paper Flow Map
    fmap1 = DSESGraph()
    fmap2 = DSESGraph()
    fmap3 = DSESGraph()


    # Test case 1
    # PO
    n1_0 = fmap1.add_node(OpType.Or)
    n1_1 = fmap1.add_node(OpType.Nand)

    # Inner
    n1_2 = fmap1.add_node(OpType.And, children=n1_0)
    n1_3 = fmap1.add_node(OpType.Or, children=n1_1)
    n1_4 = fmap1.add_node(OpType.And, children=n1_1)
    n1_5 = fmap1.add_node(OpType.Nor, children=[n1_2, n1_3])
    n1_6 = fmap1.add_node(OpType.Nand, children=[n1_5, n1_4])
    n1_7 = fmap1.add_node(OpType.And, children=n1_3)
    n1_8 = fmap1.add_node(OpType.Or, children=[n1_7, n1_6])
    n1_9 = fmap1.add_node(OpType.Nand, children=[n1_2, n1_6])
    n1_10 = fmap1.add_node(OpType.Nor, children=[n1_5, n1_8])
    n1_11 = fmap1.add_node(OpType.Nand, children=[n1_0, n1_8])

    # PI
    n1_12 = fmap1.add_node(OpType.Constant, children=n1_9)
    n1_13 = fmap1.add_node(OpType.Constant, children=n1_9)
    n1_14 = fmap1.add_node(OpType.Constant, children=n1_10)
    n1_15 = fmap1.add_node(OpType.Constant, children=[n1_10, n1_11])
    n1_16 = fmap1.add_node(OpType.Constant, children=n1_11)
    n1_17 = fmap1.add_node(OpType.Constant, children=[n1_4, n1_7])


    # Test case 2
    # PO
    n2_0 = fmap2.add_node(OpType.And)
    n2_1 = fmap2.add_node(OpType.Or)

    # Inner
    n2_2 = fmap2.add_node(OpType.Nand, children=n2_0)
    n2_3 = fmap2.add_node(OpType.And, children=n2_1)
    n2_4 = fmap2.add_node(OpType.Or, children=[n2_2, n2_3])
    n2_5 = fmap2.add_node(OpType.Nand, children=n2_4)

    # PI
    n2_6 = fmap2.add_node(OpType.Constant, children=n2_0)
    n2_7 = fmap2.add_node(OpType.Constant, children=n2_0)
    n2_8 = fmap2.add_node(OpType.Constant, children=n2_1)
    n2_9 = fmap2.add_node(OpType.Constant, children=n2_1)
    n2_10 = fmap2.add_node(OpType.Constant, children=n2_2)
    n2_11 = fmap2.add_node(OpType.Constant, children=n2_3)


    # Test case 3
    # PO
    n3_0 = fmap3.add_node(OpType.Or)
    n3_1 = fmap3.add_node(OpType.Nand)

    # Inner
    n3_2 = fmap3.add_node(OpType.And, children=[n3_0, n3_1])

    # PI
    n3_3 = fmap3.add_node(OpType.Constant, children=n3_2)
    n3_4 = fmap3.add_node(OpType.Constant, children=n3_0)
    n3_5 = fmap3.add_node(OpType.Constant, children=n3_1)




    # Show graph
    fmap1.graph_to_dot("g1_unscheduled_graph")
    fmap2.graph_to_dot("g2_unscheduled_graph")
    fmap3.graph_to_dot("g3_unscheduled_graph")

    # Test asap
    fmap1.asap()
    fmap2.asap()
    fmap3.asap()
    fmap1.schedule_to_dot("g1_asap")
    fmap2.schedule_to_dot("g2_asap")
    fmap3.schedule_to_dot("g3_asap")

    # Test Ressource Binding
    # Use asap schedule
    fmap1.test_resource_binding()
    fmap2.test_resource_binding()
    fmap3.test_resource_binding()
    fmap1.schedule_to_dot("g1_binded")
    fmap2.schedule_to_dot("g2_binded")
    fmap3.schedule_to_dot("g3_binded")

    # Test Register Allocation
    fmap1.test_register_allocation()
    fmap2.test_register_allocation()
    fmap3.test_register_allocation()
    fmap1.schedule_to_dot("g1_binded_allocated")
    fmap2.schedule_to_dot("g2_binded_allocated")
    fmap3.schedule_to_dot("g3_binded_allocated")

    # Test ALAP
    fmap1.alap(10)
    fmap2.alap(10)
    fmap3.alap(10)
    fmap1.schedule_to_dot("g1_alap")
    fmap2.schedule_to_dot("g2_alap")
    fmap3.schedule_to_dot("g3_alap")

    # Test Flow Map
    fmap1.flow_map(3)
    fmap2.flow_map(3)
    fmap3.flow_map(3)

    # Test Case 1
    tmap1 = DSESGraph()
    n4_0 = tmap1.add_node(OpType.Nand)
    n4_1 = tmap1.add_node(OpType.Nand, children=n4_0)
    n4_2 = tmap1.add_node(OpType.Invert, children=n4_1)
    n4_3 = tmap1.add_node(OpType.Nand, children=n4_1)
    n4_4 = tmap1.add_node(OpType.Invert, children=n4_3)
    n4_5 = tmap1.add_node(OpType.Nand, children=n4_3)

    n4_6 = tmap1.add_node(OpType.Invert, children=n4_0)
    n4_7 = tmap1.add_node(OpType.Nand, children=n4_6)
    n4_8 = tmap1.add_node(OpType.Invert, children=n4_7)
    n4_9 = tmap1.add_node(OpType.Nand, children=n4_8)


    # Test Case 2
    tmap2 = DSESGraph()
    n5_0 = tmap2.add_node(OpType.Nand)
    n5_1 = tmap2.add_node(OpType.Nand, children=n5_0)
    n5_2 = tmap2.add_node(OpType.Invert, children=n5_0)
    n5_3 = tmap2.add_node(OpType.Invert, children=n5_1)
    n5_4 = tmap2.add_node(OpType.Invert, children=n5_1)

    # Test Case 3
    tmap3 = DSESGraph()
    n6_0 = tmap3.add_node(OpType.Invert)
    n6_1 = tmap3.add_node(OpType.Nand, children=n6_0)
    n6_2 = tmap3.add_node(OpType.Invert, children=n6_1)
    n6_3 = tmap3.add_node(OpType.Invert, children=n6_2)
    n6_4 = tmap3.add_node(OpType.Invert, children=n6_2)
    n6_5 = tmap3.add_node(OpType.Nand, children=n6_3)
    n6_6 = tmap3.add_node(OpType.Invert, children=n6_5)


    # Plot tree
    tmap1.graph_to_dot("g4_min_tree_conver")
    tmap2.graph_to_dot("g5_min_tree_conver")
    tmap3.graph_to_dot("g6_min_tree_conver")

    # Define STDC Lib
    # NAND2
    nand2 = DSESGraph()
    nand2.add_node(OpType.Nand, area=3)
    nand2.graph_to_dot("nand2")

    # INV
    inv = DSESGraph()
    inv.add_node(OpType.Invert, area=2)
    inv.graph_to_dot("inv")

    # AND2
    and2 = DSESGraph()
    and2.add_node(OpType.Nand, children=and2.add_node(OpType.Invert), area=4)
    and2.graph_to_dot("and2")

    # AND3
    and3 = DSESGraph()
    and3.add_node(
        OpType.Nand,
        children=and3.add_node(
            OpType.Invert,
            children=and3.add_node(OpType.Nand, children=and3.add_node(OpType.Invert)),
        ),
        area=7,
    )
    and3.graph_to_dot("and3")

    # NAND3
    nand3 = DSESGraph()
    nand3.add_node(OpType.Nand, children=nand3.add_node(OpType.Nand), area=5)
    nand3.graph_to_dot("nand3")

    # Standard Cell Library
    STDC_LIB = [nand2, inv, and2, and3, nand3]

    # Test Technology Mapping
    tmap1.test_tech_map(STDC_LIB)
    tmap2.test_tech_map(STDC_LIB)
    tmap3.test_tech_map(STDC_LIB)


