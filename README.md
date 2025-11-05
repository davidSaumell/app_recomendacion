# Recomendaciones Anime 🎌

Un sistema de recomendación de anime basado en filtrado colaborativo, implementado en Python, que entrena un modelo a partir de valoraciones de usuarios y ofrece recomendaciones personalizadas a través de una API Flask y una interfaz CLI (main.py).

---

## Características principales

- Entrenamiento de un modelo de correlación (pandas.corr) con ratings de usuarios.

- Recomendaciones personalizadas basadas en animes valorados.

- Endpoint REST con Flask para interactuar con el modelo.

- CLI interactiva para probar el sistema (sin necesidad de interfaz web).

## Base de Datos
1. Para tener una base de datos con la mínima información, ejecute el siguiente script:
```
create schema IF NOT EXISTS anime_recomendation;

DROP TABLE IF EXISTS `users`;
create table users (
	idUser INT NOT NULL AUTO_INCREMENT,
    userName varchar(45),
    password varchar(45),
    CONSTRAINT PK_USERS primary key (idUser)
);

insert into Users (userName, password) values ('admin', 'admin');
```

## Iniciar Backend ⚙️
El programa utiliza funciones de MySQL para realizar la conexión con la base de datos, solicitará el usuario y contraseña para acceder a ella.  
1. Instalar librerías necesarias
   1. `pip install pandas`
   2. `pip install flask`
3. Iniciar el servidor Backend
   1. Abrir un terminal dentro de la carpeta `back`
   2. Ejecutar: `python -m flask --app api.py run`
   3. Introducir las credenciales de la base de datos.

El servidor se iniciará por defecto en: `http://127.0.0.1:5000`

## Iniciar Frontend 💻
1. Abrir un terminal dentro de la carpeta `front`
2. Ejecutar: `python main.py`  

## Obtener los datos
Necesitaremos tener dos csv para poder obtener los datos y dar una recomendación al usuario en función del resto de usuarios que ya han valorado los animes.  
  
Estos datos deberán estar guardados a la misma altura que la raíz del programa en una carpeta llamada data.  
<img width="188" height="69" alt="image" src="https://github.com/user-attachments/assets/02757531-0f02-479f-b88e-04cdc765d7fb" />

1. anime.csv
   1. Visitar [anime.csv](https://www.kaggle.com/datasets/CooperUnion/anime-recommendations-database/data?select=anime.csv)
   2. Descargar `anime.csv` <img width="1226" height="602" alt="anime_csv_download" src="https://github.com/user-attachments/assets/041e4551-f4d4-46c4-8491-1eb410dbe079" />
2. ratings.csv
   1. Visitar [ratings.csv](https://www.kaggle.com/datasets/CooperUnion/anime-recommendations-database/data?select=rating.csv)
   2. Descargar `ratings.csv` <img width="1175" height="423" alt="ratings_csv_download" src="https://github.com/user-attachments/assets/34219203-2140-4c9e-8594-47d901c934b7" />
