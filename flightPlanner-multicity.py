import requests
import certifi
import json

API_KEY = "3a72285bfca3b80fb8e833c7269b3d6631fa9d6b00383fa627ec4ea6cf33da63"
API_ENDPOINT = "https://serpapi.com/search"

def consultar_voos_multicity():
    """
    Exemplo de busca multi-city (type=3), definindo as pernas do voo:
      1) GRU -> CDG (Paris) em 2025-05-01
      2) CDG -> FCO (Roma) em 2025-05-05
      3) FCO -> GRU (Brasil) em 2025-05-15
    Usando deep_search=true para resultados mais completos.
    """
    # Monta a lista de "legs" (pernas) em JSON
    # Pode incluir mais cidades conforme desejar
    legs = [
        {
            "departure_id": "GRU",   # Guarulhos
            "arrival_id": "CDG",    # Paris Charles de Gaulle
            "date": "2025-05-01"
        },
        {
            "departure_id": "CDG",  # Paris
            "arrival_id": "FCO",    # Roma Fiumicino
            "date": "2025-05-05"
        },
        {
            "departure_id": "FCO",  # Roma
            "arrival_id": "GRU",    # Brasil
            "date": "2025-05-15"
        }
    ]

    # Converte para string JSON
    multi_city_str = json.dumps(legs)

    params = {
        "engine": "google_flights",
        "type": 3,  # 3 => Multi-city
        "multi_city_json": multi_city_str,
        "travel_class": 1,    # 1 => Economy
        "adults": 1,
        "deep_search": "true",
        "hl": "en",
        "api_key": API_KEY
    }

    print("[DEBUG] Params:", params)
    response = requests.get(API_ENDPOINT, params=params, verify=certifi.where())

    if response.status_code == 200:
        data = response.json()
        best = data.get("best_flights", [])
        other = data.get("other_flights", [])
        all_flights = best + other

        if not all_flights:
            print("Nenhuma opção encontrada (best_flights e other_flights vazios).")
            return

        # Só para exibir algumas infos
        for i, flight in enumerate(all_flights, start=1):
            price = flight.get("price", "N/A")
            total_duration = flight.get("total_duration", "N/A")
            print(f"\nOpção {i}: Preço = {price}, Duração total (min) = {total_duration}")
            layovers = flight.get("layovers", [])
            if layovers:
                print("  Escalas:", ", ".join(lay["name"] for lay in layovers))
            else:
                print("  Sem escalas.")
    else:
        print(f"Erro {response.status_code} => {response.text}")

def main():
    print("=== Exemplo Multi-City ===")
    consultar_voos_multicity()

if __name__ == "__main__":
    main()
