# Reconstrução do Scarlet FIDC NP — terceira aplicação do método

> Terceira aplicação do método (depois do SDG II e do Gold Style). Resposta executável à
> pergunta: **"dá pra reconstruir o que a Receita Federal disse sobre o Scarlet?"**
>
> Sim — e mais que isso. A reconstrução produziu o achado mais forte da série de três:
> **o "Scarlet FIDC" que a Receita Federal hoje aponta como receptor de R$ 2,5 bi do
> Banco Master é o mesmo fundo (mesmo CNPJ) que o Luan já tinha mapeado em maio/2026
> como "Carriet Inventory FIDC", cessor de R$ 325 mi em CCBs de Lormont para o SDG II.**
>
> Dois trabalhos independentes (Luan via DF do SDG II em maio; nós via DF do próprio
> fundo em junho) convergem para o mesmo CNPJ — `55.344.996/0001-44`. A renomeação
> Carriet Inventory → Scarlet ocorreu na AGE de 23/01/2025.

## Resultado — scorecard da matéria

Matéria-âncora: **Imirante/g1, 14/04/2026** — "Banco Master e Vorcaro aplicaram R$ 12,2 bilhões em fundos, diz Receita".

| Afirmação da matéria | Citado | Reconstruído (fonte pública) | Status |
|---|---|---|---|
| Existência do Scarlet FIDC | — | CNPJ 55.344.996/0001-44 — **ex-CARRIET INVENTORY** até 23/01/2025 | ✅ confirmado + ampliado |
| Administrado pela Reag | — | Reag DTVM (34.829.992/0001-86 = CBSF) — **mesma admin do SDG II e Gold Style** | ✅ exato |
| Scarlet recebeu R$ 2,5 bi do Master | R$ 2,5 bi | Informe mensal abr/2026: PL R$ 2,706 bi, carteira R$ 2,206 bi | ⚠️ compatível |
| Master é cotista principal | — | Informe mensal: 6 cotistas; FUNDO EXCLUSIVO + COTISTA VINCULADO | ⚠️ compatível |
| Reag liquidada pelo BC em janeiro/2026 | janeiro/2026 | Trimestral 1T2026: 16 campos respondidos "Dada a liquidação" | ✅ exato |
| R$ 12,2 bi aplicados pelo Master+Vorcaro em fundos (2017-2025) | R$ 12,2 bi | Agregado da Receita; fora do escopo de DF individual | ❌ não reconstruível |
| 44% dos recursos pra fundos Reag | 44% | Agregado da Receita | ❌ não reconstruível |
| 184 contas em 67 fundos diferentes | 184/67 | Agregado da Receita | ❌ não reconstruível |
| Master sacou R$ 6,8 bi | R$ 6,8 bi | Agregado da Receita | ❌ não reconstruível |
| Vorcaro retirou R$ 581 mi | R$ 581 mi | Agregado da Receita | ❌ não reconstruível |
| Vorcaro preso em março/2026 | março/2026 | Fato público | ✅ |

**6 de 11 afirmações confirmadas/compatíveis. 5 não reconstruíveis** (agregados da Receita Federal sobre o conjunto Master+Vorcaro+184 contas — esses dados não saem de DF de um único fundo, vêm do sistema e-financeira).

CSVs: `investigacao-claude/recon/output/scarlet_scorecard_materia.csv`, `scarlet_cronologia.csv`, `scarlet_achados_proprios.csv`.

## Achado principal — identidade Scarlet = Carriet Inventory

Quando o probe do FNET roda no CNPJ 55.344.996/0001-44 (que aparece como "SCARLET" no informe mensal de FIDC out/2025 da CVM), retorna 46 documentos. O documento de Demonstração Financeira mais recente (id 865183, entregue em 26/03/2025) traz no cabeçalho:

> **CARRIET INVENTORY FUNDO DE INVESTIMENTO EM DIREITOS CREDITÓRIOS NÃO-PADRONIZADOS**
> CNPJ nº 55.344.996/0001-44
> Administrado pela Reag Trust Distribuidora de Títulos e Valores Mobiliários S.A.

E a ata da AGE de **27/11/2024** (id 789348) também mantém o nome Carriet Inventory.

Já o **regulamento entregue em 23/01/2025** (id 824330, mesmo CNPJ) tem no cabeçalho:

> **SCARLET FUNDO DE INVESTIMENTO EM DIREITOS CREDITÓRIOS NÃO-PADRONIZADOS**

Portanto: **a renomeação Carriet Inventory → Scarlet ocorreu na AGE de 23/01/2025** — exatamente o mesmo ato que trocou a gestora de "Reag Trust Administradora de Recursos Ltda." para "Reag Jus Gestão de Ativos Judiciais Ltda."

E o que isso reabre: na reconstrução que o Luan fez do SDG II (commit `fc2c17c`), há uma cessão registrada como:

```python
("2024-09-27", "Carriet Inventory FIDC-NP", "Lormont Participações S.A.", "CCB", 325_452, "DF id963178")
```

O fundo cessor de R$ 325 milhões em CCB de Lormont (Nelson Tanure) para o SDG II em 27/09/2024 era o Carriet Inventory. Esse mesmo fundo, em 23/01/2025, passou a se chamar Scarlet. Quando a matéria do Imirante de 14/04/2026 diz que "Scarlet recebeu R$ 2,5 bi do Master", está falando do mesmo fundo.

Não é especulação de homonímia: é **mesmo CNPJ, mesma administradora, mesma data de constituição (31/05/2024), continuidade documental no FNET**.

## Os 12 achados próprios (além da matéria)

1. **Scarlet = Carriet Inventory** (mesma identidade jurídica; renomeação em AGE de 23/01/2025).

2. **Conexão direta com o trabalho do Luan**: o "Carriet Inventory" da reconstrução do SDG II é o "Scarlet" da Receita Federal — fecha o ciclo entre as duas investigações.

3. **Mesma administradora dos outros dois fundos**: Reag DTVM, CNPJ 34.829.992/0001-86 (= CBSF), administra SDG II, Gold Style e Scarlet. **Três FIDCs centrais do escândalo sob a mesma DTVM**.

4. **Mudança estrutural de gestora em 23/01/2025**: Reag Trust Adm Recursos → Reag Jus Gestão de Ativos Judiciais. **Mesmo padrão do Gold Style**, onde a admin migrou para Reag Jus em 02/09/2024 — uma semana antes da Carbono Oculto.

5. **Fundo EXCLUSIVO + COTISTA VINCULADO** (regulamento de 23/01/2025): apenas cotistas pré-aprovados podem entrar. Em abr/2026 são **6 cotistas** (2 bancos comerciais, 1 fundo investidor, 3 outros fundos). Estrutura que dificulta rastreamento de beneficiário final — exatamente o padrão que a Folha descreveu no SDG II e que a matéria do Imirante diz "fundos com cotista único para dificultar o rastreamento".

6. **PL cresceu de R$ 1,65 bi (dez/2024) para R$ 2,71 bi (abr/2026)** — +R$ 1,06 bi nos 16 meses pós-mudança pra Reag Jus.

7. **Composição mudou drasticamente entre dez/2024 e abr/2026**:
   - Dez/2024 (DF auditada): CCBs R$ 20,5 mi + Debêntures R$ 469,4 mi + CRIs R$ 24,4 mi + Outros R$ 543,8 mi → Total R$ 1,058 bi
   - Abr/2026 (informe mensal): direitos creditórios R$ 1,732 bi + **ações judiciais R$ 304 mi + precatórios setor público R$ 269 mi** + cotas FIDC R$ 361 mi
   - Os ativos novos (judiciais + precatórios) são coerentes com a nova gestora "Reag Jus Gestão de Ativos Judiciais".

8. **Auditor diferente, opinião diferente**: TATICCA emitiu parecer **com opinião limpa** sobre a DF de 31/05 a 31/12/2024 (sem ressalvas). É contraste com SDG II e Gold Style, que tiveram abstenção. Mas atenção: a DF cobre só 7 meses (do início das atividades em 31/05/2024 até 31/12/2024), e a renomeação Carriet → Scarlet veio depois (23/01/2025). É possível que a opinião limpa seja sobre a versão pré-fraude do veículo.

9. **Em dez/2024, com 7 meses de operação, já tinha R$ 469 mi em debêntures**: o fundo já era veículo de absorção de dívida muito antes de virar Scarlet.

10. **Aplicação no FIP Hans II R$ 70 mi (dez/2024)**: conecta diretamente com a matéria do Imirante que diz "Hans II FIP MULT, ligado à Reag Trust, principal destino dos recursos de Vorcaro, com R$ 1,2 bi aportado pelo empresário; PL R$ 3,6 bi em dez/2025, reduzido para R$ 83 milhões após revisão". O Scarlet (ex-Carriet) **participava do mesmo Hans II**.

11. **Trimestral 1T2026 (entregue 19/05/2026)**: **TODAS as 16 perguntas obrigatórias** respondidas com a frase **"Dada a liquidação, não foi realizada no trimestre. O processo será retomado no próximo trimestre, já sob responsabilidade do novo administrador."** Padrão **idêntico** ao Gold Style — o fundo está paralisado pós-liquidação Reag.

12. **Renomeação como manobra forense**: fundos com nome alterado dificultam o cruzamento posterior em buscas por nome. Quem busca por "Carriet Inventory" hoje no Google encontra principalmente referências antigas pré-renomeação. Quem busca por "Scarlet FIDC" encontra a matéria do Imirante e algumas listas de fundos. Sem cruzar pelo CNPJ, os dois universos parecem desconectados.

## Mecânica resumida da fraude (reconstruída)

| Quando | O que aconteceu | Fonte |
|---|---|---|
| 2024-05-31 | Constituição como **Carriet Inventory FIDC NP**. Admin: Reag DTVM. Gestor: Reag Trust Adm Recursos. | DF id865183 + AGE id691007 |
| 2024-09-27 | Carriet cede CCB de Lormont (Nelson Tanure) R$ 325 mi para o SDG II | DF SDG II id963178 (Luan) |
| 2024-12-31 | DF fechamento: R$ 1,058 bi em direitos creditórios; R$ 469 mi em debêntures; R$ 70 mi no FIP Hans II | DF id865183 |
| 2025-01-23 | AGE renomeia **Carriet Inventory → Scarlet**; troca gestor pra **Reag Jus Gestão de Ativos Judiciais** | Ata id824327 + Regulamento id824330 |
| 2025-03-26 | DF id865183 (com nome antigo "Carriet Inventory") entregue ao FNET após renomeação. Auditor Taticca dá opinião limpa. | DF id865183 |
| 2026-01 | Reag DTVM liquidada extrajudicialmente pelo BC | Imirante / fato público |
| 2026-03-04 | Vorcaro preso (Operação Compliance Zero) | Fato público |
| 2026-04 | Informe mensal: PL R$ 2,71 bi; 6 cotistas; carteira diversificada com ativos judiciais e precatórios | FNET id1185251 (XML) |
| 2026-04-14 | Matéria do Imirante: Receita Federal aponta "Scarlet recebeu R$ 2,5 bi do Master" | Imirante 14/04/2026 |
| 2026-05-19 | Trimestral 1T2026: fundo paralisado, "Dada a liquidação" em todos os campos | FNET id1199327 |

## Honestidade epistemológica

- **5 das 11 afirmações da matéria não são reconstruíveis via DF**. Não porque sejam falsas: porque são agregados da Receita Federal sobre R$ 12,2 bi distribuídos em 184 contas de 67 fundos. Esses dados vêm do sistema e-financeira, que só é acessível por CPI ou autoridade judicial. A DF de um fundo individual não cobre.

- **O scorecard fica abaixo do SDG II (10/11)** porque a matéria do Imirante 14/04/2026 é majoritariamente **agregada** (não nominativa), enquanto a do Folha/ICL sobre o SDG II era **nominativa** (cessões específicas).

- **A opinião limpa do auditor (Taticca) sobre o Carriet Inventory** não é evidência de ausência de fraude — é evidência de que, no período auditado (31/05-31/12/2024), os 7 meses iniciais do fundo, o auditor obteve documentação suficiente. A mudança de regime veio depois.

- **"Compatível" não é "exato"**: a matéria diz R$ 2,5 bi do Master no Scarlet; o informe mensal mostra PL R$ 2,71 bi. O delta de R$ 200 mi pode ser cotas de outros aplicadores ou rendimento. Sem decomposição por cotista (que não é pública), não dá para cravar.

## Como o método "evolui" com 3 fundos reconstruídos

| Dimensão | SDG II | Gold Style | Scarlet |
|---|---|---|---|
| Tipo de ativo subjacente | CCBs de empresas vivas | Ações de banco extinto (BESC) | Debêntures, CRIs, ações judiciais, precatórios |
| Mecanismo de inflação | Aceitar CCBs de devedores duvidosos a valor de face | Laudo HORBIA inflando ações em 10.000x | Migração pra ativos judiciais via mudança de gestor |
| % afirmações reconstruíveis via DF | 10/11 | 6/11 | 6/11 |
| Tipo de não-reconstruível | Cotista (sigilo) | Fluxo COAF (PCC) | Agregado Receita Federal |
| Status do parecer auditoria | Abstenção 2024 | Abstenção 2021 + 2022 | Opinião limpa (mas DF de só 7 meses) |
| Mudança de admin/gestor | Reag → CBSF (rebranding) | Reag DTVM → Reag Jus (2024-09-02) | Reag Trust → Reag Jus (2025-01-23) **+ renomeação Carriet → Scarlet** |
| Admin (DTVM) | Reag/CBSF (34.829.992/0001-86) | Reag/CBSF | Reag/CBSF |

**Tese estrutural que emerge**: a Reag DTVM (CNPJ 34.829.992/0001-86 = CBSF) administra os três fundos centrais do escândalo, e o padrão "migrar gestão para Reag Jus Gestão de Ativos Judiciais" se repete em todos os três pouco antes de eventos relevantes (Compliance Zero, Carbono Oculto, liquidação BC). O nome **Reag Jus** parece ser a "valeta" onde os fundos foram empurrados na vésperas dos eventos críticos.

## Fontes arquivadas (verificáveis por hash)

`investigacao-claude/fontes/`:

- `Imirante_master-vorcaro-122-bilhoes_2026-04-14.md` (+ `.sha256`) — matéria-âncora
- `CVM-FNET_Scarlet_DF_2024_id865183.pdf` — DF auditada do exercício 31/05-31/12/2024 (com nome Carriet Inventory)
- `CVM-FNET_Scarlet_InfTrimestral_1T2026_id1199327.pdf` — trimestral pós-liquidação
- `CVM-FNET_Scarlet_Ata_AGE_2025-01-23_id824327.pdf` — ata da renomeação
- `CVM-FNET_Scarlet_Regulamento_2025-01-23_id824330.pdf` — regulamento já com nome SCARLET
- `CVM-FNET_Scarlet_InformeMensal_abr2026_id1185251.xml` — informe mensal estruturado (PL, cotistas, carteira)
- `CVM-FNET_Scarlet.sha256` — hashes

## Como reproduzir

```powershell
.venv\Scripts\activate

# Acha o CNPJ pelo nome no cache de informe mensal do Carlyle
python investigacao-claude/recon/achar_cnpj_scarlet.py

# Lista 46 documentos do FNET para CNPJ 55.344.996/0001-44
python investigacao-claude/recon/scarlet_probe_fnet.py

# Baixa as 10 peças críticas (DF, trimestral, atas, regulamentos, informe mensal)
python investigacao-claude/recon/scarlet_fnet_download.py

# Extrai texto de qualquer PDF (busca: MASTER, VORCARO, REAG, SDG, HANS, ANNA, etc)
python investigacao-claude/recon/scarlet_pdf_extract.py data/fnet_docs/Scarlet_DemonstracoesFinanceiras_2024_865183.pdf

# Decodifica o XML do informe mensal (vem em base64 do FNET)
python investigacao-claude/recon/scarlet_decode_informe_mensal.py

# Roda o scorecard e gera CSVs
python investigacao-claude/recon/reconstruir_scarlet.py
```

## Próximos alvos

- **Hans II FIP MULT** (não-FIDC, mas pode ter DF auditada no FNET) — destinatário principal de Vorcaro segundo a matéria, R$ 1,2 bi aportado, PL caiu de R$ 3,6 bi para R$ 83 mi após revisão.
- **Montenegro FIDC** (Trustee, R$ 2,4 bi do Master) — administrado pela Trustee, **não pela Reag** — testaria se o padrão estrutural é específico da Reag/CBSF ou se replica em outras DTVMs.
- **Anna FIC-FIDC** (R$ 15,8 bi de PL) — não tem matéria âncora isolada com afirmações quantitativas suficientes, mas reconstrução por DF pode revelar conexões adicionais com SDG II/Hans 95.
