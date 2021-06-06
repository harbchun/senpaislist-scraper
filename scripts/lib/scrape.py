import time
import requests
import json

def retrieve_anime_ids(year, season):
    with requests.get("https://api.jikan.moe/v3/season/" + str(year) + "/" + season) as seasonResponse:
        time.sleep(4)

        seasonData = seasonResponse.text
        jobj = json.loads(seasonData)

        if not jobj['anime']: return ''

        return [x['mal_id'] for x in jobj['anime']]
        
def retrieve_anime_data(anime_id):
    with requests.get("https://api.jikan.moe/v3/anime/" + str(anime_id)) as animeResponse:
        time.sleep(4)

        return animeResponse.json()
        