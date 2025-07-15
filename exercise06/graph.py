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
    """Attributes for a operation node of the DSES synthesis flow"""

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
    def add_node(
        self, op_type: OpType, exec_time: int = 1, area: float = 0.0, children=None
    ):
        node_id = self.get_new_node_id()
        self._node_attributes[node_id] = Attr(op_type, exec_time, area, -1)
        self._GRAPH.add_node(node_id)
        self._GRAPH.nodes[node_id]["label"] = str(
            self._node_attributes[node_id].op_type
        )
        if children is not None:
            if isinstance(children, Iterable):
                for v in children:
                    self.add_edge(node_id, v)
            else:
                self.add_edge(node_id, children)
        return node_id

    # adds edge from node u to node v
    def add_edge(self, u: int, v: int):
        if not (
            self._node_attributes.get(u, False) and self._node_attributes.get(v, False)
        ):
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
            self._node_attributes[n] = self._node_attributes[n]._replace(
                scheduled_time=-1
            )
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
            for u, v in zip(
                ns[:-1], [ns[(j + 1) % len(ns)] for j, x in enumerate(ns)][:-1]
            ):
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
        num_T = 0
        node_ids = list(self._GRAPH.nodes)
        while(num_T != len(node_ids)):
            for v in node_ids:
                all_scheduled = True
                temp_t_max = 0
                temp_d_max = 0
                for x in self._GRAPH.predecessors(v):
                    node_attributes = self._node_attributes.get(x)
                    temp_t_max = max(temp_t_max, node_attributes.scheduled_time)
                    temp_d_max = max(temp_d_max, node_attributes.exec_time)
                    if node_attributes.scheduled_time == -1:
                        all_scheduled = False
                node_attributes = self._node_attributes.get(v)
                if self._GRAPH.in_degree(v) == 0:
                    if node_attributes.scheduled_time == -1:
                        self._node_attributes[v] = self._node_attributes[v]._replace(
                        scheduled_time = 0)
                        num_T += 1
                elif all_scheduled and node_attributes.scheduled_time == -1:
                    self._node_attributes[v] = self._node_attributes[v]._replace(
                    scheduled_time = temp_t_max + temp_d_max)
                    num_T += 1
        return

       
    # applies alap Algorithm on the Graph
    def alap(self, goal: int):
        self.reset_graph()
        num_T = 0
        node_ids = list(self._GRAPH.nodes)
        while(num_T != len(node_ids)):
            for v in node_ids:
                all_scheduled = True
                temp_t_min = 100000
                for x in self._GRAPH.successors(v):
                    node_attributes = self._node_attributes.get(x)
                    temp_t_min = min(temp_t_min, node_attributes.scheduled_time)
                    if node_attributes.scheduled_time == -1:
                        all_scheduled = False
                node_attributes = self._node_attributes.get(v)
                if self._GRAPH.out_degree(v) == 0:
                    if node_attributes.scheduled_time == -1:
                        self._node_attributes[v] = self._node_attributes[v]._replace(
                        scheduled_time = goal - node_attributes.exec_time)
                        if goal - node_attributes.exec_time < 0:
                            raise RuntimeError()
                        num_T += 1
                elif all_scheduled and node_attributes.scheduled_time == -1:
                    self._node_attributes[v] = self._node_attributes[v]._replace(
                    scheduled_time = temp_t_min - node_attributes.exec_time)
                    if temp_t_min - node_attributes.exec_time < 0:
                        raise RuntimeError()
                    num_T += 1
        return

if __name__ == "__main__":
    # Test Graph
    G = DSESGraph()
    n0 = G.add_node(OpType.Or)
    n1 = G.add_node(OpType.And, children=n0)
    n2 = G.add_node(OpType.Constant, exec_time=1, children=[n0, n1])

    G.graph_to_dot("filename")
    G.asap()
    G.schedule_to_dot("filenmaeschedule")
    G.alap(3)
    G.schedule_to_dot("filenmaeschedulealap")


    G1 = DSESGraph()
    n = []
    for i in range(9):
        exec_time = i % 3 + 1
        n.append(G1.add_node(OpType.And, exec_time=exec_time, children=n[i-1:i] if i > 0 else []))
    G1.graph_to_dot("G1")
    G1.asap()
    G1.schedule_to_dot("G1schedule")
    G1.alap(20)
    G1.schedule_to_dot("G1schedulealap")


    G2 = DSESGraph()
    n0 = G2.add_node(OpType.Or, exec_time=1)
    n1 = G2.add_node(OpType.And, exec_time=2, children=[n0])
    n2 = G2.add_node(OpType.And, exec_time=2, children=[n0])
    n3 = G2.add_node(OpType.Xor, exec_time=1, children=[n1])
    n4 = G2.add_node(OpType.Or, exec_time=2, children=[n1, n2])
    n5 = G2.add_node(OpType.And, exec_time=1, children=[n2])
    n6 = G2.add_node(OpType.Xor, exec_time=3, children=[n3, n4, n5])
    n7 = G2.add_node(OpType.Constant, exec_time=1, children=[n6])
    n8 = G2.add_node(OpType.Constant, exec_time=1, children=[n6])
    G2.graph_to_dot("G2")
    G2.asap()
    G2.schedule_to_dot("G2schedule")
    G2.alap(10)
    G2.schedule_to_dot("G2schedulealap")


    G3 = DSESGraph()
    n0 = G3.add_node(OpType.Or, exec_time=1)
    n1 = G3.add_node(OpType.And, exec_time=2, children=[n0])
    n2 = G3.add_node(OpType.And, exec_time=2, children=[n0])
    n3 = G3.add_node(OpType.Constant, exec_time=1, children=[n1])
    n4 = G3.add_node(OpType.Xor, exec_time=1, children=[n1])
    n5 = G3.add_node(OpType.And, exec_time=2, children=[n2])
    n6 = G3.add_node(OpType.Xor, exec_time=1, children=[n2])
    n7 = G3.add_node(OpType.Or, exec_time=1, children=[n4, n5])
    n8 = G3.add_node(OpType.Constant, exec_time=1, children=[n5, n6])
    G3.graph_to_dot("G3")
    G3.asap()
    G3.schedule_to_dot("G3schedule")
    G3.alap(10)
    G3.schedule_to_dot("G3schedulealap")
    G3.alap(4)
