`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 09/21/2022 05:15:07 PM
// Design Name: 
// Module Name: adder_test
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////


module adder
  #(
    parameter random_para = 1
  )
  (
   clk,
   i_bit1,
   i_bit2,
   o_sum,
   o_carry
   );
  
  input wire clk;
  input wire i_bit1;
  input wire i_bit2;
  output wire o_sum;
  output wire o_carry;
 
  assign o_sum   = i_bit1 ^ i_bit2;  // bitwise xor
  assign o_carry = i_bit1 & i_bit2;  // bitwise and
 
endmodule 
