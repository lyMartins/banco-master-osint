"""Baixa peças críticas do Scarlet FIDC NP do FNET (CNPJ 55.344.996/0001-44)."""
import base64, os
import requests

H = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
OUT = "data/fnet_docs"
os.makedirs(OUT, exist_ok=True)

DOCS = {
    "865183":  "Scarlet_DemonstracoesFinanceiras_2024",       # DF anual exerc 31/12/2024
    "1199327": "Scarlet_InformeTrimestral_1T2026",            # snapshot pos-liquidacao
    "824327":  "Scarlet_Ata_AGE_2025-01-23",                  # AGE proxima da liquidacao
    "824330":  "Scarlet_Regulamento_2025-01-23",              # Regulamento p/s AGE 23/01
    "789348":  "Scarlet_Ata_AGE_2024-11-27",                  # AGE pre-liquidacao
    "789354":  "Scarlet_Regulamento_2024-11-27",              # Regulamento nov/2024
    "701083":  "Scarlet_Ata_AGE_2024-07-18",                  # AGE pos-constituicao
    "701089":  "Scarlet_Regulamento_2024-07-18",              # Regulamento jul/2024
    "691007":  "Scarlet_Ata_AGE_2024-07-02",                  # AGE de constituicao
    "1185251": "Scarlet_InformeMensal_2026-05",               # informe mensal mais recente
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
