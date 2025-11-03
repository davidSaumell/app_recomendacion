import requests
from flask import jsonify

BASE_URL = "http://127.0.0.1:5000"
NUMBER_OF_ANIMES_TO_RATE = 3
username = input("Escribe tu nombre de usuario: ")
password = input("Escribe tu contraseña: ")

def show_menu():
    menu = ("\033[33m1.- Obtener recomendaciones.\n"
        "2.- Entrenar el algoritmo.\n"
        "3.- Obtener la versión.\n"
        "4.- Testear el algoritmo.\n"
        "0.- Apagar programa.\033[0m\n"
    )
    return menu

def check_rating(rating):
    correct_rating = False
    if rating.isnumeric():
        rating = int(rating)
        if rating >= 0 and rating <= 10:
            correct_rating = True
            
    return correct_rating    

def show_recommendation_data(response):
    if response.ok:
        recommendations = response.json()
        if not recommendations:
            print("\nNo se generaron recomendaciones.")
            return

        print("\nTop 10 recomendaciones:\n")
        max_id_length = max(len(str(rec['anime_id'])) for rec in recommendations)
        max_name_length = max(len(rec.get('name', '')) for rec in recommendations)

        header = f"\033[1m{'N°':<3} | {'ID':<{max_id_length}} | {'Nombre':<{max_name_length}} | {'Score'}\033[0m"
        print(header)
        print("-" * len(header))
        
        for i, rec in enumerate(recommendations, start=1):
            name = rec.get('name', 'Desconocido')
            print(f"{i:2d}. | {rec['anime_id']:{max_id_length}d} | {name:<{max_name_length}} | {rec['score']:.2f}")
    else:   
        print("Error:", response.text)

loop = True
while loop:
    print(show_menu())
    option = input("Elija la opción: ")
    if option == "1":
        url = f"{BASE_URL}/list-anime/"
        response = requests.get(url)

        if response.ok:
            anime_JSON = response.json()
            for anime in anime_JSON:
                print(f"{anime['anime_id']} - {anime['name']}")
        else:
            print("Error al obtener la lista de animes:", response.text)

        user_ratings = {}
        counter = 0
        while counter < NUMBER_OF_ANIMES_TO_RATE:
            correct_anime_rating = True
            while correct_anime_rating:
                anime_id = input("Escriba el id del anime a valorar: ")
                if anime_id.isnumeric():
                    valid_anime_ids = {anime['anime_id'] for anime in anime_JSON}
                    if int(anime_id) in valid_anime_ids:
                        correct_anime_rating = False
                    else:
                        print("ID no encontrado")
                else:
                    print("Respuesta no válida")

            correct_rating = False
            while correct_rating == False:
                rating = input(f"Escriba la valoración para el anime {anime_id}: ")
                correct_rating = check_rating(rating)
                
            user_ratings[int(anime_id)] = int(rating)

            counter += 1

        url = f"{BASE_URL}/recommend/"
        response = requests.post(url, data=user_ratings)
        show_recommendation_data(response)

    elif option == "2":
        url = f"{BASE_URL}/train/"
        response = requests.patch(url)

    elif option == "3":
        url = f"{BASE_URL}/version/"
        response = requests.get(url)

        if response.ok:
            data = response.json()

            print("\nModelo actual:")
            print(f"Version: {data.get('model_version', 'Desconocida')}")
            print(f"Ruta: {data.get('artifact_path', 'No disponible')}\n")
        else:
            print("Error: ", response.text)

    elif option == "4":
        url = f"{BASE_URL}/test/"
        response = requests.get(url)
        show_recommendation_data(response)
    
    elif option == "0":
        loop = False

    else:
        print("Opción no válida")