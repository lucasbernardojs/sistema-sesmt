from flask import Flask, request, jsonify, render_template
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# CONEXÃO COM GOOGLE SHEETS
scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("credenciais.json", scope)
client = gspread.authorize(creds)

planilha = client.open("ControleEPIS_BD")

aba_lancamentos = planilha.worksheet("Lançamentos")
aba_dados = planilha.worksheet("Dados")
aba_estoque = planilha.worksheet("Estoque")

# ABRIR SISTEMA
@app.route('/')
def index():
    return render_template('index.html')

# SALVAR LANÇAMENTO
@app.route('/salvar', methods=['POST'])
def salvar():
    dados = request.json

    aba_lancamentos.append_row([
        dados['base'],
        dados['data'],
        dados['hora'],
        dados['matricula'],
        dados['colaborador'],
        dados['cargo'],
        dados['epi'],
        dados['quantidade'],
        dados['turno'],
        dados['responsavel']
    ])

    return jsonify({"status": "ok"})

# BUSCAR COLABORADOR
@app.route('/buscar-colaborador/<matricula>')
def buscar_colaborador(matricula):
    dados = aba_dados.get_all_values()

    for i in range(1, len(dados)):
        if dados[i][0] == matricula:
            return jsonify({
                "colaborador": dados[i][1],
                "cargo": dados[i][2]
            })

    return jsonify(None)

# BUSCAR ESTOQUE
@app.route('/estoque')
def estoque():
    dados = aba_estoque.get_all_values()
    dados.pop(0)
    return jsonify(dados)

if __name__ == '__main__':
    app.run(debug=True)
    
    import os

port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)