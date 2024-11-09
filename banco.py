# banco.py
import oracledb



def get_connection():
    return oracledb.connect(user= 'rm556182', password='101003',
                            dsn = "oracle.fiap.com.br/orcl")
    

def lista_pizza():
    sql = ''' select * from t_pizza '''
    with get_connection() as con:
        with con.cursor() as cur:
            cur.execute(sql)
            dado = cur.fetchall()
            # if not dado:
            #     print("Nenhuma Pizza cadastrada.")
            # else:
            #     print("Pizzas cadastradas:")
            #     for dados in dado:
            #         print(f"ID: {dados[0]}, Sabor: {dados[1]}, Tamanho: {dados[2]}, Observação: {dados[3]}")
            return dado




def lista_venda_pizza():
    sql = ''' select * from t_venda_pizza '''
    with get_connection() as con:
        with con.cursor() as cur:
            cur.execute(sql)
            dado = cur.fetchall()
            # if not dado:
            #     print("Nenhuma venda cadastrada.")
            # else:
            #     print("Vendas cadastradas:")
            #     for dados in dado:
            #         valor = dados[3] if dados[3] is not None else 0.00  # Substituir None por 0.00
            #         print(f"ID: {dados[0]}, ID Pizza: {dados[1]}, Descrição: {dados[2]}, Valor: R${valor:.2f}, Data: {dados[4]}")
            return dado


def seleciona_pizza(sabor: str):
    sql = '''
    SELECT id, sabor, tamanho, obs FROM t_pizza WHERE sabor LIKE :sabor
    '''
    
    with get_connection() as con:
        with con.cursor() as cur:
            cur.execute(sql, {'sabor': f'%{sabor}%'})  # Usa o operador LIKE para buscar por sabores que contenham o termo
            return cur.fetchall()



def seleciona_venda(id: int) -> dict:
    sql = ''' select * from t_venda_pizza where id = :id '''
    with get_connection() as con:
        with con.cursor() as cur:   
            cur.execute(sql, {'id': id})  # Corrigido o parâmetro para 'id'
            dado = cur.fetchone()
        if not dado:
            print("Venda não encontrada.")
            return None
        else:
            print(f"Venda encontrada: ID: {dado[0]}, ID Pizza: {dado[1]}, Descrição: {dado[2]}, Valor: R${dado[3]:.2f}, Data: {dado[4]}")
            return {'id': dado[0], 'id_pizza': dado[1],
                    'ds_venda': dado[2], 'valor': dado[3], 
                    'dt_venda': dado[4]}



def insere_pizza(pizza: dict):
    sql = ''' 
    insert into t_pizza (id, sabor, tamanho, obs) 
    values(:id, :sabor, :tamanho, :obs)
    '''
    
    with get_connection() as con:
        with con.cursor() as cur:
            # Obtém o próximo valor da sequência de ID
            new_id = cur.var(oracledb.NUMBER)
            cur.execute("SELECT seq_t_pizza.NEXTVAL FROM dual")
            new_id = cur.fetchone()[0]
            
            # Atualiza o dicionário com o ID obtido
            pizza['id'] = new_id
            
            # Executa o comando de inserção com o novo ID
            cur.execute(sql, pizza)
            
        con.commit()
    
    return pizza


def insere_venda(venda: dict):
    sql = ''' 
    INSERT INTO t_venda_pizza (id_pizza, ds_venda, valor, dt_venda) 
    VALUES (:id_pizza, :ds_venda, :valor, TO_DATE(:dt_venda, 'DD-MM-YYYY'))
    '''
    
    with get_connection() as con:
        with con.cursor() as cur:
            # Obtém o próximo valor da sequência para o ID da venda
            cur.execute("SELECT seq_t_venda_pizza.NEXTVAL FROM dual")
            new_id = cur.fetchone()[0]
            
            # Atribui o novo ID ao dicionário de venda
            venda['id'] = new_id
            
            # Executa a inserção (o ID não precisa estar na SQL)
            cur.execute(sql, {
                "id_pizza": venda["id_pizza"],
                "ds_venda": venda["ds_venda"],
                "valor": venda["valor"],
                "dt_venda": venda["dt_venda"]  # Certifique-se de que a data está no formato 'DD-MM-YYYY'
            })
        
        con.commit()
    
    # Retorna o dicionário de venda com o novo ID atribuído
    return venda






def atualiza_pizza(id_pizza, sabor, tamanho, obs=None):
    # Preparar os dados
    pizza = {
        'id': id_pizza,
        'sabor': sabor.lower(),
        'tamanho': tamanho.upper(),
        'obs': obs.lower() if obs else None
    }

    # SQL de atualização
    sql = ''' 
    UPDATE t_pizza 
    SET sabor = :sabor, tamanho = :tamanho
    '''
    
    # Adiciona a coluna obs apenas se for fornecida
    if pizza['obs']:
        sql += ', obs = :obs'
    
    # Finaliza a cláusula WHERE
    sql += ' WHERE id = :id'

    # Executar a atualização no banco de dados
    with get_connection() as con:
        with con.cursor() as cur:
            cur.execute(sql, pizza)
        con.commit()

    print("Pizza atualizada com sucesso!")




def atualiza_venda():

    lista_venda_pizza()

    id_venda = input("Informe o ID da venda a ser atualizada: ")

    id_pizza = input("Informe o novo ID da pizza (ID de uma pizza existente): ")
    ds_venda = input("Informe a nova descrição da venda: ")
    valor = input("Informe o novo valor total da venda (ex: 34,99): ")
    dt_venda = input("Informe a nova data da venda (dd-mm-yyyy): ")

    venda = {
        'id': id_venda,
        'id_pizza': id_pizza,
        'ds_venda': ds_venda,
        'valor': valor,
        'dt_venda': dt_venda
    }

    sql = ''' 
    UPDATE t_venda_pizza 
    SET id_pizza = :id_pizza, ds_venda = :ds_venda, valor = :valor, dt_venda = TO_DATE(:dt_venda, 'DD-MM-YYYY')
    ''' 

    sql += ' WHERE id = :id'

    with get_connection() as con:
        with con.cursor() as cur:
            cur.execute(sql, venda)
        con.commit()

    print("Venda atualizada com sucesso!")

def delete_pizza(pizza_id: int):
    sql = '''
    DELETE FROM t_pizza WHERE id = :id
    '''
    
    with get_connection() as con:
        with con.cursor() as cur:
            # Executa o comando de exclusão com o id fornecido
            cur.execute(sql, {'id': pizza_id})
        
        con.commit()
    
    return {'message': f'Pizza com ID {pizza_id} deletada com sucesso'}
