import os
import time
import requests
from telegram import Bot
from dotenv import load_dotenv

# Charger les variables d’environnement
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=TELEGRAM_TOKEN)

# Clé temporaire RapidAPI (simulée ici)
RAPIDAPI_KEY = "856323b0d3msh25017323f4c6747p1d564cjsnc15ae3e3028c"
RAPIDAPI_HOST = "api-football-v1.p.rapidapi.com"

HEADERS = {
    "X-RapidAPI-Key": RAPIDAPI_KEY,
    "X-RapidAPI-Host": RAPIDAPI_HOST
}

# Fonction pour envoyer une alerte
def send_alert(match_name, minute, score, stats, confidence):
    message = f"🔔 Alerte but probable ({minute}e)\n" \
              f"{match_name} ({score})\n" \
              f"{stats}\n" \
              f"Confiance : {confidence} %"
    bot.send_message(chat_id=CHAT_ID, text=message)

# Récupérer les matchs live via API-Football
def get_live_matches():
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures?live=all"
    try:
        response = requests.get(url, headers=HEADERS)
        data = response.json()
        return data.get("response", [])
    except Exception as e:
        print("Erreur API:", e)
        return []

# Analyser les stats et déterminer le score de confiance
def evaluate_match(match):
    teams = match["teams"]
    stats = match["statistics"]
    fixture = match["fixture"]

    home = teams["home"]["name"]
    away = teams["away"]["name"]
    minute = fixture["status"]["elapsed"]
    score = f'{match["goals"]["home"]} - {match["goals"]["away"]}'

    # Extraire quelques stats pertinentes (simulateur simple)
    shots_on_target = stats[0]["statistics"][6]["value"] or 0
    possession = int(str(stats[0]["statistics"][9]["value"]).replace("%", "")) if stats[0]["statistics"][9]["value"] else 0
    corners = stats[0]["statistics"][7]["value"] or 0

    points = 0
    if shots_on_target >= 5: points += 2
    if possession >= 55: points += 1
    if corners >= 6: points += 1
    if match["goals"]["home"] == match["goals"]["away"]: points += 1

    confidence = round((points / 5) * 100)

    if confidence >= 60:
        stats_str = f"Tirs cadrés : {shots_on_target} | Possession : {possession}% | Corners : {corners}"
        match_name = f"{home} - {away}"
        send_alert(match_name, minute, score, stats_str, confidence)

# Boucle principale
def main_loop():
    while True:
        matches = get_live_matches()
        for m in matches:
            try:
                minute = m["fixture"]["status"]["elapsed"]
                if 75 <= minute <= 90:
                    evaluate_match(m)
            except Exception as e:
                print("Erreur analyse:", e)
        time.sleep(60)

if __name__ == "__main__":
    main_loop()
