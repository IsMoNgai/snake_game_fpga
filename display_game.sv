// `include "pos_rng.sv"

module display_game (input logic clk, input logic rst_n, input logic [2:0] colour, input logic [1:0] dir,
                     input logic start, output logic done, 
                     output logic [7:0] vga_x, output logic [6:0] vga_y, output logic [2:0] vga_colour, output logic vga_plot);

    enum {IDLE, INIT, APPLE, MOVE, ERASE_SNAKE_OLD, ERASE_APPLE_OLD, GAME_OVER} state;

    // for snake
    logic [7:0] curr_snake_posX, old_snake_posX;
    logic [6:0] curr_snake_posY, old_snake_posY;

    // for apple
    logic [7:0] curr_apple_posX, old_apple_posX;
    logic [6:0] curr_apple_posY, old_apple_posY;

    // rng_pos
    logic [7:0] rng_posX;
    logic [6:0] rng_posY;

    pos_rng pos_gen(.clk(clk), .rst_n(rst_n), .rng_posX(rng_posX), .rng_posY(rng_posY));

    always_comb begin 
        vga_x = 0;
        vga_y = 0;
        vga_colour = colour; // colour here is snake color
        vga_plot = 0;
        case(state)
            IDLE: begin 
                /* do nothing */
            end
            INIT: begin 
                vga_x = curr_snake_posX;
                vga_y = curr_snake_posY;
                vga_plot = 1;
            end
            APPLE: begin 
                vga_colour = 3'b100;
                vga_x = curr_apple_posX;
                vga_y = curr_apple_posY;
                vga_plot = 1;
            end
            MOVE: begin 
                vga_x = curr_snake_posX;
                vga_y = curr_snake_posY;
                vga_plot = 1;
            end
            ERASE_SNAKE_OLD: begin 
                vga_colour = 3'b000;
                vga_x = old_snake_posX;
                vga_y = old_snake_posY;
                vga_plot = 1;
            end
            ERASE_APPLE_OLD: begin 
                vga_colour = 3'b000;
                vga_x = old_apple_posX;
                vga_y = old_apple_posY;
                vga_plot = 1;
            end
            GAME_OVER: begin 
                /* do nothing or clear screen or show game over */
            end
        endcase
    end

    always_ff @(posedge clk or negedge rst_n) begin 
        if(!rst_n) begin 
            state <= IDLE;
            done <= 0;
            curr_apple_posX <= 15;
            curr_apple_posY <= 15;
            curr_snake_posX <= 0;
            curr_snake_posY <= 0;
        end else begin 
            case(state) 
                IDLE: begin 
                    curr_apple_posX <= 15;
                    curr_apple_posY <= 15;
                    curr_snake_posX <= 0;
                    curr_snake_posY <= 0;
                    if(start) begin 
                        done <= 0;
                        state <= INIT;
                    end               
                end
                /* Initialize the snake position */
                INIT: begin 
                    // curr_snake_posX <= rng_posX;
                    // curr_snake_posY <= rng_posY;
                    curr_snake_posX <= 20;
                    curr_snake_posY <= 15;
                    state <= APPLE;
                end
                /* generate an apple */
                APPLE: begin 
                    curr_apple_posX <= rng_posX;
                    curr_apple_posY <= rng_posY;
                    state <= ERASE_SNAKE_OLD;
                end
                /* control the movement of snake and other logics */
                MOVE: begin 
                    /* if the apple got eaten */
                    if(curr_snake_posX == curr_apple_posX && curr_snake_posY == curr_apple_posY) begin 
                        state <= ERASE_APPLE_OLD;
                    end 
                    /* if the snake go outside of box */
                    else if(curr_snake_posX == 0 || curr_snake_posY == 0 || curr_snake_posX == 8'd160 || curr_snake_posY == 7'd120) begin 
                        done <= 1;
                        state <= GAME_OVER;
                    end
                    /* decide the next move of the snake */
                    else begin 
                        case(dir)
                            /* go up */
                            2'b00: begin 
                                curr_snake_posY <= curr_snake_posY - 1;
                            end 
                            /* go left */
                            2'b01: begin 
                                curr_snake_posX <= curr_snake_posX - 1;
                            end 
                            /* go right */
                            2'b10: begin 
                                curr_snake_posX <= curr_snake_posX + 1;
                            end 
                            /* go down */
                            2'b11: begin 
                                curr_snake_posY <= curr_snake_posY + 1;
                            end 
                            /* default go right */
                            default: begin 
                                curr_snake_posX <= curr_snake_posX - 1;
                            end
                        endcase   

                        /* save the old_snake_pos for removal */
                        old_snake_posX <= curr_snake_posX;
                        old_snake_posY <= curr_snake_posY;
                        
                        state <= ERASE_SNAKE_OLD;                     
                    end
                end
                /* erase the snake's old position */
                ERASE_SNAKE_OLD: begin 
                    state <= MOVE;
                end
                /* erase the apple's old position */
                ERASE_APPLE_OLD: begin 
                    state <= APPLE;
                end
                /* gameover */
                GAME_OVER: begin 
                    done <= 0; 
                    state <= IDLE;
                end
            endcase
        end
    end

endmodule: display_game