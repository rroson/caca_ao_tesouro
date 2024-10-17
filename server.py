from flask import Flask, jsonify, request, send_from_directory, render_template
import folium
import random

app = Flask(__name__)

# Posições iniciais
equipes = {
    "equipe1": [-23.5505, -46.6333],
    "equipe2": [-23.5595, -46.6403]
}
cores_equipes = ['darkred', 'white', 'gray', 'pink', 'darkgreen', 'black',
          'beige', 'purple', 'orange', 'lightgray', 'green', 'darkblue',
          'blue', 'darkpurple', 'lightblue', 'lightgreen', 'cadetblue', 'lightred']
tesouro = [-23.5650, -46.6425]

# Função paraSortear Cor das Equipes
def sortear_e_remover(cores):
    if not cores:
        return "Todas as cores já foram sorteadas!"  # Caso a lista esteja vazia
    cor_sorteada = random.choice(cores)  # Sorteia uma cor
    cores.remove(cor_sorteada)  # Remove a cor sorteada da lista
    return cor_sorteada

# Função para gerar o mapa
def gerar_mapa():
    mapa = folium.Map(location=[-23.5505, -46.6333], zoom_start=2)
    
    # Adicionar marcadores das equipes
    for equipe, posicao in equipes.items():
        cor_equipe = sortear_e_remover(cores_equipes)
        folium.Marker(location=posicao, popup=equipe, icon=folium.Icon(color=cor_equipe)).add_to(mapa)
    
    mapa.save("static/caca_ao_tesouro.html")
    
    # Adicionar o tesouro
    folium.Marker(location=tesouro, popup="Tesouro", icon=folium.Icon(color="red")).add_to(mapa)
    
    # Salvar o mapa
    mapa.save("static/caca_ao_tesouro_server.html")

# Mostrar mapa atualizado em /
@app.route('/', methods=['GET', 'POST'])
def mostrar_mapa():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == 'linus123':
            return send_from_directory('static', 'caca_ao_tesouro_server.html')
        else:
            return "Senha incorreta", 401
    return render_template('login.html')


# Rota para atualizar posição
@app.route('/atualizar', methods=['POST'])
def atualizar_posicao():
    dados = request.get_json()
    equipe = dados['equipe']
    nova_posicao = dados['posicao']
    
    # Atualizar a posição da equipe
    if equipe in equipes:
        equipes[equipe] = nova_posicao
        gerar_mapa()  # Gerar um novo mapa com as posições atualizadas
        return jsonify({"status": "Posição atualizada!"})
    return jsonify({"status": "Equipe não encontrada!"}), 404

# Rota para baixar o mapa atualizado
@app.route('/mapa')
def mapa_atualizado():
    return send_from_directory('static', 'caca_ao_tesouro.html')

if __name__ == "__main__":
    gerar_mapa()  # Gerar o mapa inicial
    app.run(debug=False)
