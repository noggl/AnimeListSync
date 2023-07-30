# This script syncs AniList to MyAnimeList or vice versa
import os
from dotenv import load_dotenv
from aniList import *
from myAnimeList import *
from util import *

def getVariables():
    # Load environment variables (aniListUser,aniListAPI_ID,aniListAPI_secret,malUser,malPassword)
    load_dotenv()
    # Get variables from .env
    aniListUser = os.getenv("aniListUser")
    aniListAPI_ID = os.getenv("aniListAPI_ID")
    aniListAPI_secret = os.getenv("aniListAPI_secret")
    malUser = os.getenv("malUser")
    malPassword = os.getenv("malPassword")
    return aniListUser,aniListAPI_ID,aniListAPI_secret,malUser,malPassword

if __name__ == "__main__":
    # Get variables
    aniListUser,aniListAPI_ID,aniListAPI_secret,malUser,malPassword=getVariables()
    # If any of the variables are null, print error and exit
    if not aniListUser or not aniListAPI_ID or not aniListAPI_secret or not malUser or not malPassword:
        print("Error: Variables not set")
        exit()
    # If token.txt exists, read token from file
    if os.path.isfile("token.txt"):
        with open("token.txt", "r") as text_file:
            token=text_file.read()
    # If token.txt does not exist, get token from AniList
    else:
        token=getAniListToken(aniListAPI_ID,aniListAPI_secret,"null")
        # write token to file
        with open("token.txt", "w") as text_file:
            text_file.write(token)
    refreshFile("https://raw.githubusercontent.com/Fribb/anime-lists/master/anime-list-full.json")
    malLists=getMyAnimeLists(malUser,malPassword)
    aniLists=getAniList(aniListUser)
    malLists=addID(malLists,aniLists)
    malListsChanges,aniListChanges=compare(malLists,aniLists)
    #update lists
    malResult = updateMAL(malListsChanges,malUser,malPassword)
    aniListResult = updateAniList(aniListChanges,token)