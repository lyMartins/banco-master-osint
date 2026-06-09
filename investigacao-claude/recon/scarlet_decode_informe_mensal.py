"""Decodifica o informe mensal estruturado do Scarlet (XML base64).

O FNET às vezes entrega o XML do informe mensal codificado em base64 dentro
de aspas. Esse script normaliza, decodifica e mostra os campos relevantes.
"""
import base64
import re
from pathlib import Path

BIN = Path("data/fnet_docs/Scarlet_InformeMensal_2026-05_1185251.bin")
OUT_XML = BIN.with_suffix(".xml")

raw = BIN.read_bytes()
# remove aspas externas se houver
if raw.startswith(b'"'):
    raw = raw.strip(b'"')

try:
    xml_bytes = base64.b64decode(raw)
    OUT_XML.write_bytes(xml_bytes)
    print(f"-> XML decodificado em {OUT_XML} ({len(xml_bytes)} bytes)")
except Exception as e:
    print(f"erro decode: {e}")
    raise

xml = xml_bytes.decode("utf-8", errors="replace")

# campos relevantes do XML do informe mensal de FIDC
campos = [
    ("DT_COMPT", "Data competência"),
    ("NR_CNPJ_FUNDO", "CNPJ do fundo"),
    ("NR_CNPJ_ADM", "CNPJ administrador"),
    ("TP_CONDOMINIO", "Tipo condomínio"),
    ("FDO_EXCL", "Fundo exclusivo"),
    ("COTST_VINCUL", "Cotista vinculado"),
    ("VL_DISPONIB", "Valor disponível"),
    ("VL_CARTEIRA", "Valor carteira (total ativo)"),
    ("VL_SOM_VALORES_MOB", "Valores mobiliários"),
    ("VL_DEBT", "Debêntures"),
    ("VL_CRI", "CRI"),
    ("VL_CLS_COTA_FIF", "Cotas FIF"),
    ("VL_COTA_FIDC", "Cotas FIDC"),
    ("VL_SOM_PASSIV", "Passivo total"),
    ("VL_PATRIM_LIQ", "Patrimônio Líquido"),
    ("VL_PATRIM_LIQ_MEDIO", "PL médio"),
    ("VL_SOM_DICRED_AQUIS", "Direitos creditórios"),
    ("VL_ACAO_JUDIC", "Ações judiciais"),
    ("VL_SETOR_PUBLIC_PRECAT", "Precatórios setor público"),
    ("QT_TOTAL_COTISTAS", "Total cotistas"),
    ("QT_TOTAL_COTISTAS_SENIOR", "Cotistas seniores"),
    ("BNC_CMR", "Bancos comerciais (cotistas)"),
    ("FND_INV_CTS", "Fundo de investimento (cotistas)"),
    ("OTR_FND_INV", "Outros fundos investidores"),
    ("PR_APURADA", "Rentabilidade %"),
]
print("\n=== Informe Mensal Estruturado — Scarlet (abr/2026) ===")
for tag, label in campos:
    m = re.search(rf"<{tag}>([^<]*)</{tag}>", xml)
    if m:
        v = m.group(1)
        print(f"  {label:42}: {v}")
