import os
import sqlite3
from contextlib import closing
from pathlib import Path

PATH = os.environ.get("NOTAFACIL_DB", "notafacil.db")

PATH_SCHEMA = Path(__file__).with_name("notafacil_schema.sql")


def conectar(caminho: str = PATH) -> sqlite3.Connection:
    con = sqlite3.connect(caminho)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON")
    return con


def inicializar_banco(caminho: str = PATH) -> None:
    sql = PATH_SCHEMA.read_text(encoding="utf-8")
    with closing(conectar(caminho)) as con, con:
        con.executescript(sql)


if __name__ == "__main__":
    inicializar_banco()
    with closing(conectar()) as con:
        objetos = con.execute(
            "SELECT type, name FROM sqlite_master "
            "WHERE name NOT LIKE 'sqlite_%' ORDER BY type, name"
        ).fetchall()
        for o in objetos:
            print(f"{o['type']:<6} {o['name']}")
        print("foreign_keys =", con.execute("PRAGMA foreign_keys").fetchone()[0])