from flask import Flask, render_template, request, redirect, url_for, session, flash
import json
import os
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from utils import carregar_alunos, salvar_alunos, carregar_usuarios, validar_usuario

app = Flask(__name__)
app.secret_key = "chave_super_secreta"

# --- Arquivo onde os dados serão salvos ---
ARQUIVO_ALUNOS = "alunos.json"
ARQUIVO_USUARIOS = "usuarios.json"

# --- Exercícios disponíveis ---
exercicios = {
    1: ["abdominal", "flexão", "prancha"],
    2: ["supino", "levantamento", "desenvolvimento de ombro"],
    3: ["bíceps", "agachamento", "remada com barra"]
}

# --- Página inicial ---
@app.route("/", methods=["GET", "POST"])
def index():
    lista = []
    if request.method == "POST":
        try:
            escolha = int(request.form["lista"])
            lista = exercicios.get(escolha, [])
        except ValueError:
            lista = []  # Caso ocorra um erro na conversão para int
    return render_template("index.html", lista=lista)

# --- Página de login ---
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"]
        senha = request.form["senha"]
        usuario_validado = validar_usuario(usuario, senha)
        if usuario_validado:
            session["usuario"] = usuario
            session["id"] = usuario_validado["id"]  # Aqui você armazena o id
            return redirect(url_for("gerenciar_alunos"))
        else:
            flash("Usuário ou senha incorretos")
    return render_template("login.html")

# --- Logout ---
@app.route("/logout")
def logout():
    session.pop("usuario", None)
    return redirect(url_for("login"))

# --- Página protegida: gerenciamento de alunos ---
@app.route("/alunos", methods=["GET", "POST"])
def gerenciar_alunos():
    if "usuario" not in session:
        return redirect(url_for("login"))

    alunos = carregar_alunos()
    usuario_id = session.get("id")  # Obtém o id do usuário logado

    # Filtra alunos para mostrar apenas o perfil do usuário logado
    alunos_exibidos = [aluno for aluno in alunos if aluno.get("usuario_id") == usuario_id]


    if request.method == "POST":
        nome = request.form.get("nome")
        idade = request.form.get("idade")
        plano = request.form.get("plano")
        lista_de_exercicios = request.form.get("lista_de_exercicios")

        if nome and idade and plano and lista_de_exercicios:
            if not idade.isdigit() or int(idade) <= 0:
                flash("Idade inválida")
                return redirect(url_for("gerenciar_alunos"))
            
            alunos.append({
    "id": str(uuid.uuid4()),  # ID do aluno
    "usuario_id": usuario_id,  # ID do usuário dono do aluno
    "nome": nome,
    "idade": idade,
    "plano": plano,
    "lista_de_exercicios": lista_de_exercicios
})

            salvar_alunos(alunos)
            flash("Aluno cadastrado com sucesso!")
            return redirect(url_for("gerenciar_alunos"))

    return render_template("alunos.html", alunos=alunos_exibidos)

# --- Rota para excluir aluno ---
@app.route("/excluir/<aluno_id>")
def excluir_aluno(aluno_id):
    if "usuario" not in session:
        return redirect(url_for("login"))

    alunos = carregar_alunos()
    alunos = [a for a in alunos if a["id"] != aluno_id]
    salvar_alunos(alunos)
    flash("Aluno excluído com sucesso!")
    return redirect(url_for("gerenciar_alunos"))

# --- Página de detalhes do aluno (com os exercícios específicos) ---
@app.route("/detalhes/<aluno_id>")
def detalhes_aluno(aluno_id):
    if "usuario" not in session:
        return redirect(url_for("login"))

    alunos = carregar_alunos()
    aluno = next((a for a in alunos if a["id"] == aluno_id), None)
    usuario_id = session.get("id")

    if not aluno or aluno.get("usuario_id") != usuario_id:
     flash("Acesso não autorizado ou aluno não encontrado!")
     return redirect(url_for("gerenciar_alunos"))


    # Mapear a lista de exercícios para o aluno
    lista_exercicios = exercicios.get(int(aluno["lista_de_exercicios"]), [])

    return render_template("detalhes_aluno.html", aluno=aluno, lista_exercicios=lista_exercicios)


# --- Início da aplicação ---
if __name__ == "__main__":
    app.run(debug=True)

import json

# Caminho para o arquivo de alunos
ARQUIVO_ALUNOS = "alunos.json"

# ID fictício para todos os alunos (substitua com IDs reais de usuários se quiser)
USUARIO_ID_FICTICIO = "usuario-exemplo-123"

def atualizar_alunos_com_usuario_id():
    try:
        with open(ARQUIVO_ALUNOS, "r", encoding="utf-8") as f:
            alunos = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        print("Erro ao carregar alunos.json")
        return

    # Atualiza cada aluno, se ainda não tiver o campo 'usuario_id'
    for aluno in alunos:
        if "usuario_id" not in aluno:
            aluno["usuario_id"] = USUARIO_ID_FICTICIO

    # Salva de volta no arquivo
    with open(ARQUIVO_ALUNOS, "w", encoding="utf-8") as f:
        json.dump(alunos, f, indent=4, ensure_ascii=False)

    print("Arquivo alunos.json atualizado com sucesso!")

# Executa a função
if __name__ == "__main__":
    atualizar_alunos_com_usuario_id()


from werkzeug.security import generate_password_hash
print(generate_password_hash("1234"))

from werkzeug.security import generate_password_hash
import json

usuario = {
    "id": "admin1234",
    "usuario": "admin",
    "senha": generate_password_hash("1234")
}

with open("usuarios.json", "w", encoding="utf-8") as f:
    json.dump([usuario], f, indent=4, ensure_ascii=False)

print("Usuário salvo com sucesso.")
