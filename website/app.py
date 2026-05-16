from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

# Coloque aqui sua chave da TMDb
API_KEY = "03653c3faab388510f4c1ad642dd9b5f"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/recommend", methods=["POST"])
def recommend():
    # tira espaços extras no começo/fim do nome digitado
    movie_name = request.form["movie"].strip()

    # busca filmes na TMDb em PT-BR
    search_url = (
        "https://api.themoviedb.org/3/search/movie"
        f"?api_key={API_KEY}"
        f"&language=pt-BR"
        f"&query={movie_name}"
    )
    response = requests.get(search_url).json()

    if response.get("results"):
        movie_id = response["results"][0]["id"]

        # pega recomendações também em PT-BR
        rec_url = (
            f"https://api.themoviedb.org/3/movie/{movie_id}/recommendations"
            f"?api_key={API_KEY}"
            f"&language=pt-BR"
        )
        rec_response = requests.get(rec_url).json()

        print("Total vindo da API:", len(rec_response.get("results", [])))

        recommendations = rec_response.get("results", [])[:30]
    else:
        recommendations = []

    return render_template("index.html", recommendations=recommendations, movie_name=movie_name)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)