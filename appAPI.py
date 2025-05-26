import pandas as pd
from pathlib import Path
datapath = Path("nba.csv")
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI()
@app.get("/{player}")
def get_player(player: str):
    df = pd.read_csv(datapath, sep=',')
    
    # We define a filter and search for the player name in a case-insensitive manner. No matter if the name are in uppercase or lowercase.
    player_data = df
    
    if player_data.empty:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    
    return JSONResponse(content=player_data.to_dict(orient='records')[0]) # Names should be unique, but in case there are duplicates, we return the first one.


@app.get("/top_players")
def get_top_players():
    nba = pd.read_csv(datapath, sep=',')
    top_players = nba[['Name', 'Salary', 'Team']].query('Salary > 10000000').sort_values(by='Salary', ascending=False)
    team_info = nba[['Team', 'Weight (KG)', 'Height (cm)']].drop_duplicates(subset='Team')
    players_teams = pd.merge(top_players, team_info, on = 'Team', how = 'inner')

    if players_teams.empty:
        raise HTTPException(status_code=404, detail="No hay jugadores con salario mayor a 10 millones")
    return JSONResponse(content=players_teams.to_dict(orient='records'))
