# Projeto Compilador Go

Este projeto consiste em um compilador para a linguagem Go, desenvolvido durante a disciplina de 'Lógica da Computação'. O compilador analisa código-fonte Go e gera código de máquina correspondente.

## Índice

- [Instalação](#instalação)
- [Uso](#uso)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Contribuição](#contribuição)

## Instalação

1. **Clone o repositório:**
   ```bash
    git clone https://github.com/BrunoSaboya/Projeto-Compilador.git
    cd Projeto-Compilador
    pip install -r requirements.txt
   ```
## Uso

Para compilar um arquivo Go, utilize o seguinte comando:
  ```bash
  python main.py caminho/para/seu/arquivo.go
  exemplo:
  python main.py teste.go
  ``` 

## Estrutura do Projeto

- `main.py`: Arquivo principal que executa o compilador.
- `assembler.py`: Contém funções relacionadas à geração de código assembly.
- `assembler_init.txt` e `assembler_end.txt`: Arquivos de template para o código assembly gerado.
- `teste.go`: Exemplo de código-fonte Go para testes.

## Contribuição

Contribuições são bem-vindas! Siga os passos abaixo para contribuir:

1. Faça um fork do projeto.
2. Crie uma branch para sua feature ou correção de bug:
   ```bash
   git checkout -b minha-feature
   git commit -m 'Adiciona minha feature'
   git push origin minha-feature
   ```


