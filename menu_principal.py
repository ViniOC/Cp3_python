# menu_principal.py
import negocio


def print_header(title):
    print("\n" + "=" * 30)
    print(f"{title}".center(30))
    print("=" * 30)

def menu_pizza():
    while True:
        print_header("Gerenciador Pizzas.")
        print("1. Cadastrar Pizza.")
        print("2. Listar todas as Pizza.")
        print("3. Listar pizza por nome.")
        print("4. Editar Pizza.")
        print("0. Voltar.")
        opcao = int (input("Escolha uma opção: \n"))
        
        if opcao == 1:
            sabor = input("Sabor da Pizza: ")
            tamanho = input("Tamanho da Pizza(P, M ou G): ")
            obss = input("Alguma observação ?s/n ")
            obss.lower()
            if obss == "s":
                obs = input("Informe a obervação da sua pizza: ")
            else:
                obs = ""
            
            negocio.cadastrar_pizza(sabor, tamanho, obs)
        elif opcao == 2:
            negocio.banco.lista_pizza()
        elif opcao == 3:
            nome = input("informe o sabor da pizza que deseja buscar: ")
            negocio.banco.seleciona_pizza(nome)
        elif opcao == 4: 
            negocio.banco.atualiza_pizza()
        elif opcao == 0:
            break
        else:
            print("opção invalida!")

def menu_venda():
    while True:
        print_header("Gerenciador Vendas.")
        print("1. Cadastrar Venda.")
        print("2. Listar todas as Vendas.")
        print("3. Listar Vendas por id.")
        print("4. Editar Venda.")
        print("0. Voltar.")
        opcao = int (input("Escolha uma opção: \n"))
        
        if opcao == 1:
            sabor = input("Digite o sabor da pizza para a venda: ")
            id_pizza = negocio.get_pizza_id(sabor)
            ds_venda = input("Descreva a venda: ")
            valor = input("Valor total da venda (00,00): R$")
            dt_venda = input("Informe a data da venda (dd-mm-yyyy): ")
            negocio.cadastra_venda(id_pizza, ds_venda, valor, dt_venda)
        elif opcao == 2:
            negocio.banco.lista_venda_pizza()
        elif opcao == 3:
            
            id= input("insira o id da venda que deseja selecionar: ")
            negocio.banco.seleciona_venda(id)
        elif opcao==4:
            negocio.banco.atualiza_venda()
        elif opcao == 0:
            break
        else:
            print("opção invalida!")
            

def menu_principal():
    while True:
        print_header("Pizzaria")
        print("1. Gerenciar pizza ")
        print("2. Gerenciar Venda")
        print("0. Encerrar")
        opcao = int (input("Escolha uma opção: \n"))
        
        
        if opcao == 1:
            menu_pizza()
        elif opcao == 2:
            menu_venda()
        elif opcao == 0:
            print("saindo...")
            break
        else:
            print("opção invalida")