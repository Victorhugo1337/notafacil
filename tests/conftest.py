"""Fixtures compartilhadas pelos testes de integração."""

import pytest

from app import create_app


@pytest.fixture
def app(tmp_path):
    """Aplicação de teste apontando para um banco SQLite temporário e vazio.

    tmp_path é uma pasta nova criada pelo pytest para cada teste e apagada
    depois, então um teste nunca enxerga os dados de outro (risco R6).
    """
    caminho_banco = tmp_path / "teste.db"
    return create_app({"TESTING": True, "DATABASE": str(caminho_banco)})


@pytest.fixture
def client(app):
    """Cliente HTTP do Flask: faz requisições sem subir um servidor de verdade."""
    return app.test_client()
