"""Testes unitários do módulo app/regras.py (CT-01 a CT-11).

Cada função de teste corresponde a um caso de teste do plano.
Os dados vêm dos Quadros 21 e 22 (partições e valores-limite).
"""

import pytest

from app.regras import (
    calcular_media,
    determinar_situacao,
    validar_frequencia,
    validar_nome,
    validar_nota,
    validar_ra,
)

# Mensagens de erro definidas no plano de testes.
MSG_NOTA_FAIXA = "Nota deve estar entre 0,0 e 10,0"
MSG_NOTA_NUMERICA = "Nota deve ser numérica"
MSG_NOTA_DECIMAL = "Nota deve ter no máximo uma casa decimal"
MSG_FREQ_FAIXA = "Frequência deve estar entre 0,0 e 100,0"
MSG_FREQ_NUMERICA = "Frequência deve ser numérica"
MSG_RA = "RA deve conter exatamente 13 dígitos numéricos"
MSG_NOME = "Nome deve ter entre 3 e 100 caracteres"


# ---------------------------------------------------------------------------
# CT-01 – Calcular média com notas válidas (RF04 / RN01)
# ---------------------------------------------------------------------------
@pytest.mark.smoke
@pytest.mark.parametrize(
    "p1, p2, esperado",
    [
        (7.0, 8.0, 7.50),
        (0.0, 0.0, 0.00),
        (10.0, 10.0, 10.00),
        (5.9, 6.0, 5.95),
    ],
)
def test_ct01_calcular_media(p1, p2, esperado):
    assert calcular_media(p1, p2) == pytest.approx(esperado)


# ---------------------------------------------------------------------------
# CT-02 – Validar limite inferior da nota (RF02 / RN02)
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("valor", [0.0, 0.1])
def test_ct02_nota_limite_inferior_valida(valor):
    assert validar_nota(valor) == valor


def test_ct02_nota_abaixo_do_limite_inferior():
    with pytest.raises(ValueError, match=MSG_NOTA_FAIXA):
        validar_nota(-0.1)


# ---------------------------------------------------------------------------
# CT-03 – Validar limite superior da nota (RF02 / RN02)
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("valor", [9.9, 10.0])
def test_ct03_nota_limite_superior_valida(valor):
    assert validar_nota(valor) == valor


def test_ct03_nota_acima_do_limite_superior():
    with pytest.raises(ValueError, match=MSG_NOTA_FAIXA):
        validar_nota(10.1)


# ---------------------------------------------------------------------------
# CT-04 – Rejeitar nota em formato inválido (RF02 / RN02)
# ---------------------------------------------------------------------------
@pytest.mark.parametrize(
    "valor",
    [
        pytest.param("abc", id="CI3-texto"),
        pytest.param("", id="CI4-vazio"),
        pytest.param(None, id="CI4-None"),
    ],
)
def test_ct04_nota_nao_numerica(valor):
    with pytest.raises(ValueError, match=MSG_NOTA_NUMERICA):
        validar_nota(valor)


def test_ct04_nota_com_mais_de_uma_casa_decimal():
    with pytest.raises(ValueError, match=MSG_NOTA_DECIMAL):
        validar_nota(7.25)


def test_ct04_nota_valida_de_controle():
    assert validar_nota(7.5) == 7.5


# ---------------------------------------------------------------------------
# CT-05 – Validar limites da frequência (RF03 / RN03)
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("valor", [0.0, 0.1, 99.9, 100.0])
def test_ct05_frequencia_valida(valor):
    assert validar_frequencia(valor) == valor


@pytest.mark.parametrize("valor", [-0.1, 100.1])
def test_ct05_frequencia_fora_da_faixa(valor):
    with pytest.raises(ValueError, match=MSG_FREQ_FAIXA):
        validar_frequencia(valor)


def test_ct05_frequencia_nao_numerica():
    with pytest.raises(ValueError, match=MSG_FREQ_NUMERICA):
        validar_frequencia("abc")


# ---------------------------------------------------------------------------
# CT-06 – Situação aprovado nos limites mínimos (RF05 / RN04)
# ---------------------------------------------------------------------------
@pytest.mark.smoke
@pytest.mark.parametrize(
    "media, frequencia",
    [
        (6.00, 75.0),
        (6.05, 75.1),
        (10.00, 100.0),
    ],
)
def test_ct06_aprovado(media, frequencia):
    assert determinar_situacao(media, frequencia) == "APROVADO"


# ---------------------------------------------------------------------------
# CT-07 – Situação reprovado por nota abaixo do limite (RF05 / RN06)
# ---------------------------------------------------------------------------
@pytest.mark.parametrize(
    "media, frequencia",
    [
        (5.95, 75.0),
        (5.95, 100.0),
        (0.00, 80.0),
    ],
)
def test_ct07_reprovado_por_nota(media, frequencia):
    assert determinar_situacao(media, frequencia) == "REPROVADO_NOTA"


# ---------------------------------------------------------------------------
# CT-08 – Reprovado por falta e prioridade sobre a nota (RF05 / RN05)
# ---------------------------------------------------------------------------
@pytest.mark.parametrize(
    "media, frequencia",
    [
        (6.00, 74.9),
        (10.00, 74.9),
        (4.00, 50.0),
        (10.00, 0.0),
    ],
)
def test_ct08_reprovado_por_falta(media, frequencia):
    assert determinar_situacao(media, frequencia) == "REPROVADO_FALTA"


# ---------------------------------------------------------------------------
# CT-09 – Situação pendente sem notas lançadas (RF05 / RN07)
# ---------------------------------------------------------------------------
@pytest.mark.parametrize(
    "media, frequencia",
    [
        (None, None),
        (None, 90.0),
    ],
)
def test_ct09_pendente(media, frequencia):
    assert determinar_situacao(media, frequencia) == "PENDENTE"


# ---------------------------------------------------------------------------
# CT-10 – Validar formato do RA (RF01 / RN08)
# ---------------------------------------------------------------------------
def test_ct10_ra_valido():
    assert validar_ra("2410000000001") == "2410000000001"


@pytest.mark.parametrize(
    "ra",
    [
        pytest.param("241000000001", id="CI9-12-digitos"),
        pytest.param("24100000000011", id="CI10-14-digitos"),
        pytest.param("24100000000A1", id="CI11-com-letra"),
        pytest.param("", id="CI12-vazio"),
    ],
)
def test_ct10_ra_invalido(ra):
    with pytest.raises(ValueError, match=MSG_RA):
        validar_ra(ra)


# ---------------------------------------------------------------------------
# CT-11 – Validar tamanho do nome (RF01 / RN09)
# ---------------------------------------------------------------------------
@pytest.mark.parametrize(
    "nome",
    [
        pytest.param("Ana", id="3-caracteres"),
        pytest.param("A" * 100, id="100-caracteres"),
    ],
)
def test_ct11_nome_valido(nome):
    assert validar_nome(nome) == nome


def test_ct11_nome_com_espacos_nas_extremidades():
    assert validar_nome("  Ana  ") == "Ana"


@pytest.mark.parametrize(
    "nome",
    [
        pytest.param("Jo", id="CI14-2-caracteres"),
        pytest.param("A" * 101, id="CI15-101-caracteres"),
        pytest.param("", id="CI16-vazio"),
        pytest.param("     ", id="CI16-somente-espacos"),
    ],
)
def test_ct11_nome_invalido(nome):
    with pytest.raises(ValueError, match=MSG_NOME):
        validar_nome(nome)
