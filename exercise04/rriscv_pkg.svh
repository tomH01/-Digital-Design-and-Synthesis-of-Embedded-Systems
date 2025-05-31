`ifndef RRISCV_PKG_
`define RRISCV_PKG_
package rriscv_pkg;

  // Defined by riscv32 standard
  localparam int XLEN = 32;

  // Mem Sizes
  localparam unsigned INSTR_MEM_SIZE = 32;
  localparam unsigned DATA_MEM_SIZE = 2**22;

  // Generic memory type
  typedef logic [XLEN - 1 : 0] instr_mem_type_t[INSTR_MEM_SIZE];
  typedef logic [XLEN - 1 : 0] data_mem_type_t[DATA_MEM_SIZE];



  // Instruction type
  typedef struct packed {
    logic [6 : 0] funct7;
    logic [9 : 0] tba1;
    logic [2 : 0] funct3;
    logic [4 : 0] tba0;
    logic [6 : 0] opcode;
  } unresolved_type;

  typedef struct packed {
    logic [6 : 0] funct7;
    logic [4 : 0] rs2;
    logic [4 : 0] rs1;
    logic [2 : 0] funct3;
    logic [4 : 0] rd;
    logic [6 : 0] opcode;
  } r_type;

  typedef struct packed {
    logic [11 : 0] imm;
    logic [4 : 0]  rs1;
    logic [2 : 0]  funct3;
    logic [4 : 0]  rd;
    logic [6 : 0]  opcode;
  } i_type;

  typedef struct packed {
    logic [6 : 0] imm;
    logic [4 : 0] rs2;
    logic [4 : 0] rs1;
    logic [2 : 0] funct3;
    logic [4 : 0] imm0;
    logic [6 : 0] opcode;
  } s_type;

  typedef struct packed {
    logic [19 : 0] imm;
    logic [4 : 0]  rd;
    logic [6 : 0]  opcode;
  } u_type;

  // Instructions
  localparam r_type ADD = '{
      funct7 : 'b0000000,
      rs2 : '{default: '0},
      rs1 : '{default: '0},
      funct3 : 'b000,
      rd : '{default: '0},
      opcode : 'b0110011
  };

  localparam r_type MUL = '{
      funct7 : 'b0000001,
      rs2 : '{default: '0},
      rs1 : '{default: '0},
      funct3 : 'b000,
      rd : '{default: '0},
      opcode : 'b0110011
  };

  // TODO
  localparam r_type XOR = '{
      funct7 : 'b0000000,
      rs2 : '{default: '0},
      rs1 : '{default: '0},
      funct3 : 'b100,
      rd : '{default: '0},
      opcode : 'b0110011   
  }; 

  localparam i_type ADDI = '{
      imm : '{default: '0},
      rs1 : '{default: '0},
      funct3 : 'b000,
      rd : '{default: '0},
      opcode : 'b0010011
  };

  localparam i_type LW = '{
      imm : '{default: '0},
      rs1 : '{default: '0},
      funct3 : 'b010,
      rd : '{default: '0},
      opcode : 'b0000011
  };

  localparam s_type SW = '{
      imm : '{default: '0},
      rs2 : '{default: '0},
      rs1 : '{default: '0},
      funct3 : 'b010,
      imm0 : '{default: '0},
      opcode : 'b0100011
  };

  localparam u_type JAL = '{imm : '{default: '0}, rd : '{default: '0}, opcode : 'b1101111};

  // TODO
  localparam s_type BEQ = '{
      imm : '{default: '0},
      rs2 : '{default: '0},
      rs1 : '{default: '0},
      funct3 : 'b000,
      imm0 : '{default: '0},
      opcode : 'b1100011
  }; 

  localparam s_type BNE = '{
      imm : '{default: '0},
      rs2 : '{default: '0},
      rs1 : '{default: '0},
      funct3 : 'b001,
      imm0 : '{default: '0},
      opcode : 'b1100011
  };

  // Immediate types
  typedef struct packed {
    logic [20 : 0] inst_31;
    logic [5 : 0] inst_30_25;
    logic [3 : 0] inst_24_21;
    logic inst_20;
  } i_immediate_type;

  typedef struct packed {
    logic [20 : 0] inst_31;
    logic [5 : 0] inst_30_25;
    logic [3 : 0] inst_11_8;
    logic inst_7;
  } s_immediate_type;

  typedef struct packed {
    logic [19 : 0] inst_31;
    logic inst_7;
    logic [5 : 0] inst_30_25;
    logic [3 : 0] inst_11_8;
    logic zero;
  } b_immediate_type;

  typedef struct packed {
    logic inst_31;
    logic [10 : 0] inst_30_20;
    logic [7 : 0] inst_19_12;
    logic zero;
  } u_immediate_type;

  typedef struct packed {
    logic [11 : 0] inst_31;
    logic [7 : 0] inst_19_12;
    logic inst_20;
    logic [5 : 0] inst_30_25;
    logic [3 : 0] inst_24_21;
    logic zero;
  } j_immediate_type;
endpackage
`endif
