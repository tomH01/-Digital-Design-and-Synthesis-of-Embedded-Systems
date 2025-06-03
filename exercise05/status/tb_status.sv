module tb_status;
  logic clk_i = 0;
  logic rst_ni;
  logic [7:0] data_i;
  logic [14:0] fourteen_seg_o;

  seq_display i_dut (
      .clk_i(clk_i),
      .rst_ni(rst_ni),
      .data_i(data_i),
      .fourteen_seg_o(fourteen_seg_o)
  );

  // Clock generation
  always #(10ns) clk_i = ~clk_i;

  initial begin
    rst_ni = 1;
    data_i = 0;
    #25ns;    // expect RESET
    rst_ni = 0;

    // Test cases
    @(posedge clk_i); data_i = 10;  // expect OKAY
    @(posedge clk_i); data_i = 50;  // expect WARM
    @(posedge clk_i); data_i = -20; // expect COLD
    @(posedge clk_i); data_i = -60; // expect TOO COLD
    @(posedge clk_i);               // expect RESET
    @(posedge clk_i); data_i = 70;  // expect WARM 
    @(posedge clk_i);               // expect TOO WARM
    @(posedge clk_i);               // expect RESET
    @(posedge clk_i); data_i = 0;   // expect OKAY
    @(posedge clk_i);
    $finish;
  end

endmodule