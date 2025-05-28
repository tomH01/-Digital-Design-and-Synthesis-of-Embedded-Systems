import rriscv_pkg::*;
module mem (
    input logic clk_i,
    input logic rst_n_i,
    input logic write_enable_i,
    input logic [XLEN - 1 : 0] data_i,
    input logic [XLEN - 1 : 0] addr_i,
    output logic [XLEN - 1 : 0] data_o
);


  // Mem Type
  data_mem_type_t mem_r;

  // write process
  always_ff @(posedge clk_i or negedge rst_n_i) begin
    if (!rst_n_i) begin
      for (int j = 0; j < DATA_MEM_SIZE; j++) begin
        mem_r[j] <= '0;
      end
      data_o <= '0;
    end else begin
      // Connect outputs
      data_o <= mem_r[addr_i];

      // Write
      if (write_enable_i) begin
        mem_r[addr_i] <= data_i;
      end
    end
  end
endmodule
