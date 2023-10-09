from flask import Flask, request, jsonify
import oracledb
import json

app = Flask(__name__)

# Configurações de conexão com o banco de dados Oracle
db_user = 'rm551211'
db_password = 'fiap23'
db_dsn = 'oracle.fiap.com.br/orcl'

# Função para criar uma conexão com o banco de dados
def conectar_bd():
    try:
        connection = oracledb.connect(user=db_user, password=db_password, dsn=db_dsn)
        return connection
    except oracledb.DatabaseError as error:
        raise Exception(f"Erro ao conectar ao banco de dados: {error}")

# Classe de modelo para animais
class Animal:
    def __init__(self, id, nome, especie, peso, data_nascimento):
        self.id = id
        self.nome = nome
        self.especie = especie
        self.peso = peso
        self.data_nascimento = data_nascimento

# Rota para criar um novo animal
@app.route('/animais', methods=['POST'])
def criar_animal():
    try:
        data = request.json
        novo_animal = Animal(None, data['nome'], data['especie'], data['peso'], data['data_nascimento'])

        with conectar_bd() as connection:
            with connection.cursor() as cursor:
                # Executar a inserção sem fornecer um valor para o ID
                cursor.execute("INSERT INTO animais (nome, especie, peso, data_nascimento) VALUES (:nome, :especie, :peso, TO_DATE(:data_nascimento, 'YYYY-MM-DD')) RETURNING id INTO :new_id",
                               nome=novo_animal.nome, especie=novo_animal.especie, peso=novo_animal.peso, data_nascimento=novo_animal.data_nascimento, new_id=novo_animal.id)

        return jsonify({'message': 'Animal criado com sucesso', 'id': novo_animal.id}), 201

    except oracledb.DatabaseError as error:
        return jsonify({'error': str(error)}), 500
    except Exception as erro:
        return jsonify({'error': str(erro)}), 500


# Rota para listar todos os animais
@app.route('/animais', methods=['GET'])
def listar_animais():
    try:
        with conectar_bd() as connection:
            with connection.cursor() as cursor:
                # Executar a consulta
                cursor.execute("SELECT id, nome, especie, peso, TO_CHAR(data_nascimento, 'YYYY-MM-DD') FROM animais")
                resultado = cursor.fetchall()

        animais = []
        for row in resultado:
            animal = Animal(id=row[0], nome=row[1], especie=row[2], peso=row[3], data_nascimento=row[4])
            animais.append(animal.__dict__)

            # Converter a lista de animais em JSON com codificação UTF-8
        json_animais = json.dumps(animais, ensure_ascii=False).encode('utf-8').decode('utf-8')


        return jsonify(animais), 200

    except oracledb.DatabaseError as error:
        return jsonify({'error': str(error)}), 500
    except Exception as erro:
        return jsonify({'error': str(erro)}), 500

# Rota para buscar um animal por ID
@app.route('/animais/<int:id>', methods=['GET'])
def buscar_animal_por_id(id):
    try:
        with conectar_bd() as connection:
            with connection.cursor() as cursor:
                # Executar a consulta
                cursor.execute("SELECT id, nome, especie, peso, TO_CHAR(data_nascimento, 'YYYY-MM-DD') FROM animais WHERE id = :id", id=id)
                resultado = cursor.fetchone()

        if resultado:
            animal = Animal(id=resultado[0], nome=resultado[1], especie=resultado[2], peso=resultado[3], data_nascimento=resultado[4])
            return jsonify(animal.__dict__), 200
        else:
            return jsonify({'message': 'Animal não encontrado'}), 404

    except oracledb.DatabaseError as error:
        return jsonify({'error': str(error)}), 500
    except Exception as erro:
        return jsonify({'error': str(erro)}), 500


        # Rota para atualizar um animal por ID
@app.route('/animais/<int:id>', methods=['PUT'])
def atualizar_animal_por_id(id):
    try:
        data = request.json
        animal_atualizado = Animal(id, data['nome'], data['especie'], data['peso'], data['data_nascimento'])

        with conectar_bd() as connection:
            with connection.cursor() as cursor:
                # Verificar se o animal com o ID especificado existe
                cursor.execute("SELECT id FROM animais WHERE id = :id", id=id)
                resultado = cursor.fetchone()

                if not resultado:
                    return jsonify({'error': 'Animal não encontrado'}), 404

                # Atualizar o animal com os novos dados
                cursor.execute("UPDATE animais SET nome = :nome, especie = :especie, peso = :peso, data_nascimento = TO_DATE(:data_nascimento, 'YYYY-MM-DD') WHERE id = :id",
                               nome=animal_atualizado.nome, especie=animal_atualizado.especie, peso=animal_atualizado.peso, data_nascimento=animal_atualizado.data_nascimento, id=id)

        return jsonify({'message': 'Animal atualizado com sucesso', 'id': id}), 200

    except oracledb.DatabaseError as error:
        return jsonify({'error': str(error)}), 500
    except Exception as erro:
        return jsonify({'error': str(erro)}), 500

        # Rota para excluir um animal por ID
@app.route('/animais/<int:id>', methods=['DELETE'])
def excluir_animal_por_id(id):
    try:
        with conectar_bd() as connection:
            with connection.cursor() as cursor:
                # Verificar se o animal com o ID especificado existe
                cursor.execute("SELECT id FROM animais WHERE id = :id", id=id)
                resultado = cursor.fetchone()

                if not resultado:
                    return jsonify({'error': 'Animal não encontrado'}), 404

                # Excluir o animal com o ID especificado
                cursor.execute("DELETE FROM animais WHERE id = :id", id=id)

        return jsonify({'message': 'Animal excluído com sucesso', 'id': id}), 200

    except oracledb.DatabaseError as error:
        return jsonify({'error': str(error)}), 500
    except Exception as erro:
        return jsonify({'error': str(erro)}), 500



if __name__ == '__main__':
    app.run(debug=True)
