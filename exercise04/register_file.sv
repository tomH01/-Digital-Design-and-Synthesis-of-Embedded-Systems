import rriscv_pkg::*;

module register_file (
    input logic clk_i,
    input logic halt_i,
    input logic rst_n_i,
    input logic write_enable_i,
    input logic [XLEN - 1 : 0] data_i,
    input logic [$clog2(XLEN)-1 : 0] waddr_i,
    input logic [$clog2(XLEN)-1 : 0] raddr_a_i,
    input logic [$clog2(XLEN)-1 : 0] raddr_b_i,
    output logic [XLEN - 1 : 0] data_a_o,
    output logic [XLEN - 1 : 0] data_b_o
);

  // Define register file
  logic [XLEN - 1 : 0] reg_file[XLEN];

  // Connect outputs
  assign data_a_o = reg_file[raddr_a_i];
  assign data_b_o = reg_file[raddr_b_i];

  // Write process
  always_ff @(posedge clk_i or negedge rst_n_i) begin
    if (!rst_n_i) begin
      for (int i = 0; i < XLEN; i++) begin
        reg_file[i] <= '0;
      end
    end else if (~halt_i & write_enable_i) begin
      // Ensure that reg_file[0] is not written
      if (|waddr_i) begin
        reg_file[waddr_i] <= data_i;
      end
    end
  end
endmodule
