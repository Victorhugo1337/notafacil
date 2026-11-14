
CREATE TABLE IF NOT EXISTS Professores (
    id_professor INTEGER PRIMARY KEY AUTOINCREMENT,         
    nome         TEXT NOT NULL
                 CHECK (length(trim(nome)) BETWEEN 3 AND 100),
    email        TEXT UNIQUE                                 
);

CREATE TABLE IF NOT EXISTS Alunos (
    ra   TEXT PRIMARY KEY                                    
         CHECK (length(ra) = 13 AND ra NOT GLOB '*[^0-9]*'), 
    nome TEXT NOT NULL
         CHECK (length(trim(nome)) BETWEEN 3 AND 100)       
);

CREATE TABLE IF NOT EXISTS Turmas (
    id_turma INTEGER PRIMARY KEY AUTOINCREMENT,       
    codigo   TEXT NOT NULL UNIQUE,                           
    nome     TEXT NOT NULL                                   
);

CREATE TABLE IF NOT EXISTS Disciplinas (
    id_disciplina INTEGER PRIMARY KEY AUTOINCREMENT,        
    codigo        TEXT NOT NULL UNIQUE,                     
    nome          TEXT NOT NULL                              
);

CREATE TABLE IF NOT EXISTS Alunos_x_Turmas (
    ra       TEXT    NOT NULL REFERENCES Alunos(ra)         ON DELETE CASCADE, 
    id_turma INTEGER NOT NULL REFERENCES Turmas(id_turma)   ON DELETE CASCADE, 
    PRIMARY KEY (ra, id_turma)                                                 
);


CREATE TABLE IF NOT EXISTS Disciplinas_x_Professores (
    id_disciplina INTEGER NOT NULL REFERENCES Disciplinas(id_disciplina) ON DELETE CASCADE,
    id_professor  INTEGER NOT NULL REFERENCES Professores(id_professor)  ON DELETE CASCADE,
    PRIMARY KEY (id_disciplina, id_professor)               
);

CREATE TABLE IF NOT EXISTS Disciplinas_x_Alunos (
    id_disciplina INTEGER NOT NULL REFERENCES Disciplinas(id_disciplina) ON DELETE CASCADE,
    ra            TEXT    NOT NULL REFERENCES Alunos(ra)                 ON DELETE CASCADE,
    p1            REAL CHECK (p1 IS NULL OR (p1 BETWEEN 0.0 AND 10.0 AND p1 = round(p1, 1))), 
    p2            REAL CHECK (p2 IS NULL OR (p2 BETWEEN 0.0 AND 10.0 AND p2 = round(p2, 1))), 
    frequencia    REAL CHECK (frequencia IS NULL OR (frequencia BETWEEN 0.0 AND 100.0
                                                     AND frequencia = round(frequencia, 1))), 
    PRIMARY KEY (id_disciplina, ra)                          
);

CREATE INDEX IF NOT EXISTS idx_disc_alunos_ra ON Disciplinas_x_Alunos(ra);

CREATE INDEX IF NOT EXISTS idx_alunos_turmas_turma ON Alunos_x_Turmas(id_turma);
CREATE INDEX IF NOT EXISTS idx_disc_prof_prof      ON Disciplinas_x_Professores(id_professor);


CREATE VIEW IF NOT EXISTS vw_boletim AS
SELECT
    a.ra,
    a.nome,
    dxa.id_disciplina,
    dxa.p1,
    dxa.p2,
    dxa.frequencia,
    -- Média sem arredondamento no banco (RN01); a exibição com 2 casas é feita pela aplicação.
    CASE WHEN dxa.p1 IS NOT NULL AND dxa.p2 IS NOT NULL
         THEN (dxa.p1 + dxa.p2) / 2.0 END AS media,
    CASE
        -- RN07: sem P1, P2 ou frequência lançadas, a situação é pendente.
        WHEN dxa.p1 IS NULL OR dxa.p2 IS NULL OR dxa.frequencia IS NULL
            THEN 'PENDENTE'
        -- RN05: falta prevalece sobre a nota (frequência < 75,0).
        WHEN dxa.frequencia < 75.0
            THEN 'REPROVADO_FALTA'
        -- RN06: média < 6,00 equivale a soma < 12,0; round(,1) evita erro de ponto flutuante no limite.
        WHEN round(dxa.p1 + dxa.p2, 1) < 12.0
            THEN 'REPROVADO_NOTA'
        -- RN04: média >= 6,00 e frequência >= 75,0.
        ELSE 'APROVADO'
    END AS situacao
FROM Disciplinas_x_Alunos dxa
JOIN Alunos a ON a.ra = dxa.ra;
