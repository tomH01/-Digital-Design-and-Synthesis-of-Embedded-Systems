module n_bit_cdc (
    input logic rst_ni,
    input logic clk_0_i,
    input logic [7 : 0] data_i,
    input logic clk_1_i,
    output logic [7 : 0] data_o
);
  logic [7 : 0] ff_1, ff_2, ff_3;

  always_ff @(posedge clk_0_i or negedge rst_ni) begin
    if (!rst_ni) begin
      ff_1 <= '0;
    end else begin
      ff_1 <= data_i;
    end
  end

  always_ff @(posedge clk_1_i or negedge rst_ni) begin
    if (!rst_ni) begin
      ff_2 <= '0;
      ff_3 <= '0;
    end else begin
      ff_2 <= ff_1;
      ff_3 <= ff_2;
    end
  end

  assign data_o = ff_3;

endmodule