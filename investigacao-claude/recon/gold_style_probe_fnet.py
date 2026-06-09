"""Probe: lista documentos do FIDC Gold Style no FNET.

Mesma técnica do probe_fnet.py do Luan, mas para CNPJ 34081900000122 (Gold Style FIDC NP).
Output: lista os documentos com id, data, tipo — pra escolher quais baixar.
"""
import json
import requests

CNPJ = "34081900000122"   # Gold Style FIDC NP (Reag)
H = {"User-Agent": "Mozilla/5.0", "Accept": "application/json,*/*"}

URL = "https://fnet.bmfbovespa.com.br/fnet/publico/pesquisarGerenciadorDocumentosDados"
params = {
    "d": 0, "s": 0, "l": 200,           # l=200 pra pegar tudo
    "o[0][dataEntrega]": "desc",
    "cnpjFundo": CNPJ,
    "idCategoriaDocumento": 0,
    "idTipoDocumento": 0,
    "idEspecieDocumento": 0,
}

try:
    r = requests.get(URL, params=params, headers=H, timeout=60)
    print("status", r.status_code, "| ct", r.headers.get("content-type"))
    if r.status_code == 200 and "json" in (r.headers.get("content-type") or ""):
        j = r.json()
        total = j.get("recordsTotal")
        print(f"recordsTotal: {total}\n")
        for d in j.get("data", []):
            print(f"  id={d.get('id')} | {d.get('dataEntrega')} | "
                  f"{d.get('categoriaDocumento')} / {d.get('tipoDocumento')} / "
                  f"{d.get('especieDocumento')} | {d.get('denominacaoSocial')}")
    else:
        print(r.text[:500])
except Exception as e:
    print("ERRO:", e)
