module tb_alu;
    logic [1:0] instruction;
    logic [15:0] a, b, result; 

    alu uut (
        .instruction(instruction),
        .a(a),
        .b(b),
        .result(result)
    );

    task testcase (
        input [1:0] instr,
        input [15:0] operand_a,
        input [15:0] operand_b    
    );
    begin
        instruction = instr;
        a = operand_a;
        b = operand_b;
        #1;
    end
    endtask

    initial begin
        $dumpfile("alu.vcd");
        $dumpvars(0, tb_alu);

        // add
        testcase(2'b00, 16'd10, 16'd15);
        testcase(2'b00, 16'd10000, 16'd2000);

        // sub
        testcase(2'b01, 16'd50, 16'd20);
        testcase(2'b01, 16'd3000, 16'd1500);

        // encrypt
        testcase(2'b10, 16'hA5A5, 16'h1234);
        testcase(2'b10, 16'hFFFF, 16'h0001);

        // decrypt
        testcase(2'b11, 16'h0001, 16'hFFFF);
        testcase(2'b11, 16'h1234, 16'hA5A5);
    end
endmodule