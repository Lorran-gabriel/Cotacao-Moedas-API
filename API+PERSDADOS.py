import os
import requests
import sqlite3
from datetime import datetime

# Caminho fixo onde o banco será salvo
caminho_pasta = r"C:\Users\viana\OneDrive\Documentos\Python Scripts\Sistemas distribuídos e mobile\atv2"
os.makedirs(caminho_pasta, exist_ok=True)  # garante que a pasta exista

# Caminho completo do banco
caminho_bd = os.path.join(caminho_pasta, "bdcotacoes.db")

# URL da API de cotações
url = "https://api.hgbrasil.com/finance?key=fe302142"

# Faz a requisição e obtém os dados
response = requests.get(url)
data = response.json()

# Extrai as cotações (preço de compra)
dolar = data['results']['currencies']['USD']['buy']
euro = data['results']['currencies']['EUR']['buy']

# Mostra as cotações no terminal
print(f"Dólar (compra): R$ {dolar}")
print(f"Euro  (compra): R$ {euro}")

# Conecta (ou cria) o banco de dados
conn = sqlite3.connect(caminho_bd)
cursor = conn.cursor()

# Cria a tabela se não existir
cursor.execute('''
CREATE TABLE IF NOT EXISTS moedas (
    data TEXT,
    dolar REAL,
    euro REAL
)
''')

# Insere os dados atuais
data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
cursor.execute("INSERT INTO moedas (data, dolar, euro) VALUES (?, ?, ?)",
               (data_atual, dolar, euro))

# Salva e fecha a conexão
conn.commit()
conn.close()

print(f"\n✅ Cotação salva com sucesso em: {caminho_bd}")
