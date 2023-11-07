import sys

#create an assembler generator for my python compiler
class AssemblyGenerator:
    
    instructions = ''

    @staticmethod
    def writeStart():
        file = sys.argv[1]
        file = file.split('.')
        teste = file[0] + '.asm'
        with open(teste, 'w') as file:
            with open('assembler_init.txt', 'r') as start:
                file.write(start.read())


    @staticmethod
    def writeAsm(instruction):
        instruction = instruction + '\n'
        AssemblyGenerator.instructions += instruction

    @staticmethod
    def writeEnd():
        file = sys.argv[1]
        file = file.split('.')
        teste = file[0] + '.asm'
        with open(teste, 'a') as file:
            with open('assembler_end.txt', 'r') as end:
                file.write(AssemblyGenerator.instructions+end.read())