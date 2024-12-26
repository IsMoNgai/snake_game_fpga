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
    logic [1:0] dir;
    logic clock_slow;
    logic [31:0] count_slow;

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
            if(count_slow == 500000) begin 
                clock_slow <= !clock_slow;
                count_slow <= 0;
            end else begin 
                count_slow <= count_slow + 1;
            end
        end
    end

    display_game snake_game_display(
        .clk(clock_slow),
        .rst_n(rst_n_display),
        .colour(3'b010), // RGB
        .start(start),
        .done(done), 
        .dir(dir),
        .vga_x(VGA_X), 
        .vga_y(VGA_Y),
        .vga_colour(VGA_COLOUR),
        .vga_plot(VGA_PLOT)
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

    always_comb begin 
        case(state)
            START: begin end
            GAME: begin 

            end
            GAME_END: begin end
        endcase
    end

    always_ff @(posedge clk) begin 
        if(!rst_n) begin 
            start <= 1;
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
                GAME: begin 
                    if(done) begin 
                        start <= 0;
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
                    state <= START;
                end
            endcase
        end
    end

endmodule: snake_game