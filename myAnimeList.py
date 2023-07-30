import malupdate
import datetime
import json
from util import addID

def getMyAnimeLists(username,password):
    # User.login(username, password): Takes in username and password of MAL account as arguments and returns a loginObject (dictionary) consisting of keys access_token, expires_in, refresh_token.
    # User.getAnimeList(Access_Token, type_of_list, [field_1, field_2, ....]):
    login = malupdate.User.login(username, password)
    # Turn lists into a dictionary containing the list type as the key and the list as the value
    malList = malupdate.User.getAnimeList(
            login['access_token'], "", ['id', 'title', 'status', 'score', 'my_list_status'])
    formattedList=[]
    for page in malList:
        for entry in page["data"]:
            entry=entry["node"]
            item={}
            item["MALID"]=entry["id"]
            item["list"]=entry["my_list_status"]["status"].lower()
            item["updatedAt"]=datetime.datetime.fromisoformat(entry["my_list_status"]["updated_at"]).strftime('%Y-%m-%d %H:%M:%S')
            item["progress"]=entry["my_list_status"]["num_episodes_watched"]
            item["score"]=entry["my_list_status"]["score"]
            formattedList.append(item)
    return formattedList

def updateMAL(list,username,password):
    # If completed, set num_episodes_watched to total_episodes
    login = malupdate.User.login(username, password)
    # Turn lists into a dictionary containing the list type as the key and the list as the value
    fields={}
    for item in list:
        fields["num_episodes_watched"]=item["progress"]
        fields["score"]=item["score"]
        if item["list"]=="planning":
            fields["status"]="plan_to_watch"
        else:
            fields["status"]=item["list"]
        # get integer version of score
        fields["score"]=round(fields["score"],0)
        # MAL API uses num_watched_episodes for put but num_episodes_watched on get. Weird.
        malList = malupdate.User.updateList(login["access_token"], item["MALID"], {"score":fields["score"],"status":fields["status"],"num_watched_episodes":fields["num_episodes_watched"]})
        # if error is a key in mallist
        if "error" in malList:
            print (malList["error"])
            print("Error: "+str(item["MALID"]) +" not updated")
            print("Fields Sent were:" + str({"score":fields["score"],"status":fields["status"],"num_watched_episodes":fields["num_episodes_watched"]}))
            print("Fields Received were:" + str(malList))
        # print response
        elif malList["status"]!=fields["status"] or malList["score"]!=fields["score"] or malList["num_episodes_watched"]!=fields["num_episodes_watched"]:
            print("Error: "+str(item["MALID"]) +" not updated")
            print("Fields Sent were:" + str({"score":fields["score"],"status":fields["status"],"num_watched_episodes":fields["num_episodes_watched"]}))
            print("Fields Received were:" + str(malList))
    return malList