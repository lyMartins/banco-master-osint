"""Acha CNPJs de fundos do escândalo Master no informe mensal cacheado."""
import csv
import io
import sys
import zipfile
from pathlib import Path

csv.field_size_limit(min(sys.maxsize, 2**31 - 1))

CACHE = Path("coleta/data/cvm_fidc_mensal")
ALVOS = ["SCARLET", "CARNIVAL", "HANS", "MONTENEGRO", "ANNA",
         "ASTRALO", "MAIA", "OLAF", "FROZEN", "ELSA", "GOLDEN GREEN"]

vistos = {}

for zpath in sorted(CACHE.glob("*.zip")):
    with zipfile.ZipFile(zpath) as zf:
        for name in zf.namelist():
            if not name.endswith(".csv"):
                continue
            with zf.open(name) as f:
                txt = io.TextIOWrapper(f, encoding="latin-1", newline="")
                reader = csv.DictReader(txt, delimiter=";")
                if not reader.fieldnames:
                    continue
                campo_nome = next((c for c in reader.fieldnames
                                   if "DENOM" in c.upper() or "NOME" in c.upper()), None)
                campo_cnpj = next((c for c in reader.fieldnames
                                   if "CNPJ" in c.upper()), None)
                if not campo_nome or not campo_cnpj:
                    continue
                for row in reader:
                    nm = (row.get(campo_nome) or "").upper()
                    cnpj = row.get(campo_cnpj) or ""
                    for alvo in ALVOS:
                        if alvo in nm:
                            key = (alvo, cnpj)
                            if key not in vistos:
                                vistos[key] = (row.get(campo_nome), zpath.name)

# ordena: alvo primeiro, depois cnpj
for (alvo, cnpj), (nome, zip_) in sorted(vistos.items()):
    print(f"[{alvo:12}] {cnpj:20} | {nome[:80]:80}  ({zip_})")

print(f"\nTotal: {len(vistos)} ocorrências únicas")
