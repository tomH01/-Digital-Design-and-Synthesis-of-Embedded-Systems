module alu (
    input logic[1:0] instruction,   // 00 = add, 01=sub, 1x= encrypt/decrypt
    input logic [15:0] a,
    input logic [15:0] b, 
    output logic [15:0] result 
);

    logic[15:0] add_out, sub_out, encdec_out;
    logic enc_dec;
    
    assign add_out = a + b;
    assign sub_out = a - b;
    assign enc_dec = instruction[0]; 


    cbc_cipher #(.n(2), .m(1)) cbc_inst (
        .enc_dec(enc_dec),
        .message(b),
        .key(a),
        .result(encdec_out)
    );

    always_comb begin
        case (instruction)
            2'b00: result = add_out;
            2'b01: result = sub_out;
            default: begin
                result = encdec_out;
            end
        endcase
    end
endmodule

