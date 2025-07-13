module clocked_ripple_carry #(
    parameter N = 8
) (
    input logic clk_i,
    input logic rst_ni,
    input logic [N - 1 : 0] a_i,
    input logic [N - 1 : 0] b_i,
    output logic [N - 1 : 0] o_o,
    output logic c_o
);
  
  logic [N - 1 : 0] sum;
  logic carry;

  ripple_carry #(
    .N(N)
  ) ripple_carry_inst (
    .a_i(a_i),
    .b_i(b_i),
    .c_i(0'b0), // clocked ripple carry does not use a carry-in
    .c_o(carry),
    .o_o(sum)
  );

  always_ff @(posedge clk_i or negedge rst_ni) begin
    if (!rst_ni) begin
      o_o <= '0;
      c_o <= 1'b0;
    end else begin
      o_o <= sum;
      c_o <= carry;
    end
  end
endmodule