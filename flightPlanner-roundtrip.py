import requests
import certifi

API_KEY = "3a72285bfca3b80fb8e833c7269b3d6631fa9d6b00383fa627ec4ea6cf33da63"
API_ENDPOINT = "https://serpapi.com/search"

def consultar_voos_round_trip(origem, destino, data_ida, data_volta, stopover_max=2):
    """
    Consulta voos de ida e volta (round trip) usando a SerpApi (Google Flights).

    :param origem: Código IATA de origem (ex: "GRU" para Guarulhos).
    :param destino: Código IATA de destino (ex: "FCO" para Roma-Fiumicino).
    :param data_ida: Data de ida (ex: "2025-06-01").
    :param data_volta: Data de volta (ex: "2025-06-15").
    :param stopover_max: Quantidade máxima de escalas (para filtrar manualmente).
    :return: Lista de rotas (list of dicts) com informações de preço, duração, etc.
    """
    # Monta os parâmetros conforme a doc atual
    params = {
        "engine": "google_flights",
        "departure_id": origem,       # ex.: "GRU"
        "arrival_id": destino,        # ex.: "FCO"
        "outbound_date": data_ida,    # ex.: "2025-06-01"
        "return_date": data_volta,    # ex.: "2025-06-15"
        "type": 1,                    # 1 => Round trip
        "travel_class": 1,            # 1 => Economy
        "adults": 1,                  # Quantos adultos
        "deep_search": "true",        # Força pesquisa mais aprofundada
        "stops": 3,                   # 3 => até 2 escalas (0=ilimitado, 1=nonstop, 2=1stop, 3=2stops)
        "hl": "en",
        "api_key": API_KEY
    }

    rotas = []

    response = requests.get(API_ENDPOINT, params=params, verify=certifi.where())
    if response.status_code == 200:
        resultados = response.json()
        # Estrutura comum: "best_flights" e "other_flights"
        best = resultados.get("best_flights", [])
        other = resultados.get("other_flights", [])

        # Vamos agrupar tudo para simplificar
        all_flights = best + other

        for flight in all_flights:
            # "flight" normalmente tem "flights" (lista de pernas) e "layovers"
            stopovers = flight.get("layovers", [])

            # Filtra manualmente pela quantidade de escalas
            if len(stopovers) <= stopover_max:
                rotas.append({
                    "preco": flight.get("price", "N/A"),
                    "duracao": flight.get("total_duration", "N/A"),  # minutos totais
                    "stopovers": [lay["name"] for lay in stopovers],
                    "detalhes": flight
                })
    else:
        print(f"Erro na consulta: {response.status_code}, {response.text}")

    return rotas

def exibir_melhores_rotas(rotas):
    """ Ordena rotas pelo preço e exibe. """
    rotas_ordenadas = sorted(
        rotas,
        key=lambda x: x["preco"] if x["preco"] != "N/A" else float('inf')
    )
    for i, rota in enumerate(rotas_ordenadas, start=1):
        print(f"\nRota {i}:")
        print(f"  Preço: {rota['preco']}")
        print(f"  Duração (min): {rota['duracao']}")
        if rota['stopovers']:
            print(f"  Escalas: {', '.join(rota['stopovers'])}")
        else:
            print("  Escalas: Direto")

def main():
    print("=== Consulta Round Trip ===")
    origem = input("Origem (ex.: GRU): ").strip()
    destino = input("Destino (ex.: FCO): ").strip()
    data_ida = input("Data de ida (YYYY-MM-DD): ").strip()
    data_volta = input("Data de volta (YYYY-MM-DD): ").strip()
    stopover_max = int(input("Máximo de escalas: "))

    print("\nPesquisando...")
    rotas = consultar_voos_round_trip(origem, destino, data_ida, data_volta, stopover_max)

    if rotas:
        print("\nMelhores rotas encontradas:")
        exibir_melhores_rotas(rotas)
    else:
        print("Nenhuma rota encontrada.")

if __name__ == "__main__":
    main()
