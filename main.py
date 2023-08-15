import sys

def evaluate_expression(expression):
    terms = expression.split('+')
    total = 0
    
    for term in terms:
        if '-' in term:
            sub_terms = term.split('-')
            sub_total = int(sub_terms[0])
            for sub_term in sub_terms[1:]:
                sub_total -= int(sub_term)
            total += sub_total
        else:
            total += int(term)
    
    return total

def handle_error(error_message):
    print("Erro:", error_message, file=sys.stderr)

if len(sys.argv) != 2:
    handle_error("Input vazio")
else:
    expression = sys.argv[1]
    expression = ' '.join(expression.split())
    
    if not expression:
        handle_error("Input vazio")
    elif "+" in expression and "-" in expression:
        handle_error("Mais de uma operação em sequência")
    elif expression.startswith("+"):
        handle_error("String começa com uma operação")
    elif expression.endswith("+"):
        handle_error("String termina com uma operação")
    elif " " in expression and not expression.replace(" ", "").isdigit():
        handle_error("Espaço sem operação entre números")
    else:
        try:
            result = evaluate_expression(expression)
            print("Resultado:", result)
        except:
            handle_error("Expressão inválida")
