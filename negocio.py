# negocio.py
import banco
from exception import PizzaNotFoundError



def cadastrar_pizza(sabor, tamanho, obs)-> dict:
    pizza = banco.seleciona_pizza(sabor)
    if pizza == None:
        pizza = {'sabor':sabor, 'tamanho':tamanho, 'obs': obs}
        banco.insere_pizza(pizza)
    return pizza

def cadastra_venda(id_pizza, ds_venda, valor, dt_venda) -> dict:
    
    
    venda = {'id_pizza': id_pizza, 'ds_venda': ds_venda, 'valor': valor, 'dt_venda': dt_venda}
    banco.insere_venda(venda)
    return venda


def get_pizza_id(sabor: str) -> int:
    pizza = banco.seleciona_pizza(sabor)
    if pizza:
        return pizza['id']
    else:
        raise PizzaNotFoundError(sabor)
