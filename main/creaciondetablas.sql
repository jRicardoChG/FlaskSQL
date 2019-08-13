CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    usuario VARCHAR(20) NOT NULL,
    passwords VARCHAR(30) NOT NULL
);

CREATE TABLE libros (
    id SERIAL  PRIMARY KEY,
    isbn VARCHAR(10) NOT NULL,
    titulo VARCHAR(30) NOT NULL,
    autor VARCHAR(30) NOT NULL,
    years INT NOT NULL
);