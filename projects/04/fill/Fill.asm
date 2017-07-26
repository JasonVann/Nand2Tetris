// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed.
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.
//while True:
//  IF RAM[KBD] !=0:
//    for row in 0..255:
//      for column in 0..31:
//        M = -1;
//  ELSE:
//    white;

(LOOP)

@SCREEN
D = A
@addr
M = D // addr = 16384

  // If RAM[KBD] != 0
  @KBD // 24576
  D = M

  @kbval
  M = D // show the scan code

  @BLACK
  D; JNE

  @WHITE
  0; JMP

  @KBD
  D = A
  @SCREEN
  D = D - A
  @diff
  M = D // diff = 8K

  (BLACK)
      @addr
      A = M
      M = -1  // RAM[addr] = -1

      @addr
      M = M + 1 // addr = addr + 1

      @KBD
      D = A
      @addr
      D = D - M
      @diff
      M = D // diff = 8K

      @BLACK
      D; JGT  // continue drawing until diff = 0

    @LOOP
    D; JEQ    // back to beginning if fully drawn
    
  (WHITE)
      @addr
      A = M
      M = 0  // RAM[addr] = 0

      @addr
      M = M + 1 // addr = addr + 1

      @KBD
      D = A
      @addr
      D = D - M
      @diff
      M = D // diff = 8K

      @WHITE
      D; JGT  // continue drawing until diff = 0

    @LOOP
    D; JEQ    // back to beginning if fully drawn

@LOOP
0; JMP
