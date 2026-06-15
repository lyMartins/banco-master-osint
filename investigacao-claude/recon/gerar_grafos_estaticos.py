"""Gera 3 grafos SVG estaticos - um para cada fundo reconstruido.

Diferente do PyVis (HTML interativo): SVG puro, renderiza no GitHub, layout fixo
calculado manualmente para cada fundo, com identidade visual propria.

Output:
- investigacao-claude/recon/output/grafo_sdg2_estatico.svg
- investigacao-claude/recon/output/grafo_goldstyle_estatico.svg
- investigacao-claude/recon/output/grafo_scarlet_estatico.svg
"""
import math
from dataclasses import dataclass, field
from pathlib import Path

OUT = Path(__file__).parent / "output"
OUT.mkdir(exist_ok=True)

W, H = 1400, 900
PAD_TOP_HEADER = 120  # header reservado em cima
PAD_BOTTOM_LEGEND = 90  # legenda reservada embaixo


@dataclass
class No:
    nid: str
    label: str
    x: float
    y: float
    cor: str
    raio: int = 38
    sublabel: str = ""   # info menor (CNPJ, valor)
    cor_borda: str = ""  # se vazio = cor escurecida


@dataclass
class Aresta:
    orig: str
    dest: str
    label: str = ""
    cor: str = "#37474F"
    espessura: float = 2.0
    tracejada: bool = False
    curva: float = 0.0   # curvatura em pixels (positivo = curva pra cima)


@dataclass
class Grafo:
    fundo: str
    cnpj: str
    admin: str
    materia: str
    materia_data: str
    cor_tema: str
    cor_secundaria: str
    carimbo: str
    nos: list = field(default_factory=list)
    arestas: list = field(default_factory=list)


# ============================================================================
# helpers de posicionamento
# ============================================================================
CX, CY = W / 2, PAD_TOP_HEADER + (H - PAD_TOP_HEADER - PAD_BOTTOM_LEGEND) / 2


def pol(cx, cy, raio_dist, angulo_deg):
    """coordenadas polares -> cartesianas (angulo em graus, 0=leste, 90=norte)."""
    rad = math.radians(angulo_deg)
    return (cx + raio_dist * math.cos(rad), cy - raio_dist * math.sin(rad))


# ============================================================================
# GRAFO 1: SDG II
# ============================================================================
def grafo_sdg2() -> Grafo:
    g = Grafo(
        fundo="SDG II FIDC NP",
        cnpj="46.909.301/0001-33",
        admin="Reag Trust DTVM (= CBSF DTVM)",
        materia="Folha/ICL — Master usou fundo de R$ 5,4 bi para esconder dividas",
        materia_data="26/05/2026",
        cor_tema="#B8860B",
        cor_secundaria="#FFD700",
        carimbo="Abstencao do auditor — 62% dos direitos creditorios sem lastro",
    )
    # centro
    g.nos.append(No("SDG2", "SDG II FIDC", CX, CY, "#FFD700", 60,
                    "R$ 5,455 bi — 2 cotistas"))
    # cessores FIDC (anel sul-leste)
    for i, (nid, lb, val) in enumerate([
        ("CARRIET", "Carriet/Scarlet", "R$ 325 mi"),
        ("BROL",    "B-ROL",            "R$ 41 mi"),
        ("CIBK",    "CIB-K",            "R$ 41 mi"),
        ("DELREY",  "Del Rey",          "R$ 43 mi"),
        ("RUNEARD", "Runeard",          "R$ 44 mi"),
    ]):
        ang = -10 - i * 18  # de -10 a -82 graus
        x, y = pol(CX, CY, 300, ang)
        cor = "#00ACC1" if nid == "CARRIET" else "#FF8C00"
        g.nos.append(No(nid, lb, x, y, cor, 32, val))
    # Banco Master (oeste)
    x, y = pol(CX, CY, 280, 180)
    g.nos.append(No("MASTER", "Banco Master", x, y, "#E53935", 48,
                    "Cessao direta R$ 1,232 bi"))
    # Lormont (sul oeste — devedor central)
    x, y = pol(CX, CY, 320, -135)
    g.nos.append(No("LORMONT", "Lormont", x, y, "#8B0000", 44,
                    "Tanure — devedor de 6 CCBs"))
    # Banvox, Super (no leste)
    x, y = pol(CX, CY, 290, 195)
    g.nos.append(No("BANVOX", "Banvox", x, y, "#43A047", 34,
                    "Debenture R$ 380 mi"))
    x, y = pol(CX, CY, 270, 210)
    g.nos.append(No("SUPER", "Super Empreend.", x, y, "#43A047", 32,
                    "R$ 22 mi (Vorcaro)"))
    # Cotistas (norte)
    x, y = pol(CX, CY, 240, 130)
    g.nos.append(No("ANNA", "Anna FIC-FIDC", x, y, "#9C27B0", 36,
                    "PL R$ 15,8 bi"))
    x, y = pol(CX, CY, 260, 70)
    g.nos.append(No("HANS95", "Hans 95", x, y, "#EC407A", 30,
                    "via Anna"))
    x, y = pol(CX, CY, 260, 50)
    g.nos.append(No("MKS", "MKS Solucoes(?)", x, y, "#BDBDBD", 28,
                    "Nao confirmado"))
    # Admin
    x, y = pol(CX, CY, 270, 25)
    g.nos.append(No("REAG", "Reag DTVM = CBSF", x, y, "#1E88E5", 36,
                    "Administradora"))
    # Pessoas
    x, y = pol(CX, CY, 360, -90)
    g.nos.append(No("VORCARO", "D. Vorcaro", x, y, "#EC407A", 28,
                    "Controla Master"))
    x, y = pol(CX, CY, 380, -160)
    g.nos.append(No("TANURE", "N. Tanure", x, y, "#EC407A", 28,
                    "Controla Lormont"))

    # ARESTAS
    # cedentes -> SDG II
    g.arestas += [
        Aresta("MASTER", "SDG2", "R$ 1,232 bi", "#E53935", 5.5),
        Aresta("BANVOX", "SDG2", "R$ 380 mi", "#43A047", 4.0),
        Aresta("SUPER", "SDG2",  "R$ 22 mi", "#43A047", 2.5),
        Aresta("CARRIET", "SDG2", "R$ 325 mi (CCB Lormont)", "#00ACC1", 4.0),
        Aresta("BROL", "SDG2", "", "#FF8C00", 2.0),
        Aresta("CIBK", "SDG2", "", "#FF8C00", 2.0),
        Aresta("DELREY", "SDG2", "", "#FF8C00", 2.0),
        Aresta("RUNEARD", "SDG2", "", "#FF8C00", 2.0),
    ]
    # Lormont como devedor (linhas tracejadas indicam "deve")
    for cid in ["MASTER", "CARRIET", "BROL", "CIBK", "DELREY", "RUNEARD"]:
        g.arestas.append(Aresta("LORMONT", cid, "", "#8B0000", 1.5, True, 0))
    # cotistas
    g.arestas.append(Aresta("ANNA", "SDG2", "cotista", "#9C27B0", 3.0))
    g.arestas.append(Aresta("MKS", "SDG2", "cotista?", "#BDBDBD", 1.5, True))
    g.arestas.append(Aresta("HANS95", "ANNA", "via Anna", "#EC407A", 2.0))
    # admin
    g.arestas.append(Aresta("REAG", "SDG2", "administra", "#1E88E5", 2.5, True))
    # pessoas controlam
    g.arestas.append(Aresta("VORCARO", "MASTER", "controla", "#EC407A", 2.0, True))
    g.arestas.append(Aresta("TANURE", "LORMONT", "controla", "#EC407A", 2.0, True))
    return g


# ============================================================================
# GRAFO 2: Gold Style
# ============================================================================
def grafo_goldstyle() -> Grafo:
    g = Grafo(
        fundo="Gold Style FIDC NP",
        cnpj="34.081.900/0001-22",
        admin="Reag DTVM (= CBSF) → Reag Jus em 02/09/2024",
        materia="Imirante/g1 — Fundo ligado a Reag recebeu R$ 1 bi de empresas do PCC",
        materia_data="18/03/2026",
        cor_tema="#7B5E00",
        cor_secundaria="#D4A017",
        carimbo="Abstencao em 2 exercicios consecutivos (PwC + Baker Tilly) — laudo HORBIA inflou ativo 10.000x",
    )
    # centro
    g.nos.append(No("GS", "Gold Style FIDC", CX, CY, "#D4A017", 60,
                    "PL R$ 1,36 bi (DF 2022)"))
    # ativo subjacente (norte) — BESC banco extinto
    x, y = pol(CX, CY, 260, 90)
    g.nos.append(No("BESC", "BESC (extinto 2008)", x, y, "#607D8B", 44,
                    "18,17 mi acoes preferenciais"))
    # laudo HORBIA (noroeste) — destacado como achado
    x, y = pol(CX, CY, 320, 140)
    g.nos.append(No("HORBIA", "Laudo HORBIA\n(dez/2019)", x, y, "#00ACC1", 42,
                    "Avaliou em R$ 13,78 bi — fundo registrou a 10%"))
    # cessor original (oeste)
    x, y = pol(CX, CY, 280, 175)
    g.nos.append(No("EXCALIBUR", "Excalibur FIM CP", x, y, "#FF8C00", 40,
                    "Cessao 11/03/2020"))
    # auditores (nordeste) - abstencao
    x, y = pol(CX, CY, 290, 35)
    g.nos.append(No("PWC", "PwC", x, y, "#6A1B9A", 32,
                    "Abstencao DF 2021"))
    x, y = pol(CX, CY, 290, 5)
    g.nos.append(No("BAKER", "Baker Tilly", x, y, "#6A1B9A", 32,
                    "Abstencao DF 2022"))
    # admin -> gestor (sul-leste)
    x, y = pol(CX, CY, 240, -30)
    g.nos.append(No("REAG", "Reag DTVM\n(= CBSF)", x, y, "#1E88E5", 38,
                    "Admin ate 02/09/2024"))
    x, y = pol(CX, CY, 290, -65)
    g.nos.append(No("REAG_JUS", "Reag Jus\nGestao Ativos Jud.", x, y, "#EF6C00", 38,
                    "Assumiu 02/09/2024 (1 semana antes da Carbono Oculto)"))
    # fluxo COAF (sul) — marcadas como NAO na DF
    x, y = pol(CX, CY, 240, -110)
    g.nos.append(No("ASTER", "Aster Petroleo", x, y, "#BDBDBD", 30,
                    "R$ 759 mi (COAF)"))
    x, y = pol(CX, CY, 280, -135)
    g.nos.append(No("BK", "BK Bank", x, y, "#BDBDBD", 28,
                    "R$ 158 mi (COAF)"))
    x, y = pol(CX, CY, 290, -160)
    g.nos.append(No("INOV", "Inovanti", x, y, "#BDBDBD", 28,
                    "R$ 175 mi (COAF)"))
    # fato relevante reprecificacao (canto)
    x, y = pol(CX, CY, 360, 170)
    g.nos.append(No("FR", "FR 10/01/2025\nREPRECIFICACAO", x, y, "#00ACC1", 36,
                    "Reag admite por escrito"))

    # arestas
    g.arestas += [
        Aresta("EXCALIBUR", "GS", "cede 18,17 mi acoes", "#FF8C00", 3.5),
        Aresta("BESC", "EXCALIBUR", "ativo subjacente", "#607D8B", 2.0, True),
        Aresta("HORBIA", "BESC", "avaliou", "#00ACC1", 2.0, True),
        Aresta("PWC", "GS", "abstencao 2021", "#6A1B9A", 2.5, True),
        Aresta("BAKER", "GS", "abstencao 2022", "#6A1B9A", 2.5, True),
        Aresta("REAG", "GS", "administra", "#1E88E5", 2.5, True),
        Aresta("REAG", "REAG_JUS", "transfere gestao\n02/09/2024", "#EF6C00", 2.5),
        Aresta("REAG_JUS", "GS", "gestor pos-09/2024", "#EF6C00", 2.5, True),
        Aresta("ASTER", "GS", "fluxo COAF\n(NAO na DF)", "#BDBDBD", 2.0, True),
        Aresta("BK", "GS",   "(NAO na DF)", "#BDBDBD", 1.5, True),
        Aresta("INOV", "GS", "(NAO na DF)", "#BDBDBD", 1.5, True),
        Aresta("FR", "GS", "Reag admite\nreprecificacao", "#00ACC1", 2.5),
    ]
    return g


# ============================================================================
# GRAFO 3: Scarlet (= Carriet Inventory)
# ============================================================================
def grafo_scarlet() -> Grafo:
    g = Grafo(
        fundo="Scarlet FIDC NP (ex-Carriet Inventory)",
        cnpj="55.344.996/0001-44",
        admin="Reag DTVM (= CBSF) → Reag Jus em 23/01/2025",
        materia="Imirante/g1 — Master e Vorcaro aplicaram R$ 12,2 bi em fundos, diz Receita",
        materia_data="14/04/2026",
        cor_tema="#C41E3A",
        cor_secundaria="#FF3030",
        carimbo="Scarlet = Carriet Inventory FIDC (mesma identidade, mesmo CNPJ — renomeado em AGE de 23/01/2025)",
    )
    # centro (com label duplo - identidade revelada)
    g.nos.append(No("SCARLET", "CARRIET INVENTORY\n=  SCARLET", CX, CY, "#FF3030", 70,
                    "Mesmo CNPJ — renomeado 23/01/2025"))
    # SDG II como destino da cessao (norte)
    x, y = pol(CX, CY, 280, 90)
    g.nos.append(No("SDG2", "SDG II FIDC", x, y, "#FFD700", 50,
                    "Recebeu R$ 325 mi (CCB Lormont) em 27/09/2024"))
    # Banco Master (oeste)
    x, y = pol(CX, CY, 280, 175)
    g.nos.append(No("MASTER", "Banco Master", x, y, "#E53935", 45,
                    "Aporte R$ 2,5 bi (segundo Receita)"))
    # Hans II FIP (leste)
    x, y = pol(CX, CY, 280, 5)
    g.nos.append(No("HANSII", "Hans II FIP", x, y, "#FF8C00", 40,
                    "R$ 70 mi aplicado em dez/2024"))
    # Lormont (sul-oeste) - devedor da CCB
    x, y = pol(CX, CY, 310, -150)
    g.nos.append(No("LORMONT", "Lormont", x, y, "#8B0000", 36,
                    "Devedor da CCB cedida"))
    # Reag DTVM (norte-leste)
    x, y = pol(CX, CY, 240, 40)
    g.nos.append(No("REAG", "Reag DTVM\n(= CBSF)", x, y, "#1E88E5", 38,
                    "Admin ate hoje"))
    # Reag Trust gestora antiga (sul-leste)
    x, y = pol(CX, CY, 250, -50)
    g.nos.append(No("REAG_TR", "Reag Trust\nAdm Recursos", x, y, "#90A4AE", 32,
                    "Gestora ate 23/01/2025"))
    # Reag Jus (sul)
    x, y = pol(CX, CY, 290, -90)
    g.nos.append(No("REAG_JUS", "Reag Jus\nGestao Ativos Jud.", x, y, "#EF6C00", 40,
                    "Assumiu na AGE da renomeacao"))
    # Materia Imirante (canto superior direito)
    x, y = pol(CX, CY, 380, 50)
    g.nos.append(No("MATERIA", "Materia\n14/04/2026", x, y, "#C41E3A", 36,
                    "'Scarlet recebeu R$ 2,5 bi do Master'"))
    # Achado central: AGE 23/01/2025
    x, y = pol(CX, CY, 340, -125)
    g.nos.append(No("AGE", "AGE 23/01/2025", x, y, "#00ACC1", 44,
                    "Renomeacao + troca de gestora"))

    # arestas
    g.arestas += [
        Aresta("MASTER", "SCARLET", "aporta R$ 2,5 bi\n(segundo Receita)", "#E53935", 4.5),
        Aresta("SCARLET", "SDG2", "cede CCB Lormont\nR$ 325 mi (27/09/24)", "#1565C0", 4.0),
        Aresta("SCARLET", "HANSII", "aplica R$ 70 mi", "#FF8C00", 2.5),
        Aresta("LORMONT", "SCARLET", "devedor da CCB", "#8B0000", 2.0, True),
        Aresta("REAG", "SCARLET", "administra", "#1E88E5", 2.5, True),
        Aresta("REAG_TR", "SCARLET", "gestora ate 23/01/25", "#90A4AE", 2.0, True),
        Aresta("REAG_JUS", "SCARLET", "gestora pos-23/01/25", "#EF6C00", 2.5, True),
        Aresta("AGE", "SCARLET", "renomeia + troca gestor", "#00ACC1", 3.5),
        Aresta("MATERIA", "SCARLET", "cita como 'Scarlet'", "#C41E3A", 2.0, True),
    ]
    return g


# ============================================================================
# renderizador SVG
# ============================================================================
def escape_xml(s: str) -> str:
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace("\"", "&quot;").replace("'", "&apos;"))


def darken(hex_color: str, factor: float = 0.7) -> str:
    h = hex_color.lstrip("#")
    r, gr, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"#{int(r*factor):02x}{int(gr*factor):02x}{int(b*factor):02x}"


def render(g: Grafo) -> str:
    parts = []
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
        f'width="{W}" height="{H}" font-family="Arial,Helvetica,sans-serif">'
    )
    # fundo
    parts.append(f'<rect width="{W}" height="{H}" fill="#FAFAFA"/>')

    # ============== HEADER ==============
    parts.append(f'<rect x="0" y="0" width="{W}" height="{PAD_TOP_HEADER}" fill="{g.cor_tema}"/>')
    parts.append(
        f'<rect x="0" y="{PAD_TOP_HEADER - 6}" width="{W}" height="6" fill="{g.cor_secundaria}"/>'
    )
    parts.append(
        f'<text x="60" y="50" font-size="32" font-weight="bold" fill="#FFFFFF">'
        f'{escape_xml(g.fundo)}</text>'
    )
    parts.append(
        f'<text x="60" y="78" font-size="14" fill="#FFFFFF" opacity="0.92">'
        f'CNPJ {escape_xml(g.cnpj)}  —  Administrador: {escape_xml(g.admin)}</text>'
    )
    parts.append(
        f'<text x="60" y="103" font-size="13" fill="#FFFFFF" opacity="0.85" font-style="italic">'
        f'Materia-ancora: {escape_xml(g.materia)} ({escape_xml(g.materia_data)})</text>'
    )
    parts.append(
        f'<text x="{W - 60}" y="50" font-size="14" fill="#FFFFFF" opacity="0.7" '
        f'text-anchor="end">grafo de relacoes — sem linha temporal</text>'
    )

    # ============== ARESTAS (renderizadas primeiro pra ficar atras dos nos) ==============
    nos_by_id = {n.nid: n for n in g.nos}
    for ar in g.arestas:
        if ar.orig not in nos_by_id or ar.dest not in nos_by_id:
            continue
        n1 = nos_by_id[ar.orig]
        n2 = nos_by_id[ar.dest]
        # ponto de borda dos nos (recuar pela raio)
        dx, dy = n2.x - n1.x, n2.y - n1.y
        dist = math.hypot(dx, dy) or 1
        ux, uy = dx / dist, dy / dist
        x1 = n1.x + ux * n1.raio
        y1 = n1.y + uy * n1.raio
        x2 = n2.x - ux * (n2.raio + 8)  # 8 = espaco pra cabeca da seta
        y2 = n2.y - uy * (n2.raio + 8)
        # linha
        dash = ' stroke-dasharray="6,4"' if ar.tracejada else ""
        marker = ""  # vamos desenhar a setinha manualmente (simples polygon)
        parts.append(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{ar.cor}" stroke-width="{ar.espessura}" opacity="0.75"{dash}/>'
        )
        # setinha
        # vetor perpendicular pra base da seta
        # ponta em (x2, y2), base em (x2 - 12*ux + 5*-uy, y2 - 12*uy + 5*ux)
        bx = x2 - 12 * ux
        by = y2 - 12 * uy
        px, py = -uy, ux  # perpendicular
        p1 = (bx + 6 * px, by + 6 * py)
        p2 = (bx - 6 * px, by - 6 * py)
        parts.append(
            f'<polygon points="{x2:.1f},{y2:.1f} {p1[0]:.1f},{p1[1]:.1f} '
            f'{p2[0]:.1f},{p2[1]:.1f}" fill="{ar.cor}"/>'
        )
        # label da aresta (no meio, ligeiramente acima)
        if ar.label:
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            # quebrar em 2 linhas se tiver \n
            for li, ln in enumerate(ar.label.split("\n")):
                ly = my - 3 + li * 12
                # fundo branco translucido pro texto ser legivel
                tw = max(50, len(ln) * 6)
                parts.append(
                    f'<rect x="{mx - tw/2:.1f}" y="{ly - 9:.1f}" width="{tw:.1f}" '
                    f'height="12" fill="#FFFFFF" opacity="0.92" rx="2"/>'
                )
                parts.append(
                    f'<text x="{mx:.1f}" y="{ly:.1f}" font-size="10" '
                    f'fill="{darken(ar.cor, 0.7)}" text-anchor="middle" font-weight="bold">'
                    f'{escape_xml(ln)}</text>'
                )

    # ============== NOS ==============
    for n in g.nos:
        borda = n.cor_borda or darken(n.cor, 0.65)
        parts.append(
            f'<circle cx="{n.x:.1f}" cy="{n.y:.1f}" r="{n.raio}" '
            f'fill="{n.cor}" stroke="{borda}" stroke-width="3"/>'
        )
        # label (quebrar em linhas por \n)
        linhas = n.label.split("\n")
        nlh = len(linhas)
        # tamanho da fonte adaptado ao raio
        if n.raio >= 55:
            fsize = 15
        elif n.raio >= 40:
            fsize = 13
        else:
            fsize = 11
        # cor do texto contrastante
        h = n.cor.lstrip("#")
        r_, g_, b_ = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        luminance = 0.299 * r_ + 0.587 * g_ + 0.114 * b_
        text_color = "#FFFFFF" if luminance < 140 else "#1A1A1A"
        # render
        y_start = n.y - (nlh - 1) * (fsize + 1) / 2
        for i, ln in enumerate(linhas):
            parts.append(
                f'<text x="{n.x:.1f}" y="{y_start + i*(fsize+1) + 4:.1f}" '
                f'font-size="{fsize}" font-weight="bold" fill="{text_color}" '
                f'text-anchor="middle">{escape_xml(ln)}</text>'
            )
        # sublabel embaixo do no (fora do circulo)
        if n.sublabel:
            sub_y = n.y + n.raio + 14
            # background suave pra legibilidade
            sublines = []
            words = n.sublabel.split()
            atual = ""
            for w in words:
                if len(atual + " " + w) > 30 and atual:
                    sublines.append(atual)
                    atual = w
                else:
                    atual = (atual + " " + w).strip()
            if atual:
                sublines.append(atual)
            sublines = sublines[:2]
            for j, sl in enumerate(sublines):
                tw = max(60, len(sl) * 6)
                parts.append(
                    f'<rect x="{n.x - tw/2:.1f}" y="{sub_y - 9 + j*13:.1f}" '
                    f'width="{tw:.1f}" height="13" fill="#FFFFFF" opacity="0.92" rx="2"/>'
                )
                parts.append(
                    f'<text x="{n.x:.1f}" y="{sub_y + j*13:.1f}" font-size="10" '
                    f'fill="#37474F" text-anchor="middle">{escape_xml(sl)}</text>'
                )

    # ============== CARIMBO ==============
    y_carimbo = H - PAD_BOTTOM_LEGEND + 8
    parts.append(
        f'<rect x="60" y="{y_carimbo}" width="{W - 120}" height="44" '
        f'fill="{g.cor_tema}" rx="6"/>'
    )
    parts.append(
        f'<text x="{W/2}" y="{y_carimbo + 17}" font-size="11" fill="#FFFFFF" '
        f'opacity="0.85" text-anchor="middle">CARIMBO DA RECONSTRUCAO</text>'
    )
    palavras = g.carimbo.split()
    linhas_c = []
    atual = ""
    for p in palavras:
        if len(atual + " " + p) > 120 and atual:
            linhas_c.append(atual)
            atual = p
        else:
            atual = (atual + " " + p).strip()
    if atual:
        linhas_c.append(atual)
    cy_t = y_carimbo + 35
    for ln in linhas_c[:1]:
        parts.append(
            f'<text x="{W/2}" y="{cy_t}" font-size="13" font-weight="bold" '
            f'fill="#FFFFFF" text-anchor="middle">{escape_xml(ln)}</text>'
        )
    # rodape
    parts.append(
        f'<text x="{W - 60}" y="{H - 8}" font-size="10" fill="#90A4AE" '
        f'text-anchor="end">reconstrucao via DF FNET — lyMartins/banco-master-osint</text>'
    )

    parts.append('</svg>')
    return "".join(parts)


def main():
    for func, nome in [(grafo_sdg2, "grafo_sdg2_estatico.svg"),
                       (grafo_goldstyle, "grafo_goldstyle_estatico.svg"),
                       (grafo_scarlet, "grafo_scarlet_estatico.svg")]:
        g = func()
        path = OUT / nome
        path.write_text(render(g), encoding="utf-8")
        print(f"-> {path}  ({len(g.nos)} nos, {len(g.arestas)} arestas)")


if __name__ == "__main__":
    main()
