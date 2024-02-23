from flask import Flask, request, render_template
import requests
import logging
import time

app = Flask(__name__)

logging.basicConfig(filename='app.log', level=logging.INFO)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/search", methods=["POST"])
def search():
    query = request.form["q"]
    start_time = time.time()

    location = requests.get(
        "https://nominatim.openstreetmap.org/search",
        params={"q": query, "format": "json", "limit": "1"},
    ).json()

    duration = time.time() - start_time
    logging.info(f"Request to /search endpoint took {duration} seconds")

    if location:
        coordinate = [location[0]["lat"], location[0]["lon"]]
        time_data = requests.get(
            "https://timeapi.io/api/Time/current/coordinate",
            params={"latitude": coordinate[0], "longitude": coordinate[1]},
        ).json()

        return render_template("success.html", location=location[0], time=time_data)
    else:
        return render_template("fail.html")

if __name__ == "__main__":
    app.run(debug=True)
