from flask import Flask, request, jsonify
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

def validar_cpf(cpf: str) -> bool:
    if len(cpf) != 11 or not cpf.isdigit():
        return False
    
    soma = 0
    for i in range(9):
        soma += int(cpf[i]) * (10 - i)
    digito1 = 11 - (soma % 11)
    if digito1 >= 10:
        digito1 = 0
    
    soma = 0
    for i in range(10):
        soma += int(cpf[i]) * (11 - i)
    digito2 = 11 - (soma % 11)
    if digito2 >= 10:
        digito2 = 0
    
    return cpf[-2:] == f"{digito1}{digito2}"

@app.route('/')
def home():
    return "Bem-vindo à API de Verificação de CPF! Acesse /verificar-cpf?cpf=xxx para verificar um CPF."

@app.route('/verificar-cpf', methods=['GET'])
def verificar_cpf():
    """
    Verifica se o CPF fornecido é válido
    ---
    parameters:
      - name: cpf
        in: query
        type: string
        required: true
        description: O CPF a ser validado
    responses:
      200:
        description: CPF válido ou inválido
        schema:
          type: object
          properties:
            valido:
              type: boolean
              example: true
    """
    cpf = request.args.get('cpf')
    if cpf is None:
        return jsonify({"erro": "CPF não fornecido"}), 400
    
    valido = validar_cpf(cpf)
    return jsonify({"valido": valido})

if __name__ == '__main__':
    app.run(debug=True)
