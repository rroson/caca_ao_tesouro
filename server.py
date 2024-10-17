from flask import Flask, jsonify, request, send_from_directory, render_template
import folium
import random
import math

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
posicoes_iniciais = equipes.copy() # Armazena as posições iniciais

# Sortear cor
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

# Calcula a distância entre dois pontos
def distancia(ponto1, ponto2):
    lat1, lon1 = ponto1
    lat2, lon2 = ponto2
    radius = 6371  # Radius of the earth in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) * math.sin(dlon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = radius * c
    return distance

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
        
        # Calcular e retornar a distância
        distancia_atual = distancia(nova_posicao, tesouro)
        distancia_inicial = distancia(posicoes_iniciais[equipe], tesouro)
        
        if distancia_atual < distancia_inicial:
            mensagem_distancia = "A distância até o tesouro diminuiu!"
        elif distancia_atual > distancia_inicial:
            mensagem_distancia = "A distância até o tesouro aumentou!"
        else:
            mensagem_distancia = "A distância até o tesouro permanece a mesma."
        
        return jsonify({"status": "Posição atualizada!", "mensagem_distancia": mensagem_distancia})
    return jsonify({"status": "Equipe não encontrada!"}), 404

# Rota para baixar o mapa atualizado
@app.route('/mapa')
def mapa_atualizado():
    return send_from_directory('static', 'caca_ao_tesouro.html')

if __name__ == "__main__":
    gerar_mapa()  # Gerar o mapa inicial
    app.run(debug=False)
