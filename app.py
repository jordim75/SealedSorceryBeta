from flask import Flask, render_template, jsonify
import pandas as pd
import random

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
        
    # 11 Ordinary
    sobre.extend(random.sample(cartes_per_tipus["Ordinary"], 11))

    # 1 BoosterAvatar or BoosterSite
    if random.random() < 0.1:  # 10% BoosterAvatarElite
        sobre.append(random.choice(cartes_per_tipus["BoosterAvatar"]))
    else:  # 24% Unique
        sobre.append(random.choice(cartes_per_tipus["Booster"]))
    

    return sobre

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/sobre")
def sobre():
    return jsonify(generar_sobre())

if __name__ == "__main__":
    app.run(debug=True)
