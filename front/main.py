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
        print("\nTop 10 recomendaciones:")
        max_id_length = max(len(str(rec['anime_id'])) for rec in recommendations)
        for i, rec in enumerate(recommendations, start=1):
            print(f"{i:2d}. Anime ID: {rec['anime_id']:{max_id_length}d}  |  Score: {rec['score']:.2f}")
    else:
        print("Error:", response.text)

loop = True
while loop:
    print(show_menu())
    option = input("Elija la opción: ")
    if option == "1":
        url = f"{BASE_URL}/list-anime/"
        response = requests.get(url)

        anime_JSON = response.json()
        for anime in anime_JSON:
            print(anime)

        user_ratings = {}
        counter = 0
        while counter < NUMBER_OF_ANIMES_TO_RATE:
            loop = True
            while loop:
                anime_id = input("Escriba el id del anime a valorar: ")
                if anime_id.isnumeric():
                    if int(anime_id) in anime_JSON:
                        loop = False
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