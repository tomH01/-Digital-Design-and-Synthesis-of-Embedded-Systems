module sram #(
    parameter BW = 32,
    parameter AW = 7
) (
    input logic clk_i,
    chip_enable_i,
    write_enable_i,
    input logic [AW - 1 : 0] addr_i,
    input logic [BW - 1 : 0] data_i,
    output logic [BW - 1 : 0] data_o
);

  // Mem
  logic [BW - 1 : 0] mem[2**AW - 1 : 0];

  // Memory Read process
  always_ff @(posedge clk_i) begin
    if ((chip_enable_i == 'b0) & (write_enable_i == 'b0)) begin
      mem[addr_i] <= data_i;
    end
  end

  // Memory Write process
  always_ff @(posedge clk_i) begin
    if ((chip_enable_i == 'b0) & (write_enable_i == 'b1)) begin
      data_o <= mem[addr_i];
    end
  end
endmodule
