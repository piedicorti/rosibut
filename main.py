import os
import time
from telegram import Bot
from dotenv import load_dotenv

# Chargement des variables d’environnement
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=TELEGRAM_TOKEN)

# Fonction pour envoyer une alerte Telegram
def send_alert(match_name, minute, score, stats, confidence):
    message = f"🔔 Alerte but probable ({minute}e)\n" \
              f"{match_name} ({score})\n" \
              f"{stats}\n" \
              f"Confiance : {confidence} %"
    bot.send_message(chat_id=CHAT_ID, text=message)

# Match fictif simulé (tu remplaceras plus tard par des stats réelles)
def extract_live_matches():
    return [{
        "match": "Marseille - Nice",
        "minute": 78,
        "score": "1-1",
        "stats": {
            "tirs_cadres": 6,
            "xg": 1.7,
            "possession": 61,
            "corners": 6,
            "dangerous_attacks_ratio": 2.4,
            "momentum": 72,
            "score_status": "draw"
        }
    }]

# Calcul du score de confiance et déclenchement alerte
def evaluate_match(match):
    stats = match["stats"]
    points = 0
    if stats["tirs_cadres"] >= 5: points += 1
    if stats["xg"] > 1.5: points += 2
    if stats["possession"] > 60: points += 1
    if stats["corners"] >= 5: points += 1
    if stats["dangerous_attacks_ratio"] >= 2: points += 1
    if stats["momentum"] >= 70: points += 1
    if stats["score_status"] in ["draw", "losing"]: points += 1

    confidence = round((points / 7) * 100)

    if points >= 3:
        stats_str = f"Tirs cadrés : {stats['tirs_cadres']} | xG : {stats['xg']} | Corners : {stats['corners']}"
        send_alert(match["match"], match["minute"], match["score"], stats_str, confidence)

# Boucle principale
def main_loop():
    while True:
        try:
            matches = extract_live_matches()
            for match in matches:
                if 75 <= match["minute"] <= 90:
                    evaluate_match(match)
        except Exception as e:
            print("Erreur :", e)
        time.sleep(60)  # une analyse par minute

if __name__ == "__main__":
    main_loop()

