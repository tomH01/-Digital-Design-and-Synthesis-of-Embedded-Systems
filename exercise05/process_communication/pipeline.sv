module pipeline (
    input logic rst_ni,
    input logic clock_slow,
    input logic clock_fast,
    input logic [7 : 0] temperature,
    output logic [14 : 0] fourteen_seg_o
);

  logic [7 : 0] avg_out;
  logic [7 : 0] cdc_out;
  // AVGM instance
  avg avg (
      .rst_ni(rst_ni),
      .clk_i (clock_fast),
      .data_i(temperature),
      .data_o(avg_out)
  );

  if (`USE_CDC) begin : gen_cdc
    // CDC
    n_bit_cdc i_cdc (
        .rst_ni (rst_ni),
        .clk_0_i(clock_fast),
        .data_i (avg_out),
        .clk_1_i(clock_slow),
        .data_o (cdc_out)
    );
  end else begin : gen_no_cdc
    assign cdc_out = avg_out;
  end

  // Seg display
  seg_display i_seg_display (
      .clk_i           (clock_slow),
      .rst_ni          (rst_ni),
      .data_i          (cdc_out),
      .fourteen_seg_out(fourteen_seg_o)
  );

endmodule
