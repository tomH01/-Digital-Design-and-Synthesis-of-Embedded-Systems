module avg (
  input logic rst_ni,
  input logic clk_i,
  input logic [7 : 0] data_i,
  output logic [7 : 0] data_o
);

  logic signed [7 : 0] val1, val2, val3;

  always_ff @(posedge clk_i or posedge rst_ni) begin
    if (rst_ni) begin
      val1 <= 0;
      val2 <= 0;
      val3 <= 0;
      data_o <= 0;
    end else begin
      // shift values
      val3 <= val2; 
      val2 <= val1; 
      val1 <= signed'(data_i);

      // average 
      data_o <= unsigned'((val1 + val2 + val3) / 3);
    end
  end 
endmodule