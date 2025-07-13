module tb_pld;

  localparam unsigned NUM_PORTS_IN = 1;
  localparam unsigned NUM_PORTS_OUT = 1;

  logic [NUM_PORTS_IN - 1 : 0] inputs;
  logic [(2**(NUM_PORTS_IN + 2)) * (NUM_PORTS_IN**2) - 1 : 0] and_matrix_fuses_conf;
  logic [NUM_PORTS_OUT * (2**(2*NUM_PORTS_IN)) - 1 : 0] or_matrix_fuses_conf;
  logic [NUM_PORTS_OUT - 1 : 0] outputs;

`ifndef SYNTHESIS
  pld #(
    .NUM_PORTS_IN (NUM_PORTS_IN),
    .NUM_PORTS_OUT(NUM_PORTS_OUT)
  ) i_dut (
      .inputs_i               (inputs),
      .and_matrix_fuses_conf_i(and_matrix_fuses_conf),
      .or_matrix_fuses_conf_i (or_matrix_fuses_conf),
      .outputs_o              (outputs)
  );
`else
  pld i_dut (
      .inputs_i               (inputs),
      .and_matrix_fuses_conf_i(and_matrix_fuses_conf),
      .or_matrix_fuses_conf_i (or_matrix_fuses_conf),
      .outputs_o              (outputs)
  );
`endif

  initial begin
    // config for 8 bit out 3 bit in
    and_matrix_fuses_conf = 'b01101010;
    or_matrix_fuses_conf  = 'b0011;


    // Testbench Start
    #(10ns);
    inputs = 'b0;
    #(10ns);
    inputs = 'b1;
    #(10ns);
    // Testbench End

  end
endmodule
