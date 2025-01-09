# Sistema de Testes de Hardware

Este programa é uma aplicação Python desenvolvida para realizar testes de hardware em computadores. Ele inclui funcionalidades para verificar o estado da câmera, teclado, som, bateria e outros componentes, gerando um relatório final em formato PDF.

## Funcionalidades

1. **Teste Inicial**:
   - Verifica o número de série da BIOS.
   - Confirma a ativação do Windows.
   - Calcula a saúde e carga da bateria.

2. **Teste de Câmera**:
   - Permite capturar uma foto para verificar o funcionamento da câmera.

3. **Teste de Som**:
   - Realiza testes no microfone e no fone de ouvido.

4. **Teste de Teclado**:
   - Permite testar teclas individualmente, indicando quais foram testadas e quais não.

5. **Geração de Relatório**:
   - Cria um relatório detalhado em PDF, incluindo os resultados de todos os testes.

## Requisitos

- Python 3.10 ou superior.
- Dependências listadas no arquivo `requirements.txt`.

## Instalação

1. Clone o repositório ou baixe os arquivos.
   ```bash
   git clone <link-do-repositorio>
   cd <diretorio>
