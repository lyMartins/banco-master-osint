"""Extrai texto de PDFs do Gold Style e busca entidades/valores da matéria.

Adaptado do pdf_extract.py do Luan. Alvos específicos do Gold Style/PCC/Master.
"""
import re
import sys
import pdfplumber

ALVOS = [
    # PCC / Carbono Oculto
    "ASTER", "BK BANK", "BK PAGAMENTOS", "INOVANTI", "PCC",
    "CARBONO OCULTO", "LAVAGEM",
    # Master / Compliance Zero
    "MASTER", "VORCARO", "ZETTEL", "FABIANO", "DV HOLDING",
    "SUPER EMPREEND", "DANIEL", "COMPLIANCE ZERO",
    # Reag (administrador)
    "REAG", "CBSF", "TRUSTEE",
    # Lormont / Tanure (já mapeado pelo Luan, marcar conexão)
    "LORMONT", "TANURE",
    # Núcleo da matéria — afirmações quantitativas
    "DEBÊNTURE", "DEBENTURE", "CEDENTE", "COTISTA", "DIREITOS CRED",
    "CCB", "CRÉDITO BANCÁRIO",
    # Audit / parecer
    "AUDITOR", "ABSTENÇÃO", "RESSALVA", "LASTRO", "RECUPERABILIDADE",
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
        print("  (nenhum alvo encontrado — possível PDF escaneado/imagem)")


if __name__ == "__main__":
    main()
