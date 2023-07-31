import datetime
import json
import os
import subprocess

def getCommitDate(URL):
    # Parse url for file name, user, and repo
    githubFile=URL.split("/")[-1]
    githubRepo=URL.split("/")[-3]
    githubUser=URL.split("/")[-4]
    requestURL="https://api.github.com/repos/" + githubUser + "/" + githubRepo + "/commits?path=" + githubFile
    # Get last updated date from github
    result = subprocess.check_output("curl -s " + requestURL, shell=True)
    # convert result to dictionary
    result = json.loads(result)
    date=result[0]["commit"]["author"]["date"]
    # Convert date to datetime object
    lastUpdated=datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
    return lastUpdated

def refreshFile(url):
    changes=False
    filename=url.split("/")[-1]
    if not os.path.exists(filename):
        print(filename + " not found. Downloading...")
        changes=True
        # Download the file
        downloadFile(url)
    else:
        localDate=getLocalDate(filename)
        # Get date from github
        githubDate=getCommitDate(url)
        # Compare dates
        if localDate == False or localDate < githubDate:
            print(filename + " is out of date. Downloading...")
            changes=True
            # Download the file
            downloadFile(url)
        else:
            print("No changes to " + filename)
    return changes

def downloadFile(url):
    #parse url for file name
    fileName=url.split("/")[-1]
    os.system("curl -s "+ url + " -o " + fileName)
    # Write current date to updated.txt
    if os.path.exists("updated.txt"):
        # If filename is already in the doc, update it, otherwise append it
        found=False
        with open("updated.txt", "r") as f:
            for line in f:
                if line.startswith(fileName):
                    found=True
                    break
        if found:
            with open("updated.txt", "r") as f:
                lines=f.readlines()
            with open("updated.txt", "w") as f:
                for line in lines:
                    if line.startswith(fileName):
                        #Write Datetime to file
                        f.write(fileName + " was last updated at " + str(datetime.datetime.utcnow()) + "\n")
                    else:
                        f.write(line)
        else:
            with open("updated.txt", "a") as f:
                f.write(fileName + " was last updated at " + str(datetime.datetime.utcnow()) + "\n")
    else:
        # Create the file
        with open("updated.txt", "w") as f:
            f.write(fileName + " was last updated at " + str(datetime.datetime.utcnow()) + "\n")

def getLocalDate(filename):
    found=False
    if not os.path.exists("updated.txt"):
        return False
    with open("updated.txt", "r") as f:
        # Get date from updated.txt. Find line that starts with "anime-list-full.json was last updated"
        for line in f:
            if line.startswith(filename + " was last updated"):
                # Get "%Y-%m-%dT%H:%M:%SZ" from line
                lastUpdated=datetime.datetime.strptime(line.split(" was last updated at ")[1].strip(), "%Y-%m-%d %H:%M:%S.%f")
                found=True
                break
    if not found:
        return False
    else:
        return lastUpdated
    
def compare(list1,list2):
    # Find the differences between the two lists.
    # There are 2 types of differences
    # 1. Item is missing from one list
    # 2. Item is on both lists but has different values for progress, score, or list

    # Return 2 lists of entries to be changed or added for list 1 and for list 2
    list1Changes=[]
    list2Changes=[]

    # Filter out any items that don't have both MALID and AniListID
    list1=[item for item in list1 if "MALID" in item and "AniListID" in item]
    list2=[item for item in list2 if "MALID" in item and "AniListID" in item]
    # Find items that are in list1 but not in list2
    for item in list1:
        malID=item["MALID"]
        aniListID=item["AniListID"]
        found=False
        for item2 in list2:
            if item2["MALID"]==malID or item2["AniListID"]==aniListID:
                found=True
                break
        if not found:
            list2Changes.append(item)
    # Find items that are in list2 but not in list1
    for item in list2:
        malID=item["MALID"]
        aniListID=item["AniListID"]
        found=False
        for item2 in list1:
            if item2["MALID"]==malID or item2["AniListID"]==aniListID:
                found=True
                break
        if not found:
            list1Changes.append(item)
    # Find items that are in both lists but have different values
    for item1 in list1:
        for item2 in list2:
            if item1["AniListID"]==item2["AniListID"] or item1["MALID"]==item2["MALID"]:
                if item1["progress"]!=item2["progress"] or int(item1["score"])!=int(item2["score"]) or item1["list"]!=item2["list"]:
                    # if lists are both completed, score is the same, and progress is within 2 episodes, ignore
                    if not(item1["list"]=="completed" and item2["list"]=="completed" and abs(item1["progress"]-item2["progress"])<=2 and int(item1["score"])==int(item2["score"])):
                        #use the list that has the most recent update
                        if item1["updatedAt"]>item2["updatedAt"]:
                            list2Changes.append(item1)
                        else:
                            list1Changes.append(item2)
    return list1Changes,list2Changes

def addID(list, AniList):
    #open anime-list-full.json
    with open('anime-list-full.json') as f:
        animeList = json.load(f)
    #add AniListID to list
    #filter out items from animeList that don't have both MALID and AniListID
    animeList=[item for item in animeList if "mal_id" in item and "anilist_id" in item]
    itemsToRemove=[]
    for item in list:
        for anime in animeList:
            if "MALID" in item and item["MALID"]==anime["mal_id"]:
                if "AniListID" not in item:
                    item["AniListID"]=anime["anilist_id"]
                elif item["AniListID"]!=anime["anilist_id"]:
                    print("Error: AniListID mismatch")
                    print(item["AniListID"])
                    print(anime["anilist_id"])
            if "AniListID" in item and item["AniListID"]==anime["anilist_id"]:
                if "MALID" not in item:
                    item["MALID"]=anime["mal_id"]
                elif item["MALID"]!=anime["mal_id"]:
                    print("Error: MALID mismatch")
                    print(item["MALID"])
                    print(anime["mal_id"])
        if "MALID" not in item or "AniListID" not in item:
            if "MALID" not in item:
                print("Error: MALID not found for AniListID: " + str(item["AniListID"]))
            if "AniListID" not in item:
                print("Error: AniListID not found for MALID: " + str(item["MALID"]))
            # Looking to see if match can be made through AniList
            if "MALID" in item:
                for anime in AniList:
                    if item["MALID"]==anime["MALID"]:
                        item["AniListID"]=anime["AniListID"]
                        break
            #remove item from list
            itemsToRemove.append(item)
    for item in itemsToRemove:
        list.remove(item)
    return list