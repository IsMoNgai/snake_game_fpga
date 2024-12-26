`timescale 1ps / 1ps // delay of 1ps and precision down to 1ps

module tb_pos_rng();
    logic clk = 0;
    logic rst_n = 1;
    logic [7:0] rng_posX;
    logic [6:0] rng_posY;

    pos_rng dut(.*);

    always #5 clk = ~clk;

    initial begin 
        rst_n = 0;
        #10;
        rst_n = 1;
        #936; // <- change this to simulate a random pos generator
        $display("rng_posX: ", rng_posX);
        $display("rng_posY: ", rng_posY);
        $stop;
    end

endmodule: tb_pos_rng