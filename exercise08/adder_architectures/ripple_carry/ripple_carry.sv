module ripple_carry #(
    parameter N = 8
) (
    input logic [N - 1 : 0] a_i,
    input logic [N - 1 : 0] b_i,
    input logic c_i,
    output logic c_o,
    output logic [N - 1 : 0] o_o
);

  logic [N - 1 : 0] S;  // cadence keep_signal_name S
  logic [N : 0] C;  // cadence keep_signal_name C

  always_comb begin : blockName
    // C_in
    C[0] = c_i;

    // C
    for (int i = 0; i < N; i++) begin
      C[i+1] = (C[i] & (a_i[i] ^ b_i[i])) | (a_i[i] & b_i[i]);
    end

    // S
    S[N-1 : 0] = a_i[N-1 : 0] ^ b_i[N-1 : 0] ^ C[N-1 : 0];

    // Cout
    c_o = C[N];

    // S
    o_o = S;
  end
endmodule
