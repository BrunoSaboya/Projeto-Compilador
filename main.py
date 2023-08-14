import re
import sys

def operacao(expressao):
    try:
        # Substitui os caracteres de subtração por adição de números negativos
        expressao = expressao.replace('-', '+-')
        
        # Remove todos os espaços em branco da expressão usando uma expressão regular
        expressao = re.sub(r'\s', '', expressao)
    
        # Separa a cadeia de operações em termos
        terms = expressao.split('+')
        
        total = 0
        for term in terms:
            if term:  # Ignora strings vazias após a divisão
                total += int(term)
        
        return total
    except:
        return "Erro: Expressão inválida."

if len(sys.argv) != 2:
    print("Uso: python calculadora.py 'expressão'")
else:
    expression = sys.argv[1]
    result = operacao(expression)
    print("Resultado:", result)