module tb_pld;

  localparam NUM_PORTS_IN = 3;
  localparam NUM_PORTS_OUT = 2;

  logic [NUM_PORTS_IN - 1 : 0] inputs;
  logic [(2**(NUM_PORTS_IN + 2)) * (NUM_PORTS_IN**2) - 1 : 0] and_matrix_fuses_conf;
  logic [NUM_PORTS_OUT * (2**(2*NUM_PORTS_IN)) - 1 : 0] or_matrix_fuses_conf;
  logic [NUM_PORTS_OUT - 1 : 0] outputs;

  pld #(
    .NUM_PORTS_IN(NUM_PORTS_IN),
    .NUM_PORTS_OUT(NUM_PORTS_OUT)
  ) i_dut (
    .inputs_i(inputs),
    .and_matrix_fuses_conf_i(and_matrix_fuses_conf),
    .or_matrix_fuses_conf_i(or_matrix_fuses_conf),
    .outputs_o(outputs)
  );

  initial begin
    and_matrix_fuses_conf = 288'b000100000100000100000001010000000100001000001000001000000010100000001000001000001000001000000001010000001000000100000100000100000001100000000100001000001000001000000001100000001000000100000100000100000010010000000100001000001000001000000010010000001000000100000100000100000010100000000100;
    or_matrix_fuses_conf = 128'b00000000000000000000000000000000000000000000000000000000000000000000000000000000111111110000000000000000010000000000000010111111;

    #(10ns);
    inputs = 'b000;
    #(10ns);
    inputs = 'b001;
    #(10ns);
    inputs = 'b010;
    #(10ns);
    inputs = 'b011;
    #(10ns);
    inputs = 'b100;
    #(10ns);
    inputs = 'b101;
    #(10ns);
    inputs = 'b110;
    #(10ns);
    inputs = 'b111;
    #(10ns);

  end
endmodule
