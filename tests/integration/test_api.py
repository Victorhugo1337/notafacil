"""Testes de integração: API (Flask) + banco SQLite."""

import sqlite3
from contextlib import closing

import pytest


# ---------------------------------------------------------------------------
# CT-12 – Cadastrar aluno válido pela API (RF01, RNF02)
# ---------------------------------------------------------------------------
@pytest.mark.smoke
def test_ct12_cadastrar_aluno_valido(app, client):
    # Passo 1: enviar POST /alunos com o JSON do caso de teste.
    resposta = client.post("/alunos", json={"ra": "2410000000001", "nome": "Ana Souza"})

    # Passo 2: conferir o status e o corpo da resposta.
    assert resposta.status_code == 201
    assert resposta.get_json() == {
        "ra": "2410000000001",
        "nome": "Ana Souza",
        "situacao": "PENDENTE",
    }

    # Passo 3: consultar diretamente a tabela de alunos do banco temporário.
    with closing(sqlite3.connect(app.config["DATABASE"])) as con:
        linha = con.execute(
            "SELECT ra, nome FROM Alunos WHERE ra = ?", ("2410000000001",)
        ).fetchone()
    assert linha == ("2410000000001", "Ana Souza")


# ---------------------------------------------------------------------------
# CT-13 – Impedir cadastro de RA duplicado (RF01 / RN08)
# ---------------------------------------------------------------------------
def test_ct13_impedir_ra_duplicado(app, client):
    # Pré-condição: Ana Souza já cadastrada.
    client.post("/alunos", json={"ra": "2410000000001", "nome": "Ana Souza"})

    # Passo 1: tentar cadastrar o mesmo RA com outro nome.
    resposta = client.post("/alunos", json={"ra": "2410000000001", "nome": "Outro Nome"})

    # Passo 2: conferir o status e a mensagem.
    assert resposta.status_code == 409
    assert resposta.get_json() == {"erro": "RA já cadastrado"}

    # Passo 3: o banco continua com um único registro, com o nome original.
    with closing(sqlite3.connect(app.config["DATABASE"])) as con:
        linhas = con.execute(
            "SELECT nome FROM Alunos WHERE ra = ?", ("2410000000001",)
        ).fetchall()
    assert linhas == [("Ana Souza",)]


# ---------------------------------------------------------------------------
# CT-14 – Rejeitar cadastro com dados inválidos (RF01, RNF01)
# ---------------------------------------------------------------------------
@pytest.mark.parametrize(
    "dados, mensagem",
    [
        pytest.param({"ra": "241000000001", "nome": "Ana Souza"},
                     "RA deve conter exatamente 13 dígitos numéricos", id="a-ra-12-digitos"),
        pytest.param({"ra": "24100000000A1", "nome": "Ana Souza"},
                     "RA deve conter exatamente 13 dígitos numéricos", id="b-ra-com-letra"),
        pytest.param({"ra": "2410000000001", "nome": "Jo"},
                     "Nome deve ter entre 3 e 100 caracteres", id="c-nome-2-caracteres"),
        pytest.param({"ra": "2410000000001"},
                     "Campo nome é obrigatório", id="d-sem-campo-nome"),
    ],
)
def test_ct14_rejeitar_cadastro_invalido(app, client, dados, mensagem):
    # Passo 1: enviar POST /alunos com o dado inválido.
    resposta = client.post("/alunos", json=dados)

    # Passo 2: status 400 e mensagem que identifica o campo.
    assert resposta.status_code == 400
    assert resposta.get_json() == {"erro": mensagem}

    # Passo 3: nenhum registro foi gravado.
    with closing(sqlite3.connect(app.config["DATABASE"])) as con:
        total = con.execute("SELECT COUNT(*) FROM Alunos").fetchone()[0]
    assert total == 0
