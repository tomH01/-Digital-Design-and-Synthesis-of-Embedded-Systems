module tb_cbc_cipher;
    parameter n = 2;
    parameter m = 2;

    logic enc_dec;
    logic [8*n*m-1:0] message;
    logic [8*n-1:0] key;
    logic [8*n*m-1:0] result;

    cbc_cipher #(n, m) uut (
        .enc_dec(enc_dec),
        .message(message),
        .key(key),
        .result(result)
    );

    initial begin
        $dumpfile("cbc_cipher.vcd");
        $dumpvars(0, tb_cbc_cipher);

        // Test case 1
        key = 16'h1111;
        message = {
            8'h11, 8'h22,
            8'h33, 8'h44
        };
        
        enc_dec = 1'b1;     // Encrypt
        #1;

        enc_dec = 1'b0;     // Decrypt
        message = result;
        #1;

        // Test case 2
        key = 16'h2222;
        message = {
            8'h10, 8'h20,
            8'h30, 8'h40
        };
        
        enc_dec = 1'b1;     // Encrypt
        #1;

        enc_dec = 1'b0;     // Decrypt
        message = result;
        #1;

        // Test case 3
        key = 16'h9999;
        message = {
            8'hAA, 8'hBB,
            8'hCC, 8'hDD
        };
        
        enc_dec = 1'b1;     // Encrypt
        #1;

        enc_dec = 1'b0;     // Decrypt
        message = result;
        #1;

        // Test case 4
        key = 16'hAAAA;
        message = {
            8'h00, 8'h00,
            8'h00, 8'h00
        };
        
        enc_dec = 1'b1;     // Encrypt
        #1;

        enc_dec = 1'b0;     // Decrypt
        message = result;
        #1;  

        // Test case 5
        key = 16'hCCCC;
        message = {
            8'h19, 8'h29,
            8'h39, 8'h49
        };
        
        enc_dec = 1'b1;     // Encrypt
        #1;

        enc_dec = 1'b0;     // Decrypt
        message = result;
        #1;      

        $finish;
    end
endmodule