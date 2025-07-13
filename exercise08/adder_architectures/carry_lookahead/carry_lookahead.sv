module carry_lookahead (
    input logic [7 : 0] a_i,
    input logic [7 : 0] b_i,
    input logic c_i,
    output logic c_o,
    output logic [7 : 0] o_o
);

  logic [7 : 0] C;  // cadence keep_signal_name C
  logic [7 : 0] G;  // cadence keep_signal_name G
  logic [7 : 0] P;  // cadence keep_signal_name P

  always_comb begin : lookahead_adder
    P = a_i ^ b_i;
    G = a_i & b_i;

    // Pos 0
    C[0] = G[0] | (c_i & P[0]);

    // Pos 1
    C[1] = G[1] | (G[0] & P[1]) | (c_i & P[1] & P[0]);

    // Pos 2
    C[2] = G[2] | (G[1] & P[2]) | (G[0] & P[2] & P[1]) | (c_i & P[2] & P[1] & P[0]);

    // Pos 3
    C[3] = G[3] |
    (G[2] & P[3]) |
    (G[1] & P[3] & P[2]) |
    (G[0] & P[3] & P[1]) |
    (c_i & P[3] & P[2] & P [1] & P[0]);

    // Pos 4
    C[4] = G[4] |
    (G[3] & P[4]) |
    (G[2] & P[4] & P[3]) |
    (G[1] & P[4] & P[3] & P[2]) |
    (G[0] & P[4] & P[3] & P[2] & P[1]) |
    (c_i & P[4] & P[3] & P[2] & P[1] & P[0]);

    //Pos 5
    C[5] = G[5] |
    (G[4] & P[5]) |
    (G[3] & P[5] & P[4]) |
    (G[2] & P[5] & P[4] & P[3]) |
    (G[1] & P[5] & P[4] & P[3] & P[2]) |
    (G[0] & P[5] & P[4] & P[3] & P[2] & P[1]) |
    (c_i & P[5] & P[4] & P[3] & P[2] & P[1] & P[0]);

    // Pos 6
    C[6] = G[6] |
    (G[5] & P[6]) |
    (G[4] & P[6] & P[5]) |
    (G[3] & P[6] & P[5] & P[4]) |
    (G[2] & P[6] & P[5] & P[4] & P[3]) |
    (G[1] & P[6] & P[5] & P[4] & P[3] & P[2]) |
    (G[0] & P[6] & P[5] & P[4] & P[3] & P[2] & P[1]) |
    (c_i & P[6] & P[5] & P[4] & P[3] & P[2] & P[1] & P[0]);

    // Pos 7
    C[7] = G[7] |
    (G[6] & P[7]) |
    (G[5] & P[7] & P[6]) |
    (G[4] & P[7] & P[6] & P[5]) |
    (G[3] & P[7] & P[6] & P[5] & P[4]) |
    (G[2] & P[7] & P[6] & P[5] & P[4] & P[3]) |
    (G[1] & P[7] & P[6] & P[5] & P[4] & P[3] & P[2]) |
    (G[0] & P[7] & P[6] & P[5] & P[4] & P[3] & P[2] & P[1]) |
    (c_i & P[7] & P[6] & P[5] & P[4] & P[3] & P[2] & P[1] & P[0]);


    o_o[0] = P[0] ^ c_i;
    o_o[7 : 1] = P[7 : 1] ^ C[6 : 0];

    c_o = C[7];
  end

endmodule
