module xor_block #(parameter n = 2) (
    input logic [8*n-1:0] chunk,
    input logic [8*n-1:0] key,
    output logic [8*n-1:0] result
);

    assign result = chunk ^ key;

endmodule