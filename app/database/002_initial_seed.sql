INSERT INTO maps (focus_question, topic_id_central)
VALUES ('O que há no sistema solar?', NULL)
RETURNING id;

INSERT INTO topics (map_id, name) VALUES
(1, 'sistema solar'),
(1, 'sol'),
(1, 'planetas'),
(1, 'outros corpos celestes'),
(1, 'luas'),
(1, 'plutão'),
(1, 'cinturão de asteroides'),
(1, 'planetas interiores'),
(1, 'planetas exteriores'),
(1, 'mercúrio'),
(1, 'vênus'),
(1, 'terra'),
(1, 'marte'),
(1, 'júpiter'),
(1, 'saturno'),
(1, 'urano'),
(1, 'netuno')
RETURNING id;

UPDATE maps
SET topic_id_central = 1
WHERE id = 1;

INSERT INTO propositions (map_id, topic_id_origin, topic_id_destination, text) VALUES
(1, 1, 2, 'inclui'),
(1, 1, 3, 'inclui'),
(1, 1, 4, 'inclui'),
(1, 3, 8, 'são divididos em'),
(1, 3, 9, 'são divididos em'),
(1, 8, 10, 'incluem'),
(1, 8, 11, 'incluem'),
(1, 8, 12, 'incluem'),
(1, 8, 13, 'incluem'),
(1, 9, 14, 'incluem'),
(1, 9, 15, 'incluem'),
(1, 9, 16, 'incluem'),
(1, 9, 17, 'incluem');