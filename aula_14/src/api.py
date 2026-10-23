from flask import Flask, jsonify, abort, request
from flasgger import Swagger
import requests

app = Flask(__name__) 
swagger = Swagger(app)

URL_BASE = "https://www.fruityvice.com/api/fruit"

sucos = []
proximo_id = 1

##
@app.route('/frutas/<string:nome>', methods=['GET'])
def consultar_fruta(nome: str):
    """
    Consulta informações de uma fruta.
    ---
    parameters:
      - name: nome
        in: path
        type: string
        required: true
        description: Nome da fruta em inglês (ex. apple, banana).
    responses:
      200:
        description: Retorna nome, calorias e açúcar em português.
      404:
        description: Fruta não encontrada.
    """
    try:
        response = requests.get(f"{URL_BASE}/{nome.lower()}", timeout=10)
        
        if response.status_code == 404:
            abort(404, description="Fruta não encontrada.") 
            
        if response.status_code == 200:
            data = response.json()
            nutri = data.get("nutritions", {})
            
            result = {
                "nome": data.get("name"),
                "calorias": nutri.get("calories", 0),
                "acucar": nutri.get("sugar", 0)
            }
            return jsonify(result), 200 
            
        abort(response.status_code)
        
    except requests.exceptions.RequestException:
        abort(500)

##
@app.route('/sucos', methods=['POST'])
def cadastrar_suco():
    """
    Cadastra um novo suco.
    ---
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - nome
            - frutas
            - tem_gosto_de
          properties:
            nome:
              type: string
              example: Vitamina Tropical
            frutas:
              type: array
              items:
                type: string
              example: ["banana", "strawberry"]
            tem_gosto_de:
              type: string
              example: Tamarindo
    responses:
      201:
        description: Suco cadastrado.
      400:
        description: Falta informação obrigatória.
      404:
        description: Uma das frutas não foi encontrada.
    """
    global proximo_id, sucos 
    
    dados = request.json
    if not dados or not all(k in dados for k in ("nome", "frutas", "tem_gosto_de")):
        abort(400, description=" 'nome', 'frutas' e 'tem_gosto_de' são obrigatórios") 
        
    total_calorias = 0.0
    total_acucar = 0.0
    
    for fruta in dados["frutas"]:
        resposta = requests.get(f"{URL_BASE}/{fruta.lower()}", timeout=10)
        
        if resposta.status_code == 404:
            abort(404, description=f"'{fruta}' não foi encontrada.")
            
        if resposta.status_code == 200:
            nutri = resposta.json().get("nutritions", {})
            total_calorias += nutri.get("calories", 0)
            total_acucar += nutri.get("sugar", 0)
        else:
            abort(resposta.status_code, description=f"Erro ao buscar '{fruta}'.")

    novo_suco = {
        "id": proximo_id,
        "nome": dados["nome"],
        "frutas": dados["frutas"],
        "tem_gosto_de": dados["tem_gosto_de"],
        "total_calorias": round(total_calorias, 2),
        "total_acucar": round(total_acucar, 2)
    }
    
    sucos.append(novo_suco)
    proximo_id += 1
    
    return jsonify(novo_suco), 201

##
@app.route('/sucos', methods=['GET'])
def listar_sucos():
    """
    Lista todos os sucos.
    ---
    responses:
      200:
        description: Lista com todos os sucos e valores nutricionais.
    """
    return jsonify(sucos), 200 

##
@app.route('/sucos/<int:id>', methods=['PUT'])
def atualizar_suco(id: int):
    """
    Atualiza um suco.
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID do suco cadastrado.
      - in: body
        name: body
        schema:
          type: object
          properties:
            nome:
              type: string
            frutas:
              type: array
              items:
                type: string
            tem_gosto_de:
              type: string
    responses:
      200:
        description: Suco atualizado.
      404:
        description: Não encontrados.
    """
    global sucos
    
    suco = next((s for s in sucos if s['id'] == id), None)
    if suco is None:
        abort(404, description="Suco não encontrado.")
        
    dados = request.json or {}
    
    if "frutas" in dados:
        total_calorias = 0.0
        total_acucar = 0.0
        
        for fruta in dados["frutas"]:
            resposta = requests.get(f"{URL_BASE}/{fruta.lower()}", timeout=10)
            
            if resposta.status_code == 404:
                abort(404, description=f"'{fruta}' não encontrada.")
                
            if resposta.status_code == 200:
                nutri = resposta.json().get("nutritions", {})
                total_calorias += nutri.get("calories", 0)
                total_acucar += nutri.get("sugar", 0)
            else:
                abort(resposta.status_code)
                
        suco["frutas"] = dados["frutas"]
        suco["total_calorias"] = round(total_calorias, 2)
        suco["total_acucar"] = round(total_acucar, 2)
        
    suco["nome"] = dados.get("nome", suco["nome"])
    suco["tem_gosto_de"] = dados.get("tem_gosto_de", suco["tem_gosto_de"])
    
    return jsonify(suco), 200

##
if __name__ == '__main__':
    localhost = '127.0.0.1'
    port = 5000
    url_swagger = f"http://{localhost}:{port}/apidocs"
    
    print(f"\n[INFO] Swagger: {url_swagger}\n")
    
    app.run(host=localhost, port=port, debug=True)