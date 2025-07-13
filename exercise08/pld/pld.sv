module pld #(
    parameter NUM_PORTS_IN  = 1,  // --N
    parameter NUM_PORTS_OUT = 1   // --M
) (
  input  logic [                               NUM_PORTS_IN - 1 : 0] inputs_i,
  // With N many inputs we have 2**N many ANDs, which means we have (2*N * 2*N) * 2**N many fuses
  // With M many outputs we have M many ORs, which means we have M * (2**N * 2**N) many fuses
  input  logic [(2**(NUM_PORTS_IN + 2)) * (NUM_PORTS_IN**2) - 1 : 0] and_matrix_fuses_conf_i,
  input  logic [      NUM_PORTS_OUT * (2**(2*NUM_PORTS_IN)) - 1 : 0] or_matrix_fuses_conf_i,
  output logic [                              NUM_PORTS_OUT - 1 : 0] outputs_o
);

  // AND MATRIX has 2**N * ((2*num_ports_in) * (2*num_ports_in)) - 1 many fuses
  logic [2 * NUM_PORTS_IN - 1 : 0] and_matrix_fuse_control[2 ** NUM_PORTS_IN - 1 : 0][2 * NUM_PORTS_IN - 1 : 0];
  // OR MATRIX has M * ((2**num_ports_in) * (2**num_ports_in)) - 1 many fuses
  logic [2 ** NUM_PORTS_IN - 1 : 0] or_matrix_fuse_control[NUM_PORTS_OUT - 1 : 0][2 ** NUM_PORTS_IN - 1 : 0];
  // AND MATRIX has 2**N * 2 * num_ports_in - 1 many wires
  logic [2 * NUM_PORTS_IN - 1 : 0] and_matrix_fuse_output[2 ** NUM_PORTS_IN - 1 : 0];
  // AND MATRIX has 2**N - 1 outputs
  logic [2 ** NUM_PORTS_IN - 1 : 0] and_matrix_output;
  // OR MATRIX has M * 2**N - 1 many wires
  logic [2 ** NUM_PORTS_IN - 1 : 0] or_matrix_fuse_output[NUM_PORTS_OUT - 1 : 0];

  // Connect and matrix fuses control
  for (genvar i = 0; i < 2 ** NUM_PORTS_IN; i++) begin : gen_fuses_for_each_and_block
    for (genvar j = 0; j < 2 * NUM_PORTS_IN; j++) begin : gen_fuses_for_each_row
      assign and_matrix_fuse_control [i][j] = and_matrix_fuses_conf_i[(i * 4*(NUM_PORTS_IN ** 2) + (j + 1) * 2 * NUM_PORTS_IN) - 1 : (i * 4*(NUM_PORTS_IN ** 2) + j * 2 * NUM_PORTS_IN)];
    end
  end

  // Connect or matrix fuses control
  for (genvar i = 0; i < NUM_PORTS_OUT; i++) begin : gen_fuses_for_each_or_block
    for (genvar j = 0; j < 2 ** NUM_PORTS_IN; j++) begin : gen_fuses_for_each_row
      assign or_matrix_fuse_control [i][j] = or_matrix_fuses_conf_i[   (i + 1) * (2**NUM_PORTS_IN) + j * NUM_PORTS_OUT * (2**(NUM_PORTS_IN)) - 1 : i * (2**NUM_PORTS_IN) + j * NUM_PORTS_OUT * (2**(NUM_PORTS_IN)) ];
    end
  end

  // Generate AND-Matrix
  // Iterate over each AND-Block
  for (genvar i = 0; i < 2 ** NUM_PORTS_IN; i++) begin : gen_fuses_and
    // Iterate over each row in i-th AND-Block
    for (genvar y = 0; y < 2 * NUM_PORTS_IN; y++) begin : gen_any_port
      // Iterate over each pair of fuses (input-fuse and inverted-input-fuse)
      for (genvar x = 0; x < NUM_PORTS_IN; x++) begin : gen_any_input
        // Generate fuses

        // Fuse normal
        fuse fuse_normal (
            .a  (inputs_i[x]),
            .set(and_matrix_fuse_control[i][y][x*2]),
            .b  (and_matrix_fuse_output[i][y])
        );

        // Fuse inverted
        fuse fuse_inverted (
            .a  (~inputs_i[x]),
            .set(and_matrix_fuse_control[i][y][x*2+1]),
            .b  (and_matrix_fuse_output[i][y])
        );
      end
    end
    // Generate AND output
    assign and_matrix_output[i] = &and_matrix_fuse_output[i];
  end

  // Generate OR-Matrix
  // Iterate over each OR-Block
  for (genvar i = 0; i < NUM_PORTS_OUT; i++) begin : gen_fuses_or  // iterate over all ORs
    // Iterate over each row
    for (
        genvar y = 0; y < 2 ** NUM_PORTS_IN; y++
    ) begin : gen_any_port  // iterate over every port (including inverted ports)
      // Iterate over each column
      for (
          genvar x = 0; x < 2 ** NUM_PORTS_IN; x++
      ) begin : gen_any_input  // iterate over every input for each OR
        // Generate Fuses for each OR
        fuse fuse_or (
            .a  (and_matrix_output[y]),
            .set(or_matrix_fuse_control[i][y][x]),
            .b  (or_matrix_fuse_output[i][x])
        );
      end
    end
    // Generate OR output
    assign outputs_o[i] = |or_matrix_fuse_output[i];
  end
endmodule
