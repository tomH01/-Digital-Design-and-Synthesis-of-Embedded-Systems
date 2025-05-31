import rriscv_pkg::*;

module instr_mem (
    input logic clk_i,
    input logic rst_n_i,
    input logic [XLEN - 1 : 0] addr_i,
    input logic addr_valid_i,
    output logic [XLEN - 1 : 0] data_o
);

  instr_mem_type_t instr_mem_r;
  initial begin
    $readmemb("test_prog.mem", instr_mem_r);
  end


  always_ff @(posedge clk_i or negedge rst_n_i) begin
    if (!rst_n_i) begin
      data_o <= instr_mem_r[0];
    end else begin
      if (addr_valid_i) begin
        data_o <= instr_mem_r[addr_i[XLEN-1 : 2]];
      end
    end
  end

endmodule

// Fib Code
// def fib(n):
//     one = 0
//     two = 1
//     thr = 0
//     if (n == 0):
//         return 0
//     if (n == 1):
//         return 1
//     if (n == 2):
//         return 1
//     for i in range(2, n + 1):
//         thr = one + two
//         one = two
//         two = thr
//     return two
//
// x1 := one
// x2 := two
// x3 := thr
// x4 := 1
// x5 := 2
// x6 := n
// x7 := n + 1
// x8 := i := 2
//
// # Load constants
// addi x1, x0, 0
// addi x2, x0, 1
// addi x3, x0, 0
// addi x4, x0, 1
// addi x5, x0, 2
//
// addi x6, x0, {N}
// add  x7, x6, x4
// addi x8, x0, 2
// bne  x6, x0, 4
// jal  x10,    24
// bne  x6, x4, 4
// jal  x10,    24
// bne  x6, x5 , 4
// jal  x10,    20
// bne  x8, x7, 4
// jal  x10,   20
// add  x3, x1, x2
// add  x1, x0, x2
// add  x2, x0, x3
// addi x8, x8,  1
// jal  x10, -16
// addi x15, x0, 0
// jal  x10, 8
// addi x15, x0, 1
// jal  x10, 4
// add  x15, x0, x2
// sw   x15, 0(x0) 
