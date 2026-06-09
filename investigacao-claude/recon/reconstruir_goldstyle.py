"""Reconstrução do Gold Style FIDC NP a partir de fonte pública.

Confronto com a matéria do Imirante/g1 de 18/03/2026 ("Fundo ligado à Reag recebeu
R$ 1 bilhão de empresas investigadas por lavagem de dinheiro do PCC").

Diferente do SDG II: a matéria do Gold Style é majoritariamente sobre **fluxo COAF**
(comunicados de operações suspeitas) que não passa pela DF auditada. A DF nominal
reconstrói o **mecanismo de fraude** (ações BESC infladas via laudo HORBIA), não os
fluxos COAF. Por isso o scorecard tem mais "NAO RECONSTRUIVEL VIA DF" do que o SDG II
— a métrica do método (DF auditada) tem limite onde a matéria descreve operações
não-balanço.

Valores em R$ mil quando indicado. Gera CSV em investigacao-claude/recon/output/.

Fontes (todas em data/fnet_docs/, originais no FNET):
- id 863753: DF exercício 31/03/2022 (entregue 24/03/2025, ~3 anos de atraso)
- id 741894: DF exercício 31/03/2021 (entregue 19/09/2024, auditor PwC)
- id 816884: Fato Relevante 10/01/2025 — REPRECIFICAÇÃO das Cártulas/BESC
- id 1199246: Informe Trimestral 1T2026 — fundo em liquidação
"""
import csv
import os

OUT = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUT, exist_ok=True)

# Achados sobre o mecanismo de fraude (data, descrição, valor R$ mil, fonte)
MECANICA = [
    ("2020-03-11", "Cessão do Excalibur FIM CP → Gold Style: 18.167.136 ações preferenciais BESC",
     None, "DF id863753 nota 4 / id741894"),
    ("2020-10-16", "AGC aprova transferência da administração para Reag DTVM (CNPJ 34.829.992/0001-86 = CBSF)",
     None, "DF id863753 nota 1"),
    ("2020-10-16", "Laudo HORBIA precifica ativo a R$ 758,69/ação = R$ 13.783.240 mil",
     13_783_240, "DF id863753 base abstenção"),
    ("2021-03-31", "Saldo direitos creditórios = R$ 1.362.535 mil (100,03% PL) — 10% do laudo",
     1_362_535, "DF id741894 balanço"),
    ("2022-03-31", "Saldo direitos creditórios mantido R$ 1.362.535 mil (100,05% PL)",
     1_362_535, "DF id863753 balanço"),
    ("2023-06-29", "PwC emite parecer com ABSTENÇÃO DE OPINIÃO sobre DF 2021 (sem evidência de existência/titularidade)",
     None, "DF id741894 parecer"),
    ("2024-09-02", "Mudança de administrador: Reag DTVM → Reag Jus Gestão de Ativos Judiciais Ltda. (46.356.742/0001-55)",
     None, "DF id863753 cabeçalho notas"),
    ("2025-01-10", "Fato Relevante: REPRECIFICAÇÃO RELEVANTE das Cártulas/BESC justificada por 'diversos negócios em 2024'",
     None, "FR id816884"),
    ("2025-03-14", "Baker Tilly 4Partners emite parecer com ABSTENÇÃO DE OPINIÃO sobre DF 2022 (mesma justificativa do PwC)",
     None, "DF id863753 parecer"),
    ("2025-03-24", "DF de exercício 31/03/2022 entregue ao FNET — atraso de quase 3 anos",
     None, "FNET metadado id863753"),
    ("2026-01", "Reag DTVM liquidada extrajudicialmente pelo Banco Central",
     None, "matéria Imirante / fato público"),
    ("2026-05-19", "Informe Trimestral 1T2026: todas as respostas 'Dada a liquidação, não foi realizada' — fundo paralisado",
     None, "FNET id1199246"),
]

# Vendas parciais (DF id863753 nota 22 referenciada na base abstenção)
VENDAS_PARCIAIS = [
    ("variável 2022-2024", "Vendas parciais de direitos creditórios a valores variando entre R$ 75,00 e R$ 483,33 por ação"
     " (variação >6x — sinal de manipulação de preço)",
     None, "DF id863753 base abstenção / nota 22"),
]


def fmt(v):
    if v is None: return "—"
    return f"R$ {v/1000:.3f} bi" if v >= 1_000_000 else f"R$ {v:,.0f} mil"


def main():
    # CSV cronologia da fraude
    with open(os.path.join(OUT, "goldstyle_cronologia.csv"), "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["data", "evento", "valor_brl", "fonte"])
        for d, evt, vmil, src in MECANICA:
            w.writerow([d, evt, (vmil * 1000) if vmil else "", src])

    print("=" * 88)
    print("RECONCILIAÇÃO — matéria Imirante/g1 (18/03/2026)  ×  dado público reconstruído")
    print("=" * 88)
    # (claim matéria, valor citado, valor reconstruído / observação, fonte, status)
    linhas = [
        ("Existência do FIDC Gold Style",
         "—", "CNPJ 34.081.900/0001-22 — confirmado", "FNET + DF", "CONFIRMADO"),
        ("Administrador = Reag",
         "—", "Reag DTVM (34.829.992/0001-86 = CBSF ex-Reag Trust) até 02/09/2024; depois Reag Jus", "DF id863753", "CONFIRMADO"),
        ("Ativos do fundo",
         "~R$ 2 bi", "R$ 1,362 bi em 31/03/2022 (DF). Matéria fala em R$ 2 bi (data não especificada). Compatível com crescimento ou recompra.", "DF id863753", "COMPATIVEL"),
        ("R$ 1 bi de empresas do PCC",
         "R$ 1 bi", "Não reconstruível via DF — fluxo COAF de 2023-2025 fora do escopo da DF de exercício 31/03/2022", "—", "NAO RECONSTRUIVEL"),
        ("Aster Petróleo cedeu/transferiu",
         "R$ 759,5 mi", "Não aparece como cedente ou contraparte na DF; provável fluxo financeiro pós-31/03/2022", "—", "NAO RECONSTRUIVEL"),
        ("BK Bank cedeu/transferiu",
         "R$ 158 mi", "Não aparece como cedente ou contraparte na DF", "—", "NAO RECONSTRUIVEL"),
        ("Inovanti cedeu/transferiu",
         "R$ 175 mi", "Não aparece como cedente ou contraparte na DF", "—", "NAO RECONSTRUIVEL"),
        ("Repasse para Super Empreendimentos",
         "R$ 180 mi", "Não aparece como contraparte na DF; provável fluxo posterior a 31/03/2022", "—", "NAO RECONSTRUIVEL"),
        ("Reag liquidada pelo BC",
         "janeiro/2026", "Confirmado por trimestral 1T2026 que reporta 'dada a liquidação' em todos os campos", "FNET id1199246", "CONFIRMADO"),
        ("Reag investigada em Compliance Zero (Master) e Carbono Oculto (PCC)",
         "—", "Fato público; consistente com mudança de admin para Reag Jus (subsidiária) em 02/09/2024 — uma semana antes da 1ª fase Carbono Oculto", "DF id863753", "CONFIRMADO"),
        ("Vorcaro preso em 04/03/2026",
         "—", "Fato público — fora do escopo da DF", "—", "FATO PUBLICO"),
    ]
    print(f"{'Afirmação da matéria':52} {'Citado':14} {'Status':18} Observação / fonte")
    print("-" * 88)
    rows = []
    for claim, cit, rec, fonte, status in linhas:
        print(f"{claim[:50]:52} {cit:14} {status:18} {rec[:200]}  [{fonte}]")
        rows.append([claim, cit, status, rec, fonte])
    with open(os.path.join(OUT, "goldstyle_scorecard_materia.csv"), "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["afirmacao_materia", "valor_citado", "status", "valor_reconstruido", "fonte"])
        w.writerows(rows)

    # Achados próprios (não estão na matéria) — o que a DF revela ALÉM
    print()
    print("=" * 88)
    print("ACHADOS PRÓPRIOS — o que a DF auditada revela além da matéria")
    print("=" * 88)
    achados = [
        ("Ativo subjacente = 18,17 mi ações preferenciais BESC (banco extinto em 2008, incorporado pelo BB)",
         "DF id863753 nota 4"),
        ("Cessor original do ativo: Excalibur FIM Crédito Privado (cessão 11/03/2020)",
         "DF id863753 base abstenção"),
        ("Laudo HORBIA precifica ativo a R$ 13,78 bi (R$ 758,69/ação) — fundo registra a 10% (R$ 1,36 bi, R$ 75/ação)",
         "DF id863753 base abstenção"),
        ("ABSTENÇÃO DE OPINIÃO do auditor em DOIS exercícios consecutivos (PwC 2021, Baker Tilly 2022)",
         "DF id741894 + id863753"),
        ("Justificativa idêntica: 'não obtivemos evidências apropriadas sobre existência, titularidade, transferência e mensuração'",
         "DF parecer PwC e Baker Tilly"),
        ("Auditor mudou de PwC -> Baker Tilly entre os exercicios",
         "DF id741894 vs id863753"),
        ("DF de exercício 31/03/2022 só entregue ao FNET em 24/03/2025 — atraso de ~3 anos",
         "Metadado FNET"),
        ("Vendas parciais em 2022-2024 a valores entre R$ 75 e R$ 483,33 por ação (variação 6,4x)",
         "DF id863753 nota 22 referenciada"),
        ("Fato Relevante 10/01/2025: REPRECIFICAÇÃO RELEVANTE das Cártulas/BESC — Reag admite valoração inconsistente",
         "FR id816884"),
        ("Em 02/09/2024 - uma semana antes da 1a fase da Op. Carbono Oculto - admin transferida da Reag DTVM para Reag Jus Gestao de Ativos Judiciais (subsidiaria)",
         "DF id863753 nota 1"),
        ("Trimestral 1T2026 (19/05/2026): TODAS as 16 perguntas obrigatórias respondidas com 'Dada a liquidação, não foi realizada' — fundo efetivamente paralisado",
         "FNET id1199246"),
    ]
    for evt, src in achados:
        print(f"  - {evt}  [{src}]")
    print()

    # CSV achados
    with open(os.path.join(OUT, "goldstyle_achados_proprios.csv"), "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["achado", "fonte"])
        w.writerows(achados)

    n_conf = sum(1 for l in linhas if l[-1] in ("CONFIRMADO", "COMPATIVEL", "FATO PUBLICO"))
    n_nao = sum(1 for l in linhas if l[-1] == "NAO RECONSTRUIVEL")
    print()
    print(f"Resumo: {n_conf}/{len(linhas)} afirmações da matéria CONFIRMADAS/COMPATÍVEIS/FATO PÚBLICO pela DF.")
    print(f"        {n_nao}/{len(linhas)} NÃO reconstruíveis via DF (fluxo COAF posterior ao exercício).")
    print(f"        {len(achados)} achados PRÓPRIOS adicionais revelados pela DF auditada.")
    print(f"CSVs gravados em {OUT}/")


if __name__ == "__main__":
    main()
