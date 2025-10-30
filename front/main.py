NUMBER_OF_ANIMES_TO_VALORATE = 3
username = input("Escribe tu nombre de usuario: ")
password = input("Escribe tu contraseña: ")

def check_valoration(valoration):
    correct_valoration = False
    if valoration.isnumeric():
        valoration = int(valoration)
        if valoration >= 0 and valoration <= 10:
            correct_valoration = True
            
    return correct_valoration

user_ratings = {}
counter = 0
while counter < NUMBER_OF_ANIMES_TO_VALORATE:
    # TO-DO: Add check_anime_id
    anime_id = input("Escriba el id del anime a valorar: ")

    correct_valoration = False
    while correct_valoration == False:
        valoration = input(f"Escriba la valoración para el anime {anime_id}: ")
        correct_valoration = check_valoration(valoration)
        
    user_ratings[int(anime_id)] = int(valoration)

    counter += 1
