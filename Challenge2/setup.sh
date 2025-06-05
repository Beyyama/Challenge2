#!/bin/bash

echo "🔧 Starte Installation der System- und Python-Abhängigkeiten..."

# Systempakete installieren
sudo apt update
sudo apt install -y mpg123 python3 python3-pip

# Python-Abhängigkeiten aus requirements.txt installieren
pip3 install -r requirements.txt

echo "✅ Setup abgeschlossen. Du kannst das Projekt jetzt mit 'python3 challenge2.py' starten."
