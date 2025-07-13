module fuse (
    input  logic a,
    input  logic set,
    output logic b
);

  assign b = (set == 1) ? a : 1'bz;
endmodule
