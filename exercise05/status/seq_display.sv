module seq_display (
  input logic clk_i,
  input logic rst_ni,
  input logic [7:0] data_i,
  output logic [14:0]  fourteen_seg_o
); 
  logic signed [7:0] data_signed_i;

  // following segment order a - DP
  localparam logic [14:0]
    CHAR_R    = 15'b110011110000010,  //0x6782
    CHAR_O    = 15'b111111000001010,  //0x7E0A    
    CHAR_W    = 15'b011011000001010,  //0x360A
    CHAR_W_D  = 15'b011011000001011,  //0x360B
    CHAR_C    = 15'b100111000000000,  //0x4E00
    CHAR_C_D  = 15'b100111000000001;  //0x4E01

  typedef enum logic[2:0] {
    S_RESET,
    S_OKAY,
    S_WARM,
    S_WARM_DOT,
    S_COLD,
    S_COLD_DOT
  } state_t; 

  state_t current_state, next_state;

  always_ff @(posedge clk_i or posedge rst_ni) begin
    if (rst_ni) begin
      current_state <= S_RESET;
      fourteen_seg_o <= CHAR_R;
    end else begin
      current_state <= next_state;

      unique case (next_state)
        S_OKAY:     fourteen_seg_o <= CHAR_O;
        S_WARM:     fourteen_seg_o <= CHAR_W;
        S_WARM_DOT: fourteen_seg_o <= CHAR_W_D;
        S_COLD:     fourteen_seg_o <= CHAR_C;
        S_COLD_DOT: fourteen_seg_o <= CHAR_C_D;
        default:    fourteen_seg_o <= CHAR_R;
      endcase
    end
  end

  always_comb begin
    data_signed_i = signed'(data_i);

    unique case (current_state)
      S_RESET: begin
        if (data_signed_i > 45)
          next_state = S_WARM;
        else if (data_signed_i <= -16)
          next_state = S_COLD;
        else
          next_state = S_OKAY;
      end
      S_OKAY: begin
        if (data_signed_i > 45)
          next_state = S_WARM;
        else if (data_signed_i <= -16)
          next_state = S_COLD;
        else 
          next_state = S_OKAY;
      end
      S_WARM: begin
        if (data_signed_i > 60)
          next_state = S_WARM_DOT;
        else if (data_signed_i > -16 && data_signed_i <= 45)
          next_state = S_OKAY;
        else if (data_signed_i <= -16)
          next_state = S_COLD;
        else
          next_state = S_WARM;
      end
      S_WARM_DOT: begin
        next_state = S_RESET;
      end
      S_COLD: begin
        if (data_signed_i < -45)
          next_state = S_COLD_DOT;
        else if (data_signed_i > -16 && data_signed_i < 45)
          next_state = S_OKAY;
        else if (data_signed_i > 45)
          next_state = S_WARM;
        else
          next_state = S_COLD;
      end
      S_COLD_DOT: begin
        next_state = S_RESET;
      end
      default: next_state = S_RESET;
    endcase
  end

endmodule