CREATE TABLE usuarios (
    id_usuario SERIAL PRIMARY KEY,
    usuario VARCHAR(20) UNIQUE NOT NULL,
    email VARCHAR(30) UNIQUE NOT NULL,
    passwords VARCHAR(30) NOT NULL
);

CREATE TABLE libros (
    id_libro SERIAL PRIMARY KEY,
    isbn VARCHAR(10) NOT NULL,
    titulo VARCHAR(30) NOT NULL,
    autor VARCHAR(30) NOT NULL,
    years INT NOT NULL
);

CREATE TABLE reviews (
    id_reviews SERIAL PRIMARY KEY,
    id_libro SERIAL NOT NULL,
    id_usuario SERIAL NOT NULL,
    review VARCHAR(256),
    estrellas INT,
    CONSTRAINT fk_libro FOREIGN KEY (id_libro) REFERENCES libros (id_libro),
    CONSTRAINT fk_usuario FOREIGN KEY (id_usuario) REFERENCES usuarios (id_usuario)
);

