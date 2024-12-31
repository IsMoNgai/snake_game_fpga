/*
This module is a top level for the actual 
snake game interfacing with De1-Soc
*/

module snake_game(input logic CLOCK_50, input logic [3:0] KEY,
                  input logic [9:0] SW, output logic [9:0] LEDR,
                  output logic [6:0] HEX0, output logic [6:0] HEX1, output logic [6:0] HEX2,
                  output logic [6:0] HEX3, output logic [6:0] HEX4, output logic [6:0] HEX5,
                  output logic [7:0] VGA_R, output logic [7:0] VGA_G, output logic [7:0] VGA_B,
                  output logic VGA_HS, output logic VGA_VS, output logic VGA_CLK,
                  output logic [7:0] VGA_X, output logic [6:0] VGA_Y,
                  output logic [2:0] VGA_COLOUR, output logic VGA_PLOT);
    
    /* initialization */
    logic VGA_BLANK, VGA_SYNC;
    logic [9:0] VGA_R_10, VGA_G_10, VGA_B_10;
    logic clk, rst_n, rst_n_display, should_rst_n;
    logic start, done;
    logic start_fs, done_fs; // fillscreen
    logic [1:0] dir;
    logic clock_slow;
    logic [31:0] count_slow;

    /* fillscreen */
    logic [7:0] vga_x_fs;
    logic [6:0] vga_y_fs;
    logic [2:0] vga_colour_fs;
    logic vga_plot_fs;

    /* display game */
    logic [7:0] vga_x_dg;
    logic [6:0] vga_y_dg;
    logic [2:0] vga_colour_dg;
    logic vga_plot_dg;

    /* assignment */
    assign VGA_R = VGA_R_10[9:2];
    assign VGA_G = VGA_G_10[9:2];
    assign VGA_B = VGA_B_10[9:2];

    assign clk = CLOCK_50;
    assign rst_n = ~SW[0];

    assign LEDR[0] = start;
    assign LEDR[1] = done;

    assign {LEDR[9], LEDR[8]} = dir;
    
    /* state machine */
    enum {START, GAME, GAME_END} state;

    /* clock divider */
    always_ff@(posedge CLOCK_50) begin 
        if(!rst_n) begin 
            clock_slow = 0;
            count_slow <= 0;
        end else begin 
            // 5 if testing for model sim
            if(count_slow == 5) begin
            // 500000 is good for hardware display
            // if(count_slow == 500000) begin
                clock_slow <= !clock_slow;
                count_slow <= 0;
            end else begin 
                count_slow <= count_slow + 1;
            end
        end
    end

    /* fillscreen to black again (clear) */
    fillscreen clear_screen(
        .clk(clk), 
        .rst_n(rst_n), 
        .colour(3'b000),
        .start(start_fs), 
        .done(done_fs),
        .vga_x(vga_x_fs), 
        .vga_y(vga_y_fs),
        .vga_colour(vga_colour_fs), 
        .vga_plot(vga_plot_fs)
    );

    /* actual game logic and display */
    display_game snake_game_display(
        .clk(clock_slow),
        .rst_n(rst_n_display),
        .colour(3'b010), // RGB
        .start(start),
        .done(done),    
        .dir(dir),
        .vga_x(vga_x_dg), 
        .vga_y(vga_y_dg),
        .vga_colour(vga_colour_dg),
        .vga_plot(vga_plot_dg)
    );

    /* vga display here */
    vga_adapter#(.RESOLUTION("160x120")) MyVGA(
        .resetn(rst_n), 
        .clock(CLOCK_50), 
        .colour(VGA_COLOUR),
        .x(VGA_X), 
        .y(VGA_Y), 
        .plot(VGA_PLOT),
        .VGA_R(VGA_R_10), 
        .VGA_G(VGA_G_10), 
        .VGA_B(VGA_B_10),
        .*
    );

    /* mux for vga_x, vga_y, colour, vga_plot */
    always_comb begin 
        VGA_X = 0;
        VGA_Y = 0;
        VGA_COLOUR = 0;
        VGA_PLOT = 0;
        case(state)
            START: begin end
            GAME: begin 
                VGA_X = vga_x_dg;
                VGA_Y = vga_y_dg;
                VGA_COLOUR = vga_colour_dg;
                VGA_PLOT = vga_plot_dg;
            end
            GAME_END: begin 
                VGA_X = vga_x_fs;
                VGA_Y = vga_y_fs;
                VGA_COLOUR = vga_colour_fs;
                VGA_PLOT = vga_plot_fs;
            end
        endcase
    end

    always_ff @(posedge clk) begin 
        if(!rst_n) begin 
            start <= 1;
            start_fs <= 0;
            state <= START;
        end else begin 
            case(state)
                START: begin 
                    if(start) begin
                        rst_n_display <= 1;
                        should_rst_n <= 1;
                        state <= GAME;
                    end 
                end
                /*This part control which button move the snake*/
                GAME: begin 
                    if(done) begin 
                        start <= 0;
                        start_fs <= 1;
                        state <= GAME_END;
                    end else begin 
                        if(rst_n_display && should_rst_n) begin 
                            rst_n_display <= 0;
                            should_rst_n <= 0;
                        end
                        else if (rst_n_display) begin 
                            rst_n_display <= 1;
                        end 
                        else if (!rst_n_display) begin 
                            rst_n_display <= 1;
                        end
                        /* go up */
                        if(!KEY[0]) begin 
                            dir <= 0;
                        end 
                        /* go left */
                        else if(!KEY[2]) begin 
                            dir <= 1;
                        end
                        /* go right */
                        else if(!KEY[1]) begin 
                            dir <= 2;
                        end
                        /* go down */
                        else if(!KEY[3]) begin 
                            dir <= 3;
                        end 
                        /* keep original direction */
                        else begin 
                            dir <= dir;
                        end
                    end
                end
                GAME_END: begin 
                    start <= 1; 
                    if(done_fs) begin 
                        start_fs <= 0;
                        state <= START;                        
                    end
                end
            endcase
        end
    end

endmodule: snake_game