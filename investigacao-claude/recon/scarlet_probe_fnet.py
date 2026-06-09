"""Probe FNET para o Scarlet FIDC NP (CNPJ 55.344.996/0001-44)."""
import requests

CNPJ = "55344996000144"   # Scarlet FIDC NP (Reag)
H = {"User-Agent": "Mozilla/5.0", "Accept": "application/json,*/*"}

URL = "https://fnet.bmfbovespa.com.br/fnet/publico/pesquisarGerenciadorDocumentosDados"
params = {
    "d": 0, "s": 0, "l": 200,
    "o[0][dataEntrega]": "desc",
    "cnpjFundo": CNPJ,
    "idCategoriaDocumento": 0,
    "idTipoDocumento": 0,
    "idEspecieDocumento": 0,
}

r = requests.get(URL, params=params, headers=H, timeout=60)
print("status", r.status_code, "| ct", r.headers.get("content-type"))
if r.status_code == 200 and "json" in (r.headers.get("content-type") or ""):
    j = r.json()
    print(f"recordsTotal: {j.get('recordsTotal')}\n")
    for d in j.get("data", []):
        print(f"  id={d.get('id')} | {d.get('dataEntrega')} | "
              f"{d.get('categoriaDocumento')} / {d.get('tipoDocumento')} / "
              f"{d.get('especieDocumento')}")
else:
    print(r.text[:500])
