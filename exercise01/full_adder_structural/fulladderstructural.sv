module fulladderstruct (
    input logic a, b, cin,
    output logic sum, cout
);

    logic s1, c1, c2;

    halfadder ha1 (
        .a(a),
        .b(b),
        .s(s1),
        .c(c1)
    );

    halfadder ha2 (
        .a(s1),
        .b(cin),
        .s(sum),
        .c(c2)
    );

    assign cout = c1 | c2;

endmodule