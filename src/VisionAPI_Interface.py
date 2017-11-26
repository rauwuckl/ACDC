
import json
import requests

with open("general_config.json", "r") as f:
    config = json.load(f)

with open("ms_id_2_key.json", "r") as f:
    ms_id_2_key = json.load(f)

def get_face_id(binary_stream):

    # Request headers.
    headers = {
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': config["subscription_key"],
    }

    # Request parameters.
    params = {
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'false',
        'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
    }

    # Body. The URL of a JPEG image to analyze.

    # Execute the REST API call and get the response.
    response = requests.request('POST', 'https://' + config["uri_base"] + '/face/v1.0/detect/', data=binary_stream, headers=headers, params=params)

    response_json = json.loads(response.text)

    if len(response_json) == 0:
        raise ValueError("No Face in the image")

    pain =  classify_pain(response_json)
    faceID = response_json[0]['faceId']
    print(['faceId'])

    ms_person_id = identify_person(faceID)
    print(ms_person_id)
    our_person_id = ms_id_2_key[ms_person_id]

    #TODO translate faceID to our Key
    return our_person_id, pain

def classify_pain(parsed):
    sadness_num= parsed[0]['faceAttributes']['emotion']['sadness']
    anger_num = parsed[0]['faceAttributes']['emotion']['anger']
    contempt_num = parsed[0]['faceAttributes']['emotion']['contempt']
    disgust_num = parsed[0]['faceAttributes']['emotion']['disgust']
    fear_num = parsed[0]['faceAttributes']['emotion']['fear']
    pain = (sadness_num + anger_num + contempt_num + disgust_num + fear_num)
    return pain

def identify_person(faceID):
    print("identify_person")

    # Request headers.
    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': config["subscription_key"],
    }

    body = {
        "personGroupId": config["personGroupID"],
        "faceIds":[
            faceID
        ],
        "maxNumOfCandidatesReturned": 1,
        "confidenceThreshold": 0.5
    }

    # Body. The URL of a JPEG image to analyze.

    # Execute the REST API call and get the response.
    response = requests.request('POST', 'https://' + config["uri_base"] + '/face/v1.0/identify', json=body, headers=headers)
    print(response)
    print(response.text)
    response_json = json.loads(response.text)
    if len(response_json[0]["candidates"]) == 0:
        raise RuntimeError("Face wasn't recognised")

    canidate = response_json[0]["candidates"][0]["personId"]
    return canidate
