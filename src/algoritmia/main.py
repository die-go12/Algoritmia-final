import sys
from antlr4 import *
from .AlgoritmiaLexer import AlgoritmiaLexer
from .AlgoritmiaParser import AlgoritmiaParser
from .Executor import AlgoritmiaExecutor

def main():
    
    if len(sys.argv) < 2:
        print("Uso: python -m algoritmia.main <archivo.alg> [ProcedimientoInicial]")
        return

    input_file = sys.argv[1]
    
    
    start_procedure = "Main" 
    if len(sys.argv) > 2:
        start_procedure = sys.argv[2]

    print(f"Procesando: {input_file}")
    print(f"Punto de entrada: {start_procedure}")

    
    input_stream = FileStream(input_file, encoding='utf-8')
    lexer = AlgoritmiaLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = AlgoritmiaParser(stream)
    tree = parser.programa()

    
    executor = AlgoritmiaExecutor()
    executor.entry_point = start_procedure  
    
   
    executor.DEBUG = True

    
    executor.visit(tree)

if __name__ == '__main__':
    main()