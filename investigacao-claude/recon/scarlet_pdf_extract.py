"""Extrai texto de PDFs do Scarlet e busca entidades/valores da matéria."""
import sys
import pdfplumber

ALVOS = [
    # Master / Vorcaro
    "MASTER", "VORCARO", "DV HOLDING", "BANCO MASTER",
    # Reag
    "REAG", "CBSF", "TRUST",
    # Conectados
    "SDG", "HANS", "ANNA", "CARNIVAL", "MONTENEGRO",
    "GOLDEN GREEN", "ASTRALO", "MAIA",
    # Estrutura
    "DEBÊNTURE", "DEBENTURE", "CEDENTE", "COTISTA", "DIREITOS CRED",
    "CCB", "CRÉDITO BANCÁRIO", "INTEGRAL", "APORTE",
    # Audit
    "AUDITOR", "ABSTENÇÃO", "RESSALVA", "LASTRO", "OPINIÃO",
    # Outros
    "LIQUIDAÇÃO", "BACEN", "BANCO CENTRAL",
]


def extrair(path):
    full = []
    with pdfplumber.open(path) as pdf:
        for pg in pdf.pages:
            t = pg.extract_text() or ""
            full.append(t)
    return "\n".join(full)


def main():
    path = sys.argv[1]
    out_txt = path.rsplit(".", 1)[0] + ".txt"
    texto = extrair(path)
    with open(out_txt, "w", encoding="utf-8") as f:
        f.write(texto)
    print(f"[{path}] {len(texto)} chars de texto -> {out_txt}")
    linhas = texto.splitlines()
    print("\n=== linhas mencionando entidades/valores-alvo ===")
    seen = 0
    for i, ln in enumerate(linhas):
        up = ln.upper()
        if any(a in up for a in ALVOS):
            ctx = ln.strip()
            if ctx:
                print(f"  L{i:4}: {ctx[:200]}")
                seen += 1
        if seen > 150:
            print("  ... (truncado em 150 matches)")
            break
    if not seen:
        print("  (nenhum alvo encontrado)")


if __name__ == "__main__":
    main()
