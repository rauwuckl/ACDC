import requests
import json
import time

global config
global ms_id_2_key
global key_2_ms_id

ms_id_2_key = dict()
key_2_ms_id = dict()

with open("../general_config.json", "r") as f:
    config = json.load(f)

personGroupID = config["personGroupID"]

def add_person(personID):
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': config["subscription_key"],
    }

    body = {
        "name": personID,
        "userData": personID,
    }

    response = requests.request('POST', 'https://' + config["uri_base"] + '/face/v1.0/persongroups/{}/persons'.format(personGroupID), headers=headers, json=body)
    r = json.loads(response.text)
    print(response)
    print(response.text)
    ms_personID = r['personId']

    ms_id_2_key[ms_personID] = personID
    key_2_ms_id[personID] = ms_personID




def add_face(personID, picID):
    ms_personID = key_2_ms_id[personID]

    # Request headers.
    headers = {
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': config["subscription_key"],
    }

    fp = open("{}/{}".format(personID, picID), "rb")

    # Request parameters.
    params = {
        'userData': personID + "_" + picID,
    }

    # Body. The URL of a JPEG image to analyze.

    # Execute the REST API call and get the response.
    response = requests.request('POST', 'https://' + config["uri_base"] + '/face/v1.0/persongroups/{}/persons/{}/persistedFaces'.format(personGroupID, ms_personID), data=fp, headers=headers, params=params)

    print(response)
    print(response.text)

def train_group():
    print("training")
    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': config["subscription_key"],
    }

    response = requests.request('POST', 'https://' + config["uri_base"] + '/face/v1.0/persongroups/{}/train'.format(personGroupID), headers=headers)
    print(response)
    print(response.text)

def add_group():
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': config["subscription_key"],
    }
    body = {
        'name': personGroupID,
    }

    response = requests.request('PUT', 'https://' + config["uri_base"] + '/face/v1.0/persongroups/{}'.format(personGroupID), json=body, headers=headers)
    print(response)
    print(response.text)



def train_all_faces():
    add_group()
    people = config["people"]
    pics = config["files"]
    for pers in people:
        add_person(pers)
        for pic in pics:
            add_face(pers, pic)
        time.sleep(30)

    train_group()
    with open("../ms_id_2_key.json", "w") as f:
        json.dump(ms_id_2_key, f)


train_all_faces()