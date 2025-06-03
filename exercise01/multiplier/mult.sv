module mult (
    input logic a0, a1, a2, b0, b1, b2,
    output logic s0, s1, s2, s3, s4, s5
)

    // partial products
    logic p00, p01, p02, p10, p11, p12, p20, p21, p22;

    // carry outputs from full adders
    logic c1, c2, c3, c4;

    and_gate and1 (.a(a0), .b(b0), .o(p00));
    and_gate and2 (.a(a0), .b(b1), .o(p01));
    and_gate and3 (.a(a0), .b(b2), .o(p02));
    and_gate and4 (.a(a1), .b(b0), .o(p10));
    and_gate and5 (.a(a1), .b(b1), .o(p11));
    and_gate and6 (.a(a1), .b(b2), .o(p12));   
    and_gate and7 (.a(a2), .b(b0), .o(p20));
    and_gate and8 (.a(a2), .b(b1), .o(p21));
    and_gate and9 (.a(a2), .b(b2), .o(p22));

    // least significant bit
    assign s0 = p00;

    full_adder adder1 (.a(p01), .b(p10), .cin(1'b0), .sum(s1), .cout(c1));
    full_adder adder2 (.a(p02), .b(p11), .cin(c1), .sum(s2), .cout(c2));
    full_adder adder3 (.a(p12), .b(p20), .cin(c2), .sum(s3), .cout(c3));
    full_adder adder4 (.a(p21), .b(p22), .cin(c3), .sum(s4), .cout(c4));

    // most significant bit
    assign s5 = c4;

endmodule    


