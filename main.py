# import re
# import sys

# def operacao(expressao):


#         # Remove todos os espaços em branco da expressão usando uma expressão regular
#         expressao = re.sub(r'\s', '', expressao)
    
#         # Separa a cadeia de operações em termos
#         terms = expressao.split('+')
        
#         total = 0
#         for term in terms:
#             if term:  # Ignora strings vazias após a divisão
#                 try:
#                     total += int(term)
#                 except ValueError:
#                     raise ValueError(f"Termo inválido: {term}")
#         return total

# if len(sys.argv) != 2:
#     print("Uso: python calculadora.py 'expressão'")
# else:
#     expression = sys.argv[1]
#     result = operacao(expression)
#     print(result)

import re
import sys

def validate_expression(expression):
    pattern = r'^\s*\d+(\s*[+-]\s*\d+)*\s*$'
    return re.match(pattern, expression)

def evaluate_expression(expression):
    terms = re.findall(r'[+-]?\s*\d+', expression)
    total = 0
    for term in terms:
        total += int(term)
    return total

if len(sys.argv) != 2:
    print("Uso: python calculator.py 'expressão'")
else:
    expression = sys.argv[1]
    if validate_expression(expression):
        result = evaluate_expression(expression)
        print("Resultado:", result)
    else:
        print("Erro: Expressão inválida.")