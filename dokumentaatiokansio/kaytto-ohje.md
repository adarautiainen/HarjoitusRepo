# Käyttöohje

## Ohjelman lataaminen 

Ohjelman lataaminen
```bash
git clone git@github.com:adarautiainen/connectfour-game.git
```
Riippuvuuksien asentaminen
```bash
poetry install
```
Ohjelman käynnistäminen
```bash
poetry run python3 connectfour/game/connect4.py
```

## Ohjelman käyttö

- Ohjelma pyytää käyttäjältä syötteen eli kolumnin, johon käyttäjä haluaa pelimerkin sijoittaa. Ohjelma hyväksyy käyttäjän syötteenä numerot 1-7.
