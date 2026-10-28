"""
Sistema de Autodiagnóstico de Gestão para MEI
Baseado nos domínios de desempenho do PMBOK Guide (PMI), adaptados
à rotina de microempreendedores individuais.

Etapas do guia contempladas:
1 Menu e funções | 2 Cadastro | 3 Listagem e busca
4 Plano de ação (status Sim/Não, como empréstimo/devolução)
5 Persistência em JSON | 6 Extras | 7 Organização
"""

import json
from datetime import date

ARQUIVO_DADOS = "diagnosticos.json"

# Lista global que guarda os diagnósticos em memória (Etapa 2).
# Cada diagnóstico é um dicionário:
# negocio, responsavel, ano, notas (por área, em %), pontuacao_geral, plano_concluido
diagnosticos = []

# Áreas do diagnóstico, inspiradas nos domínios de desempenho do PMBOK.
AREAS = [
    {"nome": "Clientes e parceiros",
     "perguntas": ["Sei quem são meus clientes ideais e o que esperam de mim.",
                   "Registro pedidos e combinados por escrito."],
     "dica": "Liste seus 5 principais clientes e combine tudo por escrito."},
    {"nome": "Você e quem te ajuda",
     "perguntas": ["Sei quais tarefas posso delegar ou terceirizar.",
                   "Tenho uma rotina que evita sobrecarga e protege meu descanso."],
     "dica": "Reserve 1 hora por semana para estudo e mapeie 2 tarefas para delegar."},
    {"nome": "Planejamento",
     "perguntas": ["Tenho metas claras para os próximos 3 a 6 meses.",
                   "Antes de aceitar um trabalho, estimo tempo, custo e escopo."],
     "dica": "Escreva 3 metas com prazo e revise toda segunda-feira."},
    {"nome": "Execução do trabalho",
     "perguntas": ["Tenho passo a passo para as tarefas que se repetem.",
                   "Acompanho o que está em andamento, pendente e concluído."],
     "dica": "Crie um quadro simples: A fazer, Fazendo, Feito."},
    {"nome": "Entrega e qualidade",
     "perguntas": ["Combino com o cliente o que será entregue e quando.",
                   "Peço opinião dos clientes depois da entrega."],
     "dica": "Crie uma lista de verificação de qualidade e envie uma pesquisa de satisfação."},
    {"nome": "Números e resultados",
     "perguntas": ["Sei quanto entra e quanto sai por mês.",
                   "Uso indicadores (vendas, lucro, clientes) para decidir preços."],
     "dica": "Monte uma planilha mensal de entradas e saídas e acompanhe 3 indicadores."},
    {"nome": "Imprevistos e riscos",
     "perguntas": ["Tenho reserva financeira para meses fracos.",
                   "Evito depender de um único cliente ou fornecedor."],
     "dica": "Liste 5 riscos do negócio, o que faria em cada um e comece uma reserva."},
    {"nome": "Visão geral e formalização",
     "perguntas": ["Minhas obrigações de MEI (DAS, declaração anual) estão em dia.",
                   "Reviso o que deu certo e errado e ajusto o rumo."],
     "dica": "Marque os vencimentos do DAS na agenda e revise o negócio todo mês."},
]


# ---------------------------------------------------------------- Persistência
def carregar_dados():
    """Lê o arquivo JSON ao iniciar e preenche a lista (Etapa 5)."""
    try:
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as arquivo:
            diagnosticos.extend(json.load(arquivo))
    except FileNotFoundError:
        pass  # primeira execução: ainda não existe arquivo
    except json.JSONDecodeError:
        print("Aviso: o arquivo de dados está corrompido. Começando com a lista vazia.")


def salvar_dados():
    """Grava a lista no arquivo JSON após cada alteração."""
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as arquivo:
        json.dump(diagnosticos, arquivo, ensure_ascii=False, indent=2)


# --------------------------------------------------------- Entrada de dados
def ler_texto(mensagem):
    """Pede um texto e repete até o usuário digitar algo."""
    while True:
        texto = input(mensagem).strip()
        if texto:
            return texto
        print("Entrada vazia. Tente novamente.")


def ler_inteiro(mensagem, minimo, maximo):
    """Pede um número inteiro dentro de um intervalo, tratando erros de digitação."""
    while True:
        try:
            valor = int(input(mensagem))
        except ValueError:
            print("Digite apenas números.")
            continue
        if minimo <= valor <= maximo:
            return valor
        print(f"Digite um valor entre {minimo} e {maximo}.")


# ------------------------------------------------------------------- Cálculos
def calcular_percentual(respostas):
    """Converte notas de 1 a 5 em percentual de 0 a 100."""
    return round((sum(respostas) - len(respostas)) / (4 * len(respostas)) * 100)


def classificar(percentual):
    """Devolve o nível de maturidade correspondente ao percentual."""
    if percentual < 40:
        return "Atenção prioritária"
    if percentual < 65:
        return "Em desenvolvimento"
    if percentual < 85:
        return "Boa base"
    return "Ponto forte"


# --------------------------------------------------------- Etapa 2: cadastro
def cadastrar_diagnostico():
    """Cadastra um novo diagnóstico fazendo as perguntas de cada área."""
    print("\n--- Novo diagnóstico ---")
    negocio = ler_texto("Nome do negócio: ")
    responsavel = ler_texto("Nome do responsável: ")
    ano = ler_inteiro("Ano do diagnóstico: ", 2000, 2100)
    print("\nDê uma nota de 1 (discordo totalmente) a 5 (concordo totalmente).")

    notas = {}
    for area in AREAS:
        print(f"\n{area['nome']}")
        respostas = [ler_inteiro(f"  {pergunta} ", 1, 5) for pergunta in area["perguntas"]]
        notas[area["nome"]] = calcular_percentual(respostas)

    pontuacao_geral = round(sum(notas.values()) / len(notas))
    diagnosticos.append({
        "negocio": negocio,
        "responsavel": responsavel,
        "ano": ano,
        "notas": notas,
        "pontuacao_geral": pontuacao_geral,
        "plano_concluido": "Não",
    })
    salvar_dados()
    print(f"\nDiagnóstico salvo. Pontuação geral: {pontuacao_geral}% ({classificar(pontuacao_geral)})")


# -------------------------------------------------- Etapa 3: listagem e busca
def exibir_diagnostico(posicao, diag):
    """Mostra um diagnóstico em formato resumido."""
    print(f"{posicao}. {diag['negocio']} | Responsável: {diag['responsavel']} | "
          f"Ano: {diag['ano']} | Pontuação: {diag['pontuacao_geral']}% "
          f"({classificar(diag['pontuacao_geral'])}) | Plano concluído: {diag['plano_concluido']}")


def listar_diagnosticos(lista=None):
    """Lista todos os diagnósticos ou uma lista já filtrada."""
    lista = diagnosticos if lista is None else lista
    if not lista:
        print("Nenhum diagnóstico encontrado.")
        return
    print()
    for posicao, diag in enumerate(lista, start=1):
        exibir_diagnostico(posicao, diag)


def buscar_diagnostico():
    """Busca por nome do negócio ou do responsável."""
    termo = ler_texto("Digite parte do nome do negócio ou do responsável: ").lower()
    encontrados = [d for d in diagnosticos
                   if termo in d["negocio"].lower() or termo in d["responsavel"].lower()]
    if encontrados:
        listar_diagnosticos(encontrados)
    else:
        print(f"Nenhum diagnóstico encontrado para '{termo}'.")


def escolher_diagnostico():
    """Lista os diagnósticos e devolve o escolhido (ou None se não houver)."""
    if not diagnosticos:
        print("Nenhum diagnóstico cadastrado.")
        return None
    listar_diagnosticos()
    posicao = ler_inteiro("\nNúmero do diagnóstico: ", 1, len(diagnosticos))
    return diagnosticos[posicao - 1]


# ------------------------------------------- Etapa 4: plano de ação (status)
def alterar_plano(novo_status):
    """Marca o plano de ação como concluído ('Sim') ou reaberto ('Não')."""
    diag = escolher_diagnostico()
    if diag is None:
        return
    if diag["plano_concluido"] == novo_status:
        print(f"O plano já estava com o status '{novo_status}'.")
        return
    diag["plano_concluido"] = novo_status
    salvar_dados()
    print("Status do plano atualizado.")


# ------------------------------------------------------ Etapa 6: extras
def mostrar_contadores():
    """Extra 1: totais do acervo de diagnósticos."""
    total = len(diagnosticos)
    concluidos = sum(1 for d in diagnosticos if d["plano_concluido"] == "Sim")
    print(f"\nTotal: {total} | Planos concluídos: {concluidos} | Pendentes: {total - concluidos}")


def ordenar_e_listar():
    """Extra 2: lista ordenada por negócio (A-Z), ano ou pontuação."""
    print("\n1. Nome do negócio (A-Z)\n2. Ano (mais antigo primeiro)\n3. Pontuação (maior primeiro)")
    opcao = ler_inteiro("Ordenar por: ", 1, 3)
    if opcao == 1:
        ordenados = sorted(diagnosticos, key=lambda d: d["negocio"].lower())
    elif opcao == 2:
        ordenados = sorted(diagnosticos, key=lambda d: d["ano"])
    else:
        ordenados = sorted(diagnosticos, key=lambda d: d["pontuacao_geral"], reverse=True)
    listar_diagnosticos(ordenados)


def remover_diagnostico():
    """Extra 3: exclui um diagnóstico depois de confirmar."""
    diag = escolher_diagnostico()
    if diag is None:
        return
    if input(f"Remover '{diag['negocio']}'? (s/n): ").strip().lower() == "s":
        diagnosticos.remove(diag)
        salvar_dados()
        print("Diagnóstico removido.")
    else:
        print("Operação cancelada.")


def ver_relatorio():
    """Extra 4: relatório com notas por área e dicas para as 3 áreas mais fracas."""
    diag = escolher_diagnostico()
    if diag is None:
        return
    print(f"\nRelatório: {diag['negocio']} ({diag['ano']})")
    for nome, nota in diag["notas"].items():
        print(f"  {nome}: {nota}% - {classificar(nota)}")
    mais_fracas = sorted(diag["notas"], key=diag["notas"].get)[:3]
    print("\nPor onde começar:")
    for nome in mais_fracas:
        dica = next(a["dica"] for a in AREAS if a["nome"] == nome)
        print(f"  - {nome}: {dica}")


# ------------------------------------------------------- Etapa 1: menu
def mostrar_menu():
    print("\n===== Autodiagnóstico MEI =====")
    print("1. Novo diagnóstico")
    print("2. Listar diagnósticos")
    print("3. Buscar diagnóstico")
    print("4. Marcar plano de ação como concluído")
    print("5. Reabrir plano de ação")
    print("6. Contadores")
    print("7. Ordenar e listar")
    print("8. Ver relatório com dicas")
    print("9. Remover diagnóstico")
    print("0. Sair")


def main():
    """Carrega os dados e repete o menu até o usuário sair."""
    carregar_dados()
    acoes = {
        1: cadastrar_diagnostico,
        2: listar_diagnosticos,
        3: buscar_diagnostico,
        4: lambda: alterar_plano("Sim"),
        5: lambda: alterar_plano("Não"),
        6: mostrar_contadores,
        7: ordenar_e_listar,
        8: ver_relatorio,
        9: remover_diagnostico,
    }
    while True:
        mostrar_menu()
        opcao = ler_inteiro("Escolha uma opção: ", 0, 9)
        if opcao == 0:
            print("Até logo!")
            break
        acoes[opcao]()


if __name__ == "__main__":
    main()
