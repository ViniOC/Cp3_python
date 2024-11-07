from flask import Flask, request, jsonify
import negocio

app = Flask(__name__)

@app.route("/pizzas", methods = ["GET"])
def get_all_pizzas():
    pizzas = negocio.banco.lista_pizza()
    print(pizzas)
    pizzas_mapeadas = [{'id' : pizzas[i][0],'sabor': pizzas[i][1], 'tamanho': pizzas[i][2], 'observacao': pizzas [i][3]} for i in range(len(pizzas))]
    return jsonify (pizzas_mapeadas)


@app.route("/vendas", methods = ["GET"])
def get_all_vendas():
    vendas = negocio.banco.lista_venda_pizza()
    print(vendas)
    vendas_mapeadas = [{'id' : vendas[i][0],'id_pizza': vendas[i][1], 'descrição venda': vendas[i][2], 'valor': vendas [i][3], 'data venda': vendas[i][4]} for i in range(len(vendas))]
    return jsonify (vendas_mapeadas)


app.run(debug = True)