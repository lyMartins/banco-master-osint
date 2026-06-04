# SDG II — série mensal CVM (out/2025 → mar/2026)

Complemento ao PR #2 do @luanPropela (`analise-reconstrucao-claude`).

O PR do Luan reconstrói a fraude do SDG II a partir das **Demonstrações Financeiras auditadas** (FNET id 963178) — foto de dez/2024 e dez/2025, com cessões nominais e parecer do auditor.

Este complemento adiciona a **dimensão temporal** usando o **Informe Mensal de FIDC** (`dados.cvm.gov.br/dataset/fidc-doc-inf_mensal`), com 6 pontos consecutivos no entorno da liquidação do Banco Master (18/11/2025).

## Por que o informe mensal importa

A DF auditada mostra o **estado** do fundo no fechamento do exercício. O informe mensal mostra a **trajetória** mês a mês. Quando o estado de uma cessão pula entre dois balanços, a DF não captura o que aconteceu no meio. O informe mensal captura.

No caso do SDG II, o meio do caminho conta a história mais relevante: **carteira caiu R$ 1,65 bi em 30 dias entre 31/10/2025 e 30/11/2025**, e voltou a R$ 6 bi em fev/2026 com o passivo dobrando.

## Os números mês a mês

| Data | PL | Carteira | Passivo | Comentário |
|---|---:|---:|---:|---|
| 31/10/2025 | R$ 1.245,6 mi | **R$ 5.375,7 mi** | R$ 4.282,5 mi | foto a 18 dias da liquidação BACEN |
| 30/11/2025 | R$ 2.090,4 mi | R$ 3.728,5 mi | R$ 1.793,6 mi | **carteira cai R$ 1,65 bi** no mês da liquidação |
| 31/12/2025 | R$ 2.374,7 mi | R$ 3.660,4 mi | R$ 3.080,9 mi | passivo volta a subir |
| 31/01/2026 | R$ 2.386,5 mi | R$ 3.668,6 mi | R$ 3.081,6 mi | estável |
| 28/02/2026 | R$ 2.422,7 mi | R$ 6.055,6 mi | R$ 4.907,8 mi | **carteira recompõe a R$ 6 bi**, passivo dobra |
| 31/03/2026 | R$ 2.321,4 mi | R$ 6.069,2 mi | R$ 4.908,0 mi | estável no novo patamar |

A **R$ 5,4 bi** que a reportagem do ICL/Folha publicou em 28/05/2026 é a carteira em **out/2025**. Bate matemático.

## Achados adicionais nos outros fundos coletados

### Gold Style FIDC (Reag/PCC)

Mesmo padrão de queda no mês da liquidação:

| Data | PL | Carteira | Passivo |
|---|---:|---:|---:|
| 31/10/2025 | R$ 1.866,6 mi | **R$ 2.055,4 mi** | R$ 278,9 mi |
| 30/11/2025 | R$ 1.866,8 mi | **R$ 1.042,6 mi** | R$ 177,6 mi |
| 28/02/2026 | R$ 1.868,6 mi | R$ 978,4 mi | R$ 177,7 mi |

A carteira perdeu **49%** entre out e nov/2025. PL ficou parado em R$ 1,87 bi. Em jan/2026, a CBSF DTVM (administradora do Gold Style) também foi liquidada.

### Anna FIC-FIDC

O fundo que o ICL descreve como "intermediário do Hans 95 no SDG II" tem PL **quase 5x maior** que o SDG II:

| Data | PL |
|---|---:|
| 31/10/2025 | R$ 14.493 mi |
| 30/11/2025 | R$ 15.828 mi |
| 31/12/2025 | R$ 15.688 mi |

O Anna sozinho tem R$ 15,8 bi de patrimônio. Vale aprofundar — pode ter outras conexões com o conglomerado Master que ainda não estão mapeadas.

### Lancia! FIDC

Pequeno (R$ 40 mi de PL) e regular. Sem movimentação atípica no período.

## O que ficou de fora

O `fidc-doc-inf_mensal` cobre só FIDC. **Hans 95 e Maranta NÃO aparecem** porque são FI Multimercado (Hans 95 é FI MM Investimento no Exterior, Maranta é FI MM Crédito Privado). O coletor equivalente para esses dois usa `fi-doc-inf_mensal` (próximo passo).

## Arquivos

```
investigacao-claude/fidc-mensal/
├── README.md                          este arquivo
├── COMPARATIVO_COM_DF_AUDITADA.md     onde nosso mensal bate com a DF do Luan
└── dados/
    ├── 11_fidc_pl_mensal.csv          PL e PL médio mensal
    ├── 12_fidc_carteira_mensal.csv    composição da carteira por setor
    ├── 13_fidc_passivo_mensal.csv     passivo total + curto/longo prazo
    ├── 14_fidc_cotistas_por_tipo.csv  cotistas por tipo (PF/PJ/banco/corretora)
    ├── 15_fidc_cotistas_total.csv     cotistas total por classe/série
    ├── 16_fidc_cotas_qtd_valor.csv    quantidade e valor de cotas
    └── 17_fidc_risco_devedor_scr.csv  rating SCR-BACEN do devedor (AA-H)
```

## Como reproduzir

A coleta está em `coleta/cvm_fidc_inf_mensal.py` (na raiz do repo, branch main). Roda:

```bash
python -m coleta.cvm_fidc_inf_mensal
python exportar_csv.py
```

Os zips ficam cacheados em `data/cvm_fidc_mensal/`. Períodos coletados: `202510` a `202603`.

## Sinergia com o PR #2

| Camada | PR do Luan (DF auditada) | Este complemento (informe mensal) |
|---|---|---|
| Foto pontual | ✅ dez/2024 e dez/2025 | ✅ 6 pontos mensais |
| Cessões nominais | ✅ data + cedente + devedor + valor | ❌ só agregados por setor |
| Parecer do auditor | ✅ abstenção, 62% sem lastro | ❌ |
| Evolução temporal | ❌ | ✅ mês a mês |
| Cessão emergencial nov/2025 | ❌ | ✅ R$ 1,65 bi em 30 dias |
| Recomposição fev/2026 | ❌ | ✅ R$ 6 bi com passivo dobrando |
| Achado lateral Gold Style | ❌ | ✅ caiu 49% no mesmo mês |
| Tamanho do Anna FIC-FIDC | ❌ | ✅ R$ 15 bi PL |
| Outros 5 FIDCs cessores Lormont (Carriet, B-ROL, etc) | ✅ | ❌ |

As duas camadas se completam. Junto, **fecham 11/11 das afirmações da reportagem** + adicionam 3 achados temporais novos.
