# NotaFácil

![Testes](https://github.com/Victorhugo1337/notafacil/actions/workflows/testes.yml/badge.svg)

Sistema simples que cadastra alunos e calcula média final e situação acadêmica
(aprovado, reprovado por nota, reprovado por falta ou pendente).

Trabalho Prático Semestral da disciplina **Gestão da Qualidade de Software**,
Fatec Rio Preto, 2026.

**Integrantes:** Arthur Alves, Milton da Luz Neto e Victor Hugo Almeida de Oliveira.

## Tecnologias

Python 3.14, Flask 3.1, SQLite 3, pytest 9 e pytest-cov. Pipeline no GitHub Actions.

## Como instalar

Pré-requisito: Python 3.14.

```bash
git clone https://github.com/Victorhugo1337/notafacil.git
cd notafacil
python -m venv .venv
```

Ativar o ambiente virtual:

- Windows (PowerShell): `.\.venv\Scripts\Activate.ps1`
- Linux/Mac: `source .venv/bin/activate`

Instalar as dependências:

```bash
python -m pip install -r requirements.txt
```

## Como executar os testes localmente

Com o ambiente virtual ativado, na raiz do projeto:

| Comando | O que faz |
|---|---|
| `pytest` | Roda a suíte completa (regressão) |
| `pytest -v` | Mostra o nome e o resultado de cada teste |
| `pytest tests/unit` | Só os testes unitários (CT-01 a CT-11) |
| `pytest tests/integration` | Só os testes de integração (CT-12 a CT-14) |
| `pytest -m smoke` | Só o subconjunto de fumaça |
| `pytest --cov=app --cov-report=term-missing` | Suíte completa com cobertura de código |

## Como executar a aplicação

```bash
python main.py
```

A API fica disponível em `http://localhost:5000`. Exemplo de cadastro:

```
POST /alunos
{"ra": "2410000000001", "nome": "Ana Souza"}
```

## Estrutura

| Caminho | Finalidade |
|---|---|
| `app/__init__.py` | Fábrica da aplicação Flask (`create_app`) |
| `app/regras.py` | Regras de negócio: validações, média e situação |
| `app/rotas.py` | Rotas da API REST |
| `app/db.py` | Conexão e criação do banco SQLite |
| `app/notafacil_schema.sql` | Estrutura das tabelas |
| `tests/unit/test_regras.py` | Testes unitários |
| `tests/integration/test_api.py` | Testes de integração (API + banco) |
| `tests/conftest.py` | Fixtures: aplicação de teste e banco temporário |
| `.github/workflows/testes.yml` | Pipeline de testes (GitHub Actions) |
| `docs/DEFEITOS.md` | Registro de defeitos (DEF-01) |
| `docs/evidencias/` | Saídas dos testes antes e depois da correção e da regressão |
