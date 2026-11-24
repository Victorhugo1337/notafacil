"""Regras de negócio do NotaFácil (RN01 a RN09).

Funções puras: não acessam banco nem Flask. Quando um valor é inválido,
lançam ValueError com a mensagem que a API devolve ao usuário (HTTP 400).
"""

import re
from decimal import Decimal, InvalidOperation

MEDIA_MINIMA = 6.0
FREQUENCIA_MINIMA = 75.0


def _converter_numero(valor, mensagem):
    """Converte o valor para Decimal ou lança ValueError com a mensagem dada.

    Usamos Decimal (e não float) para contar as casas decimais sem erro de
    arredondamento: Decimal("7.25") tem exatamente duas casas.
    """
    if valor is None or isinstance(valor, bool):
        raise ValueError(mensagem)
    texto = str(valor).strip()
    if texto == "":
        raise ValueError(mensagem)
    try:
        numero = Decimal(texto)
    except InvalidOperation:
        raise ValueError(mensagem)
    if not numero.is_finite():  # recusa "NaN" e "Infinity"
        raise ValueError(mensagem)
    return numero


def _casas_decimais(numero):
    """Quantidade de casas decimais significativas (7.50 conta como 1)."""
    expoente = numero.normalize().as_tuple().exponent
    return max(0, -expoente)


def calcular_media(p1, p2):
    """RN01: média aritmética de P1 e P2, sem arredondamento."""
    return (p1 + p2) / 2


def validar_nota(valor):
    """RN02: nota numérica, entre 0,0 e 10,0, com no máximo uma casa decimal."""
    numero = _converter_numero(valor, "Nota deve ser numérica")
    if numero < 0 or numero > 10:
        raise ValueError("Nota deve estar entre 0,0 e 10,0")
    if _casas_decimais(numero) > 1:
        raise ValueError("Nota deve ter no máximo uma casa decimal")
    return float(numero)


def validar_frequencia(valor):
    """RN03: frequência numérica, entre 0,0 e 100,0, com no máximo uma casa decimal."""
    numero = _converter_numero(valor, "Frequência deve ser numérica")
    if numero < 0 or numero > 100:
        raise ValueError("Frequência deve estar entre 0,0 e 100,0")
    if _casas_decimais(numero) > 1:
        raise ValueError("Frequência deve ter no máximo uma casa decimal")
    return float(numero)


def determinar_situacao(media, frequencia):
    """RN04 a RN07: situação do aluno.

    A ordem dos testes é a própria regra: pendente primeiro, depois falta
    (que prevalece sobre a nota), depois nota e, por fim, aprovado.
    """
    if media is None or frequencia is None:
        return "PENDENTE"
    if frequencia < FREQUENCIA_MINIMA:
        return "REPROVADO_FALTA"
    # A média tem no máximo duas casas; round evita que 5.9999999 vire reprovação.
    if round(media, 2) < MEDIA_MINIMA:
        return "REPROVADO_NOTA"
    return "APROVADO"


def validar_ra(ra):
    """RN08: RA com exatamente 13 dígitos de 0 a 9 (texto, para manter zeros à esquerda)."""
    if not isinstance(ra, str) or not re.fullmatch(r"[0-9]{13}", ra):
        raise ValueError("RA deve conter exatamente 13 dígitos numéricos")
    return ra


def validar_nome(nome):
    """RN09: nome com 3 a 100 caracteres, ignorando espaços nas extremidades."""
    if not isinstance(nome, str):
        nome = ""
    nome = nome.strip()
    if len(nome) < 3 or len(nome) > 100:
        raise ValueError("Nome deve ter entre 3 e 100 caracteres")
    return nome
