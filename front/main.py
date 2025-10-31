import requests
from flask import jsonify

BASE_URL = "http://127.0.0.1:5000"
NUMBER_OF_ANIMES_TO_RATE = 3
username = input("Escribe tu nombre de usuario: ")
password = input("Escribe tu contraseña: ")

def showMenu():
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

loop = True
while loop:
    print(showMenu())
    option = input("Elija la opción: ")
    if option == "1":
        user_ratings = {}
        counter = 0
        while counter < NUMBER_OF_ANIMES_TO_RATE:
            # TODO: Add check_anime_id
            anime_id = input("Escriba el id del anime a valorar: ")

            correct_rating = False
            while correct_rating == False:
                rating = input(f"Escriba la valoración para el anime {anime_id}: ")
                correct_rating = check_rating(rating)
                
            user_ratings[int(anime_id)] = int(rating)

            counter += 1

        url = f"{BASE_URL}/recommend/"
        requests.get(url, data=user_ratings)

    elif option == "0":
        loop = False

    else:
        print("Opción no válida")