# Nand to Tetris Capstone Project Report
## Course: ETCCNT301 — Make the Computer Draw a Box

---

**Name:** Himalaya Singh
**Roll Number:** 2501730154
**K = 54**
**Box Specification:** Starting Row = 54, Height = 20 rows, Width = 48 pixels (3 screen words)
**Start Address:** 16384 + (32 × 54) = **18112**

---

## 1. Introduction

This report documents the capstone project for the Nand to Tetris course (ETCCNT301), which involves building the complete Hack computer hardware, writing a Python-based assembler, and creating a Box-drawing assembly program customized for K = 54. The project demonstrates a full understanding of the Hack computer architecture — from hardware design to machine-level programming.

The value of K is derived from the last two digits of my roll number (2501730154), giving **K = 54**. This determines the box parameters:
- **Starting row:** 54
- **Height:** 20 rows
- **Width:** 16 × ((54 mod 4) + 1) = 16 × 3 = **48 pixels** (3 words per row)
- **Screen memory start address:** 16384 + (32 × 54) = **18112**

---

## 2. Part A: Hardware Implementation (CPU, Memory, Computer)

### 2.1 Memory.hdl

The Memory chip maps the 32K address space of the Hack computer into three regions using address bits [14] and [13]:

| Address Range | Bits [14:13] | Component |
|--------------|-------------|-----------|
| 0 – 16383 | 00 or 01 | RAM16K (data memory) |
| 16384 – 24575 | 10 | Screen (memory-mapped display) |
| 24576 | 11 | Keyboard (memory-mapped input) |

The implementation uses a DMux to route the write signal (load) to the correct component based on the address bits, and a Mux to select the correct output. When address bit [14] is 0, the RAM is selected. When bit [14] is 1 and bit [13] is 0, the Screen is selected. When both are 1, the Keyboard register is selected.

### 2.2 CPU.hdl

The CPU implements the Hack processor with the following key design decisions:

- **Instruction decoding:** Bit [15] of the instruction determines whether it is an A-instruction (0) or C-instruction (1).
- **A-register:** Loaded with either the instruction value (A-instruction) or the ALU output (C-instruction with destination bit d1 set).
- **D-register:** Loaded with ALU output when destination bit d2 is set in a C-instruction.
- **ALU control:** Bits [11:6] of a C-instruction directly control the ALU's six control inputs (zx, nx, zy, ny, f, no).
- **Jump logic:** Bits [2:0] of a C-instruction specify the jump condition. The jump is evaluated against the ALU output's zero (zr) and negative (ng) flags.
- **Program Counter (PC):** Increments by default, loads the A-register value on a jump, or resets to 0 on a reset signal.

### 2.3 Computer.hdl

The top-level Computer chip connects the three major components:
- **ROM32K:** Stores the program (instruction memory), addressed by the PC output.
- **CPU:** Fetches instructions from ROM, reads/writes data memory, and produces the next PC value.
- **Memory:** The data memory (RAM + Screen + Keyboard), addressed by the CPU's address output.

### 2.4 Test Results

All five official hardware tests passed successfully in the nand2tetris Web IDE (green bar — "output file is identical"):

1. **Memory.tst** — Verified RAM read/write, Screen memory mapping, and Keyboard input detection. ✅
2. **CPU.tst** — Verified all instruction types, ALU operations, register loading, and jump conditions. ✅
3. **ComputerAdd.tst** — Verified the complete computer running an addition program. ✅
4. **ComputerMax.tst** — Verified the computer running a max-finding program. ✅
5. **ComputerRect.tst** — Verified the computer running a rectangle-drawing program. ✅

**Note:** The implementation uses built-in chips (RAM16K, ALU, ARegister, DRegister, PC, ROM32K, Screen, Keyboard) provided by the nand2tetris platform, as permitted by the assignment guidelines.

---

## 3. Part B: Python Assembler

### 3.1 Design Overview

The assembler (assembler.py) translates Hack assembly language (.asm) into Hack machine code (.hack) using the standard **two-pass algorithm**:

**Pass 1 — Label Collection:**
- Scans through the entire source file line by line.
- Removes comments (text after //) and all whitespace.
- Skips blank lines.
- When a label declaration like `(LOOP)` is found, records its address (the ROM line number of the next instruction) in the symbol table.

**Pass 2 — Code Translation:**
- Translates each instruction into a 16-bit binary string.
- **A-instructions** (`@value`): If the value is a number, it is converted directly to binary. If it is a symbol, it is looked up in the symbol table. Unknown symbols are treated as new variables and allocated starting from RAM address 16.
- **C-instructions** (`dest=comp;jump`): The dest, comp, and jump fields are looked up in their respective tables and concatenated as `111 + comp(7 bits) + dest(3 bits) + jump(3 bits)`.

### 3.2 Robustness Features

- **All predefined symbols** supported: R0–R15, SP, LCL, ARG, THIS, THAT, SCREEN, KBD.
- **Commutative computation forms:** The assembler accepts both `D+M` and `M+D`, both `D&A` and `A&D`, etc. The `norm_comp()` function automatically swaps operands when the given form is not in the lookup table.
- **Flexible destination ordering:** Accepts any permutation of destination letters — `DM`, `MD`, `AM`, `MA`, `ADM`, `MDA`, etc. The `norm_dest()` function normalizes them to the canonical order (A, D, M).

### 3.3 Extra Feature (K mod 3 = 0): Symbol Table Export

Since K mod 3 = 0, the assembler writes a **symbols.txt** file after each assembly run. This file lists all labels and variables with their resolved addresses. For example, after assembling Box.asm:

```
LOOP       0       label
DRAW       8       label
ROWLOOP    16      label
color      16      variable
addr       17      variable
rows       18      variable
```

This feature aids in debugging and verifying that the assembler correctly resolves all symbols.

### 3.4 Testing Results

The assembler was tested against the official nand2tetris assembler on four standard programs. The output matched **bit-for-bit** in every case:

| Program | Instructions | Result |
|---------|-------------|--------|
| Add.asm | 6 lines | ✅ Match |
| Max.asm | 16 lines | ✅ Match |
| Rect.asm | 25 lines | ✅ Match |
| Pong.asm | 27,483 lines | ✅ Match |
| Box.asm | 36 lines | ✅ Match |

The Pong.asm test is particularly significant as it is a large, compiler-generated program with 27,483 machine-code instructions and hundreds of symbols, confirming the assembler handles real-world programs correctly.

---

## 4. Part C: Box Drawing Program (Box.asm)

### 4.1 Program Design

Box.asm draws a filled rectangle on the Hack computer's screen based on the K = 54 parameters. The program continuously checks the keyboard:
- **Key pressed:** Draws a black (filled) box at the specified position.
- **Key released:** Erases the box (fills with white).

### 4.2 Key Constants

| Parameter | Value | Derivation |
|-----------|-------|-----------|
| Start address | 18112 | 16384 + (32 × 54) |
| Width | 48 px (3 words) | 16 × ((54 mod 4) + 1) |
| Height | 20 rows | Fixed |
| Row range | Rows 54 – 73 | 54 + 20 - 1 = 73 |

### 4.3 Algorithm

```
LOOP:
    color = 0 (white)
    if KBD != 0: color = -1 (black, all bits set)
DRAW:
    addr = 18112 (screen start for row 54)
    rows = 20
ROWLOOP:
    mem[addr] = color      (word 0: pixels 0-15)
    mem[addr+1] = color    (word 1: pixels 16-31)
    mem[addr+2] = color    (word 2: pixels 32-47)
    addr = addr + 32       (next row = 32 words ahead)
    rows = rows - 1
    if rows > 0: goto ROWLOOP
    goto LOOP
```

### 4.4 Assembly Output

The program compiles to **36 instructions** (Box.hack = 648 bytes). It was assembled using my own Python assembler and loaded into the CPU Emulator, where it successfully drew and erased the box based on keyboard input.

### 4.5 CPU Emulator Verification

- ROM row 8 contains `0100011011000000` (binary for 18112), confirming the correct start address.
- When a key is held, the box appears at row 54, spanning 48 pixels wide and 20 rows tall.
- When the key is released, the box disappears and the screen returns to blank.

---

## 5. Bug Found and Fixed

During the development of the assembler, I discovered an interesting difference between my implementation and the official nand2tetris assembler. The official assembler **rejects** the instruction `M=M+D` — it only accepts the canonical form `M=D+M`, where the D register must appear as the first operand in addition with M.

My assembler's `norm_comp()` function was designed to handle **commutative forms** automatically. When a computation like `M+D` is not found in the lookup table, the function swaps the operands and checks for `D+M`, which is a valid entry. This makes the assembler more flexible and forgiving of different coding styles.

While Box.asm uses the canonical form `M=D+M` (so this was not a runtime issue), the flexibility ensures robustness when assembling programs written in either style. I discovered this behavior difference by systematically comparing my assembler's output with the official assembler during the validation phase.

---

## 6. Files Submitted

All project files are organized in the `capstone/` folder of the GitHub repository:

| File | Description |
|------|-------------|
| CPU.hdl | Hack CPU implementation using built-in chips |
| Memory.hdl | Memory map (RAM16K + Screen + Keyboard) |
| Computer.hdl | Top-level Hack computer |
| assembler.py | Python assembler with symbol table export |
| Box.asm | Box drawing program for K = 54 |
| Box.hack | Assembled machine code (36 instructions) |
| symbols.txt | Symbol table output for Box.asm |

---

## 7. Conclusion

This capstone project successfully demonstrates the complete Hack computer system — from hardware chips (CPU, Memory, Computer) to software tools (assembler) to application programs (Box.asm). All official tests pass, the assembler produces bit-identical output to the reference implementation across all test programs including the 27,483-line Pong, and the Box program correctly renders a 48×20 pixel rectangle at row 54 based on K = 54.
