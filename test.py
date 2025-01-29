import requests
import certifi

API_KEY = "3a72285bfca3b80fb8e833c7269b3d6631fa9d6b00383fa627ec4ea6cf33da63"
API_ENDPOINT = "https://serpapi.com/search"


def test_google_flights():
  params = {
    "engine": "google_flights",
    # Em VEZ de 'origin', use 'departure_id'
    "departure_id": "ORY",
    # Em VEZ de 'destination', use 'arrival_id'
    "arrival_id": "FCO",
    # Em VEZ de 'departure_date', use 'outbound_date'
    "outbound_date": "2025-01-30",

    # Em VEZ de 'trip_type=oneway', use 'type=2'
    # 1 = Round trip, 2 = One way, 3 = Multi-city
    "type": 2,

    # Em VEZ de 'class_type=economy', use 'travel_class=1'
    # 1 = Economy, 2 = Premium eco, 3 = Business, 4 = First
    "travel_class": 1,

    # Número de adultos
    "adults": 1,

    # Outras configs suportadas (conforme docs):
    "currency": "USD",  # (opcional)
    "hl": "en",  # idioma (opcional)

    "api_key": API_KEY
  }

  print("[DEBUG] Enviando estes parâmetros:", params)
  response = requests.get(API_ENDPOINT, params=params, verify=certifi.where())
  print("[DEBUG] URL requisitada:", response.url)

  if response.status_code == 200:
    print("Consulta retornou 200 OK.")
    data = response.json()
    print("JSON SerpApi:", data)
  else:
    print(f"Erro na consulta: {response.status_code}, {response.text}")


if __name__ == "__main__":
  test_google_flights()