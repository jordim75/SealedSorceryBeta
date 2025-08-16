from flask import Flask, render_template, jsonify
import pandas as pd
import random
import io
from flask import Response

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

@app.route("/sobre/<int:n>")
def sobres(n):
    return jsonify([generar_sobre() for _ in range(n)])

@app.route("/export_csv/<int:n>")
def export_csv(n):
    sobres = [generar_sobre() for _ in range(n)]

    output = io.StringIO()
    # Capçalera
    output.write("Sobre,Posicio,Carta\n")
    for i, sobre in enumerate(sobres, start=1):
        for j, carta in enumerate(sobre, start=1):
            output.write(f"{i},{j},{carta}\n")

    csv_data = output.getvalue()
    output.close()

    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=sobres.csv"}
    )

if __name__ == "__main__":
    app.run(debug=True)
