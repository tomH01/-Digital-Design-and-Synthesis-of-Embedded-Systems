module tb_xor_block;
    parameter int n = 2;

    logic [8*n-1:0] chunk;
    logic [8*n-1:0] key;
    logic [8*n-1:0] result;

    xor_block #(.n(n)) uut (
        .chunk(chunk),
        .key(key),
        .result(result)
    );

    initial begin 
        // test case 1
        chunk = {"f", "e"};
        key = {"H", "h"};   
        #10;

        // test case 2
        chunk = {"a", "b"};
        key = {"a", "b"};
        #10;

        $finish;
    end

endmodule

