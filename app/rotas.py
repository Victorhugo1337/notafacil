"""Rotas da API REST do NotaFácil."""

import sqlite3
from contextlib import closing

from flask import Blueprint, current_app, jsonify, request

from . import db, regras

bp = Blueprint("rotas", __name__)


@bp.post("/alunos")
def cadastrar_aluno():
    """RF01: cadastra um aluno. Respostas: 201, 400 (dado inválido) ou 409 (RA repetido)."""
    dados = request.get_json(silent=True) or {}

    # RNF01: campo ausente recebe mensagem própria, que identifica o campo.
    for campo in ("ra", "nome"):
        if dados.get(campo) is None:
            return jsonify({"erro": f"Campo {campo} é obrigatório"}), 400

    try:
        ra = regras.validar_ra(dados.get("ra"))
        nome = regras.validar_nome(dados.get("nome"))
    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 400

    try:
        with closing(db.conectar(current_app.config["DATABASE"])) as con, con:
            con.execute("INSERT INTO Alunos (ra, nome) VALUES (?, ?)", (ra, nome))
    except sqlite3.IntegrityError:
        return jsonify({"erro": "RA já cadastrado"}), 409

    # Aluno recém-cadastrado ainda não tem notas nem frequência (RN07).
    situacao = regras.determinar_situacao(None, None)
    return jsonify({"ra": ra, "nome": nome, "situacao": situacao}), 201
