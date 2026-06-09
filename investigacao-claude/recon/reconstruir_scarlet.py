"""Reconstrucao do Scarlet FIDC NP (ex-Carriet Inventory) a partir de fonte publica.

Confronto com a materia do Imirante/g1 de 14/04/2026: "Banco Master e Vorcaro
aplicaram R$ 12,2 bilhoes em fundos, diz Receita". A materia cita especificamente o
SCARLET FIDC como receptor de R$ 2,5 bi do Master.

ACHADO PRINCIPAL desta reconstrucao:
**Scarlet FIDC e Carriet Inventory FIDC sao o MESMO fundo** (CNPJ 55.344.996/0001-44).
Renomeacao na AGE de 23/01/2025 - o mesmo ato que trocou a gestora pra Reag Jus.

O Luan ja havia mapeado "Carriet Inventory FIDC-NP" como cessor de CCB de Lormont
(R$ 325.452 mil em 27/09/2024) para o SDG II. Isto e: o "Scarlet" que a Receita Federal
hoje aponta como receptor de R$ 2,5 bi do Master e exatamente o mesmo fundo que ha 5
meses ja estava mapeado como peca da cadeia de cessoes do SDG II.

Fontes:
- id 865183: DF auditada exerc 31/05/2024-31/12/2024 (Taticca, opiniao limpa)
- id 1199327: Trimestral 1T2026 (pos-liquidacao)
- id 824327 + 824330: Ata AGE + Regulamento de 23/01/2025 (renomeacao + nova gestora)
- id 789348: Ata AGE 27/11/2024 (ainda como Carriet Inventory)
- id 1185251: Informe Mensal abr/2026 (XML estruturado)
"""
import csv
import os

OUT = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUT, exist_ok=True)

# Cronologia da renomeacao + composicao
CRONOLOGIA = [
    ("2024-05-31", "Constituicao como CARRIET INVENTORY FIDC NP",
     None, "DF id865183 / FNET id691007"),
    ("2024-07-02", "AGE de constituicao do fundo entregue ao FNET",
     None, "FNET id691007"),
    ("2024-07-18", "AGE adapta o fundo a Resolucao CVM 175/22",
     None, "FNET id701083"),
    ("2024-09-27", "Carriet Inventory cede CCB de Lormont (R$ 325,452 mi) pro SDG II",
     325_452, "DF SDG II id963178 / reconstrucao Luan"),
    ("2024-11-27", "AGE mantem nome CARRIET INVENTORY; aprova reforma do regulamento",
     None, "FNET id789348"),
    ("2024-12-31", "Composicao da carteira fechamento ex 2024:",
     None, "DF id865183 nota 6"),
    ("2024-12-31", "- CCBs R$ 20,518 mi", 20_518, "DF id865183"),
    ("2024-12-31", "- Debentures R$ 469,390 mi", 469_390, "DF id865183"),
    ("2024-12-31", "- CRIs R$ 24,388 mi", 24_388, "DF id865183"),
    ("2024-12-31", "- Outros recebiveis R$ 543,818 mi (R$ 13,784 mi vencidos)",
     543_818, "DF id865183"),
    ("2024-12-31", "Total direitos creditorios R$ 1,058 bi", 1_058_114, "DF id865183"),
    ("2024-12-31", "FIP Hans II R$ 70 mi (cota de fundo de participacoes)", 70_000, "DF id865183"),
    ("2025-01-23", "AGE renomeia CARRIET INVENTORY -> SCARLET FIDC NP; mesma data troca gestora pra Reag Jus",
     None, "FNET id824327 + id824330"),
    ("2025-03-26", "Taticca emite parecer COM OPINIAO LIMPA sobre DF 2024 (sem ressalvas)",
     None, "DF id865183 parecer"),
    ("2026-01", "Reag DTVM (admin) liquidada extrajudicialmente pelo BC",
     None, "materia Imirante / fato publico"),
    ("2026-03-04", "Daniel Vorcaro preso (Operacao Compliance Zero)",
     None, "materia Imirante / fato publico"),
    ("2026-04", "Informe mensal abr/2026: PL R$ 2,706 bi; 6 cotistas; carteira R$ 2,206 bi",
     2_706_331, "FNET id1185251 (XML)"),
    ("2026-04", "Composicao abr/2026: direitos cred R$ 1,732 bi + acoes judiciais R$ 304 mi + precatorios R$ 269 mi + cotas FIDC R$ 361 mi",
     None, "FNET id1185251"),
    ("2026-05-19", "Trimestral 1T2026: 16 campos respondidos 'Dada a liquidacao, nao foi realizada' - fundo paralisado",
     None, "FNET id1199327"),
]


def main():
    with open(os.path.join(OUT, "scarlet_cronologia.csv"), "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["data", "evento", "valor_brl", "fonte"])
        for d, evt, vmil, src in CRONOLOGIA:
            w.writerow([d, evt, (vmil * 1000) if vmil else "", src])

    print("=" * 88)
    print("RECONCILIACAO - materia Imirante/g1 (14/04/2026)  x  dado publico reconstruido")
    print("=" * 88)
    # (claim materia, valor citado, valor reconstruido / observacao, fonte, status)
    linhas = [
        ("Existencia do Scarlet FIDC",
         "-", "CNPJ 55.344.996/0001-44 (ex-CARRIET INVENTORY ate 23/01/2025) - CONFIRMADO + AMPLIADO",
         "FNET + DF id865183 + Regulamento id824330", "CONFIRMADO+"),
        ("Administrado pela Reag",
         "-", "Admin: Reag DTVM (34.829.992/0001-86 = CBSF, MESMA do SDG II e Gold Style); Gestora: ate 23/01/2025 Reag Trust Adm Recursos, depois Reag Jus Gestao de Ativos Judiciais",
         "DF id865183 + Reg id824330", "CONFIRMADO"),
        ("Master recebeu/aportou ~R$ 2,5 bi",
         "R$ 2,5 bi", "Informe mensal abr/2026: PL R$ 2,706 bi; carteira R$ 2,206 bi - BATE no agregado",
         "FNET id1185251", "COMPATIVEL"),
        ("Fundo onde Master e cotista principal",
         "-", "Informe mensal mostra apenas 6 cotistas (2 bancos comerciais + 1 fundo + 3 outros fundos), FUNDO EXCLUSIVO + COTISTA VINCULADO - consistente com 'cotista principal' Master",
         "FNET id1185251", "COMPATIVEL"),
        ("Reag liquidada pelo BC em janeiro/2026",
         "janeiro/2026", "Confirmado por trimestral 1T2026: TODOS os 16 campos respondidos 'Dada a liquidacao'",
         "FNET id1199327", "CONFIRMADO"),
        ("R$ 12,2 bi aplicados pelo Master+Vorcaro em fundos (2017-2025)",
         "R$ 12,2 bi", "Nao reconstruivel via DF (agregado da Receita Federal); fora do escopo da DF de um fundo individual",
         "-", "NAO RECONSTRUIVEL"),
        ("44% dos recursos pra fundos Reag",
         "44%", "Nao reconstruivel via DF; agregado da Receita",
         "-", "NAO RECONSTRUIVEL"),
        ("184 contas em 67 fundos diferentes",
         "184/67", "Nao reconstruivel via DF",
         "-", "NAO RECONSTRUIVEL"),
        ("Master sacou R$ 6,8 bi do agregado",
         "R$ 6,8 bi", "Nao reconstruivel via DF",
         "-", "NAO RECONSTRUIVEL"),
        ("Vorcaro retirou R$ 581 mi",
         "R$ 581 mi", "Nao reconstruivel via DF",
         "-", "NAO RECONSTRUIVEL"),
        ("Vorcaro preso em marco/2026",
         "marco/2026", "Fato publico",
         "-", "FATO PUBLICO"),
    ]
    print(f"{'Afirmacao da materia':52} {'Citado':14} {'Status':18} Observacao / fonte")
    print("-" * 88)
    rows = []
    for claim, cit, rec, fonte, status in linhas:
        print(f"{claim[:50]:52} {cit:14} {status:18} {rec[:200]}  [{fonte}]")
        rows.append([claim, cit, status, rec, fonte])
    with open(os.path.join(OUT, "scarlet_scorecard_materia.csv"), "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["afirmacao_materia", "valor_citado", "status", "valor_reconstruido", "fonte"])
        w.writerows(rows)

    # Achados proprios
    print()
    print("=" * 88)
    print("ACHADOS PROPRIOS - o que a DF + atas + regulamento + informe revelam")
    print("=" * 88)
    achados = [
        ("Scarlet FIDC = Carriet Inventory FIDC (renomeacao 23/01/2025 na mesma AGE que trocou gestor pra Reag Jus)",
         "FNET id824330 (regulamento) vs id789348 (ata anterior)"),
        ("O fundo que a Receita Federal hoje cita como 'Scarlet R$ 2,5 bi do Master' eh o MESMO que o Luan ja havia mapeado como 'Carriet Inventory cedeu CCB de Lormont (R$ 325 mi) ao SDG II em 27/09/2024'",
         "DF SDG II id963178 / Luan reconstrucao + DF id865183"),
        ("Administrado pela Reag DTVM (CNPJ 34.829.992/0001-86 = CBSF) - MESMA admin do SDG II e Gold Style. 3 fundos do escandalo sob a mesma administradora",
         "DF id865183 + Informe mensal id1185251"),
        ("Gestora trocou de Reag Trust Adm Recursos para REAG JUS GESTAO DE ATIVOS JUDICIAIS em 23/01/2025 - mesmo movimento estrutural do Gold Style (02/09/2024) e SDG II",
         "Ata id824327 + Regulamento id824330"),
        ("Fundo EXCLUSIVO + COTISTA VINCULADO - regulamento restringe cotistas a entidades pre-aprovadas",
         "Informe mensal id1185251 (FDO_EXCL=SIM, COTST_VINCUL=SIM)"),
        ("Apenas 6 cotistas em abr/2026 (2 bancos + 1 FIF + 3 outros fundos)",
         "FNET id1185251"),
        ("PL cresceu de R$ 1,65 bi (dez/2024) para R$ 2,71 bi (abr/2026) - +R$ 1,06 bi pos-mudanca pra Reag Jus",
         "DF id865183 vs informe mensal id1185251"),
        ("Composicao da carteira em abr/2026 mudou: ativos judiciais novos (acoes judiciais R$ 304 mi + precatorios setor publico R$ 269 mi) - coerente com nova gestora 'Reag Jus Gestao de Ativos Judiciais'",
         "Informe mensal id1185251"),
        ("Auditor TATICCA emitiu parecer com OPINIAO LIMPA sobre DF 2024 (diferente do SDG II e Gold Style que tiveram ABSTENCAO) - mas DF cobre periodo de apenas 7 meses (31/05 a 31/12/2024)",
         "DF id865183 parecer auditor"),
        ("Em dez/2024 o fundo ja tinha R$ 469 mi em debentures + R$ 20 mi em CCBs - ja era veiculo de divida em poucos meses apos constituicao",
         "DF id865183 nota 6"),
        ("Trimestral 1T2026 (entregue 19/05/2026): TODAS as 16 perguntas obrigatorias respondidas com 'Dada a liquidacao, nao foi realizada' - PADRAO IDENTICO ao Gold Style",
         "FNET id1199327"),
        ("Aplicacao no FIP Hans II de R$ 70 mi (dez/2024) - conecta com a materia que cita Hans II FIP MULT como destino principal de Vorcaro (R$ 1,2 bi de aporte; PL R$ 3,6 bi -> R$ 83 mi pos-revisao)",
         "DF id865183 nota 5"),
    ]
    for evt, src in achados:
        print(f"  - {evt}  [{src}]")
    print()

    with open(os.path.join(OUT, "scarlet_achados_proprios.csv"), "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["achado", "fonte"])
        w.writerows(achados)

    n_conf = sum(1 for l in linhas if "CONFIRMADO" in l[-1] or l[-1] in ("COMPATIVEL", "FATO PUBLICO"))
    n_nao = sum(1 for l in linhas if l[-1] == "NAO RECONSTRUIVEL")
    print()
    print(f"Resumo: {n_conf}/{len(linhas)} afirmacoes da materia CONFIRMADAS/COMPATIVEIS pela DF/informe.")
    print(f"        {n_nao}/{len(linhas)} NAO reconstruiveis (agregados da Receita Federal).")
    print(f"        {len(achados)} achados PROPRIOS adicionais.")
    print(f"        DESTAQUE: identidade Scarlet = Carriet Inventory FIDC.")
    print(f"CSVs gravados em {OUT}/")


if __name__ == "__main__":
    main()
