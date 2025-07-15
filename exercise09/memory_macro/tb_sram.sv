module tb_sram;

  logic clk;
  logic cs_n;
  logic wc_n;
  logic [6 : 0] addr;
  logic [31 : 0] data_in;
  logic [31 : 0] data_out, data_out2;

  SRAM_32x128_1rw i_dut (
      .clk0 (clk),
      .csb0 (cs_n),
      .web0 (wc_n),
      .addr0(addr),
      .din0 (data_in),
      .dout0(data_out)
  );

  sram i_dut_regs (
      .clk_i         (clk),
      .chip_enable_i (cs_n),
      .write_enable_i(wc_n),
      .addr_i        (addr),
      .data_i        (data_in),
      .data_o        (data_out2)
  );

  always #(10ns) clk = ~clk;

  initial begin
    clk = 0;
    #(1ns);


    addr = 'b0;
    cs_n = 'b1;
    wc_n = 'b1;
    data_in = 42;

    @(posedge clk);
    @(posedge clk);
    wc_n = 'b0;

    @(posedge clk);
    @(posedge clk);
    cs_n = 'b0;

    @(posedge clk);
    @(posedge clk);
    wc_n = 'b1;

    @(posedge clk);
    @(posedge clk);
    $stop;
  end
endmodule
