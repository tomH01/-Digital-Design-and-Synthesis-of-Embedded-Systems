// README: Add this module to the HDL_TB_SRC variable in the Makefile
module tmp_sens (
    input logic sample_i,
    output logic [7 : 0] tmp_o
);

  // Sample random date when sample_i is asserted
  always_ff @(posedge sample_i) begin
    tmp_o = $urandom_range(0, 256) - 128;
  end
endmodule
