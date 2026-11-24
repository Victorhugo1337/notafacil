# Registro de defeitos – NotaFácil

Projeto: NotaFácil – Gestão da Qualidade de Software, Fatec Rio Preto (2026).
Integrantes: Arthur Alves, Milton da Luz Neto e Victor Hugo Almeida de Oliveira.

Fluxo de acompanhamento: Aberto → Corrigido → Fechado (se o reteste falhar, volta para Aberto).

## DEF-01 – `create_app` quebra ao receber configuração de teste

| Campo | Registro |
|---|---|
| **ID** | DEF-01 |
| **Descrição** | A função `create_app` declarava o parâmetro como `test_confg`, mas usava `test_config` no corpo. Qualquer chamada com configuração (como a dos testes, que aponta para um banco temporário) lançava `NameError`. Defeito real, não introduzido de propósito. |
| **Caso de teste relacionado** | CT-12 – Cadastrar aluno válido pela API (também afetava CT-13 e CT-14) |
| **Requisitos relacionados** | RF01 (cadastrar aluno) e RNF02 (persistência) |
| **Passos para reprodução** | 1. Instalar as dependências (`python -m pip install -r requirements.txt`). 2. Executar `pytest tests/integration/test_api.py::test_ct12_cadastrar_aluno_valido -v`. |
| **Resultado esperado** | Teste aprovado: `POST /alunos` retorna 201 e o aluno é gravado no banco temporário. |
| **Resultado obtido** | `ERROR at setup` – `NameError: name 'test_config' is not defined` em `app/__init__.py`, linha 12. |
| **Gravidade** | Alta – impede a criação da aplicação com qualquer configuração e bloqueia todos os testes de integração. |
| **Responsável** | Victor Hugo Almeida de Oliveira (back-end); reteste: Arthur Alves (QA) |
| **Commit em que foi detectado** | `a7302d8` |
| **Correção** | Parâmetro renomeado para `test_config` em `app/__init__.py`. |
| **Reteste** | CT-12 aprovado; suíte completa (regressão) com 52 testes aprovados. |
| **Status atual** | Fechado |

### Histórico

| Data | Status | Observação |
|---|---|---|
| 23/11/2026 | Aberto | CT-12, CT-13 e CT-14 com erro no setup (`NameError`). |
| 23/11/2026 | Corrigido | Parâmetro de `create_app` renomeado para `test_config`. |
| 23/11/2026 | Fechado | Reteste do CT-12 aprovado e regressão completa aprovada (52 testes). |

### Evidências

- Antes da correção: [`evidencias/DEF-01_antes_CT-12.txt`](evidencias/DEF-01_antes_CT-12.txt)
- Depois da correção: [`evidencias/DEF-01_depois_CT-12.txt`](evidencias/DEF-01_depois_CT-12.txt)
- Regressão (suíte completa com cobertura): [`evidencias/regressao_suite_completa.txt`](evidencias/regressao_suite_completa.txt)
