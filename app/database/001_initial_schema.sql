CREATE TABLE IF NOT EXISTS maps (
    id SERIAL PRIMARY KEY,
    uuid UUID DEFAULT gen_random_uuid(),
    focus_question VARCHAR(512) NOT NULL,
    topic_id_central INT NULL,
    created TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS topics (
    id SERIAL PRIMARY KEY,
    map_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    created TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),  
    CONSTRAINT fk_topic_map
        FOREIGN KEY (map_id)
        REFERENCES maps (id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS propositions (
    id SERIAL PRIMARY KEY,
    map_id INT NOT NULL,
    text VARCHAR(255) NOT NULL,
    topic_id_origin INT NOT NULL,
    topic_id_destination INT NOT NULL,
    created TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    CONSTRAINT fk_prop_map
        FOREIGN KEY (map_id)
        REFERENCES maps (id)
        ON DELETE CASCADE,
    CONSTRAINT fk_topic_origin
        FOREIGN KEY (topic_id_origin)
        REFERENCES topics (id)
        ON DELETE CASCADE,
    CONSTRAINT fk_topic_destination
        FOREIGN KEY (topic_id_destination)
        REFERENCES topics (id)
        ON DELETE CASCADE
);

ALTER TABLE maps
    ADD CONSTRAINT fk_topic_central
        FOREIGN KEY (topic_id_central)
        REFERENCES topics (id)
        ON DELETE SET NULL;