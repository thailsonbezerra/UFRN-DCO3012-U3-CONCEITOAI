CREATE TABLE IF NOT EXISTS topics (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    created TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS maps (
    id SERIAL PRIMARY KEY,
    uuid UUID DEFAULT gen_random_uuid(),
    focus_question VARCHAR(512) NOT NULL,
    topic_id_central INT NOT NULL,
    created TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    CONSTRAINT fk_topic_central
        FOREIGN KEY (topic_id_central)
        REFERENCES topics (id)
        ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS propositions (
    id SERIAL PRIMARY KEY,
    text VARCHAR(255) NOT NULL,
    topic_id_origin INT NOT NULL,
    topic_id_destination INT NOT NULL,
    created TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    CONSTRAINT fk_topic_origin
        FOREIGN KEY (topic_id_origin)
        REFERENCES topics (id)
        ON DELETE CASCADE,
    CONSTRAINT fk_topic_destination
        FOREIGN KEY (topic_id_destination)
        REFERENCES topics (id)
        ON DELETE CASCADE,
    CONSTRAINT uq_proposition_unique
        UNIQUE (topic_id_origin, topic_id_destination, text)
);