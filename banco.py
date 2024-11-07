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
            if not dado:
                print("Nenhuma Pizza cadastrada.")
            else:
                print("Pizzas cadastradas:")
                for dados in dado:
                    print(f"ID: {dados[0]}, Sabor: {dados[1]}, Tamanho: {dados[2]}, Observação: {dados[3]}")




def lista_venda_pizza():
    sql = ''' select * from t_venda_pizza '''
    with get_connection() as con:
        with con.cursor() as cur:
            cur.execute(sql)
            dado = cur.fetchall()
            if not dado:
                print("Nenhuma venda cadastrada.")
            else:
                print("Vendas cadastradas:")
                for dados in dado:
                    valor = dados[3] if dados[3] is not None else 0.00  # Substituir None por 0.00
                    print(f"ID: {dados[0]}, ID Pizza: {dados[1]}, Descrição: {dados[2]}, Valor: R${valor:.2f}, Data: {dados[4]}")


def seleciona_pizza(sabor: str) -> dict:
    sql = ''' select * from t_pizza where sabor = :sabor '''
    with get_connection() as con:
        with con.cursor() as cur:   
            cur.execute(sql, {'sabor': sabor})
            dado = cur.fetchone()
            if not dado:
                print("Nenhuma Pizza cadastrada.")
            else:
                print("Pizza cadastrada:")
                print(f"ID: {dado[0]}, Sabor: {dado[1]}, Tamanho: {dado[2]}, Observação: {dado[3]}")


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
    INSERT INTO t_venda_pizza (id, id_pizza, ds_venda, valor, dt_venda) 
    VALUES (:id, :id_pizza, :ds_venda, :valor, TO_DATE(:dt_venda, 'DD-MM-YYYY'))
    '''
    
    with get_connection() as con:
        with con.cursor() as cur:
            # Obtém o próximo valor da sequência para o ID da venda
            cur.execute("SELECT seq_t_venda_pizza.NEXTVAL FROM dual")
            new_id = cur.fetchone()[0]
            
            # Atribui o novo ID ao dicionário de venda
            venda['id'] = new_id
            
            # Executa a inserção com o novo ID e data formatada
            cur.execute(sql, venda)
        
        con.commit()
    
    return venda




def atualiza_pizza():
    lista_pizza()
    id_pizza = input("Informe o ID da pizza a ser atualizada: ")

    # Solicitar os novos dados para a pizza
    sabor = input("Informe o novo sabor da pizza: ")
    tamanho = input("Informe o novo tamanho da pizza (P, M ou G): ")
    obs = input("Informe a nova observação (deixe em branco se não houver alteração): ")
    sabor.lower()
    tamanho.upper()
    obs.lower()
    # Criar o dicionário com os dados fornecidos
    pizza = {
        'id': id_pizza,
        'sabor': sabor,
        'tamanho': tamanho
    }
    
    # Adicionar 'obs' ao dicionário apenas se o usuário não deixou em branco
    if obs:
        pizza['obs'] = obs

    # SQL de atualização
    sql = ''' 
    UPDATE t_pizza 
    SET sabor = :sabor, tamanho = :tamanho
    ''' 

    # Adicionar a cláusula de observação ao SQL, se a obs for fornecida
    if 'obs' in pizza:
        sql += ', obs = :obs'

    # Finalizar a cláusula WHERE
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
