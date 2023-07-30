# AnimeListSync
2 Way Sync between MyAnimeList.com and AniList.co

## Running via Docker
1. Modify the included docker-compose.yml file with your credentials and rename to docker-compose.yml
2. Get the AniList API token (see below)
2. Run `docker-compose up` to start the program (you can pass `-d` to run in the background)
## Running Locally
1. [Download](https://github.com/noggl/AnimeListSync/archive/refs/heads/main.zip) or `git clone` this repository
2. Run `pip install -r requirements.txt` to install dependencies
3. Populate .env file with your credentials
4. Run `python code/sync.py` to start the program
5. When prompted to go to a link, go to the link and copy the part of the url after `?code=`

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
4. **If you're using docker**, you'll need to get the token by first running the script locally and copying the token from the generated token.txt