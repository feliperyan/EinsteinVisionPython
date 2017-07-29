API_ROOT = 'https://api.einstein.ai/v2/'
API_GET_USAGE = API_ROOT + 'apiusage'
API_GET_MODEL_INFO = API_ROOT + 'vision/models/'
API_GET_DATASETS_INFO = API_ROOT + 'vision/datasets'
API_GET_PREDICTION_IMAGE_URL = API_ROOT + 'vision/predict'
API_OAUTH = API_ROOT + 'oauth2/token'

import requests
import jwt
import time

class EinsteinVisionService:

    def __init__(self, token='', email=''):
        self.token = token
        self.email = email


    def get_token(self, pem_file):

        pem = open(pem_file, 'r')
        pem_data = pem.read()
        pem.close()

        payload = {
            'aud': API_OAUTH,
            'exp': time.time()+600, # 10 minutes
            'sub': self.email
        }

        header = {'Content-type':'application/x-www-form-urlencoded'}

        assertion = jwt.encode(payload, pem_data, algorithm='RS256')
        assertion = assertion.decode('utf-8')

        response = requests.post(
            url=API_OAUTH,
            headers=header,
            data='grant_type=urn:ietf:params:oauth:grant-type:jwt-bearer&assertion='+assertion
        )

        print(response.text)

        if response.status_code == 200:
            self.token = response.json()['access_token']


    def check_for_token(self, token):
        if token:
            return token
        else:
            return self.token


    def get_model_info(self, model_id, token=None, url=API_GET_MODEL_INFO):
        auth = 'Bearer ' + self.check_for_token(token)
        h = {'Authorization': auth, 'Cache-Control':'no-cache'}
        the_url = url + model_id
        r = requests.get(the_url, headers=h)

        return r.json()


    def get_datasets_info(self, token=None, url=API_GET_DATASETS_INFO):
        auth = 'Bearer ' + self.check_for_token(token)
        h = {'Authorization': auth, 'Cache-Control':'no-cache'}
        the_url = url
        r = requests.get(the_url, headers=h)

        return r.json()


    def get_image_prediction(self, model_id, picture_url, token=None, url=API_GET_DATASETS_INFO):
        auth = 'Bearer ' + self.check_for_token(token)
        h = {'Authorization': auth, 'Cache-Control':'no-cache', 'Content-Type': 'multipart/form-data'}
        the_url = url
        r = requests.post(the_url, headers=h, data={'sampleLocation':picture_url, 'modelId': model_id})

        return r.json()

