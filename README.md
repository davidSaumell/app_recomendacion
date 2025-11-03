# Recomendaciones Anime 🎌

Un sistema de recomendación de anime basado en filtrado colaborativo, implementado en Python, que entrena un modelo a partir de valoraciones de usuarios y ofrece recomendaciones personalizadas a través de una API Flask y una interfaz CLI (main.py).

---

## Características principales

- Entrenamiento de un modelo de correlación (pandas.corr) con ratings de usuarios.

- Recomendaciones personalizadas basadas en animes valorados.

- Endpoint REST con Flask para interactuar con el modelo.

- CLI interactiva para probar el sistema (sin necesidad de interfaz web).

## Iniciar Backend ⚙️
1. Instalar librerias necesarias
  1. `pip install pandas`
  2. `pip install flask`
2. Iniciar el servidor Backend
  1. Abrir un terminal dentro de la carpeta `back`
  2. Ejecutar: `flask --app api.py run`
4. El servidor se iniciará por defecto en:
   `http://127.0.0.1:5000`

## Iniciar Frontend 💻
1. Abrir un terminal dentro de la carpeta `front`
2. Ejecutar: python main.py
