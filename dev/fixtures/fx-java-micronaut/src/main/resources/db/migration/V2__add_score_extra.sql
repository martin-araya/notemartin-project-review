-- Migracion V2: agrega la tabla score_categories. La columna
-- ``categoria_ajustada`` solo la consume la @Query nativa de ScoreRepository
-- (ver src/main/java/com/fxmicronaut/repository/ScoreRepository.java).
-- Esto es la trampa del ecosistema #6: la columna aparece unicamente
-- en una query nativa; el modelo de datos Micronaut Data no la ve.

CREATE TABLE score_categories (
    code VARCHAR(32) PRIMARY KEY,
    categoria_ajustada VARCHAR(32) NOT NULL,
    descripcion VARCHAR(255)
);

INSERT INTO score_categories (code, categoria_ajustada, descripcion) VALUES
    ('AAA', 'premium',  'Cliente premium'),
    ('BBB', 'standard', 'Cliente standard'),
    ('CCC', 'basic',    'Cliente basico');
