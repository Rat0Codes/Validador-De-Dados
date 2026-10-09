# Validador de Dados em Python

## Sobre o projeto

O Validador de Dados é um projeto desenvolvido para praticar manipulação de arquivos CSV, expressões regulares (Regex), tratamento de exceções e formatação de relatórios utilizando Python.

O programa lê um arquivo de entrada, verifica os formatos dos dados, classifica os registros como válidos ou inválidos e gera um relatório com os resultados da análise.

## Funcionalidades

* Leitura de arquivos CSV com o módulo `csv`.
* Validação de e-mails, CPFs, telefones e datas.
* Verificação de idade com uma regra de negócio específica.
* Tratamento de erros com `try`, `except`, `else` e `finally`.
* Criação de exceções personalizadas.
* Separação de registros válidos e inválidos.
* Cálculo de estatísticas da análise.
* Geração de relatório formatado com f-strings.

## Tecnologias utilizadas

* Python 3
* `csv`
* `re`
* `datetime`
* `pathlib`

Todas as bibliotecas utilizadas fazem parte da biblioteca padrão do Python.

## Estrutura do projeto

```text
validador-de-dados/
├── dados/
│   └── entrada.csv
├── relatorios/
│   └── .gitkeep
├── main.py
├── README.md
└── .gitignore
```

## Formato do arquivo de entrada

O arquivo `dados/entrada.csv` deve conter as seguintes colunas, separadas por ponto e vírgula:

```csv
email;cpf;telefone;data;idade
ana.silva@email.com;123.456.789-09;(98) 98765-4321;15/03/2004;22
```

A primeira linha contém o cabeçalho. Os registros seguintes contêm os dados que serão analisados.

## Justificativa das validações

### E-mail

O padrão Regex verifica uma estrutura básica de endereço eletrônico, com texto antes do `@`, um domínio e pelo menos uma extensão separada por ponto.

### CPF

O padrão aceita CPF com pontuação (`000.000.000-00`) ou somente com onze dígitos (`00000000000`).

**Limitação:** essa validação verifica apenas o formato, não os dígitos verificadores nem a existência do documento.

### Telefone

O padrão aceita números brasileiros com DDD, com dez ou onze dígitos, ou com formatação como parênteses e hífen.

### Data

O programa utiliza `datetime.strptime()` para verificar o formato `DD/MM/AAAA` e se a data existe no calendário. Por exemplo, `31/02/2020` é rejeitada.

### Idade

A idade deve ser um número inteiro entre 0 e 120. Valores fora desse intervalo geram `IdadeInvalidaError`.

## Metacaracteres Regex utilizados

| Metacaractere | Significado                          |                           |
| ------------- | ------------------------------------ | ------------------------- |
| `\d`          | Dígito numérico                      |                           |
| `\w`          | Caractere alfanumérico ou sublinhado |                           |
| `\s`          | Espaço em branco                     |                           |
| `^`           | Início da string                     |                           |
| `$`           | Final da string                      |                           |
| `+`           | Uma ou mais ocorrências              |                           |
| `?`           | Ocorrência opcional                  |                           |
| `{n}`         | Quantidade exata de ocorrências      |                           |
| `             | `                                    | Alternativa entre padrões |

O código utiliza `re.fullmatch()` para exigir que todo o conteúdo corresponda ao padrão.

## Tratamento de exceções

* `FileNotFoundError`: ocorre quando o arquivo de entrada não é encontrado.
* `ValueError`: trata valores inválidos, como conversões numéricas e arquivos sem cabeçalho.
* `KeyError`: identifica colunas obrigatórias ausentes.
* `FormatoInvalidoError`: representa campos vazios ou valores que não respeitam uma regra de formato.
* `IdadeInvalidaError`: representa idades fora do intervalo permitido.
* `PermissionError` e `OSError`: tratam problemas de acesso e gravação de arquivos.
* `finally`: garante que o arquivo de entrada seja fechado após a tentativa de leitura.

O bloco `else` informa quando a leitura termina sem erros.

## Como executar

É necessário ter Python 3 instalado.

1. Clone o repositório.
2. Entre na pasta do projeto.
3. Coloque seus registros em `dados/entrada.csv`.
4. Execute:

```bash
python3 main.py
```

O relatório será exibido no terminal e salvo em `relatorios/relatorio.txt`.

## Exemplo de saída

```text
=======================================================
RELATÓRIO DE ANÁLISE DE DADOS
=======================================================
Total de registros: 4
Registros válidos: 1
Registros inválidos: 3
Taxa de aprovação: 25.00%

REGISTROS VÁLIDOS
-------------------------------------------------------
Linha 2: ana.silva@email.com | CPF: 123.456.789-09 | ...

REGISTROS INVÁLIDOS
-------------------------------------------------------
Linha 3: email-invalido | Motivos: e-mail inválido, ...
```

Os resultados completos dependem dos registros presentes no arquivo de entrada.

## Limitações

As validações de CPF, telefone e e-mail são verificações de formato e não garantem que os dados correspondam a documentos, números ou endereços reais.

O projeto tem finalidade educacional e não deve ser utilizado para decisões críticas sem validações adicionais.

## Autor

Projeto acadêmico desenvolvido para praticar conceitos fundamentais de Python, manipulação de arquivos, Regex e tratamento de exceções.
