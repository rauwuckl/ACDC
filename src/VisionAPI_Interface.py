
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
    """
    Function receives response object as is delivered by the Microsoft vision api.

    :param response: reaquest.response object
    :return: (patient_id: String, distress_level: float(between 0 and 1, 1 is max pain)
    """
    return ("Ankunding307_Kevin849_40", 0.3) #TODO there needs to go functionallity here

