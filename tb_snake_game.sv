`timescale 1ps / 1ps;

module tb_snake_game();

    logic CLOCK_50 = 0;
    logic [3:0] KEY;
    logic [9:0] SW;
    logic [9:0] LEDR;
    logic [6:0] HEX0; 
    logic [6:0] HEX1; 
    logic [6:0] HEX2;
    logic [6:0] HEX3; 
    logic [6:0] HEX4; 
    logic [6:0] HEX5;
    logic [7:0] VGA_R;
    logic [7:0] VGA_G;
    logic [7:0] VGA_B;
    logic VGA_HS;
    logic VGA_VS; 
    logic VGA_CLK;
    logic [7:0] VGA_X;
    logic [6:0] VGA_Y;
    logic [2:0] VGA_COLOUR;
    logic VGA_PLOT;
    
    always #5 CLOCK_50 = !CLOCK_50;   

    snake_game dut(.*);

    initial begin 
        #5;
        SW[0] = 0;
        #10;
        SW[0] = 1;
        #10;
        SW[0] = 0;

        wait(dut.state == dut.GAME_END);
    end

endmodule: tb_snake_game

