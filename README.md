# backtrader_codex

Ce dépôt contient un exemple minimal d'utilisation de [Backtrader](https://www.backtrader.com/) pour analyser des données financières. La stratégie définie dans `strategy.py` affiche plusieurs indicateurs techniques pour chaque bougie d'un fichier CSV.
Un indicateur personnalisé appelé **ConfluenceOscillator** combine RSI, CCI, MACD, ATR et les bandes de Bollinger selon des pondérations prédéfinies.

## Installation

1. Installez Python 3.11 ou supérieur.
2. Installez les dépendances avec `pip` :
   ```bash
   pip install -r requirements.txt
   ```

## Fichier de données

Le script attend un fichier `datas/EURUSD_H1.csv` au format CSV avec les colonnes suivantes :

1. `DATE` – date au format `AAAA.MM.JJ`
2. `TIME` – heure au format `HH:MM:SS`
3. `OPEN`
4. `HIGH`
5. `LOW`
6. `CLOSE`
7. `TICKVOL` (volume)

Si vous ne disposez pas de ce fichier, vous pouvez le remplacer par vos propres données en conservant la structure ci-dessus.

## Utilisation

Exécutez simplement :

```bash
python strategy.py
```
Le script charge le fichier de données puis affiche dans la console les valeurs des indicateurs ainsi que l'oscillateur de confluence.
