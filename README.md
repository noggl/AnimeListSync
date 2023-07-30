# AnimeListSync
2 Way Sync between MyAnimeList.com and AniList.co

## Usage
1. [Download](https://github.com/noggl/AnimeListSync/archive/refs/heads/main.zip) or `git clone` this repository
2. Run `pip install -r requirements.txt` to install dependencies
3. Populate .env file with your credentials
4. Run `python sync.py` to start the program
5. When prompted to go to a link, go to the link and authorize the app with AniList.co

## .env file

```
aniListUser="noggl"
aniListAPI_ID="12345"
aniListAPI_secret="some_secret"

malUser="noggl"
malPassword="mal_password"
```

## Getting AniList API credentials
1. Go to https://anilist.co/settings/developer
2. Create a new client with any name and empty redirect url
3. Copy the client ID and client secret into the .env file