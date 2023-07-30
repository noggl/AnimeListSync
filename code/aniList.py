import requests
import datetime
import json

def getAniList(username):
    query = query = """
                query ($username: String) {
                MediaListCollection(userName: $username, type: ANIME) {
                    lists {
                    name
                    entries {
                        progress
                        score
                        repeat
                        updatedAt
                        media{
                        id
                        idMal
                        format
                        title {
                            romaji
                            english
                        }
                        }
                    }
                    }
                }
                }
    """

    # Define our query variables and values that will be used in the query request
    variables = {
        'username': username
    }
    url = 'https://graphql.anilist.co'
    # Make the HTTP Api request
    response = requests.post(
        url, json={'query': query, 'variables': variables})
    # if response is not 200, throw error
    if response.status_code != 200:
        print("Error: AniList response is not 200")
        return
    # filter down to entries of returned list
    aniList = response.json(
    )['data']['MediaListCollection']['lists']
    formattedList=[]
    for list in aniList:
        for entry in list["entries"]:
            item={}
            item["AniListID"]=entry["media"]["id"]
            item["MALID"]=entry["media"]["idMal"]
            item["list"]=list["name"].lower()
            item["updatedAt"]=datetime.datetime.fromtimestamp(entry["updatedAt"]).strftime('%Y-%m-%d %H:%M:%S')
            item["progress"]=entry["progress"]
            item["score"]=entry["score"]
            formattedList.append(item)
    return formattedList

def getAniListToken(clientID,clientSecret,redirect_uri="https://github.com/noggl/Sync"):
    #print url 'https://anilist.co/api/v2/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code'
    print("Go to the following URL and authorize the app:")
    print('https://anilist.co/api/v2/oauth/authorize?client_id='+clientID+'&redirect_uri='+redirect_uri+'&response_type=code')
    code=input("Enter the code from the URL: ")
    #print code
    #post to https://anilist.co/api/v2/oauth/token with client_id, client_secret, grant_type, redirect_uri, code
    url = 'https://anilist.co/api/v2/oauth/token'
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    data = {
        'grant_type': 'authorization_code',
        'client_id': clientID,
        'client_secret': clientSecret,
        'redirect_uri': redirect_uri,
        'code': code
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()["access_token"]


def updateAniList(list,token):
    for anime in list:
        if anime["list"]=="plan_to_watch":
            anime["list"]="planning"
        elif anime["list"]=="watching":
            anime["list"]="current"
        query = """
            mutation ($mediaId: Int, $status: MediaListStatus, $score: Float) {
            SaveMediaListEntry (mediaId: $mediaId, status: $status, score: $score) {
                id
                status
            }
        }
        """
        # Define our query variables and values that will be used in the query request
        variables = {
            "mediaId": anime["AniListID"],
            "status": anime["list"].upper(),
            "score": anime["score"]
        }

        url = 'https://graphql.anilist.co'

        headers = {
            'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
        response = requests.post(url, json={'query': query, 'variables': variables}, headers=headers).json()
    return True