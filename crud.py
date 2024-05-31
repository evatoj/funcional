import json
import os

ARQUIVO_DADOS = 'cadastros.json'


def carregar_dados():
    if os.path.exists(ARQUIVO_DADOS):
        with open(ARQUIVO_DADOS, 'r') as arquivo:
            return json.load(arquivo)
    return []


def salvar_dados(dados):
    with open(ARQUIVO_DADOS, 'w') as arquivo:
        json.dump(dados, arquivo, indent=4)


def inserir_contato():
    nome = input("Insira o nome: ")
    email = input("Insira o e-mail: ")
    telefone = input("Insira o telefone: ")
    dados = carregar_dados()
    novo_contato = {
        'id': len(dados) + 1,
        'nome': nome,
        'email': email,
        'telefone': telefone
    }
    dados.append(novo_contato)
    salvar_dados(dados)
    print("Contato adicionado.")


def editar_contato():
    id = int(input("Insira o ID do contato a ser editado: "))
    dados = carregar_dados()
    for contato in dados:
        if contato['id'] == id:
            contato['nome'] = input("Insira o novo nome: ")
            contato['email'] = input("Insira o novo e-mail: ")
            contato['telefone'] = input("Insira o novo telefone: ")
            salvar_dados(dados)
            print("Contato atualizado.")
            return
    print("Contato não encontrado.")


def pesquisar_por_nome():
    nome = input("Insira o nome a ser pesquisado: ")
    dados = carregar_dados()
    resultados = [
        contato for contato in dados if contato['nome'].lower() == nome.lower()]
    if resultados:
        for contato in resultados:
            print(f"ID: {contato['id']}, Nome: {
                  contato['nome']}, E-mail: {contato['email']}, Telefone: {contato['telefone']}")
    else:
        print("Nenhum contato encontrado com esse nome.")


def remover_contato():
    id = int(input("Insira o ID do contato a ser removido: "))
    dados = carregar_dados()
    dados = [contato for contato in dados if contato['id'] != id]
    salvar_dados(dados)
    print("Contato removido.")


def exibir_todos():
    dados = carregar_dados()
    if not dados:
        print("Nenhum contato cadastrado ainda.")
    else:
        for contato in dados:
            print(f"ID: {contato['id']}, Nome: {
                  contato['nome']}, E-mail: {contato['email']}, Telefone: {contato['telefone']}")


def exibir_um():
    id = int(input("Insira o ID do contato a ser exibido: "))
    dados = carregar_dados()
    for contato in dados:
        if contato['id'] == id:
            print(f"ID: {contato['id']}, Nome: {
                  contato['nome']}, E-mail: {contato['email']}, Telefone: {contato['telefone']}")
            return
    print("Contato não encontrado.")


def menu():
    while True:
        print("\n1. Inserir Contato")
        print("2. Editar Contato")
        print("3. Pesquisar por Nome")
        print("4. Remover Contato")
        print("5. Exibir Todos os Contatos")
        print("6. Buscar Contato por ID")
        print("7. Sair")
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            inserir_contato()
        elif escolha == '2':
            editar_contato()
        elif escolha == '3':
            pesquisar_por_nome()
        elif escolha == '4':
            remover_contato()
        elif escolha == '5':
            exibir_todos()
        elif escolha == '6':
            exibir_um()
        elif escolha == '7':
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    menu()
