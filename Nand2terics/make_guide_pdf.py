"""Generate Viva Guide PDF."""
from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(150, 150, 150)
        self.cell(0, 8, 'Viva Guide - Nand to Tetris Capstone | Himalaya Singh | K = 54', align='C', new_x="LMARGIN", new_y="NEXT")
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(3)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', align='C')

    def section_title(self, title):
        self.set_font('Helvetica', 'B', 14)
        self.set_text_color(30, 80, 160)
        self.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(30, 80, 160)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(3)

    def sub_title(self, title):
        self.set_font('Helvetica', 'B', 12)
        self.set_text_color(50, 50, 50)
        self.cell(0, 8, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def body_text(self, text):
        self.set_font('Helvetica', '', 10)
        self.set_text_color(30, 30, 30)
        self.multi_cell(0, 5.5, text)
        self.ln(2)

    def bullet(self, text):
        self.set_font('Helvetica', '', 10)
        self.set_text_color(30, 30, 30)
        self.cell(5)
        self.cell(5, 5.5, '-')
        self.multi_cell(0, 5.5, text)
        self.ln(1)

    def code_block(self, text):
        self.set_font('Courier', '', 9)
        self.set_fill_color(240, 240, 240)
        self.set_text_color(30, 30, 30)
        x = self.get_x()
        self.cell(5)
        for line in text.strip().split('\n'):
            self.cell(5)
            self.cell(0, 5, '  ' + line, fill=True, new_x="LMARGIN", new_y="NEXT")
        self.ln(3)

    def qa(self, q, a):
        self.set_x(10)
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(30, 80, 160)
        self.multi_cell(0, 5.5, q)
        self.set_x(10)
        self.set_font('Helvetica', '', 10)
        self.set_text_color(30, 30, 30)
        self.multi_cell(0, 5.5, a)
        self.ln(3)

    def table(self, headers, rows, col_widths=None):
        if col_widths is None:
            col_widths = [190 / len(headers)] * len(headers)
        # Header
        self.set_font('Helvetica', 'B', 9)
        self.set_fill_color(30, 80, 160)
        self.set_text_color(255, 255, 255)
        for i, h in enumerate(headers):
            self.cell(col_widths[i], 7, h, border=1, fill=True, align='C')
        self.ln()
        # Rows
        self.set_font('Helvetica', '', 9)
        self.set_text_color(30, 30, 30)
        for row in rows:
            self.set_fill_color(248, 248, 248)
            for i, val in enumerate(row):
                self.cell(col_widths[i], 6.5, val, border=1, align='C')
            self.ln()
        self.ln(3)


pdf = PDF()
pdf.alias_nb_pages()
pdf.set_auto_page_break(auto=True, margin=20)
pdf.add_page()

# ============ TITLE ============
pdf.set_font('Helvetica', 'B', 22)
pdf.set_text_color(30, 80, 160)
pdf.cell(0, 15, 'Viva Guide', align='C', new_x="LMARGIN", new_y="NEXT")
pdf.set_font('Helvetica', '', 14)
pdf.set_text_color(80, 80, 80)
pdf.cell(0, 10, 'Nand to Tetris Capstone Project', align='C', new_x="LMARGIN", new_y="NEXT")
pdf.ln(5)
pdf.set_font('Helvetica', 'B', 12)
pdf.set_text_color(30, 30, 30)
pdf.cell(0, 8, 'Himalaya Singh  |  Roll: 2501730154  |  K = 54', align='C', new_x="LMARGIN", new_y="NEXT")
pdf.ln(8)

# ============ PROJECT SUMMARY ============
pdf.section_title('Project Ka Summary')
pdf.body_text(
    'Humne ek Hack Computer banaya hai (CPU + Memory + Computer) HDL mein, '
    'phir ek Python Assembler likha jo assembly language ko machine code mein convert karta hai, '
    'aur last mein ek Box.asm program likha jo screen pe ek box draw karta hai jab key press karo.'
)

# ============ IMPORTANT NUMBERS ============
pdf.section_title('Teri Important Numbers (Yaad Kar Le!)')
pdf.table(
    ['Cheez', 'Value', 'Kaise Aaya'],
    [
        ['K', '54', 'Roll ke last 2 digits'],
        ['Box start row', '54', 'K hi hai'],
        ['Box height', '20 rows', 'Fixed (assignment mein)'],
        ['Box width', '48 pixels', '16 x ((54 mod 4)+1) = 16x3'],
        ['Width in words', '3 words', '48 / 16 = 3'],
        ['Screen start addr', '18112', '16384 + (32 x 54)'],
        ['Row range', 'Row 54 to 73', '54 + 20 - 1 = 73'],
        ['Box.hack lines', '36', '36 instructions'],
        ['K mod 3', '0', 'Extra feature = symbols.txt'],
    ],
    [55, 45, 90]
)

# ============ PART A ============
pdf.section_title('Part A: Hardware - Kya Banaya')

pdf.sub_title('1. Memory.hdl - Computer ki memory')
pdf.body_text(
    '3 cheezein hain memory mein: RAM, Screen, Keyboard. '
    'Address ke bit [14] aur [13] se decide hota hai kaunsa select hoga:'
)
pdf.bullet('00 ya 01 = RAM (address 0 to 16383)')
pdf.bullet('10 = Screen (address 16384 to 24575)')
pdf.bullet('11 = Keyboard (address 24576)')
pdf.body_text('DMux se load signal route hota hai, Mux se output select hota hai.')

pdf.sub_title('2. CPU.hdl - Computer ka processor')
pdf.body_text('Instruction ka bit [15] dekhta hai:')
pdf.bullet('0 = A-instruction (number load karo A register mein, jaise @18112)')
pdf.bullet('1 = C-instruction (calculation karo, jaise D=D+A, M=D)')
pdf.body_text(
    'C-instruction ke parts: Bits [11:6] = ALU control, '
    'Bits [5:3] = Destination (A, D, ya M), Bits [2:0] = Jump condition (JGT, JEQ, JMP etc.)'
)

pdf.sub_title('3. Computer.hdl - Sab connect kiya')
pdf.bullet('ROM32K = program store (instruction memory)')
pdf.bullet('CPU = instructions execute karta hai')
pdf.bullet('Memory = data store (RAM + Screen + Keyboard)')
pdf.body_text('Sab 5 tests pass: Memory, CPU, ComputerAdd, ComputerMax, ComputerRect. Built-in chips use kiye (allowed hai).')

# ============ PART B ============
pdf.add_page()
pdf.section_title('Part B: Python Assembler')

pdf.sub_title('Two-Pass Algorithm:')
pdf.body_text(
    'Pass 1 - Labels dhundho: Puri file scan karo. Jahan (LOOP) jaisa label mile, '
    'uska address (line number) note karo. Example: (LOOP) line 0 pe = LOOP = 0'
)
pdf.body_text(
    'Pass 2 - Translate karo: Har line ko 16-bit binary mein convert karo. '
    '@18112 = 0100011011000000. D=A = 1110110000010000. '
    'Naya variable mile (jaise @color) toh RAM 16 se allocate karo.'
)

pdf.sub_title('Extra Feature (K mod 3 = 0): symbols.txt')
pdf.body_text('Har baar assemble karne pe symbols.txt banta hai:')
pdf.code_block(
    'LOOP       0       label\n'
    'DRAW       8       label\n'
    'ROWLOOP    16      label\n'
    'color      16      variable\n'
    'addr       17      variable\n'
    'rows       18      variable'
)

pdf.sub_title('Testing:')
pdf.body_text('5 programs pe test kiya - sab official assembler se bit-for-bit match:')
pdf.table(
    ['Program', 'Lines', 'Result'],
    [
        ['Add.asm', '6', 'Match'],
        ['Max.asm', '16', 'Match'],
        ['Rect.asm', '25', 'Match'],
        ['Pong.asm', '27,483', 'Match'],
        ['Box.asm', '36', 'Match'],
    ],
    [60, 60, 70]
)

# ============ PART C ============
pdf.section_title('Part C: Box.asm - Kaise Kaam Karta Hai')
pdf.code_block(
    'LOOP:\n'
    '    color = 0 (white)                <- default white\n'
    '    check keyboard\n'
    '    agar key pressed -> color = -1   <- black\n'
    'DRAW:\n'
    '    addr = 18112 (row 54 ka address)\n'
    '    rows = 20\n'
    'ROWLOOP:\n'
    '    screen[addr] = color      <- word 0 (px 0-15)\n'
    '    screen[addr+1] = color    <- word 1 (px 16-31)\n'
    '    screen[addr+2] = color    <- word 2 (px 32-47)\n'
    '    addr = addr + 32          <- next row\n'
    '    rows--, agar > 0 -> ROWLOOP\n'
    '    goto LOOP'
)
pdf.body_text(
    'Key points: Screen memory 16384 se start. Har row = 32 words. '
    '-1 binary mein = 1111111111111111 = sab pixels black. 0 = sab white.'
)

# ============ LIVE CHANGES ============
pdf.add_page()
pdf.section_title('Viva Mein Kya Change Karne Bol Sakte Hain')

pdf.sub_title('"Box ko neeche move karo" (Row 54 -> Row 100)')
pdf.body_text(
    'Box.asm mein @18112 change karo. Naya address = 16384 + (32 x 100) = 19584. '
    '@18112 hatao, @19584 likho. Dobara assemble karo.'
)

pdf.sub_title('"Box ki height badhao" (20 -> 30 rows)')
pdf.body_text('Box.asm mein @20 ko @30 mein change karo. Bas!')

pdf.sub_title('"Box ki width badhao" (48px -> 64px)')
pdf.body_text(
    'ROWLOOP mein ek aur pair add karo: A=A+1 aur M=D (ek aur word = 16 more pixels). '
    'Width kam karni ho toh ek A=A+1 / M=D pair hatao.'
)

# ============ TOP QUESTIONS ============
pdf.section_title('Teacher Kya Puchh Sakti Hai (Top 15 Q&A)')

pdf.qa('Q1: Memory mein RAM, Screen, Keyboard kaise select hote hain?',
       'A: Address ke bit [14] aur [13] se. 00/01 = RAM, 10 = Screen, 11 = Keyboard.')

pdf.qa('Q2: A-instruction aur C-instruction ka fark?',
       'A: Bit [15]=0 = A-instruction (number load karo A mein). Bit [15]=1 = C-instruction (compute + store + jump).')

pdf.qa('Q3: Jump kaise kaam karta hai?',
       'A: C-instruction ke last 3 bits jump condition. ALU output ke zero/negative flags se compare. True ho toh PC = A value.')

pdf.qa('Q4: Built-in chips kyun use kiye?',
       'A: Lab chips available nahi the, assignment mein built-in allowed hai.')

pdf.qa('Q5: Two-pass algorithm kya hai?',
       'A: Pass 1 = labels scan + addresses note. Pass 2 = translate instructions + allocate variables from RAM[16].')

pdf.qa('Q6: Variable kaise allocate hota hai?',
       'A: Pehla naya variable RAM[16], doosra RAM[17], aage badhta jaata hai.')

pdf.qa('Q7: symbols.txt mein kya hai?',
       'A: Labels (LOOP=0, DRAW=8, ROWLOOP=16) aur variables (color=16, addr=17, rows=18) with addresses.')

pdf.qa('Q8: M+D aur D+M mein fark?',
       'A: Same calculation (commutative), par official assembler sirf D+M accept karta hai. Mera assembler dono handle karta hai.')

pdf.qa('Q9: 18112 kaise aaya?',
       'A: Screen = 16384. Row 54 = 16384 + (32 x 54) = 18112. 32 kyunki har row mein 32 words.')

pdf.qa('Q10: 48 pixels kyun?',
       'A: Width = 16 x ((K mod 4) + 1) = 16 x ((54 mod 4) + 1) = 16 x 3 = 48.')

pdf.qa('Q11: -1 kyun use kiya black ke liye?',
       'A: -1 binary mein = 1111111111111111 (twos complement). Har bit 1 = har pixel black.')

pdf.qa('Q12: Box kaise move karoge?',
       'A: @18112 change karo. New addr = 16384 + (32 x new_row). Row 100 ke liye @19584.')

pdf.qa('Q13: Pong.asm ka output kitni lines?',
       'A: 27,483 lines - sab official assembler se match karti hain.')

pdf.qa('Q14: Computer.hdl mein kya connect kiya?',
       'A: ROM32K (program), CPU (execute), Memory (data + screen + keyboard).')

pdf.qa('Q15: Agar keyboard check nahi ho toh?',
       'A: Box permanently black rahega, erase nahi hoga. LOOP pe wapas jaana zaroori hai.')

# ============ RUN GUIDE ============
pdf.add_page()
pdf.section_title('Quick Run Guide')

pdf.sub_title('Assembler chalana:')
pdf.bullet('E:\\nand2tetris folder mein cmd kholo (address bar mein cmd type karo)')
pdf.bullet('python assembler.py Box.asm run karo')
pdf.bullet('Box.hack ban jaayega + symbols.txt update hoga')

pdf.sub_title('Web IDE pe test:')
pdf.bullet('Chrome: https://nand2tetris.github.io/web-ide')
pdf.bullet('Hardware Simulator = CPU/Memory/Computer tests')
pdf.bullet('Assembler = .asm load, >> press, .hack compare')
pdf.bullet('CPU Emulator = Box.hack load, >> press, key hold = box dikhe')

pdf.sub_title('Teacher bole change karo toh:')
pdf.bullet('Box.asm notepad mein kholo, change karo')
pdf.bullet('Terminal: python assembler.py Box.asm')
pdf.bullet('Web IDE CPU Emulator mein naya Box.hack load karo')
pdf.bullet('>> press, key hold, box dikhe!')

pdf.ln(5)
pdf.section_title('Important Terminology')
pdf.table(
    ['Term', 'Meaning'],
    [
        ['HDL', 'Hardware Description Language - chips define karte hain'],
        ['ASM', 'Assembly language - human readable code'],
        ['HACK', 'Machine code - 16-bit binary'],
        ['ROM', 'Read Only Memory - program store'],
        ['RAM', 'Random Access Memory - data store'],
        ['ALU', 'Arithmetic Logic Unit - calculations'],
        ['PC', 'Program Counter - next instruction ka address'],
        ['Screen', '256 rows x 512 px, starts at 16384'],
        ['KBD', 'Keyboard register at 24576'],
    ],
    [35, 155]
)

pdf.ln(10)
pdf.set_font('Helvetica', 'B', 16)
pdf.set_text_color(30, 80, 160)
pdf.cell(0, 10, 'All the best! Confident reh, tu sab jaanti hai!', align='C')

pdf.output(r'E:\nand2tetris\Viva_Guide_Himalaya.pdf')
print('PDF saved!')
