INSERT INTO topics (name) VALUES
('sistema solar'),
('sol'),
('planetas'),
('outros corpos celestes'),
('luas'),
('plutão'),
('cinturão de asteroides'),
('planetas interiores'),
('planetas exteriores'),
('mercúrio'),
('vênus'),
('terra'),
('marte'),
('júpiter'),
('saturno'),
('urano'),
('netuno')
RETURNING id;

INSERT INTO maps (focus_question, topic_id_central) VALUES
('O que há no sistema solar?', 1)
RETURNING id;

INSERT INTO propositions (topic_id_origin, topic_id_destination, text) VALUES
(1, 2, 'inclui'), (1, 3, 'inclui'), (1, 4, 'inclui'),
(3, 8, 'são divididos em'), (3, 9, 'são divididos em'),
(8, 10, 'incluem'), (8, 11, 'incluem'), (8, 12, 'incluem'), (8, 13, 'incluem'),
(9, 14, 'incluem'), (9, 15, 'incluem'), (9, 16, 'incluem'), (9, 17, 'incluem')