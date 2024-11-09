from flask import Flask, request, jsonify
import negocio
from datetime import datetime
app = Flask(__name__)


# {
#   "sabor": "Mussarela",
#   "tamanho": "G",
#   "observacao": "Com borda recheada"
# }

@app.route("/cadastropizza", methods=["POST"])
def post_pizza():
    pizzas = request.json 

    if not isinstance(pizzas, list) or not all(isinstance(pizza, dict) for pizza in pizzas):
        return jsonify({"error": "Formato de dados incorreto. Esperado uma lista de dicionários"}), 400

    pizzas_mapeadas = []
    
    for pizza in pizzas:
        sabor = pizza.get("sabor")
        tamanho = pizza.get("tamanho")
        observacao = pizza.get("observacao")

        if not sabor or not tamanho:
            return jsonify({"error": "Campos 'sabor' e 'tamanho' são obrigatórios"}), 400

        try:
            negocio.cadastrar_pizza(sabor, tamanho, observacao)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

        pizzas_mapeadas.append({
            'sabor': sabor,
            'tamanho': tamanho,
            'observacao': observacao
        })

    return jsonify(pizzas_mapeadas), 200

# http://127.0.0.1:5000/pizzas
@app.route("/pizzas", methods = ["GET"])
def get_all_pizzas():
    pizzas = negocio.banco.lista_pizza()
    print(pizzas)
    pizzas_mapeadas = [{'id' : pizzas[i][0],'sabor': pizzas[i][1], 'tamanho': pizzas[i][2], 'observacao': pizzas [i][3]} for i in range(len(pizzas))]
    return jsonify (pizzas_mapeadas)

# GET http://127.0.0.1:5000/sabor?sabor=mussarela

@app.route("/sabor", methods=["GET"])
def get_pizzas_by_sabor():
    sabor = request.args.get('sabor')  
    if sabor:
        pizzas = negocio.banco.seleciona_pizza(sabor)  
    else:
        pizzas = negocio.banco.lista_pizza()  

    pizzas_mapeadas = [
        {'id': pizzas[i][0], 'sabor': pizzas[i][1], 'tamanho': pizzas[i][2], 'observacao': pizzas[i][3]}
        for i in range(len(pizzas))
    ]
    
    return jsonify(pizzas_mapeadas)

# http://127.0.0.1:5000/apagapizza/30
@app.route("/apagapizza/<int:pizza_id>", methods=["DELETE"])
def delete_pizza(pizza_id):
    try:
        result = negocio.banco.delete_pizza(pizza_id)
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
    
#     {
#   "sabor": "Mussarela",
#   "tamanho": "G",
#   "observacao": "Com borda recheada"
# }


@app.route("/atualizapizza/<int:pizza_id>", methods=["PUT"])
def update_pizza(pizza_id):
    try:
        # Recebe os dados da requisição
        data = request.get_json()
        
        sabor = data.get('sabor')
        tamanho = data.get('tamanho')
        obs = data.get('observacao', '')  # Caso a observação não seja fornecida, assume-se uma string vazia

        # Valida os dados (se necessário)
        if not sabor or not tamanho:
            return jsonify({"error": "Sabor e tamanho são obrigatórios"}), 400

        # Chama a função de atualização na classe banco
        negocio.banco.atualiza_pizza(pizza_id, sabor, tamanho, obs)

        return jsonify({"message": "Pizza atualizada com sucesso!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500




@app.route("/inserevendas", methods=["POST"])
def post_venda():
    venda = request.json

    required_fields = ["id_pizza", "ds_venda", "valor", "dt_venda"]
    if not all(field in venda for field in required_fields):
        return jsonify({"error": "Todos os campos ('id_pizza', 'ds_venda', 'valor', 'dt_venda') são obrigatórios"}), 400

    try:
        result = negocio.banco.insere_venda(venda)
        return jsonify(result), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

app.run(debug=True)
# {
#   "id_pizza": 4,
#   "ds_venda": "Venda de pizza de 4 queijos",
#   "valor": 42.00,
#   "dt_venda": "09-11-2024"
# }

# o insomnia nao encontra, o metodo esta funcionando, mas nao retorna na api, tentei resolver mas infelizmente nao consegui.
@app.route("/listavendas", methods=["GET"])
def get_all_vendas():
    vendas = negocio.banco.lista_venda_pizza()
    
    if not vendas:
        return jsonify([])  
    
    vendas_mapeadas = []
    for venda in vendas:
        venda_data = venda[4]  
    
        if isinstance(venda_data, datetime):
            venda_data = venda_data.strftime('%d-%m-%Y') 
        
        venda_map = {
            'id': venda[0],
            'id_pizza': venda[1],
            'descrição venda': venda[2],
            'valor': venda[3],
            'data venda': venda_data
        }
        
        vendas_mapeadas.append(venda_map)
    
    return jsonify(vendas_mapeadas)


app.run(debug = True)