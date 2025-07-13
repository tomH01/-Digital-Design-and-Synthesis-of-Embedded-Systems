module tb_clocked_ripple_carry;

  // wait time
  localparam WT = 10ns;

  // Bitwidth
  localparam N = 8;

  // Clock
  localparam CLK = 100ps;

  logic clk_i = 0;
  logic rst_ni;
  logic [7 : 0] a_i, b_i, o_o, expected_o_o;
  logic c_o, expected_c_o;

  clocked_ripple_carry  
/*
  #(
      .N(N)
  )
*/  
  i_dut 
  (
      .clk_i(clk_i),
      .rst_ni(rst_ni),
      .a_i(a_i),
      .b_i(b_i),
      .o_o(o_o),
      .c_o(c_o)
  );

  task automatic assert_sum(
    input string test_name,
    input logic [7:0] a_val,
    input logic [7:0] b_val,
    input logic [7:0] expected_sum,
    input logic expected_carry
  );
  begin
    @(posedge clk_i);
    a_i = a_val;
    b_i = b_val;

    expected_o_o = expected_sum;
    expected_c_o = expected_carry;
    repeat (3) @(posedge clk_i);  // wait for stable result
    if (o_o == expected_o_o && c_o == expected_c_o) begin
      $display("[%s] passed!", test_name);
    end else begin
      $display("[%s] failed: \t Got o_o=%h, c_o=%b \t Expected: o_o=%h, c_o=%b ", 
                  test_name, o_o, c_o, expected_o_o, expected_c_o);
    end
    #(WT);
  end
  endtask


  always #(CLK) clk_i = ~clk_i;

  initial begin 
    rst_ni = 'b0;
    a_i = 8'b0;
    b_i = 8'b0;
    @(posedge clk_i);
    rst_ni = 'b1;
    #(WT);

    assert_sum("test_0", 8'hAA, 8'h01, 8'h00, 1'b0);  // should fail, test fail message
    assert_sum("test_1", 8'hAA, 8'h00, 8'hAA, 1'b0);
    assert_sum("test_2", 8'h00, 8'h00, 8'h00, 1'b0);
    assert_sum("test_3", 8'hFF, 8'h01, 8'h00, 1'b1);  // overflow
    assert_sum("test_4", 8'h55, 8'h55, 8'hAA, 1'b0);
    assert_sum("test_5", 8'h0F, 8'h01, 8'h10, 1'b0);
    assert_sum("test_6", 8'h80, 8'h80, 8'h00, 1'b1);  // overflow
    assert_sum("test_7", 8'h7F, 8'h01, 8'h80, 1'b0);
    assert_sum("test_8", 8'hAA, 8'h55, 8'hFF, 1'b0);
    assert_sum("test_9", 8'h01, 8'hFE, 8'hFF, 1'b0);

    @(posedge clk_i);
    @(posedge clk_i);
    $finish;
  end

endmodule