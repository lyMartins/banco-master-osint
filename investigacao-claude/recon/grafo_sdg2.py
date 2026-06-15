"""Grafo interativo da reconstrucao do SDG II.

Recria visualmente a materia Folha/ICL sobre o SDG II usando os dados reconstruidos
pelo Luan (10/11 afirmacoes confirmadas via DF auditada FNET id 963178) + os achados
proprios feitos depois:
- Identidade Carriet Inventory FIDC = Scarlet FIDC (renomeacao 23/01/2025)
- Identidade Reag DTVM = CBSF DTVM (rebranding)
- Cadeia Hans 95 -> Anna -> SDG II (mencionada na materia, nao public no DF)
- Padrao Reag Jus Gestao de Ativos Judiciais como "valeta" pre-eventos criticos

Gera:
- investigacao-claude/recon/output/grafo_sdg2.html (PyVis interativo)
- investigacao-claude/recon/output/grafo_sdg2.svg (estatico, renderiza no GitHub)
"""
import os
from pathlib import Path

from pyvis.network import Network

OUT = Path(__file__).parent / "output"
OUT.mkdir(exist_ok=True)

# ============================================================================
# nos do grafo
# ============================================================================
# cor por categoria
COR = {
    "fundo_centro":   "#FFD700",  # ouro - SDG II (centro)
    "banco":          "#E53935",  # vermelho - Banco Master
    "devedor_chave":  "#8B0000",  # vermelho escuro - Lormont (epicentro)
    "fundo_cessor":   "#FF8C00",  # laranja - FIDCs cessores
    "cotista":        "#9C27B0",  # roxo - cotistas do SDG II
    "pessoa":         "#EC407A",  # rosa - PFs
    "admin_gestor":   "#1E88E5",  # azul - Reag/CBSF
    "empresa":        "#43A047",  # verde - empresas operacionais
    "achado_proprio": "#00ACC1",  # ciano - identidades reveladas por nos
}

# (id, label, cor, tamanho, titulo_hover)
NOS = [
    # centro
    ("SDG2", "SDG II FIDC NP\nR$ 5,455 bi (dez/2025)", COR["fundo_centro"], 60,
     "SDG II Fundo de Investimento em Direitos Creditorios Nao Padronizados\n"
     "CNPJ 46.909.301/0001-33\n"
     "Ativo dez/2025: R$ 5,455 bi (DF FNET id 963178)\n"
     "2 cotistas (Anna + nao identificado)\n"
     "AUDITOR: ABSTENCAO DE OPINIAO\n"
     "62% dos direitos creditorios sem lastro comprovado"),

    # banco
    ("MASTER", "Banco Master S.A.", COR["banco"], 50,
     "CNPJ 33.923.798/0001-00\n"
     "Cedeu direto ao SDG II: R$ 1,232 bi\n"
     "Liquidado pelo BC em 18/11/2025"),

    # devedor central
    ("LORMONT", "Lormont Participacoes\n(Nelson Tanure)", COR["devedor_chave"], 55,
     "CNPJ 34.263.138/0001-03\n"
     "Devedor em 6 CCBs cedidas ao SDG II = R$ 597 mi\n"
     "Sócio oculto do Master segundo MPF/PF\n"
     "Mesmo Lormont concentra 97% do FIDC Maranta"),

    # outros devedores/cedentes
    ("BANVOX", "Banvox Holding\n(ex-Quadrado)", COR["empresa"], 40,
     "CNPJ 38.461.854/0001-48\n"
     "Debenture 4a emissao R$ 400 mi\n"
     "SDG II adquiriu R$ 380,346 mi em 22/11/2023\n"
     "Mauricio Quadrado eh socio da Trustee DTVM (Carbono Oculto)"),
    ("SUPER", "Super Empreendimentos\n(grupo Vorcaro)", COR["empresa"], 35,
     "CNPJ 31.446.245/0001-70\n"
     "Diretor 2021-2024: Fabiano Zettel (cunhado de Vorcaro)\n"
     "Cedeu R$ 22,012 mi ao SDG II em 06/03/2023\n"
     "Recebeu R$ 180 mi do Gold Style FIDC (materia Imirante)"),

    # FIDCs cessores
    ("CARRIET", "Carriet Inventory FIDC\n= SCARLET FIDC\n(renomeado 23/01/2025)",
     COR["achado_proprio"], 45,
     "CNPJ 55.344.996/0001-44\n"
     "ACHADO PROPRIO: Carriet (DF do SDG II) e Scarlet (materia Imirante 14/04) sao o MESMO fundo\n"
     "Cedeu CCB Lormont R$ 325,452 mi ao SDG II em 27/09/2024\n"
     "Materia 14/04/2026: Receita Federal aponta Scarlet receptor R$ 2,5 bi do Master\n"
     "Renomeado em AGE de 23/01/2025 (mesmo ato que trocou gestor pra Reag Jus)"),
    ("BROL",    "B-ROL FIDC-NP",   COR["fundo_cessor"], 30, "Cedeu CCB Lormont R$ 41,417 mi (31/12/2024)"),
    ("CIBK",    "CIB-K FIDC-NP",   COR["fundo_cessor"], 30, "Cedeu CCB Lormont R$ 40,572 mi (31/12/2024)"),
    ("DELREY",  "Del Rey FIDC-NP", COR["fundo_cessor"], 30, "Cedeu CCB Lormont R$ 43,107 mi (31/12/2024)"),
    ("RUNEARD", "Runeard FIDC-NP", COR["fundo_cessor"], 30, "Cedeu CCB Lormont R$ 43,953 mi (31/12/2024)"),

    # cotistas
    ("ANNA", "Anna FIC-FIDC\n(cotista)", COR["cotista"], 40,
     "CNPJ 53.273.475/0001-18\n"
     "PL R$ 15,8 bi (5x maior que SDG II)\n"
     "Integralizou cotas SDG II em 30/09/2024 (cartulas BESC)\n"
     "'Hans 95 entra via Anna' - materia Folha/ICL"),
    ("MKS", "MKS Solucoes (??)\nCotista 2 nao confirmado", "#BDBDBD", 30,
     "NAO CONFIRMADO em fonte publica\n"
     "Materia atribui a fonte de inquerito\n"
     "DF nao nomeia cotistas; atas falam em 'unico Cotista' generico"),
    ("HANS95", "Hans 95 FIM IE CP", COR["pessoa"], 35,
     "CNPJ 32.088.041/0001-78\n"
     "FI Multimercado investigado em Carbono Oculto\n"
     "Cotista da Anna; via Anna entra no SDG II\n"
     "PL R$ 35 bi em abr/2026 (caiu pra R$ 27 bi em 5 dias)"),

    # admin/gestor
    ("REAG_CBSF", "Reag DTVM\n= CBSF DTVM\n(rebranding)", COR["admin_gestor"], 45,
     "CNPJ 34.829.992/0001-86\n"
     "ACHADO: mesma entidade aparece como 'Reag Trust DTVM' (registro_fundo)\n"
     "e 'CBSF DTVM' (Informe Mensal) - rebranding\n"
     "Administra SDG II + Gold Style + Scarlet/Carriet (3 FIDCs do escandalo)"),
    ("REAG_JUS", "Reag Jus\nGestao de Ativos Judiciais", COR["admin_gestor"], 35,
     "CNPJ 46.356.742/0001-55\n"
     "Padrao: assume gestao dos fundos pouco antes de eventos criticos\n"
     "Gold Style: 02/09/2024 (1 semana antes da Carbono Oculto)\n"
     "Scarlet/Carriet: 23/01/2025 (mesma AGE da renomeacao)"),

    # pessoas
    ("TANURE", "Nelson Tanure", COR["pessoa"], 35,
     "Apontado MPF/PF como SOCIO OCULTO do Master\n"
     "Controla Lormont Participacoes\n"
     "Toffoli bloqueou patrimonio em 06/01/2026"),
    ("VORCARO", "Daniel Vorcaro", COR["pessoa"], 40,
     "Controlador do Banco Master\n"
     "Preso em 04/03/2026 (Operacao Compliance Zero)\n"
     "Transferiu R$ 700 mi para Cayman em 2025\n"
     "R$ 1,2 bi aportado no Hans II FIP"),
]

# ============================================================================
# arestas (origem, destino, label, valor_grosso_mil_BRL, cor, descricao)
# ============================================================================
ARESTAS = [
    # cessoes diretas do Master ao SDG II
    ("MASTER",   "SDG2", "CCB Lormont\nR$ 102 mi (27/02/2024)",   102_438, "#E53935", "Cessao direta Master"),
    ("MASTER",   "SDG2", "Dir.Cred R$ 193 mi\n(19/12/2024)",      192_941, "#E53935", "Cessao direta Master"),
    ("MASTER",   "SDG2", "Dir.Cred R$ 936 mi\n(19/12/2024)",      936_222, "#E53935", "Cessao direta Master - bombatica"),

    # CCBs do Lormont cedidas via FIDCs
    ("CARRIET",  "SDG2", "CCB Lormont\nR$ 325 mi (27/09/2024)",   325_452, "#FF8C00", "Cessao via Carriet/Scarlet"),
    ("BROL",     "SDG2", "CCB Lormont\nR$ 41 mi",                  41_417, "#FF8C00", ""),
    ("CIBK",     "SDG2", "CCB Lormont\nR$ 41 mi",                  40_572, "#FF8C00", ""),
    ("DELREY",   "SDG2", "CCB Lormont\nR$ 43 mi",                  43_107, "#FF8C00", ""),
    ("RUNEARD",  "SDG2", "CCB Lormont\nR$ 44 mi",                  43_953, "#FF8C00", ""),

    # Lormont como devedor das CCBs (todos os 6 fundos cessores)
    ("LORMONT",  "MASTER",  "deve CCB", None, "#8B0000", "Master tomou CCB do Lormont"),
    ("LORMONT",  "CARRIET", "deve CCB", None, "#8B0000", ""),
    ("LORMONT",  "BROL",    "deve CCB", None, "#8B0000", ""),
    ("LORMONT",  "CIBK",    "deve CCB", None, "#8B0000", ""),
    ("LORMONT",  "DELREY",  "deve CCB", None, "#8B0000", ""),
    ("LORMONT",  "RUNEARD", "deve CCB", None, "#8B0000", ""),

    # Super e Banvox
    ("SUPER",    "SDG2", "Dir.Cred R$ 22 mi\n(06/03/2023)",        22_012, "#43A047", ""),
    ("BANVOX",   "SDG2", "Debenture R$ 380 mi\n(22/11/2023)",     380_346, "#43A047", ""),

    # cotistas
    ("ANNA",     "SDG2", "Cotista\n(integralizou 30/09/2024)",       None, "#9C27B0", "Cotista confirmado"),
    ("MKS",      "SDG2", "Cotista? (nao confirmado)",                None, "#BDBDBD", "Atribuido por materia"),
    ("HANS95",   "ANNA", "Investe na Anna",                          None, "#9C27B0", "Cadeia de fundos"),

    # admin/gestor
    ("REAG_CBSF", "SDG2", "Administra",          None, "#1E88E5", "Administracao fiduciaria"),
    ("REAG_JUS",  "SDG2", "Gestor pos-24/03/25", None, "#1E88E5", "Padrao de assumir gestao pre-eventos"),

    # pessoas controlam
    ("TANURE",   "LORMONT", "controla",                  None, "#EC407A", ""),
    ("VORCARO",  "MASTER",  "controla",                  None, "#EC407A", ""),
    ("VORCARO",  "SUPER",   "cunhado Zettel diretor\n2021-2024", None, "#EC407A", "Conexao familiar"),
]


def main():
    net = Network(
        height="900px", width="100%",
        bgcolor="#1a1a2e", font_color="#FFFFFF",
        directed=True,
        notebook=False,
    )
    # fisica suave pra layout legivel
    net.barnes_hut(gravity=-8000, central_gravity=0.3, spring_length=200,
                   spring_strength=0.04, damping=0.09, overlap=0)

    # adiciona nos
    for nid, label, cor, size, title in NOS:
        net.add_node(nid, label=label, color=cor, size=size, title=title,
                     borderWidth=2, font={"size": 14, "color": "#FFFFFF",
                                          "face": "Arial", "strokeWidth": 0})

    # adiciona arestas (espessura proporcional ao valor)
    for orig, dest, label, valor_mil, cor, desc in ARESTAS:
        if valor_mil:
            # espessura em escala logaritmica (R$ 22 mi a R$ 1,1 bi)
            width = max(1.5, min(10, (valor_mil / 100_000) * 1.2))
            title_extra = f"\nValor: R$ {valor_mil/1000:.1f} milhoes" if valor_mil < 1_000_000 else \
                          f"\nValor: R$ {valor_mil/1_000_000:.3f} bilhoes"
        else:
            width = 1.5
            title_extra = ""
        net.add_edge(orig, dest, label=label, color=cor, width=width,
                     title=f"{desc}{title_extra}".strip(),
                     arrows="to", font={"size": 10, "color": "#CCCCCC",
                                        "strokeWidth": 0, "align": "middle"})

    # opcoes de interacao
    net.set_options("""
    var options = {
      "interaction": {
        "hover": true,
        "tooltipDelay": 150,
        "navigationButtons": true,
        "keyboard": true
      },
      "physics": {
        "enabled": true,
        "stabilization": {"iterations": 200}
      }
    }
    """)

    saida_html = OUT / "grafo_sdg2.html"
    net.write_html(str(saida_html), notebook=False, open_browser=False)

    # injeta titulo + legenda + nota epistemologica no HTML gerado
    legenda = """
<div style="position:fixed; top:10px; left:10px; background:rgba(26,26,46,0.92);
            color:#EEE; padding:14px 18px; border-radius:8px; font-family:Arial,sans-serif;
            font-size:13px; border:1px solid #555; max-width:340px; z-index:9999;">
  <div style="font-size:16px; font-weight:bold; margin-bottom:6px; color:#FFD700;">
    SDG II FIDC - reconstrucao do esquema
  </div>
  <div style="font-size:11px; color:#AAA; margin-bottom:10px;">
    Fonte: DF auditada FNET id 963178 (Luan, PR #2) + achados proprios
  </div>
  <div style="display:grid; grid-template-columns:18px auto; gap:4px 8px; align-items:center;">
    <span style="background:#FFD700; width:14px; height:14px; border-radius:50%;"></span><span>Fundo-alvo (SDG II)</span>
    <span style="background:#E53935; width:14px; height:14px; border-radius:50%;"></span><span>Banco Master</span>
    <span style="background:#8B0000; width:14px; height:14px; border-radius:50%;"></span><span>Lormont (devedor central)</span>
    <span style="background:#FF8C00; width:14px; height:14px; border-radius:50%;"></span><span>FIDC cessor</span>
    <span style="background:#00ACC1; width:14px; height:14px; border-radius:50%;"></span><span>Achado proprio (Carriet=Scarlet)</span>
    <span style="background:#9C27B0; width:14px; height:14px; border-radius:50%;"></span><span>Cotista</span>
    <span style="background:#EC407A; width:14px; height:14px; border-radius:50%;"></span><span>Pessoa</span>
    <span style="background:#1E88E5; width:14px; height:14px; border-radius:50%;"></span><span>Admin / Gestor (Reag/CBSF)</span>
    <span style="background:#43A047; width:14px; height:14px; border-radius:50%;"></span><span>Empresa cedente</span>
    <span style="background:#BDBDBD; width:14px; height:14px; border-radius:50%;"></span><span>Nao confirmado em DF</span>
  </div>
  <div style="font-size:11px; color:#AAA; margin-top:10px; line-height:1.4;">
    Espessura da aresta = valor. Passe o mouse nos nos para ver fonte (DF id, valor, data).
  </div>
</div>
"""
    html = saida_html.read_text(encoding="utf-8")
    html = html.replace("<body>", "<body>" + legenda)
    saida_html.write_text(html, encoding="utf-8")

    print(f"-> grafo HTML interativo: {saida_html}")
    print(f"   abra no navegador para explorar")
    print()
    print(f"Nos: {len(NOS)} | Arestas: {len(ARESTAS)}")
    print(f"Valor total das cessoes mapeadas: R$ {sum(v for *_, v, _, _ in [(0,0,0,a[3],0,0) for a in ARESTAS] if v)/1000:.0f} milhoes")


if __name__ == "__main__":
    main()
