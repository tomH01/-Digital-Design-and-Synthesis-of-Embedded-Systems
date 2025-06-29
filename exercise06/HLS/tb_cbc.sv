module tb_cbc;

logic ap_clk;
logic ap_rst;

logic ap_start;
logic ap_done;
logic ap_idle;
logic ap_ready;

logic encrypt_decrypt;
logic [63:0] message;
logic [31:0] key;

logic [63:0] ap_return;

n_block_cbc dut ( 
  .ap_clk(ap_clk),
  .ap_rst(ap_rst),
  .ap_start(ap_start),
  .ap_done(ap_done),
  .ap_idle(ap_idle),
  .ap_ready(ap_ready),
  .encrypt_decrypt(encrypt_decrypt),
  .message(message),
  .key(key),
  .ap_return(ap_return)
);

always #(10ns) ap_clk = ~ap_clk;

task reset_dut ();
begin
  ap_clk = 0;
  ap_rst = 1;
  ap_start = 0;
  encrypt_decrypt = 0;
  message = 0;
  key = 0;
  repeat (4) @(posedge ap_clk); 
  ap_rst = 0;

  wait (ap_idle == 1);
  $display("ap_idle=%b", ap_idle);
  @(posedge ap_clk); 
end
endtask

task run_testcase (
  input logic encrypt,
  input logic [63:0] in_message,
  input logic [31:0] in_key,
  input logic [63:0] expected_output   
);
begin
  encrypt_decrypt = encrypt;
  message = in_message;
  key = in_key;
  repeat(4) @(posedge ap_clk); 
  $display("in_message=%h in_key=%h", in_message, in_key);
  ap_start = 1;
  @(posedge ap_clk);
  wait (ap_done);
  if (ap_return !== expected_output) begin
    $error("Test failed: got %h, expected %h", ap_return, expected_output);
  end

  ap_start = 0;
  #(45ns);
end
endtask


  initial begin
    reset_dut();
    // $monitor("Time %t | rst=%b start=%b done=%b idle=%b ready=%b", $time, ap_rst, ap_start, ap_done, ap_idle, ap_ready);

    run_testcase(1'b1, 64'h0000000000000000, 32'h00000000, 64'h0000000000000000);

    run_testcase(1'b1, 64'h10a0c0e060007000, 32'h10101010, 64'h00b0d0f060b0a0f0); 

    run_testcase(1'b1, 64'h101000e010007300, 32'h10101010, 64'h000010f0100063f0);

    run_testcase(1'b1, 64'h1111111111111111, 32'h00000000, 64'h1111111100000000);
    $finish;

  end
endmodule