// Box.asm  (K = 54)
// Box: starts at row 54, 20 rows tall, 16 * ((54 mod 4) + 1) = 48 px wide (3 words)
// Key pressed -> draw black box. Key released -> erase it.

(LOOP)
    // color = 0 by default (white)
    @color
    M=0
    @KBD
    D=M
    @DRAW
    D;JEQ
    // key pressed -> color = -1 (black)
    @color
    M=-1

(DRAW)
    // addr = SCREEN + 32*54 = 18112
    @18112
    D=A
    @addr
    M=D
    // rows = 20
    @20
    D=A
    @rows
    M=D

(ROWLOOP)
    @color
    D=M
    @addr
    A=M
    M=D         // word 0
    A=A+1
    M=D         // word 1
    A=A+1
    M=D         // word 2

    // addr += 32 (next row)
    @32
    D=A
    @addr
    M=D+M

    // rows--, loop while rows > 0
    @rows
    M=M-1
    D=M
    @ROWLOOP
    D;JGT

    @LOOP
    0;JMP
