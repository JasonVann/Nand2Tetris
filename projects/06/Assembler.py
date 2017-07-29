# For NAND2Tetris, proj 6

class Assembler():
    '''
    Assemble the given assembly program to the Hack machine language,
    output file has the same file name as the input but with '.hack' suffix
    '''
    def __init__(self, in_filename):
        '''
        in_filename: for assembly program, eg. 'Program.asm'

        '''
        if in_filename[-4:] != '.asm':
            raise 'The input file must be a .asm code file'
        self.infn = in_filename
        self.outfn = in_filename[:-4] + '.hack'
        self.symbol_table = {}
        self.jmp_lookup = self.build_jmp_lookup()
        self.comp_lookup = self.build_comp_lookup()
        self.dest_lookup = self.build_dest_lookup()

    def build_jmp_lookup(self):
        '''
        Build the lookup table for the jmp filed of C instruction
        '''
        jmp_lookup = {}
        jmp_lookup['JGT'] = '001'
        jmp_lookup['JEQ'] = '010'
        jmp_lookup['JGE'] = '011'
        jmp_lookup['JLT'] = '100'
        jmp_lookup['JNE'] = '101'
        jmp_lookup['JLE'] = '110'
        jmp_lookup['JMP'] = '111'
        return jmp_lookup

    def build_dest_lookup(self):
        '''
        Build the lookup table for the jmp filed of C instruction
        '''
        dest_lookup = {}
        dest_lookup['M'] = '001'
        dest_lookup['D'] = '010'
        dest_lookup['MD'] = '011'
        dest_lookup['A'] = '100'
        dest_lookup['AM'] = '101'
        dest_lookup['AD'] = '110'
        dest_lookup['AMD'] = '111'
        return dest_lookup

    def build_comp_lookup(self):
        '''
        Build the lookup table for the compute filed of C instruction
        '''
        comp_lookup = {}
        # a = 0
        comp_lookup['0'] = '101010'
        comp_lookup['1'] = '111111'
        comp_lookup['-1'] = '111010'
        comp_lookup['D'] = '001100'
        comp_lookup['A'] = '110000'
        comp_lookup['!D'] = '001101'
        comp_lookup['!A'] = '110001'
        comp_lookup['-D'] = '001111'
        comp_lookup['-A'] = '110011'
        comp_lookup['D+1'] = '011111'
        comp_lookup['A+1'] = '110111'
        comp_lookup['D-1'] = '001110'
        comp_lookup['A-1'] = '110010'
        comp_lookup['D+A'] = '000010'
        comp_lookup['D-A'] = '010011'
        comp_lookup['A-D'] = '000111'
        comp_lookup['D&A'] = '000000'
        comp_lookup['D|A'] = '010101'

        # a = 1
        comp_lookup['M'] = '110000'
        comp_lookup['!M'] = '110001'
        comp_lookup['-M'] = '110011'
        comp_lookup['M+1'] = '110111'
        comp_lookup['M-1'] = '110010'
        comp_lookup['D+M'] = '000010'
        comp_lookup['D-M'] = '010011'
        comp_lookup['M-D'] = '000111'
        comp_lookup['D&M'] = '000000'
        comp_lookup['D|M'] = '010101'

        return comp_lookup

    #def read(self, file_name):

    def parse(self):
        fo = open(self.outfn, 'w')

        with open(self.infn, 'r') as f:
            lines = f.readlines()
            for line in lines:
                # Remove comment
                pos = line.find('//')
                code = line[:pos]
                code = code.lstrip()  # remove leading blanks
                #print(85, line, pos, line[:pos], code)
                # Remove spaces between characters: ' D M = A '
                code = [char for char in code if char != ' ']
                code = ''.join(code)
                if len(code) == 0:
                    # comment or blank line
                    continue
                if code[0] == '@':
                    ml = self.process_A(code)
                else:
                    ml = self.process_C(code)
                print(95, code, ml)
                fo.write(ml+'\n')

        fo.close()

    def process_A(self, code):
        '''
        Process A-type instruction
        eg. @2 or @R2
        '''
        if '@R' not in code:
            dec = code[1:]
        else:
            dec = code[2:]
        try:
            binary = bin(int(dec))
            # eg. '0b101'
        except:
            raise 'A-type instruction not in a valid format: contains ' + \
                'non-number characters: {}'.format(dec)

        binary = binary[2:]
        ml = '0' + '0' * (15 - len(binary)) + binary
        return ml

    def process_C(self, code):
        '''
        Process C-type instruction
        eg. 'dest=comp; jump'
        '''
        def process_comp():
            '''
            Process the compute field
            '''
            idx1 = code.find('=')
            idx2 = code.find(';')
            if idx2 == -1:
                comp_field = code[idx1+1:]
            else:
                comp_field = code[idx1+1:idx2]

            if 'M' in comp_field:
                a = '1'
            else:
                a = '0'

            if comp_field not in self.comp_lookup:
                print("Comp field is {}".format(comp_field))
                raise "Invalid comp field in C instruction: "
            return a + self.comp_lookup[comp_field]

        def process_jump():
            '''
            Process the jump field,
            '''
            jump = '000'
            if ';' not in code:
                return jump
            if code.count(';') > 1:
                raise 'Invalid C-instruction: too many ";"!'
            j_field = code.split(';')[-1] # eg. 'JGT'

            if j_field not in self.jmp_lookup:
                raise 'Invalid jump field!'

            return self.jmp_lookup[j_field]

        def process_dest():
            '''
            Process dest field, which is located prior to '='
            '''
            dest = list('000')
            if '=' not in code:
                return ''.join(dest)
            if code.count('=') > 1:
                raise 'Invalid C-instruction: too many "="!'
            d_field = code.split('=')[0] # eg. 'AM'
            if 'A' in d_field:
                dest[0] = '1'
            if 'D' in d_field:
                dest[1] = '1'
            if 'M' in d_field:
                dest[2] = '1'

            return ''.join(dest)

        out = '111'
        c = process_comp()
        d = process_dest()
        j = process_jump()

        out = out + c + d + j
        #print(205, c, d, j, out)
        return out

def test(fn):
    assembler = Assembler(fn)
    assembler.parse()

#test('add/Add.asm')
#test('max/MaxL.asm')
#test('max/Max.asm')
#test('rect/RectL.asm')
test('pong/PongL.asm')
