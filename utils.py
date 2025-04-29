import json
import os
from werkzeug.security import check_password_hash

# --- Função para carregar dados de um arquivo JSON ---
def carregar_dados(arquivo):
    if os.path.exists(arquivo):
        with open(arquivo, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []  # Se o arquivo estiver vazio ou corrompido, retorna uma lista vazia.
    return []

# --- Função para carregar alunos ---
def carregar_alunos():
    return carregar_dados("alunos.json")

# --- Função para salvar alunos ---
def salvar_alunos(alunos):
    with open("alunos.json", "w", encoding="utf-8") as f:
        json.dump(alunos, f, indent=4, ensure_ascii=False)

# --- Função para carregar usuários ---
def carregar_usuarios():
    return carregar_dados("usuarios.json")

# --- Função para validar usuário ---
def validar_usuario(usuario, senha):
    usuarios = carregar_usuarios()
    for u in usuarios:
        if u["usuario"] == usuario and check_password_hash(u["senha"], senha):
            return u  # deve retornar o dicionário com "id"
    return None


