module cbc_cipher #(parameter n = 2, parameter m = 4) (
    input logic enc_dec,            // 1=encrypt, 0=decrypt
    input logic [8*n*m-1:0] message,
    input logic [8*n-1:0] key,
    output logic [8*n*m-1:0] result
);

    logic [8*n-1:0] block;
    logic [8*n-1:0] prev;
    logic [8*n-1:0] xor_out;

    integer i;
    always_comb begin
        prev = key;
        for (i=0; i<m; i++) begin
            block = message[i*8*n +: 8*n]; 
            xor_out = block ^ prev;
            result[i*8*n +: 8*n] = xor_out;

            if (enc_dec) begin
                // Encryption
                prev = xor_out;
            end else begin
                // Decryption
                prev = block;
            end

        end
    end
endmodule

