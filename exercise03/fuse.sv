module fuse (
    input  logic a,
    input  logic set,
    output logic b
);
  // TODO
  assign b = set ? a : 1'bz;
endmodule
