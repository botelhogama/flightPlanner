import requests
import certifi
import json

# Substitua pela sua chave de API válida da SerpApi
API_KEY = "3a72285bfca3b80fb8e833c7269b3d6631fa9d6b00383fa627ec4ea6cf33da63"
API_ENDPOINT = "https://serpapi.com/search"


def buscar_voos_ida(origem, destino, data_ida, data_volta):
    """
    1) Primeira requisição: obtém apenas os voos de ida (outbound).
       O JSON não terá os voos de volta.
       Cada opção de voo possui 'departure_token' para a 2ª requisição.
    """
    params = {
        "engine": "google_flights",
        "departure_id": origem,
        "arrival_id": destino,
        "outbound_date": data_ida,
        "return_date": data_volta,
        "type": 1,  # Round trip
        "adults": 1,
        "travel_class": 1,  # 1: Economy
        "stops": 3,  # Número máximo de escalas
        "currency": "USD",  # Adicionado para alinhar com o exemplo
        "api_key": API_KEY,
        "hl": "en",
        "deep_search": "true",  # Pode afetar a performance
    }
    try:
        resp = requests.get(API_ENDPOINT, params=params, verify=certifi.where())
        resp.raise_for_status()
    except requests.HTTPError as e:
        print(f"Erro na 1ª requisição: {e}")
        print(f"Resposta da API: {resp.text}")
        return None

    data = resp.json()
    best = data.get("best_flights", [])
    other = data.get("other_flights", [])
    outbound_options = best + other
    return outbound_options


def buscar_voos_volta(departure_token, data_volta, origem, destino, data_ida):
    """
    2) Segunda requisição para pegar a volta (inbound),
       usando o departure_token fornecido pela ida.

       IMPORTANTE: não inclua 'type=1' ou 'deep_search=true'
                   pois isso causa erro 400.
    """
    params = {
        "engine": "google_flights",
        "departure_token": departure_token,
        "departure_id": origem,  # Mesmo origem da primeira requisição
        "arrival_id": destino,  # Mesmo destino da primeira requisição
        "outbound_date": data_ida,  # Mesmo outbound_date da primeira requisição
        "return_date": data_volta,
        "currency": "USD",  # Adicionado para alinhar com o exemplo
        "hl": "en",
        "api_key": API_KEY,
    }
    try:
        resp = requests.get(API_ENDPOINT, params=params, verify=certifi.where())
        resp.raise_for_status()
    except requests.HTTPError as e:
        print(f"    Erro na 2ª requisição: {e}")
        print(f"    Resposta da API: {resp.text}")
        return None

    data = resp.json()
    best = data.get("best_flights", [])
    other = data.get("other_flights", [])
    inbound_options = best + other
    return inbound_options


def main():
    print("=== Consulta Round Trip - 2 Requisições ===")
    origem = input("Origem (ex.: BSB): ").strip().upper()
    destino = input("Destino (ex.: FCO): ").strip().upper()
    data_ida = input("Data de ida (YYYY-MM-DD): ").strip()
    data_volta = input("Data de volta (YYYY-MM-DD): ").strip()

    print("\n>>> Fazendo PRIMEIRA requisição para buscar IDA (outbound)...")
    outbound_list = buscar_voos_ida(origem, destino, data_ida, data_volta)

    if not outbound_list:
        print("Nenhum voo de ida encontrado ou erro na requisição.")
        return

    # Iterar em cada opção de ida
    for idx, voo_ida in enumerate(outbound_list, start=1):
        price = voo_ida.get("price", "N/A")
        token = voo_ida.get("departure_token")
        flights = voo_ida.get("flights", [])

        print(f"\n[{idx}] IDA => Preço: {price} USD | departure_token = {token}")
        for i, seg in enumerate(flights, start=1):
            dep_airport = seg.get("departure_airport", {})
            arr_airport = seg.get("arrival_airport", {})
            dep_id = dep_airport.get("id", "N/A")
            arr_id = arr_airport.get("id", "N/A")
            dep_time = dep_airport.get("time", "N/A")
            arr_time = arr_airport.get("time", "N/A")
            dur = seg.get("duration", "?")
            print(f"   Segmento {i}: {dep_id} -> {arr_id} (Duração: {dur} min)")
            print(f"      Partida: {dep_airport.get('name', 'N/A')} às {dep_time}")
            print(f"      Chegada: {arr_airport.get('name', 'N/A')} às {arr_time}")

        if not token:
            print("    * Sem departure_token => não podemos buscar volta.")
            continue

        print("    >>> Fazendo SEGUNDA requisição para buscar VOLTA (inbound)...")
        inbound_list = buscar_voos_volta(token, data_volta, origem, destino, data_ida)

        if not inbound_list:
            print("    * Nenhum voo de volta encontrado ou erro na requisição.")
            continue

        print(f"    Opções de volta encontradas: {len(inbound_list)}")
        # Exibir só as 2 primeiras opções
        for v_idx, voo_volta in enumerate(inbound_list[:2], start=1):
            v_price = voo_volta.get("price", "N/A")
            v_flights = voo_volta.get("flights", [])
            print(f"      - Volta {v_idx}, Preço: {v_price} USD")
            for j, seg in enumerate(v_flights, start=1):
                dep_airport = seg.get("departure_airport", {})
                arr_airport = seg.get("arrival_airport", {})
                dep_id = dep_airport.get("id", "N/A")
                arr_id = arr_airport.get("id", "N/A")
                dep_time = dep_airport.get("time", "N/A")
                arr_time = arr_airport.get("time", "N/A")
                dur = seg.get("duration", "?")
                print(f"        {j}) {dep_id} -> {arr_id} (Duração: {dur} min)")
                print(f"           Partida: {dep_airport.get('name', 'N/A')} às {dep_time}")
                print(f"           Chegada: {arr_airport.get('name', 'N/A')} às {arr_time}")
            print("")


if __name__ == "__main__":
    main()
