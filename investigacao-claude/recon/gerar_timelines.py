"""Gera 3 timelines SVG estaticas dos fundos reconstruidos.

Cada SVG eh autocontido (sem CSS/JS externo), renderiza no GitHub no preview de
arquivo SVG, e tem identidade visual propria pra cada fundo (titulo + cor + tema).

Output:
- investigacao-claude/recon/output/timeline_sdg2.svg
- investigacao-claude/recon/output/timeline_goldstyle.svg
- investigacao-claude/recon/output/timeline_scarlet.svg
"""
from dataclasses import dataclass
from pathlib import Path

OUT = Path(__file__).parent / "output"
OUT.mkdir(exist_ok=True)


@dataclass
class Evento:
    data: str          # "AAAA-MM" ou "AAAA-MM-DD"
    rotulo: str        # texto curto (max ~40 chars)
    detalhe: str = ""  # texto longo (1-2 linhas)
    tipo: str = "fato" # fato | cessao | parecer | troca | publico | achado


@dataclass
class Timeline:
    fundo: str         # nome do fundo
    cnpj: str
    admin: str
    materia: str       # titulo da materia
    materia_data: str  # data da materia
    cor_tema: str      # cor primaria (header)
    cor_secundaria: str  # cor de destaque
    carimbo: str       # "carimbo" final - o achado central
    eventos: list


# ============================================================================
# dados dos 3 fundos
# ============================================================================
SDG2 = Timeline(
    fundo="SDG II FIDC NP",
    cnpj="46.909.301/0001-33",
    admin="Reag Trust DTVM (= CBSF DTVM)",
    materia="Folha/ICL — Master usou fundo de R$ 5,4 bi para esconder dividas",
    materia_data="26/05/2026",
    cor_tema="#B8860B",       # ouro escuro
    cor_secundaria="#FFD700",
    carimbo="Auditor: ABSTENCAO DE OPINIAO — 62% dos direitos creditorios sem lastro comprovado",
    eventos=[
        Evento("2023-03-06", "Super Empreendimentos cede",
               "R$ 22,012 mi em direitos creditorios", "cessao"),
        Evento("2023-11-22", "Banvox debenture",
               "R$ 380,346 mi (4a emissao de R$ 400 mi)", "cessao"),
        Evento("2024-02-27", "Master cede CCB de Lormont",
               "R$ 102,438 mi (Lormont = Nelson Tanure)", "cessao"),
        Evento("2024-09-27", "Carriet Inventory cede CCB Lormont",
               "R$ 325,452 mi — esse Carriet vira SCARLET em 2025", "achado"),
        Evento("2024-09-30", "Anna integraliza cotas",
               "Anna FIC-FIDC (PL R$ 15,8 bi) entra como cotista", "fato"),
        Evento("2024-12-19", "Master cede R$ 1,129 bi",
               "2 cessoes no mesmo dia (R$ 193 mi + R$ 936 mi)", "cessao"),
        Evento("2024-12-31", "4 FIDCs cedem CCBs Lormont",
               "B-ROL + CIB-K + Del Rey + Runeard = R$ 169 mi", "cessao"),
        Evento("2025-11-18", "Banco Master liquidado pelo BC",
               "Liquidacao extrajudicial", "publico"),
        Evento("2025-12-31", "Ativo R$ 5,455 bi",
               "2 cotistas, abstencao do auditor", "parecer"),
        Evento("2026-03-04", "Vorcaro preso",
               "Operacao Compliance Zero", "publico"),
        Evento("2026-04", "SDG II para de reportar",
               "Coerente com a liquidacao", "fato"),
    ],
)


GOLD_STYLE = Timeline(
    fundo="Gold Style FIDC NP",
    cnpj="34.081.900/0001-22",
    admin="Reag DTVM (= CBSF) — depois Reag Jus",
    materia="Imirante/g1 — Fundo ligado a Reag recebeu R$ 1 bi de empresas do PCC",
    materia_data="18/03/2026",
    cor_tema="#7B5E00",       # dourado opaco (BESC = banco extinto)
    cor_secundaria="#D4A017",
    carimbo="Abstencao em 2 exercicios consecutivos (PwC 2021 + Baker Tilly 2022) — ativo BESC com laudo HORBIA inflado 10.000x",
    eventos=[
        Evento("2019-12", "Laudo HORBIA precifica BESC",
               "Acoes do Banco do Estado de SC (extinto 2008) a R$ 758,69 cada = R$ 13,78 bi", "achado"),
        Evento("2020-03-11", "Excalibur FIM cede 18,17 mi acoes BESC",
               "Direitos creditorios integralizados (sem dinheiro)", "cessao"),
        Evento("2020-10-16", "Reag DTVM assume administracao",
               "AGC transfere admin pra CNPJ 34.829.992/0001-86", "fato"),
        Evento("2021-03-31", "DF: PL R$ 1,362 bi",
               "Registro a 10% do laudo (R$ 75/acao em vez de R$ 758)", "parecer"),
        Evento("2023-06-29", "PwC: ABSTENCAO de opiniao DF 2021",
               "Sem evidencia de existencia/titularidade/transferencia", "parecer"),
        Evento("2024-09-02", "Mudanca: Reag DTVM → Reag Jus",
               "1 semana antes da 1a fase da Operacao Carbono Oculto", "troca"),
        Evento("2025-01-10", "Fato Relevante: REPRECIFICACAO BESC",
               "Reag admite por escrito ajuste no valor das 'Cartulas'", "achado"),
        Evento("2025-03-14", "Baker Tilly: ABSTENCAO DF 2022",
               "Mesma justificativa do PwC, novo auditor", "parecer"),
        Evento("2025-03-24", "DF 2022 entregue ao FNET",
               "Atraso de quase 3 anos do fechamento", "fato"),
        Evento("2026-01", "Reag DTVM liquidada pelo BC",
               "Liquidacao extrajudicial", "publico"),
        Evento("2026-03-04", "Vorcaro preso", "Operacao Compliance Zero", "publico"),
        Evento("2026-05-19", "Trimestral 1T26: 'Dada a liquidacao'",
               "16 campos obrigatorios todos respondidos com 'nao foi realizada'", "fato"),
    ],
)


SCARLET = Timeline(
    fundo="Scarlet FIDC NP (ex-Carriet Inventory)",
    cnpj="55.344.996/0001-44",
    admin="Reag DTVM (= CBSF) — depois Reag Jus",
    materia="Imirante/g1 — Master e Vorcaro aplicaram R$ 12,2 bi em fundos, diz Receita",
    materia_data="14/04/2026",
    cor_tema="#C41E3A",       # vermelho escarlate
    cor_secundaria="#FF3030",
    carimbo="ACHADO: Scarlet = Carriet Inventory (mesma identidade, mesmo CNPJ). Renomeacao em 23/01/2025",
    eventos=[
        Evento("2024-05-31", "Constituicao como CARRIET INVENTORY",
               "Admin: Reag DTVM. Gestor: Reag Trust Adm Recursos", "fato"),
        Evento("2024-09-27", "Carriet cede CCB Lormont R$ 325 mi ao SDG II",
               "Documentado na DF do SDG II (reconstrucao Luan)", "cessao"),
        Evento("2024-11-27", "AGE — fundo ainda se chama CARRIET INVENTORY",
               "Confirmado na ata FNET id 789348", "fato"),
        Evento("2024-12-31", "Carteira R$ 1,058 bi",
               "R$ 469 mi em debentures + R$ 20 mi em CCBs + R$ 70 mi no Hans II FIP", "fato"),
        Evento("2025-01-23", "AGE RENOMEIA Carriet → SCARLET",
               "Mesmo ato troca gestor pra Reag Jus Gestao de Ativos Judiciais", "achado"),
        Evento("2025-03-14", "Taticca: opiniao LIMPA DF 2024",
               "Diferente do SDG II / Gold Style (mas DF cobre so 7 meses)", "parecer"),
        Evento("2026-01", "Reag DTVM liquidada pelo BC",
               "Liquidacao extrajudicial", "publico"),
        Evento("2026-03-04", "Vorcaro preso", "Operacao Compliance Zero", "publico"),
        Evento("2026-04", "Informe mensal: PL R$ 2,71 bi",
               "6 cotistas (fundo exclusivo); R$ 304 mi acoes judiciais + R$ 269 mi precatorios", "fato"),
        Evento("2026-04-14", "Materia: 'Scarlet recebeu R$ 2,5 bi do Master'",
               "Imirante/g1 — mesmo CNPJ que ja era Carriet 4 meses antes", "achado"),
        Evento("2026-05-19", "Trimestral 1T26: 'Dada a liquidacao'",
               "Padrao identico ao Gold Style", "fato"),
    ],
)


# ============================================================================
# renderizador SVG
# ============================================================================
COR_TIPO = {
    "fato":    "#37474F",   # cinza-azul (neutro)
    "cessao":  "#1565C0",   # azul (fluxo de dinheiro)
    "parecer": "#6A1B9A",   # roxo (auditoria)
    "troca":   "#EF6C00",   # laranja (mudanca estrutural)
    "publico": "#C62828",   # vermelho (evento publico macro)
    "achado":  "#00838F",   # ciano (achado proprio)
}

LABEL_TIPO = {
    "fato":    "fato",
    "cessao":  "cessao / aporte",
    "parecer": "parecer auditor",
    "troca":   "troca de gestao",
    "publico": "evento publico",
    "achado":  "achado proprio",
}


def escape_xml(s: str) -> str:
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace("\"", "&quot;").replace("'", "&apos;"))


def render(tl: Timeline) -> str:
    W = 1400
    eventos = tl.eventos
    n = len(eventos)
    # margens
    PAD_X = 80
    inner_w = W - 2 * PAD_X
    # cada evento ocupa uma coluna horizontal
    col_w = inner_w / max(n, 1)
    # alturas
    H_HEADER = 130
    H_TIMELINE = 480
    H_CARIMBO = 130
    H = H_HEADER + H_TIMELINE + H_CARIMBO

    y_axis = H_HEADER + H_TIMELINE // 2 + 20  # linha do eixo

    parts = []
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
        f'width="{W}" height="{H}" font-family="Arial,Helvetica,sans-serif">'
    )
    # fundo branco
    parts.append(f'<rect width="{W}" height="{H}" fill="#FAFAFA"/>')

    # ============== HEADER ==============
    parts.append(f'<rect x="0" y="0" width="{W}" height="{H_HEADER}" fill="{tl.cor_tema}"/>')
    # faixa de destaque embaixo do header
    parts.append(
        f'<rect x="0" y="{H_HEADER - 6}" width="{W}" height="6" fill="{tl.cor_secundaria}"/>'
    )
    # titulo do fundo
    parts.append(
        f'<text x="{PAD_X}" y="50" font-size="32" font-weight="bold" fill="#FFFFFF">'
        f'{escape_xml(tl.fundo)}</text>'
    )
    # subtitulo (CNPJ + admin)
    parts.append(
        f'<text x="{PAD_X}" y="78" font-size="14" fill="#FFFFFF" opacity="0.92">'
        f'CNPJ {escape_xml(tl.cnpj)}  —  Administrador: {escape_xml(tl.admin)}</text>'
    )
    # materia-ancora
    parts.append(
        f'<text x="{PAD_X}" y="105" font-size="13" fill="#FFFFFF" opacity="0.85" font-style="italic">'
        f'Materia-ancora: {escape_xml(tl.materia)} ({escape_xml(tl.materia_data)})</text>'
    )
    # ano canto direito
    parts.append(
        f'<text x="{W - PAD_X}" y="50" font-size="14" fill="#FFFFFF" opacity="0.7" '
        f'text-anchor="end">linha do tempo da reconstrucao</text>'
    )

    # ============== EIXO ==============
    parts.append(
        f'<line x1="{PAD_X}" y1="{y_axis}" x2="{W - PAD_X}" y2="{y_axis}" '
        f'stroke="#37474F" stroke-width="2.5"/>'
    )
    # setinhas nas pontas
    parts.append(
        f'<polygon points="{W-PAD_X+8},{y_axis} {W-PAD_X-2},{y_axis-6} '
        f'{W-PAD_X-2},{y_axis+6}" fill="#37474F"/>'
    )

    # ============== EVENTOS ==============
    # alternar cima/baixo pra evitar sobreposicao
    for i, ev in enumerate(eventos):
        x = PAD_X + col_w * (i + 0.5)
        acima = (i % 2 == 0)
        cor = COR_TIPO.get(ev.tipo, "#37474F")
        r_circ = 9 if ev.tipo == "achado" else 7
        # circulo no eixo
        parts.append(
            f'<circle cx="{x:.1f}" cy="{y_axis}" r="{r_circ}" fill="{cor}" '
            f'stroke="#FFFFFF" stroke-width="2.5"/>'
        )
        # data
        data_y = y_axis + 30
        parts.append(
            f'<text x="{x:.1f}" y="{data_y}" font-size="11" fill="#37474F" '
            f'text-anchor="middle" font-weight="bold">{escape_xml(ev.data)}</text>'
        )

        # caixa de texto
        if acima:
            box_y_top = y_axis - 180
            line_y_bottom = y_axis - 16
        else:
            box_y_top = y_axis + 50
            line_y_bottom = y_axis + 50

        # linha conectora
        parts.append(
            f'<line x1="{x:.1f}" y1="{y_axis + (-r_circ - 3 if acima else r_circ + 3)}" '
            f'x2="{x:.1f}" y2="{line_y_bottom if acima else line_y_bottom - 6}" '
            f'stroke="{cor}" stroke-width="1.5" stroke-dasharray="2,3"/>'
        )
        # rotulo principal (multi-linha simples via tspan)
        rotulo = ev.rotulo
        # quebra rotulo em 2 linhas se > 28 chars
        linhas_rot = []
        palavras = rotulo.split()
        atual = ""
        for p in palavras:
            if len(atual + " " + p) > 28 and atual:
                linhas_rot.append(atual)
                atual = p
            else:
                atual = (atual + " " + p).strip()
        if atual:
            linhas_rot.append(atual)
        if len(linhas_rot) > 3:
            linhas_rot = linhas_rot[:3]
            linhas_rot[-1] = linhas_rot[-1][:25] + "..."

        # detalhe (max 2 linhas)
        linhas_det = []
        if ev.detalhe:
            palavras = ev.detalhe.split()
            atual = ""
            for p in palavras:
                if len(atual + " " + p) > 32 and atual:
                    linhas_det.append(atual)
                    atual = p
                else:
                    atual = (atual + " " + p).strip()
            if atual:
                linhas_det.append(atual)
            if len(linhas_det) > 2:
                linhas_det = linhas_det[:2]
                linhas_det[-1] = linhas_det[-1][:30] + "..."

        # caixa
        box_h = 14 * (len(linhas_rot) + len(linhas_det)) + 12
        box_w = 230
        box_x = x - box_w / 2
        box_y = box_y_top if acima else y_axis + 56

        # ajustar box pra nao sair do svg
        if box_x < 4:
            box_x = 4
        if box_x + box_w > W - 4:
            box_x = W - 4 - box_w

        parts.append(
            f'<rect x="{box_x:.1f}" y="{box_y:.1f}" width="{box_w}" height="{box_h}" '
            f'fill="#FFFFFF" stroke="{cor}" stroke-width="1.8" rx="4"/>'
        )
        # texto do rotulo
        ty = box_y + 16
        for ln in linhas_rot:
            parts.append(
                f'<text x="{box_x + box_w/2:.1f}" y="{ty:.1f}" font-size="12" '
                f'font-weight="bold" fill="{cor}" text-anchor="middle">'
                f'{escape_xml(ln)}</text>'
            )
            ty += 14
        for ln in linhas_det:
            parts.append(
                f'<text x="{box_x + box_w/2:.1f}" y="{ty:.1f}" font-size="11" '
                f'fill="#37474F" text-anchor="middle">{escape_xml(ln)}</text>'
            )
            ty += 13

    # ============== CARIMBO + LEGENDA ==============
    y_carimbo = H_HEADER + H_TIMELINE + 10
    # caixa carimbo
    parts.append(
        f'<rect x="{PAD_X}" y="{y_carimbo}" width="{W - 2*PAD_X}" height="60" '
        f'fill="{tl.cor_tema}" rx="6"/>'
    )
    parts.append(
        f'<text x="{W/2}" y="{y_carimbo + 24}" font-size="13" fill="#FFFFFF" '
        f'opacity="0.85" text-anchor="middle">CARIMBO DA RECONSTRUCAO</text>'
    )
    # carimbo pode quebrar
    palavras = tl.carimbo.split()
    linhas_carimbo = []
    atual = ""
    for p in palavras:
        if len(atual + " " + p) > 110 and atual:
            linhas_carimbo.append(atual)
            atual = p
        else:
            atual = (atual + " " + p).strip()
    if atual:
        linhas_carimbo.append(atual)
    cy = y_carimbo + 44
    for ln in linhas_carimbo[:2]:
        parts.append(
            f'<text x="{W/2}" y="{cy}" font-size="14" font-weight="bold" '
            f'fill="#FFFFFF" text-anchor="middle">{escape_xml(ln)}</text>'
        )
        cy += 16

    # legenda
    y_leg = y_carimbo + 78
    leg_x = PAD_X
    parts.append(
        f'<text x="{leg_x}" y="{y_leg}" font-size="11" fill="#37474F" '
        f'font-weight="bold">Legenda:</text>'
    )
    leg_x += 65
    for tipo, label in LABEL_TIPO.items():
        cor = COR_TIPO[tipo]
        parts.append(
            f'<circle cx="{leg_x}" cy="{y_leg - 4}" r="5" fill="{cor}"/>'
        )
        parts.append(
            f'<text x="{leg_x + 10}" y="{y_leg}" font-size="11" fill="#37474F">'
            f'{label}</text>'
        )
        leg_x += 14 + 6 * len(label) + 16

    # rodape com fonte
    parts.append(
        f'<text x="{W - PAD_X}" y="{y_leg}" font-size="10" fill="#90A4AE" '
        f'text-anchor="end">reconstrucao via DF FNET + matera-ancora — '
        f'lyMartins/banco-master-osint</text>'
    )

    parts.append('</svg>')
    return "".join(parts)


def main():
    for tl, nome in [(SDG2, "timeline_sdg2.svg"),
                     (GOLD_STYLE, "timeline_goldstyle.svg"),
                     (SCARLET, "timeline_scarlet.svg")]:
        path = OUT / nome
        path.write_text(render(tl), encoding="utf-8")
        print(f"-> {path}  ({len(tl.eventos)} eventos)")


if __name__ == "__main__":
    main()
