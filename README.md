# FlightPlanner - Pesquisa de Voos com Google Flights API

## 📌 Descrição
FlightPlanner é um conjunto de scripts Python que consulta voos utilizando a API do Google Flights via SerpApi. Ele permite pesquisar diferentes tipos de voos:

- **One-way** (Apenas ida)
- **Round-trip** (Ida e volta)
- **Multi-city** (Vários trechos)

O projeto é ideal para encontrar passagens com **deep search**, maximizando a precisão dos resultados.

---
## 📂 Estrutura do Projeto

O projeto contém três arquivos principais:

📄 `flightPlanner-onetrip.py` → Pesquisa voos **somente de ida**
📄 `flightPlanner-roundtrip.py` → Pesquisa voos **ida e volta**
📄 `flightPlanner-multicity.py` → Pesquisa **múltiplos destinos**

Cada script permite ao usuário inserir os parâmetros desejados e obter os melhores voos com base na resposta da API.

---
## 🚀 Requisitos

### 📌 Dependências:
Este projeto utiliza as seguintes bibliotecas:

- `requests` → Para realizar chamadas HTTP à API
- `certifi` → Para validação SSL
- `json` → Para manipulação de respostas

Instale as dependências executando:
```bash
pip install requests certifi
```

---
## 🛠 Configuração e Uso

Antes de rodar os scripts, **substitua** a variável `API_KEY` pelo seu próprio token da SerpApi no arquivo de cada script:

```python
API_KEY = "SUA_CHAVE_DA_SERPAPI"
```

Se você ainda não possui uma chave, registre-se em [SerpApi](https://serpapi.com/) e obtenha sua chave de API.

---
## 🔍 Como Usar

### 📌 1️⃣ Pesquisa de voo **One-way** (somente ida)
Rode o seguinte comando no terminal:
```bash
python flightPlanner-onetrip.py
```
O script solicitará as seguintes informações:

```plaintext
Digite o código IATA da cidade de origem (ex.: GRU):
Digite o código IATA da cidade de destino (ex.: FCO):
Digite a data de partida (YYYY-MM-DD):
Digite o número máximo de escalas permitido:
```

🔹 O script retornará a melhor opção disponível, incluindo **preço, duração do voo e escalas**.

### 📌 2️⃣ Pesquisa de voo **Round-trip** (ida e volta)
Rode:
```bash
python flightPlanner-roundtrip.py
```
O script pedirá as seguintes informações:

```plaintext
Origem (ex.: GRU):
Destino (ex.: FCO):
Data de ida (YYYY-MM-DD):
Data de volta (YYYY-MM-DD):
Máximo de escalas:
```

🔹 O resultado mostrará os voos de ida e volta com **deep search** ativado.

### 📌 3️⃣ Pesquisa de voo **Multi-city** (múltiplos destinos)
Rode:
```bash
python flightPlanner-multicity.py
```
Este script já contém **destinos pré-definidos**, mas você pode editar os seguintes trechos no código para personalizar:

```python
legs = [
    {"departure_id": "GRU", "arrival_id": "CDG", "date": "2025-05-01"},
    {"departure_id": "CDG", "arrival_id": "FCO", "date": "2025-05-05"},
    {"departure_id": "FCO", "arrival_id": "GRU", "date": "2025-05-15"}
]
```

🔹 O script retornará as melhores opções disponíveis para cada trecho da viagem.

---
## 🔗 Recursos Utilizados
- [SerpApi Google Flights API](https://serpapi.com/google-flights-api)
- [Lista de Códigos IATA de Aeroportos](https://www.iata.org/en/publications/directories/code-search/)

---
## 📜 Licença
Este projeto está sob a licença MIT. Sinta-se à vontade para usá-lo e modificá-lo conforme necessário.

---
## ✨ Autor
**Desenvolvido por:** Rafael Botelho
📧 Email: botelhogama@gmail.com  
🌍 GitHub: [seu-usuario](https://github.com/botelhogama)

