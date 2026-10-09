
import csv
import re
from datetime import datetime
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
ARQUIVO_ENTRADA = BASE_DIR / "dados" / "entrada.csv"
ARQUIVO_RELATORIO = BASE_DIR / "relatorios" / "relatorio.txt"

COLUNAS_OBRIGATORIAS = {
    "email", "cpf", "telefone", "data", "idade"
}


# ==========================================
# EXCEÇÕES PERSONALIZADAS
# ==========================================

class FormatoInvalidoError(Exception):
    """Indica que um campo não respeita o formato esperado."""


class IdadeInvalidaError(Exception):
     """Indica uma idade fora do intervalo permitido."""




def validar_email(email):
    padrao = r"^[\w.+-]+@[\w-]+(?:\.[\w-]+)+$"
    return re.fullmatch(padrao, email) is not None


def validar_cpf(cpf):
    padrao = r"^(?:\d{3}\.\d{3}\.\d{3}-\d{2}|\d{11})$"
    return re.fullmatch(padrao, cpf) is not None


def validar_telefone(telefone):
    padrao = (
        r"^(?:"
        r"\d{10,11}"
        r"|"
        r"\(?\d{2}\)?\s?\d{4,5}-?\d{4}"
        r")$"
    )
    return re.fullmatch(padrao, telefone) is not None


def validar_data(data):
    try:
        datetime.strptime(data, "%d/%m/%Y")
        return True
    except ValueError:
        return False




def validar_idade(valor):
    try:
        idade = int(valor)
    except ValueError as erro:
        raise FormatoInvalidoError(
            f"idade não é um número inteiro: {valor!r}"
        ) from erro

    if not 0 <= idade <= 120:
        raise IdadeInvalidaError(
            f"idade fora do intervalo de 0 a 120: {idade}"
        )

    return idade


def validar_registro(registro, numero_linha):
    erros = []

    if not validar_email(registro["email"]):
        erros.append("e-mail inválido")

    if not validar_cpf(registro["cpf"]):
        erros.append("formato de CPF inválido")

    if not validar_telefone(registro["telefone"]):
        erros.append("formato de telefone inválido")

    if not validar_data(registro["data"]):
        erros.append("data inválida")

    try:
        registro["idade"] = validar_idade(registro["idade"])
    except (FormatoInvalidoError, IdadeInvalidaError) as erro:
        erros.append(str(erro))

    return {
        "linha": numero_linha,
        "registro": registro,
        "erros": erros,
        "valido": len(erros) == 0
    }




def analisar_arquivo(caminho):
    validos = []
    invalidos = []
    arquivo = None

    try:
        arquivo = open(
            caminho,
            mode="r",
            encoding="utf-8-sig",
            newline=""
        )

        leitor = csv.DictReader(arquivo, delimiter=";")

        if leitor.fieldnames is None:
            raise ValueError("O CSV está vazio ou não possui cabeçalho.")

        leitor.fieldnames = [
            nome.strip().lower() for nome in leitor.fieldnames
        ]

        try:
            for coluna in COLUNAS_OBRIGATORIAS:
                if coluna not in leitor.fieldnames:
                    raise KeyError(coluna)
        except KeyError as erro:
            raise KeyError(
                f"Coluna obrigatória ausente: {erro.args[0]}"
            ) from erro

        for numero_linha, registro in enumerate(leitor, start=2):
            try:
                for coluna in COLUNAS_OBRIGATORIAS:
                    if registro.get(coluna) is None:
                        raise KeyError(coluna)
                    registro[coluna] = registro[coluna].strip()

                if any(
                    not registro[coluna]
                    for coluna in COLUNAS_OBRIGATORIAS
                ):
                    raise FormatoInvalidoError(
                        "existe pelo menos um campo vazio"
                    )

                resultado = validar_registro(
                    registro, numero_linha
                )

            except KeyError as erro:
                resultado = {
                    "linha": numero_linha,
                    "registro": registro,
                    "erros": [
                        f"campo ausente: {erro.args[0]}"
                    ],
                    "valido": False
                }

            except FormatoInvalidoError as erro:
                resultado = {
                    "linha": numero_linha,
                    "registro": registro,
                    "erros": [str(erro)],
                    "valido": False
                }

            if resultado["valido"]:
                validos.append(resultado)
            else:
                invalidos.append(resultado)

    except FileNotFoundError:
        print(f"Erro: arquivo não encontrado: {caminho}")
        return None

    except PermissionError:
        print(f"Erro: sem permissão para ler: {caminho}")
        return None

    except KeyError as erro:
        print(f"Erro estrutural no CSV: {erro}")
        return None

    except ValueError as erro:
        print(f"Erro nos dados ou no arquivo: {erro}")
        return None

    except csv.Error as erro:
        print(f"Erro na leitura do CSV: {erro}")
        return None

    else:
        print("Leitura do arquivo concluída com sucesso.")

    finally:
        
        if arquivo is not None:
            arquivo.close()
            print("Arquivo de entrada fechado.")

    return validos, invalidos



def gerar_relatorio(validos, invalidos, destino):
    total = len(validos) + len(invalidos)

    percentual = (
        len(validos) / total * 100
        if total > 0
        else 0
    )

    linhas = [
        "=" * 55,
        "RELATÓRIO DE ANÁLISE DE DADOS",
        "=" * 55,
        f"Total de registros: {total}",
        f"Registros válidos: {len(validos)}",
        f"Registros inválidos: {len(invalidos)}",
        f"Taxa de aprovação: {percentual:.2f}%",
        "",
        "REGISTROS VÁLIDOS",
        "-" * 55
    ]

    for item in validos:
        registro = item["registro"]
        linhas.append(
            f"Linha {item['linha']}: "
            f"{registro['email']} | "
            f"CPF: {registro['cpf']} | "
            f"Telefone: {registro['telefone']} | "
            f"Data: {registro['data']} | "
            f"Idade: {registro['idade']}"
        )

    linhas.extend([
        "",
        "REGISTROS INVÁLIDOS",
        "-" * 55
    ])

    for item in invalidos:
        registro = item["registro"]
        linhas.append(
            f"Linha {item['linha']}: "
            f"{registro.get('email', '(ausente)')} | "
            f"Motivos: {', '.join(item['erros'])}"
        )

    linhas.append("=" * 55)

    conteudo = "\n".join(linhas)

    try:
        destino.parent.mkdir(parents=True, exist_ok=True)

        with open(destino, "w", encoding="utf-8") as arquivo:
            arquivo.write(conteudo)

    except OSError as erro:
        print(f"Não foi possível salvar o relatório: {erro}")
        return

    print("\n" + conteudo)
    print(f"\nRelatório salvo em: {destino}")




def main():
    resultado = analisar_arquivo(ARQUIVO_ENTRADA)

    if resultado is None:
        return

    validos, invalidos = resultado

    gerar_relatorio(
        validos,
        invalidos,
        ARQUIVO_RELATORIO
    )


if __name__ == "__main__":
    main()