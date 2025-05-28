
# Instruction Formats
## R-type

  31        25 24     20 19     15 14  12 11      7 6           0
 +------------+---------+---------+------+---------+-------------+
 | funct7     | rs2     | rs1     |funct3| rd      | opcode      |
 +------------+---------+---------+------+---------+-------------+

## I-type

  31                  20 19     15 14  12 11      7 6           0
 +----------------------+---------+------+---------+-------------+
 | imm                  | rs1     |funct3| rd      | opcode      |
 +----------------------+---------+------+---------+-------------+

## S-type

  31        25 24     20 19     15 14  12 11      7 6           0
 +------------+---------+---------+------+---------+-------------+
 | imm        | rs2     | rs1     |funct3| imm     | opcode      |
 +------------+---------+---------+------+---------+-------------+

## U-type

  31                                   12 11      7 6           0
 +---------------------------------------+---------+-------------+
 | imm                                   | rd      | opcode      |
 +---------------------------------------+---------+-------------+

# Immediate Formats
## I-immediate

  31                                     11 10        5 4     1  0
 +-----------------------------------------+-----------+-------+--+
 |                                  <-- 31 | 30:25     | 24:21 |20|
 +-----------------------------------------+-----------+-------+--+

## S-immediate

  31                                     11 10        5 4     1  0
 +-----------------------------------------+-----------+-------+--+
 |                                  <-- 31 | 30:25     | 11:8  |7 |
 +-----------------------------------------+-----------+-------+--+

## B-immediate

  31                                  12 11 10        5 4     1  0
 +--------------------------------------+--+-----------+-------+--+
 |                               <-- 31 |7 | 30:25     | 11:8  |z |
 +--------------------------------------+--+-----------+-------+--+

## U-immediate

  31 30               20 19           12 11                      0
 +--+-------------------+---------------+-------------------------+
 |31| 30:20             | 19:12         |                   <-- z |
 +--+-------------------+---------------+-------------------------+

## J-immediate

  31                  20 19           12 11 10        5 4     1  0
 +----------------------+---------------+--+-----------+-------+--+
 |               <-- 31 | 19:12         |20| 30:25     | 24:21 |z |
 +----------------------+---------------+--+-----------+-------+--+ 

# Instructions
## ADD

 - Summary   : Addition with 3 GPRs, no overflow exception
 - Assembly  : add rd, rs1, rs2
 - Semantics : R[rd] = R[rs1] + R[rs2]
 - Format    : R-type

  31        25 24     20 19     15 14  12 11      7 6           0
 +------------+---------+---------+------+---------+-------------+
 | 0000000    | rs2     | rs1     | 000  | rd      | 0110011     |
 +------------+---------+---------+------+---------+-------------+

## MUL

 - Summary   : Signed multiplication with 3 GPRs, no overflow exception
 - Assembly  : mul rd, rs1, rs2
 - Semantics : R[rd] = R[rs1] * R[rs2]
 - Format    : R-type

  31        25 24     20 19     15 14  12 11      7 6           0
 +------------+---------+---------+------+---------+-------------+
 | 0000001    | rs2     | rs1     | 000  | rd      | 0110011     |
 +------------+---------+---------+------+---------+-------------+

## ADDI

 - Summary   : Add constant, no overflow exception
 - Assembly  : addi rd, rs1, imm
 - Semantics : R[rd] = R[rs1] + sext(imm)
 - Format    : I-type, I-immediate

  31                  20 19     15 14  12 11      7 6           0
 +----------------------+---------+------+---------+-------------+
 | imm                  | rs1     | 000  | rd      | 0010011     |
 +----------------------+---------+------+---------+-------------+

## LW

 - Summary   : Load word from memory
 - Assembly  : lw rd, imm(rs1)
 - Semantics : R[rd] = M_4B[ R[rs1] + sext(imm) ]
 - Format    : I-type, I-immediate

  31                  20 19     15 14  12 11      7 6           0
 +----------------------+---------+------+---------+-------------+
 | imm                  | rs1     | 010  | rd      | 0000011     |
 +----------------------+---------+------+---------+-------------+

All addresses used with LW instructions must be four-byte aligned. This
means the bottom two bits of every effective address (i.e., after the
base address is added to the offset) will always be zero.

## SW

 - Summary   : Store word into memory
 - Assembly  : sw rs2, imm(rs1)
 - Semantics : M_4B[ R[rs1] + sext(imm) ] = R[rs2]
 - Format    : S-type, S-immediate

  31        25 24     20 19     15 14  12 11      7 6           0
 +------------+---------+---------+------+---------+-------------+
 | imm        | rs2     | rs1     | 010  | imm     | 0100011     |
 +------------+---------+---------+------+---------+-------------+

All addresses used with SW instructions must be four-byte aligned. This
means the bottom two bits of every effective address (i.e., after the
base address is added to the offset) will always be zero.

## JAL

 - Summary   : Jump to address (Note: This is not Spec. conform)
 - Assembly  : jal rd, imm
 - Semantics : PC = PC + sext(imm)
 - Format    : U-type, J-immediate

  31                                      11      7 6           0
 +---------------------------------------+---------+-------------+
 | imm                                   | rd      | 1101111     |
 +---------------------------------------+---------+-------------+

## BNE

 - Summary   : Branch if 2 GPRs are not equal
 - Assembly  : bne rs1, rs2, imm
 - Semantics : PC = ( R[rs1] != R[rs2] ) ? PC + sext(imm) : PC + 4
 - Format    : S-type, B-immediate

  31        25 24     20 19     15 14  12 11      7 6           0
 +------------+---------+---------+------+---------+-------------+
 | imm        | rs2     | rs1     | 001  | imm     | 1100011     |
 +------------+---------+---------+------+---------+-------------+

