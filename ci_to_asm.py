from yaplVisitorCode import CONSTS, TEMPS

REG = 0
STACK = 1
HEAP = 2
CONST = 4
UNDEFINED = 5

REG_MAX = 32
REG_COUNT = 1

VAR_LOCATION = {}
REG_DESCRIPTOR = {0:['Main_ptr']}#quemado en entrypoint

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    #OKGREEN = "<span style='color:green'>"
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    #FAIL = "<span style='color:red'>"
    #ENDC = '</span>'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def convert_to_ASM(ci):
    print(f'{bcolors.OKGREEN}Converting to MIPS ASM...{bcolors.ENDC}')
    lines = ci.split('\n')

    final_lines = []
    
    for i in lines:
        line = i
        if line[0:3] == '\tla':
            line = loadAdrress(line)
        if line[0:3] == '\tlw':
            line = loadWord(line)
        if line[0:3] == '\tsw':
            line = storeWord(line)
        final_lines.append(line)

    with open('out.asm', 'w') as f:
        for i in final_lines:
            f.write(i + '\n')

    print(f'{bcolors.OKGREEN}Done!{bcolors.ENDC}')

def getReg(var):
    global REG_COUNT

    if var not in VAR_LOCATION:
        VAR_LOCATION[var] = UNDEFINED

    if var in TEMPS and REG_COUNT < REG_MAX:
        count = REG_COUNT
        REG_COUNT += 1
        VAR_LOCATION[var] = REG
        if count in REG_DESCRIPTOR:
            REG_DESCRIPTOR[count].append(var)
        else:
            REG_DESCRIPTOR[count] = [var]
        return f' ${count}, '

    if VAR_LOCATION[var] != REG:
        if REG_COUNT < REG_MAX:
            count = REG_COUNT
            REG_COUNT += 1
            VAR_LOCATION[var] = REG
            if count in REG_DESCRIPTOR:
                REG_DESCRIPTOR[count].append(var)
            else:
                REG_DESCRIPTOR[count] = [var]
            return f' ${count}, '
        #TODO Free registers
    for reg, varlist in REG_DESCRIPTOR.items():
        if var in varlist:
            return f' ${reg}, '

def loadAdrress(ci):
    varname = ci[3::]
    regname = getReg(varname)
    return ci[0:3] + regname + varname

def loadWord(ci):
    res = ci[3::].split(',')
    varname = res[0]
    regname = getReg(varname)
    return '\tlw ' + regname + res[1]

def storeWord(ci):
    res = ci[3::].split(',')
    varname = res[0]
    regname = getReg(varname)
    return '\tsw ' + regname + res[1]