module tb_adder;

  // Wait time
  localparam WT = 600ns;


  logic [7 : 0] a, b, o;
  logic c_i, c_o;

  carry_lookahead i_dut (
      .a_i(a),
      .b_i(b),
      .c_i(c_i),
      .c_o(c_o),
      .o_o(o)
  );

  initial begin
    a   = 'b110;
    b   = 'b110;
    c_i = 'b0;

    #(WT);

    a   = 'b110;
    b   = 'b110;
    c_i = 'b1;
    #(WT);

    a   = 'b10000000;
    b   = 'b10000000;
    c_i = 'b0;
    #(WT);

    a   = 'b10000000;
    b   = 'b10000000;
    c_i = 'b1;
    #(WT);

    a   = 'b0;
    b   = 'b11111111;
    c_i = 'b0;
    #(WT);

    a   = 'b0;
    b   = 'b11111111;
    c_i = 'b1;
    #(WT);
    $stop;
  end
endmodule
