import rriscv_pkg::*;
module instruction_decoder (
    input logic [XLEN - 1:0] instruction_i,
    output logic [6 : 0] opcode_o,
    output logic [4 : 0] rs1_o,
    output logic [4 : 0] rs2_o,
    output logic [2 : 0] funct3_o,
    output logic [6 : 0] funct7_o,
    output logic [4 : 0] rd_o,
    output logic rf_rw_o,
    output logic err_o,
    output logic [XLEN - 1 : 0] immediate_o
);


  // For easy instruction access
  unresolved_type unresolved_instruction;
  r_type r_type_instruction;
  i_type i_type_instruction;
  s_type s_type_instruction;
  u_type u_type_instruction;

  // For easy immediate access
  i_immediate_type i_immediate;
  s_immediate_type s_immediate;
  b_immediate_type b_immediate;
  u_immediate_type u_immediate;
  j_immediate_type j_immediate;

  // 1. Connect everything up
  // 1.0 Instruction to unresolved
  always_comb begin : assign_instr_to_unresolved
    unresolved_instruction.funct7 = instruction_i[31 : 25];
    unresolved_instruction.tba1   = instruction_i[24 : 15];
    unresolved_instruction.funct3 = instruction_i[14 : 12];
    unresolved_instruction.tba0   = instruction_i[11 : 7];
    unresolved_instruction.opcode = instruction_i[6 : 0];
  end

  // 1.1 R Type
  always_comb begin : assign_instr_to_r_type
    r_type_instruction.funct7 = instruction_i[31 : 25];
    r_type_instruction.rs2    = instruction_i[24 : 20];
    r_type_instruction.rs1    = instruction_i[19 : 15];
    r_type_instruction.funct3 = instruction_i[14 : 12];
    r_type_instruction.rd     = instruction_i[11 : 7];
    r_type_instruction.opcode = instruction_i[6 : 0];
  end

  // 1.2 I Type
  always_comb begin : assign_instr_to_i_type
    i_type_instruction.imm    = instruction_i[31 : 20];
    i_type_instruction.rs1    = instruction_i[19 : 15];
    i_type_instruction.funct3 = instruction_i[14 : 12];
    i_type_instruction.rd     = instruction_i[11 : 7];
    i_type_instruction.opcode = instruction_i[6 : 0];
  end

  // 1.3 S Type
  always_comb begin : assign_instr_to_s_type
    s_type_instruction.imm    = instruction_i[31 : 25];
    s_type_instruction.rs2    = instruction_i[24 : 20];
    s_type_instruction.rs1    = instruction_i[19 : 15];
    s_type_instruction.funct3 = instruction_i[14 : 12];
    s_type_instruction.imm0   = instruction_i[11 :  7];
    s_type_instruction.opcode = instruction_i[ 6 :  0];
  end

  // 1.4 U Type
  always_comb begin : assign_instr_to_u_type
    u_type_instruction.imm    = instruction_i[31 : 12];
    u_type_instruction.rd     = instruction_i[11 : 7];
    u_type_instruction.opcode = instruction_i[6 : 0];
  end

  // 1.5 I Immediate
  always_comb begin : assign_i_immediate
    i_immediate.inst_31    = {21{instruction_i[31]}};
    i_immediate.inst_30_25 = instruction_i[30 : 25];
    i_immediate.inst_24_21 = instruction_i[24 : 21];
    i_immediate.inst_20    = instruction_i[20];
  end

  // 1.6 S Immediate
  always_comb begin : assign_s_immediate
    s_immediate.inst_31    = {21{instruction_i[31]}};
    s_immediate.inst_30_25 = instruction_i[30 : 25];
    s_immediate.inst_11_8  = instruction_i[11 : 8];
    s_immediate.inst_7     = instruction_i[7];
  end

  // 1.7 B Immediate
  always_comb begin : assign_b_immediate
    b_immediate.inst_31    = {20{instruction_i[31]}};
    b_immediate.inst_7     = instruction_i[7];
    b_immediate.inst_30_25 = instruction_i[30 : 25];
    b_immediate.inst_11_8  = instruction_i[11 : 8];
    b_immediate.zero       = 'b0;
  end

  // 1.8 U Immediate
  always_comb begin : assign_u_immediate
    u_immediate.inst_31    = instruction_i[31];
    u_immediate.inst_30_20 = instruction_i[30 : 20];
    u_immediate.inst_19_12 = instruction_i[19 : 12];
    u_immediate.zero       = 'b0;
  end

  // 1.9 J Immediate
  always_comb begin : assign_j_immediate
    j_immediate.inst_31    = {12{instruction_i[31]}};
    j_immediate.inst_19_12 = instruction_i[19 : 12];
    j_immediate.inst_20    = instruction_i[20];
    j_immediate.inst_30_25 = instruction_i[30 : 25];
    j_immediate.inst_24_21 = instruction_i[24 : 21];
    j_immediate.zero       = 'b0;
  end

  // 1.9 Connect opcode
  assign opcode_o = unresolved_instruction.opcode;

  // 2 Instruction Output
  always_comb begin : instruction_selection
    case (unresolved_instruction.opcode)
      // ADD, MUL, XOR
      // TODO
      ADD.opcode, MUL.opcode, XOR.opcode: begin
        rs1_o    = r_type_instruction.rs1;
        rs2_o    = r_type_instruction.rs2;
        funct3_o = r_type_instruction.funct3;
        funct7_o = r_type_instruction.funct7;
        rd_o     = r_type_instruction.rd;
        rf_rw_o  = 'b1;
        err_o    = 'b0;
      end
      // ADDI, LW
      ADDI.opcode, LW.opcode: begin
        rs1_o    = i_type_instruction.rs1;
        rs2_o    = 'b0;
        funct3_o = i_type_instruction.funct3;
        funct7_o = 'b0;
        rd_o     = i_type_instruction.rd;
        rf_rw_o  = 'b1;
        err_o    = 'b0;
      end
      // SW
      SW.opcode: begin
        rs1_o    = s_type_instruction.rs1;
        rs2_o    = s_type_instruction.rs2;
        funct3_o = s_type_instruction.funct3;
        funct7_o = 'b0;
        rd_o     = 'b0;
        rf_rw_o  = 'b0;
        err_o    = 'b0;
      end
      // JAL
      JAL.opcode: begin
        rs1_o    = 'b0;
        rs2_o    = 'b0;
        funct3_o = 'b0;
        funct7_o = 'b0;
        rd_o     = u_type_instruction.rd;
        rf_rw_o  = 'b1;
        err_o    = 'b0;
      end
      // BNE, BEQ
      BNE.opcode, BEQ.opcode: begin
        rs1_o    = s_type_instruction.rs1;
        rs2_o    = s_type_instruction.rs2;
        funct3_o = s_type_instruction.funct3;
        funct7_o = 'b0;
        rd_o     = 'b0;
        rf_rw_o  = 'b0;
        err_o    = 'b0;
      end
      default: begin
        rs1_o    = 'b0;
        rs2_o    = 'b0;
        funct3_o = 'b0;
        funct7_o = 'b0;
        rd_o     = 'b0;
        rf_rw_o  = 'b0;
        err_o    = 'b1;
      end
    endcase
  end

  // 3 Immediate Output
  always_comb begin : Immediate_assignment
    case (unresolved_instruction.opcode)
      // I Immediate
      ADDI.opcode, LW.opcode: begin
        immediate_o = {
          i_immediate.inst_31, i_immediate.inst_30_25, i_immediate.inst_24_21, i_immediate.inst_20
        };
      end
      // S Immediate
      SW.opcode: begin
        immediate_o = {
          s_immediate.inst_31, s_immediate.inst_30_25, s_immediate.inst_11_8, s_immediate.inst_7
        };
      end
      // J Immediate
      JAL.opcode: begin
        immediate_o = {
          j_immediate.inst_31,
          j_immediate.inst_19_12,
          j_immediate.inst_20,
          j_immediate.inst_30_25,
          j_immediate.inst_24_21,
          j_immediate.zero
        };
      end
      // B Immediate
      // TODO
      BNE.opcode, BEQ.opcode: begin
        immediate_o = {
          b_immediate.inst_31,
          b_immediate.inst_7,
          b_immediate.inst_30_25,
          b_immediate.inst_11_8,
          b_immediate.zero
        };
      end
      default: begin
        immediate_o = 'b0;
      end
    endcase
  end
endmodule
