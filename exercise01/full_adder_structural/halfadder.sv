module halfadder (
    input logic a, b,
    output logic s, c
);

    assign s = a ^ b;
    assign c = a & b;
endmodule    
