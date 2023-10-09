import oracledb

# Configurações de conexão com o banco de dados Oracle
db_user = 'rm551211'
db_password = 'fiap23'
db_dsn = 'oracle.fiap.com.br/orcl'

def conectar_bd():
    try:
        connection = oracledb.connect(user=db_user, password=db_password, dsn=db_dsn)
        return connection
    except oracledb.DatabaseError as error:
        raise Exception(f"Erro ao conectar ao banco de dados: {error}")

def consulta_todos_animais():
    try:
        with oracledb.connect(user=db_user, password=db_password, dsn=db_dsn) as con:
            with con.cursor() as cur:
                sql = "SELECT * FROM animais"
                cur.execute(sql)
                return cur.fetchall()
            
    except Exception as erro:
        print("Erro na consulta de animais: ", erro)
        raise erro

def inserir_animal(animal):
    try:
        with oracledb.connect(user=db_user, password=db_password, dsn=db_dsn) as con:
            with con.cursor() as cur:
                sql = '''
                    INSERT INTO animais (id, nome, especie, peso, data_nascimento)
                    VALUES (:id, :nome, :especie, :peso, TO_DATE(:data_nascimento, 'YYYY-MM-DD'))
                '''
                cur.execute(sql, animal)
            
            con.commit()
    except Exception as erro:
        print("Erro ao inserir animal: ", erro)
        raise erro

def atualizar_animal(id, animal_atualizado):
    try:
        with conectar_bd() as con:
            with con.cursor() as cur:
                sql = '''
                    UPDATE animais
                    SET nome = :nome, especie = :especie, peso = :peso, data_nascimento = TO_DATE(:data_nascimento, 'YYYY-MM-DD')
                    WHERE id = :id
                '''
                cur.execute(sql, id=id, nome=animal_atualizado['nome'], especie=animal_atualizado['especie'], peso=animal_atualizado['peso'], data_nascimento=animal_atualizado['data_nascimento'])
            con.commit()
    except Exception as erro:
        print("Erro ao atualizar animal: ", erro)
        raise erro

def excluir_animal(id):
    try:
        with conectar_bd() as con:
            with con.cursor() as cur:
                sql = "DELETE FROM animais WHERE id = :id"
                cur.execute(sql, id=id)
            con.commit()
    except Exception as erro:
        print("Erro ao excluir animal: ", erro)
        raise erro

# Exemplo de uso:
# animal = {"id": 1, "nome": "Leão", "especie": "Felidae", "peso": 150.5, "data_nascimento": "2020-05-10"}
# inserir_animal(animal)
# dados_animais = consulta_todos_animais()
# print(dados_animais)
