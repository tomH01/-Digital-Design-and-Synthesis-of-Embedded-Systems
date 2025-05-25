from abc import ABC, abstractmethod


# Base Class for each Operand
class OP(ABC):
    def __init__(self, children, parent=list()):
        self._parent = parent
        self._children = children
        self._index = list()

    @property
    def children(self):
        return self._children

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        self._parent = value

    @property
    def index(self) -> int:
        return self._index

    @index.setter
    def index(self, value: int):
        self._index = value

    @abstractmethod
    def translate(self) -> str:
        pass

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def __repr__(self):
        pass


class VARIABLE(OP):
    def __init__(self, name: str, parent=list()):
        self._name = name.strip()
        super().__init__(parent=parent, children=self)

    @property
    def name(self) -> str:
        return self._name

    def translate(self) -> str:
        return "01"

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if isinstance(other, VARIABLE):
            return self.name == other.name
        else:
            raise TypeError("Cannot compare VARIABLE with non VARIABLE object")

    def __hash__(self):
        return self.name.__hash__()


class NOT(OP):
    def __init__(self, op: VARIABLE, parent=list()):
        if isinstance(op, VARIABLE):
            super().__init__(parent=parent, children=[op])
            for o in self._children:
                o.parent = self
        else:
            raise TypeError("[ERROR] NOT can only take VARIABLE operands")

    @property
    def children(self) -> OP:
        return self._children

    def translate(self) -> str:
        # Bit order (Inverse, Not Inverse)
        return "10"

    def __str__(self):
        return f"NOT({str(self.children[0])})"

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if isinstance(other, NOT):
            return self.children.name == other.children.name
        else:
            raise TypeError("Cannot compare NOT with non NOT object")


class AND(OP):
    def __init__(self, ops, parent=list()):
        if len(ops) == 0:
            raise RuntimeError("Cannot create empty AND")
        if all([isinstance(o, NOT) or isinstance(o, VARIABLE) for o in ops]):
            super().__init__(parent=parent, children=ops)
            for o in self.children:
                o.parent = self
        else:
            raise TypeError(
                "[ERROR] AND can only take VARIABLE operands or NOT operands"
            )

    def translate(self) -> str:
        # Operand order from
        pass

    def __str__(self):
        return f"AND({', '.join(str(o) for o in self.children)})"

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return self.index.__hash__()


class OR(OP):
    def __init__(self, ops, parent=list()):
        if len(ops) == 0:
            raise RuntimeError("Cannot create empty OR")

        if all([isinstance(o, AND) for o in ops]):
            super().__init__(parent=parent, children=ops)
            for o in self.children:
                o.parent = self
        else:
            raise TypeError("[ERROR] OR can only take AND operands")

    def translate(self) -> str:
        # Operand order from
        pass

    def __str__(self):
        return f"OR({', '.join(str(o) for o in self.children)})"

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return self.index.__hash__()


class EQ(OP):
    def __init__(self, ops, parent=list()):
        if len(ops) == 0:
            raise RuntimeError("Cannot create empty EQ")

        if all([isinstance(o, OR) for o in ops]):
            super().__init__(parent=parent, children=ops)
            for o in self.children:
                o.parent = self
        else:
            raise TypeError("[ERROR] EQ can only take OR operands")

    def translate(self) -> str:
        self.verify()

        # 1. Uniqify all variables
        # Unique variables
        variables = list(set(self.variables))
        variables_dict = dict()
        index_dict = dict()

        # 2. Index all Variables
        for i, a in enumerate(variables):
            variables_dict[i] = a
            index_dict[a] = i

        # 2.1 Set correct index
        # Assign uniqified index to each object
        variable_objects = self.variables
        for a in variable_objects:
            a.index = index_dict[a]

        # 3. Count amount of blocks in and matrix and index them
        ands = self.ands
        for i, a in enumerate(ands):
            a.index = i

        # 4. Count amount of blocks in or matrix and index them
        ors = self.ors
        for i, a in enumerate(ors):
            a.index = i

        # 5. Set ref to unique variable for each not
        nots = self.nots
        for a in nots:
            for v in variables:
                if a.children[0] == v:
                    a.index = v.index

        # 7. Generate AND matrix fuse controls
        and_fuse_control = dict()
        for a in ands:
            # Set the index for each AND-Block
            and_fuse_control[a.index] = dict()

            # For each subterm, set the correct fuse control for the used variable
            for i, v in enumerate(a.children):
                # Each variables is assigned to a row i inside the AND-Block.
                and_fuse_control[a.index][i] = dict()

                # Each AND-Block consists of 2 * len(variables) many rows and columns. Each row represents a logical value of a variable that contributes to the AND condition. In this loop, we set the correct fuses for each of the _used_ variables. The next steps then filles 'disconnects', i.e., which fuses should not be set.
                and_fuse_control[a.index][i][v.index] = (
                    "10" if isinstance(v, NOT) else "01"
                )

        # 7.1 Fill 'disconnects', i.e., disable all fuses that are unused in the terms.
        for i in range(0, 2 ** len(variables)):
            if and_fuse_control.get(i, None) is None:
                and_fuse_control[i] = dict()
            for j in range(2 * len(variables)):
                if and_fuse_control[i].get(j, None) is None:
                    and_fuse_control[i][j] = dict()
                for k in range(len(variables)):
                    if and_fuse_control[i][j].get(k, None) is None:
                        and_fuse_control[i][j][k] = "00"

            # 7.2 We have to ensure that rows which are completly unsused do not influence the input to the AND of the AND-Block. However, we need to enable at least of the fuses, otherweise the entire row wouldn't have a well-defined value. Thus, for each zero-row, we duplicate and already existing condition of the current i-th AND-Block as this does not change the logic.
            not_zero = list()
            zero = list()
            for j in range(2 * len(variables)):
                if "1" in "".join(and_fuse_control[i][j].values()):
                    not_zero.append(j)
                else:
                    zero.append(j)

            if len(not_zero) == 0:
                # In this case, the entire AND-Block does not have a single active row. In this case, we force the output of the AND-Block to a logical 0, by setting the first fuse in each row alternatly to the value of the first variable, or the value of the first value but negated.
                for j in range(2 * len(variables)):
                    for k in range(0, len(variables)):
                        and_fuse_control[i][j][k] = (
                            ("10" if j % 2 == 0 else "01") if k == 0 else "00"
                        )
            else:
                for j in zero:
                    and_fuse_control[i][j] = and_fuse_control[i][not_zero[0]]

        # 8. Generate OR matrix fuse constrols
        or_fuse_control = dict()
        for o in ors:
            # Set the index for each OR-Block
            or_fuse_control[o.index] = dict()

            # For each subterm, set the correct fuse control for the used variable
            for i, v in enumerate(o.children):
                or_fuse_control[o.index][i] = dict()
                # Each variables is assigned to a column i inside the OR-Block.

                # Each OR-Block consists of 2^len(variables) many rows and columns. Each column represents a logical value of a variable that contributes to the OR condition. In this loop, we set the correct fuses for each of the _used_ variables. The next steps then filles 'disconnects', i.e., which fuses should not be set.
                or_fuse_control[o.index][i][v.index] = "1"

        # 8.1 Fill 'disconnects', i.e., disable all fuses that are unused in the terms.
        for i in range(0, len(ors)):
            for j in range(0, 2 ** len(variables)):
                if or_fuse_control[i].get(j, None) is None:
                    or_fuse_control[i][j] = dict()
                for k in range(0, 2 ** len(variables)):
                    if or_fuse_control[i][j].get(k, None) is None:
                        or_fuse_control[i][j][k] = "0"

            # 8.2 We have to ensure that columns which are completly unsused do not influence the input to the OR of the OR-Block. However, we need to enable at least of the fuses, otherweise the entire column wouldn't have a well-defined value. Thus, for each zero-row, we duplicate and already existing condition of the current i-th OR-Block as this does not change the logic.
            not_zero = list()
            zero = list()
            for j in range(0, 2 ** len(variables)):
                if "1" in "".join(or_fuse_control[i][j].values()):
                    not_zero.append(j)
                else:
                    zero.append(j)

            if len(not_zero):
                for j in zero:
                    or_fuse_control[i][j] = or_fuse_control[i][not_zero[0]]

        # 9. Build AND control vector
        and_fuse_control_block_row = list()

        # 9.1 Start with filling the ands that have an index
        for a in sorted(ands, key=lambda x: x.index):
            and_fuse_control_block_row += [ "".join([fuse for _, row in sorted(and_fuse_control[a.index].items(), reverse=True) for _, fuse in sorted(row.items(), reverse=True)])]

        # 9.2 Fill the rest
        for a in range(len(ands), 2 ** len(variables)):
            and_fuse_control_block_row += [ "".join([fuse for _, row in sorted(and_fuse_control[a].items(), reverse=True) for _, fuse in sorted(row.items(), reverse=True)])]

        # 9.3 Pack to configuration port value
        and_fuse_control_vector = "".join(reversed(and_fuse_control_block_row))

         # 10. Build OR control vector, the PLD hardware gets this in row-wise layout, therefore we have to transform it here
        or_fuse_control_block_row = list()

        # 10.1 Foreach or, gather the information in row form
        for and_block_id in range(0, 2 ** len(variables)):
            # Get the fuse value for each OR, in each row AND-Block
            acc = []
            for o in sorted(ors, key=lambda x: x.index):
                acc += ["".join([col[and_block_id] for _, col in sorted(or_fuse_control[o.index].items())])]
            or_fuse_control_block_row += ["".join(reversed(acc))]

        # 10.3 Pack to configuration port value
        or_fuse_control_vector = "".join(reversed(or_fuse_control_block_row))


        # 11. Build OP ordering
        op_ordering = ", ".join(str(v) for v in list(sorted(variables, key=lambda x: x.index, reverse=True)))

        # 12. Build output ordering
        out_ordering = ", ".join([str(o) for o in sorted(ors, key=lambda o: o.index, reverse=True)])

        # 13. Build Testbench
        def gen_bin(n, b=""):
            if len(b) == n:
                return [b]
            else:
                return gen_bin(n, b + "0") + gen_bin(n, b + "1")

        tb = "  - Sample Testbench:\n\n"
        tb += "    // Testbench Start\n"
        tb += "    #(10ns);\n"
        for p in gen_bin(len(set(self.variables))):
            tb += f"    inputs = 'b{p};\n    #(10ns);\n"
        tb += "    // Testbench End"

        translation = "PLD Generator:\n"
        translation += f"  - Number of ouputs: {len(ors)}\n"
        translation += f"  - Number of inputs: {len(variables)}\n"
        translation += f"  - Ordering of inputs (on wire): inputs[{len(variables) - 1} : 0] = '" + "{" + f"{op_ordering}" + "}\n"
        translation += f"  - Ordering of outputs (on wire): outputs[{len(ors) - 1} : 0] = '" + "{" + f"{out_ordering}" + "}\n"
        translation += f"  - AND fuse controls: {and_fuse_control_vector}\n"
        translation += f"  - OR fuse controls: {or_fuse_control_vector}\n"
        translation += f"{tb}"
        return translation

    def __str__(self):
        return f"EQ({', '.join(str(o) for o in self.children)})"

    def __repr__(self):
        return str(self)

    def _get_objects(self, op, obj_type):
        from typing import Iterable

        def flatten(l):
            for i in l:
                if isinstance(i, Iterable) and not isinstance(i, (str, bytes)):
                    for s in flatten(i):
                        yield s
                else:
                    yield i

        def get_o(op, t):
            if isinstance(op, t):
                return op
            if not isinstance(op.children, Iterable):
                return list()
            else:
                return [get_o(o, t) for o in op.children]

        return list(flatten(get_o(op, obj_type)))

    @property
    def variables(self):
        return self._get_objects(self, VARIABLE)

    @property
    def ands(self):
        return self._get_objects(self, AND)

    @property
    def ors(self):
        return self._get_objects(self, OR)

    @property
    def nots(self):
        return self._get_objects(self, NOT)

    def verify(self):
        # 1. Check if amount of AND is valid
        if len(self.ands) > 2 ** (2 * len(self.variables)):
            raise RuntimeError(f"Cannot have more than {2**self.variables} 'AND's")


if __name__ == "__main__":
    eq = EQ(
        [
            OR(
                [
                    AND([VARIABLE("A"), VARIABLE("B"), VARIABLE("C")]),
                    AND([NOT(VARIABLE("A")), VARIABLE("B")]),
                ]
            ),
            OR([AND([NOT(VARIABLE("A")), VARIABLE("B")])]),
        ]
    )
    print(eq.translate())

    eq = EQ(
        [
            OR([AND([VARIABLE("A"), NOT(VARIABLE("B")), NOT(VARIABLE("C"))])]),
            OR([AND([NOT(VARIABLE("A")), VARIABLE("B"), NOT(VARIABLE("C"))])]),
            OR([AND([VARIABLE("A"), VARIABLE("B"), NOT(VARIABLE("C"))])]),
            OR([AND([NOT(VARIABLE("A")), NOT(VARIABLE("B")), VARIABLE("C")])]),
            OR([AND([VARIABLE("A"), NOT(VARIABLE("B")), VARIABLE("C")])]),
            OR([AND([NOT(VARIABLE("A")), VARIABLE("B"), VARIABLE("C")])]),
            OR([AND([NOT(VARIABLE("A")), NOT(VARIABLE("B")), NOT(VARIABLE("C"))])]),
            OR([AND([VARIABLE("A"), VARIABLE("B"), VARIABLE("C")])]),
        ]
    )
    print(eq.translate())
