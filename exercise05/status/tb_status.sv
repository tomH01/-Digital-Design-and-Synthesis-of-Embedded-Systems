module tb_status;
  logic clk_i = 0;
  logic rst_ni;
  logic [7:0] data_i;
  logic [14:0] fourteen_seg_o;

  seg_display i_dut (
      .clk_i(clk_i),
      .rst_ni(rst_ni),
      .data_i(data_i),
      .fourteen_seg_out(fourteen_seg_o)
  );

  // Clock generation
  always #(7.5ns) clk_i = ~clk_i;

  initial begin
    rst_ni = 'b0;
    data_i = 0;
    #20ns;    // expect RESET
    rst_ni = 'b1;

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