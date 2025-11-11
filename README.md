# MVP ConceitoAI

Projeto desenvolvido na disciplina **DCO3012 - Programação Avançada - T01 (2025.2)**  
Universidade Federal do Rio Grande do Norte (UFRN)

---

## Comandos Úteis

### Criar ambiente virtual
```bash
python3 -m venv .venv
```
### Ativar o Ambiente Virtual
```bash
. .venv/bin/activate
``` 
### Instalar Dependências
```bash
pip install -r requirements.txt
```

Desativar o Ambiente Virtual
```bash
deactivate
```
### Subir o serviço do llm
```bash
ollama serve
```

### Subir o servidor com uvicorn
```bash
uvicorn app.main:app --reload
```
### Tempo Médio da LLM (llama3.2:1b-instruct-q4_0):
Identificar: 4~6
Expandir: 16~20

## TODO
- Melhorar a precisão do tópico identificado
- Melhorar a qualidade e relevância dos subtópicos gerados
- Diminuir o tempo de resposta da LLM

