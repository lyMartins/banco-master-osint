# Comparativo: Informe Mensal vs. DF auditada do SDG II

Conferência de batimento entre os dois caminhos de coleta. As DFs do Luan vêm do PR #2 (`investigacao-claude/dados/fnet/SDG2_DemonstracoesFinanceiras_A_963178.pdf`).

## Pontos onde os dois caminhos se encontram

### Carteira (Direitos Creditórios + outros ativos)

| Data | Fonte | Valor |
|---|---|---|
| 31/12/2024 (encerramento exercício) | DF auditada (Luan) | R$ 6,53 bi em direitos creditórios + outros |
| 31/10/2025 | Informe Mensal CVM | R$ 5.375,7 mi |
| 31/12/2025 | Informe Mensal CVM | R$ 3.660,4 mi |

A DF é foto anual. O informe mensal preenche os 11 meses entre uma DF e outra.

### PL declarado

| Data | Fonte | Valor |
|---|---|---|
| 31/12/2024 | DF auditada | (a conferir no PDF) |
| 31/12/2025 | Informe Mensal CVM | R$ 2.374,7 mi |
| 31/03/2026 | Informe Mensal CVM | R$ 2.321,4 mi |

### Cotistas

A DF do Luan e o informe mensal **divergem** sobre quantos cotistas — informe diz 2 (jan/2025 a jan/2026); ata de 03/2025 diz "único cotista". O Luan explica em `RECONSTRUCAO_SDG2.md`: diferença de recorte por classe/série. Em qualquer caso, **nenhum dos dois nomeia o cotista** publicamente. MKS Soluções e Hans 95 vêm de fonte de inquérito.

### Administrador e gestor

Os dois caminhos confirmam:
- Administrador: CBSF DTVM (ex-Reag Trust), CNPJ 34.829.992/0001-86
- Gestor: CBSF Trust Administradora de Recursos Ltda., CNPJ 23.863.529/0001-34
- Diretores do fundo: Marcos Ferreira Costa e Diego Peres da Costa Nascimento

## O que SÓ o informe mensal vê

### 1. Cessão emergencial entre 31/10 e 30/11/2025

A carteira caiu de R$ 5.375 mi para R$ 3.728 mi. Diferença de **R$ 1.647 mi** em 30 dias. A DF auditada anual não captura esse movimento porque cai entre os fechamentos. O informe mensal sim.

### 2. Recomposição em fevereiro/2026

Entre jan e fev/2026 a carteira pulou de R$ 3.668 mi para R$ 6.055 mi. **Crescimento de R$ 2.387 mi em 30 dias** com o passivo subindo de R$ 3.081 mi para R$ 4.907 mi. Indica entrada de novos ativos com obrigações de pagamento correspondentes — operação no sentido oposto da cessão emergencial de nov/2025.

### 3. Sangria paralela no Gold Style FIDC

Outra entidade administrada pela CBSF DTVM, o Gold Style perdeu R$ 1.012 mi em carteira no mesmo mês da liquidação do Master (out → nov 2025). PL ficou estável, então a perda foi compensada por algum lado contábil — possivelmente provisão ou redução de passivo.

### 4. Tamanho do Anna FIC-FIDC

R$ 15,8 bi de PL em nov/2025. A DF auditada do SDG II menciona o Anna como cotista que integralizou cotas em 30/09/2024, mas não detalha o tamanho do próprio Anna. O informe mensal mostra que o Anna sozinho é maior que SDG II + Gold Style + Lancia! somados.

## O que SÓ a DF auditada vê

### 1. Identidade das cessões (data + cedente + devedor + valor exato)

A DF lista, por exemplo, "27/02/2024 — CCB do Lormont cedida pelo Master — R$ 102.438.000". O informe mensal agrega tudo em "vl_industrial", "vl_factor", "vl_credito" etc.

### 2. Os 5 FIDCs cessores adicionais da Lormont

Carriet Inventory, B-ROL, CIB-K, Del Rey e Runeard — todos cedendo CCBs da Lormont ao SDG II. O informe mensal não diferencia origem das cessões.

### 3. Parecer do auditor

Abstenção de opinião com motivos detalhados: 62% sem comprovação de lastro, ausência de estudo de recuperabilidade. Esse documento é o que dá o veredito qualitativo do que os números mostram quantitativamente.

### 4. Aquisição da debênture Banvox em 22/11/2023

A DF tem a data exata da operação e o valor preciso (R$ 380.346.000 da 4ª emissão de R$ 400 mi). Informe mensal traz só o saldo do mês.

## Resumo prático

| Quando usar | Para que |
|---|---|
| **DF auditada (FNET)** | identificar cedentes, devedores, valores exatos, parecer do auditor |
| **Informe Mensal (dados abertos)** | rastrear movimentação atípica, comparar fundos do mesmo grupo, fazer série temporal |

Juntos respondem o que cada um sozinho não responde.
