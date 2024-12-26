`timescale 1ps / 1ps;

module tb_display_game();
    logic clk = 0;
    logic rst_n = 1;
    logic [1:0] colour;
    logic start;

    logic done;
    logic [7:0] vga_x;
    logic [6:0] vga_y;
    logic [1:0] vga_colour;
    logic vga_plot;

    display_game dut(.*);

    always #5 clk = !clk;

    initial begin 
        rst_n = 0; #10;
        rst_n = 1; #10;
        colour = 3'b100;
        start = 1;
        #10;
        start = 0;
        #50;
        
        #852;

        colour = 3'b100;
        start = 1;
        #10;
        start = 0;
        #50;
        
        colour = 3'b100;
        start = 1;
        #10;
        start = 0;
        #50;
        $stop;

    end

endmodule: tb_display_game