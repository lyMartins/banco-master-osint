# Reconstrução do Gold Style FIDC NP a partir de dado público

> Segunda aplicação do método (depois do SDG II). Resposta executável à pergunta:
> **"o método funciona em outro fundo do escândalo Master?"** — Funciona, com um detalhe importante:
> revela o que a matéria não contou. A matéria do Imirante/g1 (18/03/2026) descreve **fluxo COAF**
> (R$ 1 bi de empresas do PCC). A DF auditada revela **outro mecanismo de fraude**: 18,17 milhões
> de ações de banco extinto (BESC) avaliadas por laudo HORBIA em R$ 13,78 bi e registradas no fundo a
> apenas 10% (R$ 1,36 bi). Auditor pediu **abstenção de opinião em dois exercícios consecutivos**.
> Tudo reproduzível com `investigacao-claude/recon/reconstruir_goldstyle.py`.

## Resultado — scorecard da matéria

| Afirmação da matéria | Citado | Reconstruído (fonte pública) | Status |
|---|---|---|---|
| Existência do FIDC Gold Style | — | CNPJ 34.081.900/0001-22 confirmado | ✅ |
| Administrador = Reag | — | Reag DTVM (34.829.992/0001-86 = CBSF ex-Reag Trust) até 02/09/2024, depois Reag Jus | ✅ exato |
| Ativos do fundo | ~R$ 2 bi | R$ 1,362 bi em 31/03/2022 (DF mais recente disponível); matéria refere data não especificada | ⚠️ compatível |
| R$ 1 bi de empresas do PCC | R$ 1 bi | **Não reconstruível via DF** — fluxo COAF de 2023-2025 está fora do escopo da DF de exercício 31/03/2022 | ❌ não reconstruível |
| Aster Petróleo cedeu | R$ 759,5 mi | Não aparece como cedente nem contraparte na DF | ❌ não reconstruível |
| BK Bank cedeu | R$ 158 mi | Não aparece na DF | ❌ não reconstruível |
| Inovanti cedeu | R$ 175 mi | Não aparece na DF | ❌ não reconstruível |
| Repasse para Super Empreendimentos | R$ 180 mi | Não aparece na DF; provável fluxo posterior a 31/03/2022 | ❌ não reconstruível |
| Reag liquidada pelo BC | janeiro/2026 | Confirmado: Informe Trimestral 1T2026 responde "dada a liquidação" em todos os 16 campos | ✅ exato |
| Reag investigada em Compliance Zero + Carbono Oculto | — | Consistente: mudança de admin para Reag Jus em 02/09/2024 — **uma semana antes** da 1ª fase da Carbono Oculto | ✅ confirmado |
| Vorcaro preso em 04/03/2026 | — | Fato público (fora do escopo da DF) | ✅ |

**6 de 11 afirmações confirmadas/compatíveis com DF auditada. 5 não reconstruíveis via DF** (fluxo COAF, não-balanço).

CSVs: `investigacao-claude/recon/output/goldstyle_scorecard_materia.csv` + `goldstyle_cronologia.csv` + `goldstyle_achados_proprios.csv`.

## Achados próprios — o que a DF revela além da matéria

A matéria do Imirante/g1 conta o **fluxo financeiro suspeito** (R$ 1 bi de empresas PCC entrando, R$ 180 mi saindo pra empresa do cunhado do Vorcaro). A DF auditada do FNET conta uma história **complementar e independente**: como o fundo foi construído para abrigar e revalorizar um ativo de origem questionável.

1. **Ativo subjacente são ações preferenciais do BESC** (Banco do Estado de Santa Catarina), banco extinto em 30/09/2008 com a incorporação pelo Banco do Brasil. O fundo detém 18.167.136 ações escriturais BESC.

2. **Cessor original: Excalibur FIM Crédito Privado**, em cessão datada de 11/03/2020. Cotista exclusivo do Gold Style.

3. **Laudo HORBIA de dezembro/2019** precifica o ativo em R$ 13.783.240 mil (R$ 758,69 por ação). A Administração registra a apenas **10% do laudo** (R$ 75,00/ação = R$ 1.362.535 mil). A escolha do desconto não é explicada na DF.

4. **Vendas parciais do ativo entre 2022 e 2024 a preços variando de R$ 75,00 a R$ 483,33 por ação** — variação de 6,4x no preço da mesma ação em janela curta, sem mercado organizado nem câmara de liquidação.

5. **Abstenção de opinião do auditor em DOIS exercícios consecutivos**:
   - DF 31/03/2021 (entregue 19/09/2024): auditor **PricewaterhouseCoopers**
   - DF 31/03/2022 (entregue 24/03/2025): auditor **Baker Tilly 4Partners**
   - Mesma justificativa em ambos: ausência de evidência sobre existência, titularidade, transferência e mensuração dos direitos creditórios.

6. **Atraso material na entrega das DFs**: a DF do exercício findo em 31/03/2022 só foi entregue ao FNET em 24/03/2025 — quase 3 anos depois do encerramento do exercício.

7. **Mudança estrutural de administrador em 02/09/2024**: a administração passa da **Reag DTVM** (CNPJ 34.829.992/0001-86, a mesma entidade que renomeada virou CBSF DTVM, e administradora também do SDG II) para a **Reag Jus Gestão de Ativos Judiciais Ltda.** (CNPJ 46.356.742/0001-55). Aconteceu **uma semana antes** da 1ª fase da Operação Carbono Oculto (setembro/2025). A Reag Jus é subsidiária do mesmo grupo Reag — então não é desinvestimento, é compartimentalização.

8. **Fato Relevante 10/01/2025** — entregue ao FNET pela própria Reag DTVM:
   > "Foi realizada uma REPRECIFICAÇÃO RELEVANTE NOS DIREITOS CREDITÓRIOS denominados 'Cártulas'. (…) tornou-se necessária devido à natureza do ativo, caracterizada por pouca liquidez no mercado secundário, além de ausência de atualizações consistentes nos últimos anos."

   Em linguagem regulatória, é a Reag admitindo por escrito que o ativo estava valorizado de forma inconsistente. O título do envelope DocuSign do documento (linha 59 do PDF) é literal: `20250110_GOLD STYLE_Fato_Relevante_BESC - OK.docx`.

9. **Trimestral 1T2026** (entregue 19/05/2026): das 16 perguntas obrigatórias do anexo II da Instrução CVM 175/2022 (lastro, originadores, garantias, cessão, alienação), TODAS são respondidas com a mesma frase: **"Dada a liquidação, não foi realizada no trimestre. O processo será retomado no próximo trimestre, já sob responsabilidade do novo administrador."** O fundo está paralisado.

## A mecânica de fraude reconstruída (o que os documentos mostram)

O Gold Style é um **FIDC-NP fechado com cotista exclusivo**. A linha do tempo, juntando DF + Fato Relevante + Trimestral:

- **2020-03-11** — Excalibur FIM CP cede 18,17 mi de ações BESC pro Gold Style por integralização de capital, sem movimentação financeira. Laudo HORBIA de dez/2019 precifica em R$ 13,78 bi.
- **2020-10-16** — AGC transfere a administração pra Reag DTVM. Registro contábil é fixado em R$ 1,36 bi (10% do laudo).
- **2021-03-31 e 2022-03-31** — PL congelado em R$ 1,362 bi nas duas DFs; auditor abstém-se de opinião nos dois exercícios.
- **2022-2024** — vendas parciais a preços entre R$ 75 e R$ 483 por ação. A 6,4x de variação no preço, sem mercado público, indica negociação entre partes não comprovadamente independentes.
- **2023 a 2025** — segundo COAF/PF, fluxo de R$ 1 bi entra no fundo via Aster Petróleo, BK Bank e Inovanti; R$ 180 mi saem para Super Empreendimentos (Fabiano Zettel, cunhado do Vorcaro, era diretor 2021-2024).
- **2024-09-02** — admin migra da Reag DTVM para Reag Jus (uma semana antes da 1ª fase da Carbono Oculto).
- **2025-01-10** — Reag emite Fato Relevante anunciando reprecificação relevante das Cártulas/BESC.
- **2026-01** — Reag DTVM (CBSF) liquidada extrajudicialmente pelo BC.
- **2026-05-19** — trimestral 1T2026 confirma o fundo paralisado.

**O "carimbo" da fraude na parte que o método alcança**: ABSTENÇÃO DE OPINIÃO em dois exercícios consecutivos, com dois auditores diferentes (PwC e Baker Tilly), sobre o mesmo ativo (ações BESC), com justificativa idêntica (sem evidência de existência, titularidade, transferência ou mensuração). Mais o atraso de 3 anos na entrega da DF. Mais a reprecificação assumida pela própria Reag em fato relevante.

## Diferenças honestas entre o caso Gold Style e o caso SDG II

O método (DF auditada via FNET + matéria-âncora) funciona em ambos, mas **rende coisas diferentes**:

| Dimensão | SDG II | Gold Style |
|---|---|---|
| Tipo de ativo subjacente | CCBs cedidas por empresas vivas (Lormont, Banvox, Super, Master) | Ações de banco extinto há 17 anos (BESC) |
| Mecanismo de inflação | Aceitação de CCBs de devedores duvidosos a valor de face | Laudo HORBIA inflando ações em 10.000x o valor original |
| % das afirmações reconstruíveis via DF | 10 de 11 (a 11ª — MKS cotista — é sigilo) | 6 de 11 (5 são fluxo COAF não-balanço) |
| Status do parecer | Abstenção 2024 | Abstenção 2021 + 2022 (dois exercícios) |
| Trocas de administrador | Reag → CBSF (rebranding) | Reag DTVM → Reag Jus (uma semana antes da Carbono Oculto) |
| Fluxo COAF aparece na DF? | Não (mas a DF capta as cessões nominais) | Não |
| Auditor independente | um (Pemom) | dois consecutivos (PwC, Baker Tilly), mesma conclusão |

A lição metodológica: **quando a matéria descreve cessões nominais, a DF cobre.** Quando a matéria descreve fluxo COAF (comunicação ao Coaf), a DF não cobre — mas a DF tipicamente abre outra porta (mecanismo de inflação, mudanças de gestão, fatos relevantes admissivos).

## Honestidade epistemológica

- O scorecard marca como **NÃO RECONSTRUÍVEL** as 5 afirmações sobre fluxo PCC. Isso não significa que sejam falsas — significa que **não saem de DF auditada via FNET**, que é a fonte do método. As fontes da matéria são relatórios bancários enviados ao Coaf e dossiês da CPI do Crime Organizado; nenhum desses é público.
- A matéria fala de **R$ 2 bi em ativos**; a DF mais recente disponível mostra R$ 1,362 bi em 31/03/2022. O delta pode ser crescimento real entre 2022 e 2025 — mas como o fundo não publicou DFs do exercício 2023, 2024 e 2025, não dá pra reconciliar a partir do balanço.
- O laudo HORBIA está citado nas duas DFs com a mesma origem (dezembro/2019), o que dá rastreabilidade. O valor R$ 13,78 bi é o que está no documento de auditoria, não uma estimativa nossa.
- O "cunhado do Vorcaro" (Fabiano Zettel) e o repasse de R$ 180 mi para a Super Empreendimentos saem direto da matéria do Imirante/g1, não da DF. Citamos como atribuído à matéria, não como reconstruído.

## Fontes arquivadas (verificáveis por hash)

`investigacao-claude/fontes/`:

- `Imirante_gold-style-pcc_2026-03-18.md` (+ `.sha256`) — matéria-âncora
- `CVM-FNET_GoldStyle_DF_ex2022_id863753.pdf` — DF auditada exercício 31/03/2022 (Baker Tilly)
- `CVM-FNET_GoldStyle_DF_ex2021_id741894.pdf` — DF auditada exercício 31/03/2021 (PwC)
- `CVM-FNET_GoldStyle_FatoRelevante_2025-01-10_id816884.pdf` — fato relevante da reprecificação
- `CVM-FNET_GoldStyle_InfTrimestral_1T2026_id1199246.pdf` — trimestral pós-liquidação
- `CVM-FNET_GoldStyle.sha256` — hashes dos 4 PDFs

## Como reproduzir

```powershell
# Windows PowerShell, ambiente .venv\ na raiz do repo
.venv\Scripts\activate

# Lista documentos do Gold Style no FNET (110 documentos)
python investigacao-claude/recon/gold_style_probe_fnet.py

# Baixa as 8 peças críticas (DFs, fato relevante, atas, trimestral)
python investigacao-claude/recon/gold_style_fnet_download.py

# Extrai texto de qualquer PDF baixado (procura alvos: ASTER, BK BANK, INOVANTI, SUPER, ZETTEL, REAG…)
python investigacao-claude/recon/gold_style_pdf_extract.py data/fnet_docs/GoldStyle_DemonstracoesFinanceiras_2024_863753.pdf

# Roda o scorecard e gera CSVs
python investigacao-claude/recon/reconstruir_goldstyle.py
```

Sem dependências extras além das já listadas no `environment.yml` (`requests`, `pdfplumber`).

## Próximos alvos pela mesma receita

Pela ordem de promessa:

- **Anna FIC-FIDC** (CNPJ 53.273.475/0001-18) — PL R$ 15,8 bi (5x maior que o SDG II). Cotista do próprio SDG II. Provável DF auditada disponível no FNET.
- **Lancia! FIDC** (CNPJ 29.786.909/0001-07) — pequeno (R$ 40 mi), mas tem pista do Luan (NGV SPE, R$ 30 mi em debêntures).
- **Hans 95** (CNPJ 32.088.041/0001-78) — FI Multimercado, não FIDC; ICL/Brasil247 dizem ter R$ 35 bi de PL. Como é FI, a receita muda: usa `fi-doc-inf_mensal` em vez de `fidc-doc-inf_mensal`.
- **Maranta** (CNPJ 42.584.801/0001-91) — FI Multimercado; matéria do Metrópoles aponta 97% da carteira em CCBs de Lormont (Tanure), R$ 73,7 mi. Reconstruir prova vínculo direto Tanure-Master.
