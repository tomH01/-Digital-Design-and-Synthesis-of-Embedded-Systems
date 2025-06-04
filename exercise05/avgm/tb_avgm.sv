module tb_avgm;

  logic clk_i = 0;
  logic rst_ni;
  logic [7:0] data_i;
  logic signed [7:0] avg_o; // unsigned in real usage

  avg i_dut (
      .rst_ni(rst_ni),
      .clk_i(clk_i),
      .data_i(data_i),
      .data_o(avg_o)
  );

  // Clock generation
  always #(2ns) clk_i = ~clk_i;

  initial begin
    rst_ni = 'b0;
    data_i = 0;
    #(10ns);
    rst_ni = 'b1;

    // Test cases
    @(posedge clk_i); data_i = 10;    // expect avg_o = 3
    @(posedge clk_i); data_i = 20;    // expect avg_o = 10
    @(posedge clk_i); data_i = -30;   // expect avg_o = 0
    @(posedge clk_i); data_i = -50;   // expect avg_o = -20
    @(posedge clk_i); data_i = 50;    // expect avg_o = -10
    @(posedge clk_i); data_i = 30;    // expect avg_o = 10
    @(posedge clk_i); data_i = 100;   // expect avg_o = 60
    @(posedge clk_i); data_i = -100;  // expect avg_o = 10
    @(posedge clk_i); data_i = -120;  // expect avg_o = -40
    @(posedge clk_i); data_i = -20;   // expect avg_o = -80
    @(posedge clk_i); data_i = 110;   // expect avg_o = -10
    @(posedge clk_i); data_i = 60;    // expect avg_o = 50
    @(posedge clk_i); data_i = -50;  // expect avg_o = 40
    @(posedge clk_i); data_i = 10;   // expect avg_o = 6
    @(posedge clk_i); data_i = 50;    // expect avg_o = 3
    @(posedge clk_i); data_i = 0;    // expect avg_o = 20
    repeat(2) @(posedge clk_i);    
    $finish;
  end
endmodule