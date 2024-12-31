module fillscreen(
     input logic clk, 
     input logic rst_n, 
     input logic [2:0] colour,
     input logic start, 
     output logic done,
     output logic [7:0] vga_x, 
     output logic [6:0] vga_y,
     output logic [2:0] vga_colour, 
     output logic vga_plot
     );   

     enum {WAIT, COLOUR, DONE, TEST} state;

     // constant for (159 for x) and (119 for y)
     logic en_x, xsel, en_y, ysel, en_c, csel;
     logic [7:0] stored_X;
     logic [6:0] stored_Y;
     logic [2:0] stored_colour;
     logic stored_done;
     logic stored_plot;

     // Output changes
     assign done = stored_done;
     assign vga_x = stored_X;
     assign vga_y = stored_Y;
     assign vga_colour = colour;
     assign vga_plot = stored_plot;

     always_ff @(posedge clk) begin
          if (!rst_n) begin
               state <= WAIT;
               stored_X <= 0;
               stored_Y <= 0;
               stored_done <= 0;
               stored_plot <= 0;
          end
          else begin
               case (state)
                    WAIT: begin
                         stored_X <= 0;
                         stored_Y <= 0;
                         stored_done <= 0;
                         stored_colour <= 0;
                         if (start) state <= COLOUR;
                    end
                    COLOUR: begin
                         stored_colour <= colour;

                         stored_plot <= 1;

                         if (stored_plot) begin
                              stored_plot <= 0;

                              if (stored_Y == 7'd119) begin
                                   stored_Y <= 0;
                                   if (stored_X == 8'd159) begin
                                        state <= DONE;
                                   end
                                   else begin
                                        stored_X <= stored_X + 1;
                                   end
                              end
                              else begin
                                   stored_Y <= stored_Y + 1;
                              end 
                         end 
                    end
                    DONE: begin
                         stored_done <= 1;
                         if (!start) state <= WAIT;
                    end
                    default: begin 
                         state <= WAIT;
                    end
               endcase
          end
     end
endmodule