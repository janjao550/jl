# atualizar_alunos.py
import json

ARQUIVO_ALUNOS = "alunos.json"
USUARIO_ID_FICTICIO = "admin1234"

def atualizar_alunos_com_usuario_id():
    try:
        with open(ARQUIVO_ALUNOS, "r", encoding="utf-8") as f:
            alunos = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        print("Erro ao carregar alunos.json")
        return

    for aluno in alunos:
        if "usuario_id" not in aluno:
            aluno["usuario_id"] = USUARIO_ID_FICTICIO

    with open(ARQUIVO_ALUNOS, "w", encoding="utf-8") as f:
        json.dump(alunos, f, indent=4, ensure_ascii=False)

    print("Arquivo alunos.json atualizado com sucesso!")

if __name__ == "__main__":
    atualizar_alunos_com_usuario_id()
