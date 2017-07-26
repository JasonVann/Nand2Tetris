// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.
// Assumes R0 >=0, R1>=0, and R0*R1 < 32768

//  RAM[2] = RAM[0] * RAM[1]
//  R2 = 0;
//  temp = R1;
//  while temp > 0
//    R2 += R0;
//    temp -=1;

  @R2
  M = 0;

  @R1
  D = M;
  @temp
  M = D;

  (LOOP)
    @temp
    D = M
    @END
    D; JEQ

    @R0
    D = M
    @R2
    M = D + M // R2 += R0

    @temp
    M = M - 1

    @LOOP
    0; JMP

  (END)
  @END
  0; JMP
