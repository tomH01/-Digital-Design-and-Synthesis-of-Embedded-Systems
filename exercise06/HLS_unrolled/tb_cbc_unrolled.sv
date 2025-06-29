module tb_cbc;

logic ap_start;
logic ap_done;
logic ap_idle;
logic ap_ready;

logic encrypt_decrypt;
logic [63:0] message;
logic [31:0] key;

logic [63:0] ap_return;

n_block_cbc dut ( 
  .ap_start(ap_start),
  .ap_done(ap_done),
  .ap_idle(ap_idle),
  .ap_ready(ap_ready),
  .encrypt_decrypt(encrypt_decrypt),
  .message(message),
  .key(key),
  .ap_return(ap_return)
);


task reset_dut ();
begin
  ap_start = 0;
  encrypt_decrypt = 0;
  message = 0;
  key = 0;

  wait (ap_idle == 1);
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

  ap_start = 1;
  #(1ns);

  $display("ap_return: %h", ap_return);
  if (ap_return !== expected_output) begin
    $error("Test failed: got %h, expected %h", ap_return, expected_output);
  end else begin
    $display("Test passed: got %h, expected %h", ap_return, expected_output);
  end
end
endtask


  initial begin
    reset_dut();
    $monitor("Time %t | start=%b done=%b idle=%b ready=%b", $time, ap_start, ap_done, ap_idle, ap_ready);

    run_testcase(1'b1, 64'h0000000000000000, 32'h00000000, 64'h0000000000000000);

    run_testcase(1'b1, 64'h10a0c0e060007000, 32'h10101010, 64'h00b0d0f060b0a0f0); 

    run_testcase(1'b1, 64'h101000e010007300, 32'h10101010, 64'h000010f0100063f0);

    run_testcase(1'b1, 64'h1111111111111111, 32'h00000000, 64'h1111111100000000);
    $finish;

  end
endmodule