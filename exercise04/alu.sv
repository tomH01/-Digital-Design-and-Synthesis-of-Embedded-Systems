import rriscv_pkg::*;

module alu (
    input logic [6 : 0] opcode_i,
    input logic [XLEN - 1 : 0] value_a_i,
    input logic [2 : 0] funct3_i,
    input logic [6 : 0] funct7_i,
    input logic [XLEN - 1 : 0] value_b_i,
    output logic zero_o,
    output logic [XLEN - 1 : 0] result_o
);

  logic [XLEN - 1 : 0] imm;

  // Assign immediate
  assign result_o = imm;

  // compute immediate
  always_comb begin : compute_immediate
    if (((opcode_i == ADD.opcode) & (funct7_i == 'b0000000)) | (opcode_i == ADDI.opcode)) begin
      imm = (value_a_i + value_b_i);
    end else if ((opcode_i == XOR.opcode) & (funct7_i == 'b0000000)) begin
      // TODO
      imm = (value_a_i ^ value_b_i);
    end else if ((opcode_i == MUL.opcode) & (funct7_i == 'b0000001)) begin
      imm = (value_a_i * value_b_i);
    end else if ((opcode_i == BEQ.opcode) & (funct3_i == 'b000)) begin
      // TODO
      imm = (value_a_i == value_b_i);
    end else if ((opcode_i == BNE.opcode) & (funct3_i == 'b001)) begin
      imm = (value_a_i ^ value_b_i);
    end else begin
      imm = 'b0;
    end
  end

  // zero flag
  // TODO
  assign zero_o = (result_o == 0);


endmodule
