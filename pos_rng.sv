module pos_rng(input logic clk, input logic rst_n, 
               output logic [7:0] rng_posX, output logic [6:0] rng_posY);
		  
parameter dividerX = 1;
parameter dividerY = 2;

logic [7:0] count_posX;
logic [6:0] count_posY;

logic clkX, clkY;
logic [7:0] counterX, counterY;

logic delay_rst_n_X;
logic delay_rst_n_Y;

/* counter based clock divider */
always_ff @(posedge clk) begin 
   if (!rst_n) begin 
      clkX <= 0;
      clkY <= 0;
      counterX <= 0;
      counterY <= 0;
      delay_rst_n_X <= 0;
      delay_rst_n_Y <= 0;
   end else begin 
      if(counterX == dividerX-1) begin 
         counterX <= 0;
         clkX <= ~clkX;
      end else begin 
         counterX <= counterX + 1;
      end
      if(counterY == dividerY-1) begin 
         counterY <= 0;
         clkY <= ~clkY;
      end else begin 
         counterY <= counterY + 1;
      end
   end
end

/* generate posx */
always_ff @(posedge clkX)
   if (!delay_rst_n_X) begin
      delay_rst_n_X <= 1;
      count_posX <= 1;  
   end else begin
      if (count_posX >= 8'd159)
         count_posX <= 1;
      else 
         count_posX <= count_posX + (dividerX % 8'd160);
   end
/* generate posY */
always_ff @(posedge clkY)
   if (!delay_rst_n_Y) begin
      delay_rst_n_Y <= 1;
      count_posY <= 1;  
   end else begin
      if (count_posY >= 7'd119)
         count_posY <= 1;
      else 
         count_posY <= count_posY + (dividerY % 8'd120);
   end

assign rng_posX = count_posX;
assign rng_posY = count_posY;

endmodule: pos_rng