import io
import sqlite3
import zipfile
from pathlib import Path

import pandas as pd
import requests

DB = Path("data/master.db")
CACHE = Path("data/cvm_fidc_mensal")
URL_TEMPLATE = "https://dados.cvm.gov.br/dados/FIDC/DOC/INF_MENSAL/DADOS/inf_mensal_fidc_{ym}.zip"
TIMEOUT = 180

PERIODOS = ["202510", "202511", "202512", "202601", "202602", "202603"]

FUNDOS_ALVO = {
    "46909301000133": "SDG II FIDC NP",
    "53273475000118": "Anna FIDC NP",
    "29786909000107": "Lancia! FIDC",
    "34081900000122": "Gold Style FIDC NP",
    "32088041000178": "Hans 95 (FI MM)",
    "42584801000191": "Maranta (FI MM)",
}

SCHEMA = """
CREATE TABLE IF NOT EXISTS fidc_carteira (
    fundo_cnpj       TEXT,
    fundo_nome       TEXT,
    data             TEXT,
    vl_carteira      REAL,
    vl_industrial    REAL,
    vl_imobiliario   REAL,
    vl_comercial     REAL,
    vl_servicos      REAL,
    vl_agronegocio   REAL,
    vl_financeiro    REAL,
    vl_credito       REAL,
    vl_factoring     REAL,
    vl_setor_publico REAL,
    vl_judicial      REAL,
    PRIMARY KEY (fundo_cnpj, data)
);

CREATE TABLE IF NOT EXISTS fidc_pl (
    fundo_cnpj   TEXT,
    fundo_nome   TEXT,
    data         TEXT,
    vl_pl        REAL,
    vl_pl_medio  REAL,
    PRIMARY KEY (fundo_cnpj, data)
);

CREATE TABLE IF NOT EXISTS fidc_passivo (
    fundo_cnpj    TEXT,
    fundo_nome    TEXT,
    data          TEXT,
    vl_passivo    REAL,
    vl_a_pagar    REAL,
    vl_curto_prazo REAL,
    vl_longo_prazo REAL,
    PRIMARY KEY (fundo_cnpj, data)
);

CREATE TABLE IF NOT EXISTS fidc_cotistas_tipo (
    fundo_cnpj                      TEXT,
    fundo_nome                      TEXT,
    data                            TEXT,
    nr_cotst_senior_pf              INTEGER,
    nr_cotst_senior_pj_nao_financ   INTEGER,
    nr_cotst_senior_banco           INTEGER,
    nr_cotst_senior_corretora       INTEGER,
    nr_cotst_subord_pf              INTEGER,
    nr_cotst_subord_pj_nao_financ   INTEGER,
    nr_cotst_subord_banco           INTEGER,
    PRIMARY KEY (fundo_cnpj, data)
);

CREATE TABLE IF NOT EXISTS fidc_cotistas_total (
    fundo_cnpj   TEXT,
    fundo_nome   TEXT,
    data         TEXT,
    classe_serie TEXT,
    nr_cotst     INTEGER,
    PRIMARY KEY (fundo_cnpj, data, classe_serie)
);

CREATE TABLE IF NOT EXISTS fidc_cotas (
    fundo_cnpj   TEXT,
    fundo_nome   TEXT,
    data         TEXT,
    classe_serie TEXT,
    qt_cota      REAL,
    vl_cota      REAL,
    PRIMARY KEY (fundo_cnpj, data, classe_serie)
);

CREATE TABLE IF NOT EXISTS fidc_risco_devedor (
    fundo_cnpj                  TEXT,
    fundo_nome                  TEXT,
    data                        TEXT,
    vl_risco_aa                 REAL,
    vl_risco_a                  REAL,
    vl_risco_b                  REAL,
    vl_risco_c                  REAL,
    vl_risco_d                  REAL,
    vl_risco_e                  REAL,
    vl_risco_f                  REAL,
    vl_risco_g                  REAL,
    vl_risco_h                  REAL,
    PRIMARY KEY (fundo_cnpj, data)
);
"""


def baixar_zip(ym: str) -> bytes | None:
    cache = CACHE / f"inf_mensal_fidc_{ym}.zip"
    if cache.exists():
        return cache.read_bytes()
    url = URL_TEMPLATE.format(ym=ym)
    print(f"[FIDC-MENSAL] baixando {url}")
    try:
        r = requests.get(url, timeout=TIMEOUT)
        if r.status_code != 200:
            print(f"[FIDC-MENSAL] HTTP {r.status_code} para {ym}")
            return None
        cache.parent.mkdir(parents=True, exist_ok=True)
        cache.write_bytes(r.content)
        return r.content
    except requests.RequestException as e:
        print(f"[FIDC-MENSAL] erro {ym}: {e}")
        return None


def to_num(val):
    if val is None or (isinstance(val, float) and pd.isna(val)) or val == "":
        return None
    try:
        return float(str(val).replace(",", "."))
    except (TypeError, ValueError):
        return None


def norm_cnpj(val):
    return "".join(filter(str.isdigit, str(val or "")))


def processar_zip(zip_bytes: bytes, ym: str, con: sqlite3.Connection) -> dict:
    inseridos = {"carteira": 0, "pl": 0, "passivo": 0, "cotistas_tipo": 0, "cotistas_total": 0, "cotas": 0, "risco": 0}

    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf:
        nomes = {n.split("/")[-1]: n for n in zf.namelist() if n.endswith(".csv")}

        def carregar(arquivo_chave):
            path = nomes.get(arquivo_chave) or next((v for k, v in nomes.items() if arquivo_chave in k), None)
            if not path:
                return pd.DataFrame()
            with zf.open(path) as f:
                df = pd.read_csv(f, sep=";", encoding="latin-1", dtype=str, on_bad_lines="skip")
            col_cnpj = next((c for c in df.columns if "CNPJ" in c.upper()), None)
            if not col_cnpj:
                return pd.DataFrame()
            df["_norm"] = df[col_cnpj].astype(str).str.replace(r"\D", "", regex=True)
            return df[df["_norm"].isin(FUNDOS_ALVO.keys())].copy()

        # Tab II - carteira
        df = carregar(f"inf_mensal_fidc_tab_II_{ym}.csv")
        for _, r in df.iterrows():
            con.execute("INSERT OR REPLACE INTO fidc_carteira VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (r["_norm"], r.get("DENOM_SOCIAL"), r.get("DT_COMPTC"),
                 to_num(r.get("TAB_II_VL_CARTEIRA")),
                 to_num(r.get("TAB_II_A_VL_INDUST")),
                 to_num(r.get("TAB_II_B_VL_IMOBIL")),
                 to_num(r.get("TAB_II_C_VL_COMERC")),
                 to_num(r.get("TAB_II_D_VL_SERV")),
                 to_num(r.get("TAB_II_E_VL_AGRONEG")),
                 to_num(r.get("TAB_II_F_VL_FINANC")),
                 to_num(r.get("TAB_II_G_VL_CREDITO")),
                 to_num(r.get("TAB_II_H_VL_FACTOR")),
                 to_num(r.get("TAB_II_I_VL_SETOR_PUBLICO")),
                 to_num(r.get("TAB_II_J_VL_JUDICIAL")),
                ))
            inseridos["carteira"] += 1

        # Tab III - passivo
        df = carregar(f"inf_mensal_fidc_tab_III_{ym}.csv")
        for _, r in df.iterrows():
            con.execute("INSERT OR REPLACE INTO fidc_passivo VALUES (?,?,?,?,?,?,?)",
                (r["_norm"], r.get("DENOM_SOCIAL"), r.get("DT_COMPTC"),
                 to_num(r.get("TAB_III_VL_PASSIVO")),
                 to_num(r.get("TAB_III_A_VL_PAGAR")),
                 to_num(r.get("TAB_III_A1_VL_CPRAZO")),
                 to_num(r.get("TAB_III_A2_VL_LPRAZO")),
                ))
            inseridos["passivo"] += 1

        # Tab IV - PL
        df = carregar(f"inf_mensal_fidc_tab_IV_{ym}.csv")
        for _, r in df.iterrows():
            con.execute("INSERT OR REPLACE INTO fidc_pl VALUES (?,?,?,?,?)",
                (r["_norm"], r.get("DENOM_SOCIAL"), r.get("DT_COMPTC"),
                 to_num(r.get("TAB_IV_A_VL_PL")),
                 to_num(r.get("TAB_IV_B_VL_PL_MEDIO")),
                ))
            inseridos["pl"] += 1

        # Tab X_1_1 - cotistas por tipo
        df = carregar(f"inf_mensal_fidc_tab_X_1_1_{ym}.csv")
        for _, r in df.iterrows():
            con.execute("INSERT OR REPLACE INTO fidc_cotistas_tipo VALUES (?,?,?,?,?,?,?,?,?,?)",
                (r["_norm"], r.get("DENOM_SOCIAL"), r.get("DT_COMPTC"),
                 int(to_num(r.get("TAB_X_NR_COTST_SENIOR_PF")) or 0),
                 int(to_num(r.get("TAB_X_NR_COTST_SENIOR_PJ_NAO_FINANC")) or 0),
                 int(to_num(r.get("TAB_X_NR_COTST_SENIOR_BANCO")) or 0),
                 int(to_num(r.get("TAB_X_NR_COTST_SENIOR_CORRETORA_DISTRIB")) or 0),
                 int(to_num(r.get("TAB_X_NR_COTST_SUBORD_PF")) or 0),
                 int(to_num(r.get("TAB_X_NR_COTST_SUBORD_PJ_NAO_FINANC")) or 0),
                 int(to_num(r.get("TAB_X_NR_COTST_SUBORD_BANCO")) or 0),
                ))
            inseridos["cotistas_tipo"] += 1

        # Tab X_1 - cotistas total
        df = carregar(f"inf_mensal_fidc_tab_X_1_{ym}.csv")
        for _, r in df.iterrows():
            con.execute("INSERT OR REPLACE INTO fidc_cotistas_total VALUES (?,?,?,?,?)",
                (r["_norm"], r.get("DENOM_SOCIAL"), r.get("DT_COMPTC"),
                 str(r.get("TAB_X_CLASSE_SERIE") or "")[:50],
                 int(to_num(r.get("TAB_X_NR_COTST")) or 0),
                ))
            inseridos["cotistas_total"] += 1

        # Tab X_2 - cotas
        df = carregar(f"inf_mensal_fidc_tab_X_2_{ym}.csv")
        for _, r in df.iterrows():
            con.execute("INSERT OR REPLACE INTO fidc_cotas VALUES (?,?,?,?,?,?)",
                (r["_norm"], r.get("DENOM_SOCIAL"), r.get("DT_COMPTC"),
                 str(r.get("TAB_X_CLASSE_SERIE") or "")[:50],
                 to_num(r.get("TAB_X_QT_COTA")),
                 to_num(r.get("TAB_X_VL_COTA")),
                ))
            inseridos["cotas"] += 1

        # Tab X - rating risco devedor
        df = carregar(f"inf_mensal_fidc_tab_X_{ym}.csv")
        for _, r in df.iterrows():
            con.execute("INSERT OR REPLACE INTO fidc_risco_devedor VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                (r["_norm"], r.get("DENOM_SOCIAL"), r.get("DT_COMPTC"),
                 to_num(r.get("TAB_X_SCR_RISCO_DEVEDOR_AA")),
                 to_num(r.get("TAB_X_SCR_RISCO_DEVEDOR_A")),
                 to_num(r.get("TAB_X_SCR_RISCO_DEVEDOR_B")),
                 to_num(r.get("TAB_X_SCR_RISCO_DEVEDOR_C")),
                 to_num(r.get("TAB_X_SCR_RISCO_DEVEDOR_D")),
                 to_num(r.get("TAB_X_SCR_RISCO_DEVEDOR_E")),
                 to_num(r.get("TAB_X_SCR_RISCO_DEVEDOR_F")),
                 to_num(r.get("TAB_X_SCR_RISCO_DEVEDOR_G")),
                 to_num(r.get("TAB_X_SCR_RISCO_DEVEDOR_H")),
                ))
            inseridos["risco"] += 1

    return inseridos


def resumo(con: sqlite3.Connection):
    print("\n[FIDC-MENSAL] === EVOLUCAO PL/CARTEIRA/PASSIVO POR FUNDO ===\n")
    rows = con.execute("""
        SELECT pl.data, pl.fundo_cnpj, pl.fundo_nome,
               pl.vl_pl, c.vl_carteira, pa.vl_passivo
        FROM fidc_pl pl
        LEFT JOIN fidc_carteira c ON c.fundo_cnpj = pl.fundo_cnpj AND c.data = pl.data
        LEFT JOIN fidc_passivo pa ON pa.fundo_cnpj = pl.fundo_cnpj AND pa.data = pl.data
        ORDER BY pl.fundo_cnpj, pl.data
    """).fetchall()
    for r in rows:
        nome_curto = (r[2] or "")[:35]
        pl = f"R$ {r[3]/1e6:>9.1f} mi" if r[3] else "          ?"
        cart = f"R$ {r[4]/1e6:>9.1f} mi" if r[4] else "          ?"
        pas = f"R$ {r[5]/1e6:>9.1f} mi" if r[5] else "          ?"
        print(f"  {r[0]}  {r[1]}  {nome_curto:35}  PL={pl}  carteira={cart}  passivo={pas}")

    print("\n[FIDC-MENSAL] === COTISTAS POR TIPO (mar/2026) ===\n")
    for r in con.execute("""
        SELECT data, fundo_nome, nr_cotst_senior_pf, nr_cotst_senior_pj_nao_financ,
               nr_cotst_senior_banco, nr_cotst_subord_pf, nr_cotst_subord_pj_nao_financ
        FROM fidc_cotistas_tipo
        WHERE data = (SELECT MAX(data) FROM fidc_cotistas_tipo)
        ORDER BY fundo_cnpj
    """):
        print(f"  {r[1][:30]:30}  PF_senior={r[2]:>3}  PJ_senior={r[3]:>3}  banco_senior={r[4]:>3}  PF_sub={r[5]:>3}  PJ_sub={r[6]:>3}")


def main():
    CACHE.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB)
    con.executescript(SCHEMA)
    for tabela in ["fidc_carteira","fidc_pl","fidc_passivo","fidc_cotistas_tipo","fidc_cotistas_total","fidc_cotas","fidc_risco_devedor"]:
        con.execute(f"DELETE FROM {tabela}")
    con.commit()

    for ym in PERIODOS:
        zip_bytes = baixar_zip(ym)
        if not zip_bytes:
            continue
        ins = processar_zip(zip_bytes, ym, con)
        con.commit()
        print(f"[FIDC-MENSAL] {ym}: " + ", ".join(f"{k}={v}" for k, v in ins.items()))

    resumo(con)
    con.close()


if __name__ == "__main__":
    main()
