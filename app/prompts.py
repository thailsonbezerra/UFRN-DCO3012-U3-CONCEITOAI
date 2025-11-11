def identify_topic_prompt(user_prompt: str) -> str:
    return f"""
Você é um assistente que extrai o tópico central de um texto.
Retorne APENAS o nome do tópico principal, em uma única palavra ou frase curta.
Sem explicações, sem formatação, sem aspas.

Texto: {user_prompt}
Tópico:
""".strip()

def expand_topic_prompt(topic: str) -> str:
    return f'''
Você é um gerador de dados estruturados. Sua única tarefa é retornar um ARRAY JSON contendo exatamente 6 subtópicos diretamente relacionados a "{topic}".

Regras obrigatórias:
- A saída DEVE ser exatamente neste formato:
  ["item1", "item2", "item3", "item4", "item5", "item6"]
- Não inclua nada antes ou depois do array.
- Não use chaves {{}}, títulos, comentários ou explicações.
- Não use "tópicos": ou outras chaves.
- Todos os itens devem ser curtos, claros e sem aspas internas.

Tópico: "{topic}"
Saída:
'''.strip()