from flask import Flask, render_template, jsonify
import pandas as pd
import random
import io
from flask import send_file
from openpyxl import Workbook

app = Flask(__name__)

# Carregar les cartes des del CSV
cartes_df = pd.read_csv("FontBeta.csv")

# Separar cartes segons tipus
cartes_per_tipus = {
    "Ordinary": cartes_df[cartes_df["tipus"] == "Ordinary"]["nom"].tolist(),
    "Booster": cartes_df[cartes_df["tipus"] == "Booster"]["nom"].tolist(),
    "BoosterAvatar": cartes_df[cartes_df["tipus"] == "BoosterAvatar"]["nom"].tolist(),
    "Exceptional": cartes_df[cartes_df["tipus"] == "Exceptional"]["nom"].tolist(),
    "Elite": cartes_df[cartes_df["tipus"] == "Elite"]["nom"].tolist(),
    "Unique": cartes_df[cartes_df["tipus"] == "Unique"]["nom"].tolist(),
}

def generar_sobre():
    sobre = []

    
    # 3 Exceptional
    sobre.extend(random.sample(cartes_per_tipus["Exceptional"], 3))

    # 1 Elite o Unique
    if random.random() < 0.76:  # 76% Elite
        sobre.append(random.choice(cartes_per_tipus["Elite"]))
    else:  # 24% Unique
        sobre.append(random.choice(cartes_per_tipus["Unique"]))
        
    # 10 Ordinary
    sobre.extend(random.sample(cartes_per_tipus["Ordinary"], 10))

    # 1 BoosterAvatar or BoosterSite
    if random.random() < 0.1:  # 10% BoosterAvatarElite
        sobre.append(random.choice(cartes_per_tipus["BoosterAvatar"]))
    else:  # 24% Unique
        sobre.append(random.choice(cartes_per_tipus["Booster"]))
    

    return sobre

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/Pack/<int:n>")
def sobres(n):
    return jsonify([generar_sobre() for _ in range(n)])

@app.route("/export_xlsx/<int:jocs>/<int:sobres>")
def export_xlsx(jocs, sobres):
    wb = Workbook()

    for jugador in range(1, jocs+1):
        if jugador == 1:
            ws = wb.active
            ws.title = f"Jugador {jugador}"
        else:
            ws = wb.create_sheet(title=f"Jugador {jugador}")

        ws.append(["Sobre", "Posicio", "Carta"])
        for s in range(1, sobres+1):
            sobre = generar_sobre()
            for j, carta in enumerate(sobre, start=1):
                ws.append([s, j, carta])

    output = io.BytesIO()
    wb.save(output)
    output.seek(0)

    return send_file(
        output,
        as_attachment=True,
        download_name="lots_jugadors.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

if __name__ == "__main__":
    app.run(debug=True)
