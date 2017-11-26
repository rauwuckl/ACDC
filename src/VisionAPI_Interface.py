
import requests

def get_face_id(binary_stream):
    subscription_key = '151948f194d6430692fad8ea8c0246c5'
    uri_base = 'westcentralus.api.cognitive.microsoft.com'

    # Request headers.
    headers = {
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': subscription_key,
    }

    # Request parameters.
    params = {
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'false',
        'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
    }

    # Body. The URL of a JPEG image to analyze.

    # Execute the REST API call and get the response.
    response = requests.request('POST', 'https://' + uri_base + '/face/v1.0/detect/', data=binary_stream, headers=headers, params=params)

    result =  parse_azure_response(response)
    return result

def parse_azure_response(response):
    parsed = json.loads(response.text)
    sadness_num= parsed[0]['faceAttributes']['emotion']['sadness']
    anger_num = parsed[0]['faceAttributes']['emotion']['anger']
    contempt_num = parsed[0]['faceAttributes']['emotion']['contempt']
    disgust_num = parsed[0]['faceAttributes']['emotion']['disgust']
    fear_num = parsed[0]['faceAttributes']['emotion']['fear']
    faceId_key = parsed [0]['faceId']
    pain = (sadness_num + anger_num + contempt_num + disgust_num + fear_num)
    return(faceId_key, pain)

