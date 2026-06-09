"""Baixa DFs e documentos críticos do Gold Style FIDC do FNET.

Mesmo handling do fnet_download.py do Luan (trata base64 quando FNET devolve).
Output em data/fnet_docs/ (gitignored).
"""
import base64, os
import requests

H = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
OUT = "data/fnet_docs"
os.makedirs(OUT, exist_ok=True)

# ids escolhidos do Gold Style FIDC (CNPJ 34081900000122)
DOCS = {
    "863753":  "GoldStyle_DemonstracoesFinanceiras_2024",       # DF anual exercício 2024
    "741894":  "GoldStyle_DemonstracoesFinanceiras_2023",       # DF anterior (exercício 2023)
    "816884":  "GoldStyle_FatoRelevante_2025-01-10",            # Fato relevante de jan/2025
    "864718":  "GoldStyle_Ata_AGO_2025-03-26",                  # AGO 2025
    "726645":  "GoldStyle_Ata_AGE_2024-08-27",                  # AGE ago/2024
    "659935":  "GoldStyle_Ata_AGE_2024-05-14",                  # AGE mai/2024
    "1199246": "GoldStyle_InformeTrimestral_2026-05-19",        # snapshot pós-liquidação
    "190302":  "GoldStyle_DemonstracoesFinanceiras_2020",       # DF antiga (origem do fundo)
}


def try_download(doc_id):
    for ep in ("downloadDocumento", "exibirDocumento"):
        url = f"https://fnet.bmfbovespa.com.br/fnet/publico/{ep}?id={doc_id}&cvm=true"
        try:
            r = requests.get(url, headers=H, timeout=120)
        except Exception as e:
            print(f"   {ep}: ERRO {e}"); continue
        ct = r.headers.get("content-type", "")
        print(f"   {ep}: {r.status_code} | {ct} | {len(r.content)} bytes")
        if r.status_code != 200 or not r.content:
            continue
        data = r.content
        # FNET pode devolver base64 do PDF como texto
        if b"%PDF" not in data[:1024]:
            try:
                dec = base64.b64decode(data, validate=False)
                if dec[:4] == b"%PDF":
                    data = dec
            except Exception:
                pass
        ext = "pdf" if data[:4] == b"%PDF" else ("html" if b"<html" in data[:2048].lower() else "bin")
        return data, ext
    return None, None


def main():
    for doc_id, name in DOCS.items():
        print(f"== id={doc_id} ({name}) ==")
        data, ext = try_download(doc_id)
        if data:
            path = f"{OUT}/{name}_{doc_id}.{ext}"
            with open(path, "wb") as f:
                f.write(data)
            print(f"   -> salvo {path} ({len(data)} bytes, tipo={ext})")
        print()


if __name__ == "__main__":
    main()
