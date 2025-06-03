module tb_cdc;
  // Connections
  logic clock_fast;
  logic clock_slow;
  logic rst_ni;
  logic [7 : 0] tmp;
  logic [14 : 0] fourteen_seg_out;

  // Tmp sense instance
  tmp_sens tmp_sens (
      .sample_i(clock_fast),
      .tmp_o   (tmp)
  );

  pipeline i_dut (
      .rst_ni        (rst_ni),
      .clock_fast    (clock_fast),
      .clock_slow    (clock_slow),
      .temperature   (tmp),
      .fourteen_seg_o(fourteen_seg_out)
  );

  always #(2ns) clock_fast = ~clock_fast;
  always #(3.7ns) clock_slow = ~clock_slow;

  initial begin
    clock_slow = 0;
    clock_fast = 0;
    rst_ni = 'b0;
    #(1ns);

    // Wait for FIFO fill
    #(50ns);

    // Run
    rst_ni = 'b1;
    #(1000ns);
    $finish;
  end

endmodule
