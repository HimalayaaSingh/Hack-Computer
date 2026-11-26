"""Generate the capstone report as a Word document."""
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

doc = Document()

# --- Styles setup ---
style = doc.styles['Normal']
font = style.font
font.name = 'Times New Roman'
font.size = Pt(12)

def add_heading_custom(text, level=1):
    h = doc.add_heading(text, level=level)
    for run in h.runs:
        run.font.color.rgb = RGBColor(0, 0, 0)
    return h

def add_screenshot_placeholder(caption):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(f'\n\n\n[Insert Screenshot: {caption}]\n\n\n')
    run.font.size = Pt(11)
    run.font.italic = True
    run.font.color.rgb = RGBColor(128, 128, 128)
    cap = doc.add_paragraph()
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = cap.add_run(f'Figure: {caption}')
    r.font.size = Pt(10)
    r.font.italic = True
    r.font.bold = True

def add_table(headers, rows):
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = 'Table Grid'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, h in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = h
        for paragraph in cell.paragraphs:
            for run in paragraph.runs:
                run.font.bold = True
                run.font.size = Pt(11)
    for r_idx, row in enumerate(rows):
        for c_idx, val in enumerate(row):
            cell = table.rows[r_idx + 1].cells[c_idx]
            cell.text = val
            for paragraph in cell.paragraphs:
                for run in paragraph.runs:
                    run.font.size = Pt(11)
    return table

# ============================================================
# PAGE 1: Title Page
# ============================================================
for _ in range(4):
    doc.add_paragraph()

title = doc.add_paragraph()
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = title.add_run('Nand to Tetris Capstone Project')
run.font.size = Pt(26)
run.bold = True

subtitle = doc.add_paragraph()
subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = subtitle.add_run('Make the Computer Draw a Box')
run.font.size = Pt(18)
run.font.color.rgb = RGBColor(80, 80, 80)

doc.add_paragraph()

course = doc.add_paragraph()
course.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = course.add_run('Course: ETCCNT301')
run.font.size = Pt(14)

doc.add_paragraph()
doc.add_paragraph()

details = [
    ('Name', 'Himalaya Singh'),
    ('Roll Number', '2501730154'),
    ('K Value', '54'),
    ('Box Size', '48 pixels wide \u00d7 20 rows tall'),
    ('Start Address', '18112 (16384 + 32 \u00d7 54)'),
]

for label, value in details:
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r1 = p.add_run(f'{label}: ')
    r1.font.size = Pt(13)
    r1.bold = True
    r2 = p.add_run(value)
    r2.font.size = Pt(13)

doc.add_page_break()

# ============================================================
# PAGE 2: Part A + Part B
# ============================================================
add_heading_custom('1. Introduction', level=1)

doc.add_paragraph(
    'This report documents the capstone project for the Nand to Tetris course (ETCCNT301), '
    'which involves building the complete Hack computer hardware, writing a Python-based assembler, '
    'and creating a Box-drawing assembly program customized for K = 54.'
)

doc.add_paragraph(
    'The value of K is derived from the last two digits of my roll number (2501730154), '
    'giving K = 54. This determines the box parameters: starting row = 54, height = 20 rows, '
    'width = 16 \u00d7 ((54 mod 4) + 1) = 48 pixels (3 screen words per row), and screen memory '
    'start address = 16384 + (32 \u00d7 54) = 18112.'
)

add_heading_custom('2. Part A: Hardware Implementation', level=1)

add_heading_custom('2.1 Memory.hdl', level=2)
doc.add_paragraph(
    'The Memory chip maps the 32K address space of the Hack computer into three regions '
    'using address bits [14] and [13]:'
)

add_table(
    ['Address Range', 'Bits [14:13]', 'Component'],
    [
        ['0 \u2013 16383', '00 or 01', 'RAM16K (data memory)'],
        ['16384 \u2013 24575', '10', 'Screen (memory-mapped display)'],
        ['24576', '11', 'Keyboard (memory-mapped input)'],
    ]
)
doc.add_paragraph()

doc.add_paragraph(
    'The implementation uses a DMux to route the write signal to the correct component based on '
    'the address bits, and a Mux to select the correct output.'
)

add_heading_custom('2.2 CPU.hdl', level=2)
doc.add_paragraph(
    'The CPU implements the Hack processor. Bit [15] of the instruction determines whether it is '
    'an A-instruction (0) or C-instruction (1). The A-register is loaded with either the instruction '
    'value or the ALU output. The D-register is loaded with ALU output when the destination bit d2 '
    'is set. Bits [11:6] control the ALU, and bits [2:0] specify the jump condition evaluated '
    'against the ALU output\'s zero and negative flags. The Program Counter increments by default, '
    'loads the A-register value on a jump, or resets to 0 on a reset signal.'
)

add_heading_custom('2.3 Computer.hdl', level=2)
doc.add_paragraph(
    'The top-level Computer chip connects ROM32K (instruction memory), CPU, and Memory (data memory) '
    'into the complete Hack computer. The implementation uses built-in chips (RAM16K, ALU, ARegister, '
    'DRegister, PC, ROM32K, Screen, Keyboard) provided by the nand2tetris platform, as permitted by '
    'the assignment guidelines.'
)

add_heading_custom('2.4 Hardware Test Results', level=2)
doc.add_paragraph('All five official hardware tests passed successfully in the nand2tetris Web IDE '
                   '(green bar \u2014 "output file is identical"):')

add_table(
    ['Test', 'Result'],
    [
        ['Memory.tst', '\u2713 Passed'],
        ['CPU.tst', '\u2713 Passed'],
        ['ComputerAdd.tst', '\u2713 Passed'],
        ['ComputerMax.tst', '\u2713 Passed'],
        ['ComputerRect.tst', '\u2713 Passed'],
    ]
)
doc.add_paragraph()

doc.add_page_break()

# ============================================================
# PAGE 3: Part B — Assembler
# ============================================================
add_heading_custom('3. Part B: Python Assembler', level=1)

add_heading_custom('3.1 Two-Pass Algorithm', level=2)
doc.add_paragraph(
    'The assembler (assembler.py) translates Hack assembly (.asm) into machine code (.hack) '
    'using a two-pass algorithm:'
)
doc.add_paragraph(
    'Pass 1 \u2014 Label Collection: Scans the source file, removes comments and whitespace, '
    'and records label declarations like (LOOP) with their ROM address in the symbol table.',
    style='List Bullet'
)
doc.add_paragraph(
    'Pass 2 \u2014 Code Translation: Translates each A-instruction to a 16-bit address and each '
    'C-instruction to its binary encoding (111 + comp + dest + jump). Unknown symbols are '
    'allocated as variables starting from RAM address 16.',
    style='List Bullet'
)

add_heading_custom('3.2 Robustness Features', level=2)
doc.add_paragraph('All predefined symbols supported: R0\u2013R15, SP, LCL, ARG, THIS, THAT, SCREEN, KBD.', style='List Bullet')
doc.add_paragraph('Commutative computation forms accepted (e.g., M+D treated as D+M, A&D as D&A).', style='List Bullet')
doc.add_paragraph('Flexible destination ordering (DM, MD, AM, MA, ADM, etc.).', style='List Bullet')

add_heading_custom('3.3 Extra Feature: Symbol Table Export (K mod 3 = 0)', level=2)
doc.add_paragraph(
    'The assembler writes a symbols.txt file listing all labels and variables with their '
    'resolved addresses. For Box.asm, this outputs: LOOP(0), DRAW(8), ROWLOOP(16) as labels, '
    'and color(16), addr(17), rows(18) as variables.'
)

add_heading_custom('3.4 Assembler Test Results', level=2)
doc.add_paragraph('Output matches the official nand2tetris assembler bit-for-bit for all test programs:')

add_table(
    ['Program', 'Instructions', 'Result'],
    [
        ['Add.asm', '6 lines', '\u2713 Match'],
        ['Max.asm', '16 lines', '\u2713 Match'],
        ['Rect.asm', '25 lines', '\u2713 Match'],
        ['Pong.asm', '27,483 lines', '\u2713 Match'],
        ['Box.asm', '36 lines', '\u2713 Match'],
    ]
)
doc.add_paragraph()

add_screenshot_placeholder('Terminal \u2014 Assembler runs + dir *.hack + symbols.txt')
add_screenshot_placeholder('Add.asm \u2014 Assembler comparison successful')
add_screenshot_placeholder('Max.asm \u2014 Assembler comparison successful')
add_screenshot_placeholder('Rect.asm \u2014 Assembler comparison successful')
add_screenshot_placeholder('Pong.asm \u2014 Assembler comparison successful')
add_screenshot_placeholder('Box.asm \u2014 Assembler comparison successful')

doc.add_page_break()

# ============================================================
# PAGE 4: Part C — Box + Bug + Conclusion
# ============================================================
add_heading_custom('4. Part C: Box Drawing Program', level=1)

add_heading_custom('4.1 Program Design', level=2)
doc.add_paragraph(
    'Box.asm draws a filled rectangle on the screen based on K = 54. The program continuously '
    'checks the keyboard \u2014 when a key is pressed, it draws a black box at the specified position, '
    'and when the key is released, it erases the box.'
)

add_heading_custom('4.2 Box Parameters', level=2)
add_table(
    ['Parameter', 'Value', 'Derivation'],
    [
        ['Start Address', '18112', '16384 + (32 \u00d7 54)'],
        ['Width', '48 pixels (3 words)', '16 \u00d7 ((54 mod 4) + 1)'],
        ['Height', '20 rows', 'Fixed'],
        ['Row Range', 'Rows 54 \u2013 73', '54 + 20 - 1 = 73'],
    ]
)
doc.add_paragraph()

doc.add_paragraph(
    'The program compiles to 36 instructions (Box.hack = 648 bytes). It was assembled using my '
    'own Python assembler and verified in the CPU Emulator. ROM row 8 contains 0100011011000000 '
    '(binary for 18112), confirming the correct start address.'
)

add_screenshot_placeholder('CPU Emulator \u2014 Box visible on screen (key held)')
add_screenshot_placeholder('CPU Emulator \u2014 Box erased / screen blank (key released)')

add_heading_custom('5. Bug Found and Fixed', level=1)
doc.add_paragraph(
    'During the development of the assembler, I discovered that the official nand2tetris assembler '
    'rejects the instruction "M=M+D" \u2014 it only accepts the canonical form "M=D+M", where D must '
    'appear as the first operand. My assembler\'s norm_comp() function handles commutative forms '
    'automatically: when "M+D" is not in the lookup table, it swaps the operands and finds "D+M". '
    'This makes the assembler more flexible. While Box.asm uses the canonical form "M=D+M", this '
    'flexibility ensures robustness for programs written in either style. I discovered this by '
    'comparing my assembler\'s behavior with the official assembler during validation.'
)

add_heading_custom('6. Files Submitted', level=1)
doc.add_paragraph('All project files are in the capstone/ folder of the GitHub repository:')

add_table(
    ['File', 'Description'],
    [
        ['CPU.hdl', 'Hack CPU implementation using built-in chips'],
        ['Memory.hdl', 'Memory map (RAM16K + Screen + Keyboard)'],
        ['Computer.hdl', 'Top-level Hack computer'],
        ['assembler.py', 'Python assembler with symbol table export'],
        ['Box.asm', 'Box drawing program for K = 54'],
        ['Box.hack', 'Assembled machine code (36 instructions)'],
        ['symbols.txt', 'Symbol table output for Box.asm'],
    ]
)
doc.add_paragraph()

add_heading_custom('7. Conclusion', level=1)
doc.add_paragraph(
    'This capstone project successfully demonstrates the complete Hack computer system \u2014 from '
    'hardware chips (CPU, Memory, Computer) to software tools (assembler) to application programs '
    '(Box.asm). All official tests pass, the assembler produces bit-identical output to the '
    'reference implementation across all test programs including the 27,483-line Pong, and the '
    'Box program correctly renders a 48\u00d720 pixel rectangle at row 54 based on K = 54.'
)

doc.save(r'E:\nand2tetris\Capstone_Report_Himalaya_Singh_v2.docx')
print('Report saved!')
