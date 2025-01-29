import requests
import json
import certifi
import serpapi


# Configura suas credenciais para a API aqui
API_KEY = "3a72285bfca3b80fb8e833c7269b3d6631fa9d6b00383fa627ec4ea6cf33da63"
API_ENDPOINT = "https://serpapi.com/search"

# Função para consultar voos
def consultar_voos(origem, destino, datas, stopover_max):
    """
    Consulta voos com base na origem, destino e stopovers máximos.

    :param origem: Código IATA da cidade de origem (ex.: "GRU").
    :param destino: Código IATA da cidade de destino (ex.: "FCO").
    :param datas: Lista com datas para pesquisa (ex.: ["2025-06-01"]).
    :param stopover_max: Máximo de dias permitido para stopovers.
    :return: Lista de rotas com informações de preço, duração e stopovers.
    """
    rotas = []

    for data in datas:
        # Parâmetros seguindo a doc atual da SerpApi para Google Flights
        params = {
            "engine": "google_flights",
            "departure_id": origem,  # Em vez de 'origin'
            "arrival_id": destino,  # Em vez de 'destination'
            "outbound_date": data,  # Em vez de 'departure_date'
            "type": 2,  # 2 = one-way (1=round trip, 3=multi-city)
            "travel_class": 1,  # 1=Economy, 2=Premium Eco, 3=Business, 4=First
            "adults": 1,  # Número de adultos
            "hl": "en",  # Idioma
            "currency": "BRL",          # Opcional
            "deep_search": "true",
            "api_key": API_KEY
        }

        response = requests.get(API_ENDPOINT, params=params, verify=certifi.where())

        if response.status_code == 200:
            resultados = response.json()
            # A SerpApi costuma retornar voos em "best_flights" ou "other_flights",
            # mas depende da resposta atual. Veja o JSON para saber exatamente.

            # Exemplo fictício (ajuste conforme a estrutura real):
            flights = resultados.get("best_flights", []) + resultados.get("other_flights", [])

            for flight in flights:
                # flight geralmente tem lista de "flights" (pernas) e "layovers" etc.
                # Aqui, adaptamos ao seu código que analisa "stopovers".
                # Supondo que 'layovers' ou 'stopovers' apareça em flight:

                stopovers = flight.get("layovers", [])
                if len(stopovers) <= stopover_max:
                    rotas.append({
                        "preco": flight.get("price", "N/A"),
                        "duracao": flight.get("total_duration", "N/A"),
                        "stopovers": [lay["name"] for lay in stopovers],
                        "detalhes": flight
                    })
        else:
            print(f"Erro na consulta: {response.status_code}, {response.text}")

    return rotas


def exibir_melhores_rotas(rotas):
    """
    Exibe as rotas ordenadas pelo preço.
    """
    rotas_ordenadas = sorted(
        rotas,
        key=lambda x: x["preco"] if x["preco"] != "N/A" else float('inf')
    )

    for i, rota in enumerate(rotas_ordenadas, start=1):
        print(f"Rota {i}:")
        print(f"  Preço: {rota['preco']}")
        print(f"  Duração: {rota['duracao']}")
        if rota['stopovers']:
            print(f"  Stopovers: {', '.join(rota['stopovers'])}")
        else:
            print("  Stopovers: Direto")
        print("  ---")


def main():
    origem = input("Digite o código IATA da cidade de origem (ex.: GRU): ").strip()
    destino = input("Digite o código IATA da cidade de destino (ex.: FCO): ").strip()
    datas = input("Digite as datas de partida separadas por vírgula (ex.: 2025-06-01,2025-06-02): ") \
        .strip().split(",")
    stopover_max = int(input("Digite o número máximo de dias permitido para stopovers: "))

    print("Consultando rotas...")
    rotas = consultar_voos(origem, destino, datas, stopover_max)

    if rotas:
        print("\nMelhores rotas encontradas:")
        exibir_melhores_rotas(rotas)
    else:
        print("Nenhuma rota encontrada.")


if __name__ == "__main__":
    main()