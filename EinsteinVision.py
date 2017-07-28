API_ROOT = 'https://api.einstein.ai/v2/'
API_GET_USAGE = API_ROOT + 'apiusage'
API_GET_MODEL_INFO = API_ROOT + 'vision/models/'
API_GET_DATASETS_INFO = API_ROOT + 'vision/datasets'
API_GET_PREDICTION_IMAGE_URL = API_ROOT + 'vision/predict'

import requests

class EinsteinVisionService:
    
    def __init__(self, token=''):
        self.token = token


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

