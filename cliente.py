import requests

url_atualizar = 'http://localhost:5000/atualizar'
url_mapa = 'http://localhost:5000/mapa'

# Nova posição da equipe 1 (exemplo de movimento)
nova_posicao = {"equipe": "equipe1", "posicao": [-22.975099, -46.833492]}

# Enviar a nova posição para o servidor
resposta = requests.post(url_atualizar, json=nova_posicao)

# Ver o status da atualização
print(resposta.json())

# Baixar o mapa atualizado
mapa = requests.get(url_mapa)
with open("caca_ao_tesouro_atualizado.html", 'wb') as f:
    f.write(mapa.content)

print("Mapa atualizado baixado!")
