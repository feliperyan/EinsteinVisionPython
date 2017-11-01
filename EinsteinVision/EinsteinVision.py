import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import jwt
import time
import base64
import os
import json


API_ROOT = 'https://api.einstein.ai/v2/'
API_GET_USAGE = API_ROOT + 'apiusage'
API_GET_MODEL_INFO = API_ROOT + 'vision/models/'
API_GET_DATASETS_INFO = API_ROOT + 'vision/datasets'
API_GET_PREDICTION_IMAGE_URL = API_ROOT + 'vision/predict'
API_OAUTH = API_ROOT + 'oauth2/token'
API_GET_MODELS = API_ROOT + 'vision/datasets/<dataset_id>/models'
API_CREATE_DATASET = API_ROOT + 'vision/datasets/upload/sync'
API_CREATE_DATASET_ASYNC = API_ROOT + 'vision/datasets/upload' #not yet used
API_TRAIN_MODEL = API_ROOT + 'vision/train'


class EinsteinVisionService:
    """ A wrapper for Salesforce's Einstein Vision API.
        :param token: string, in case you obtained a token somewhere else and want to use it here.
        :param email: string, the username for your Enstein Vision account, not needed if you already have a token
        :param pem_file: string, name of a file containing your secret key, defaults to predictive_services.pem    
    """
    def __init__(self, token=None, email=None, pem_file='predictive_services.pem'):
        self.token = token
        self.email = email

        if token is None:
            with open(pem_file, 'r') as pem:
                pem_data = pem.read()

            self.private_key = pem_data


    def get_token(self):
        """ Acquires a token for futher API calls, unless you already have a token this will be the first thing
            you do before you use this.
            :param email: string, the username for your EinsteinVision service, usually in email form
            :para pem_file: string, file containing your Secret key. Copy contents of relevant Config Var
            on Heroku to a file locally.
            attention: this will set self.token on success
            attention: currently spitting out results via a simple print
            returns: requests object
        """
        payload = {
            'aud': API_OAUTH,
            'exp': time.time()+600, # 10 minutes
            'sub': self.email
        }

        header = {'Content-type':'application/x-www-form-urlencoded'}

        assertion = jwt.encode(payload, self.private_key, algorithm='RS256')
        assertion = assertion.decode('utf-8')

        response = requests.post(
            url=API_OAUTH,
            headers=header,
            data='grant_type=urn:ietf:params:oauth:grant-type:jwt-bearer&assertion='+assertion
        )

        print(response.text)

        if response.status_code == 200:
            print('status 200 ok for Token')
            self.token = response.json()['access_token']
        else:
            print('Could not get Token. Status: ' + str(response.status_code))

        return response


    def check_for_token(self, token=None):       
        if token:
            return token
        else:
            return self.token


    def get_model_info(self, model_id, token=None, url=API_GET_MODEL_INFO):
        """ Gets information about a specific previously trained model, ie: stats and accuracy
            :param model_id: string, model_id previously supplied by the API
            returns: requests object
        """
        auth = 'Bearer ' + self.check_for_token(token)
        h = {'Authorization': auth, 'Cache-Control':'no-cache'}
        the_url = url + model_id
        r = requests.get(the_url, headers=h)

        return r


    def get_datasets_info(self, token=None, url=API_GET_DATASETS_INFO):
        """ Gets information on all datasets for this account
            returns: requests object
        """
        auth = 'Bearer ' + self.check_for_token(token)
        h = {'Authorization': auth, 'Cache-Control':'no-cache'}
        the_url = url
        r = requests.get(the_url, headers=h)

        return r


    def get_url_image_prediction(self, model_id, picture_url, token=None, url=API_GET_PREDICTION_IMAGE_URL):
        """ Gets a prediction from a supplied picture url based on a previously trained model.
            :param model_id: string, once you train a model you'll be given a model id to use.
            :param picture_url: string, in the form of a url pointing to a publicly accessible
            image file.
            returns: requests object 
        """
        auth = 'Bearer ' + self.check_for_token(token)
        m = MultipartEncoder(fields={'sampleLocation':picture_url, 'modelId':model_id})
        h = {'Authorization': auth, 'Cache-Control':'no-cache', 'Content-Type':m.content_type}
        the_url = url
        r = requests.post(the_url, headers=h, data=m)

        return r


    def get_fileb64_image_prediction(self, model_id, filename, token=None, url=API_GET_PREDICTION_IMAGE_URL):
        """ Gets a prediction from a supplied image on your machine, by encoding the image data as b64
            and posting to the API.
            :param model_id: string, once you train a model you'll be given a model id to use.
            :param filename: string, the name of a file to be posted to the api.
            returns: requests object
        """
        auth = 'Bearer ' + self.check_for_token(token)        
        h = {'Authorization': auth, 'Cache-Control':'no-cache'}
        the_url = url

        with open(filename, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())

        m = MultipartEncoder(fields={'sampleBase64Content':encoded_string, 'modelId':model_id})
        h = {'Authorization': auth, 'Cache-Control':'no-cache', 'Content-Type':m.content_type}
        r = requests.post(the_url, headers=h, data=m)

        return r


    def create_dataset_synchronous(self, file_url, dataset_type='image', token=None, url=API_CREATE_DATASET):
        """ Creates a dataset so you can train models from it
            :param file_url: string, url to an accessible zip file containing the necessary image files
            and folder structure indicating the labels to train. See docs online.
            :param dataset_type: string, one of the dataset types, available options Nov 2017 were 
            'image', 'image-detection' and 'image-multi-label'.
            returns: requests object
        """
        auth = 'Bearer ' + self.check_for_token(token)
        m = MultipartEncoder(fields={'type':dataset_type, 'path':file_url})
        h = {'Authorization': auth, 'Cache-Control':'no-cache', 'Content-Type':m.content_type}
        the_url = url
        r = requests.post(the_url, headers=h, data=m)

        return r


    def train_model(self, dataset_id, model_name, token=None, url=API_TRAIN_MODEL):
        """ Train a model given a specifi dataset previously created
            :param dataset_id: string, the id of a previously created dataset
            :para model_name: string, what you will call this model
            attention: This may take a while and a response will be returned before the model has
            finished being trained. See docos and method get_training_status.
            returns: requests object
        """
        auth = 'Bearer ' + self.check_for_token(token)
        m = MultipartEncoder(fields={'name':model_name, 'datasetId':dataset_id})
        h = {'Authorization': auth, 'Cache-Control':'no-cache', 'Content-Type':m.content_type}
        the_url = url
        r = requests.post(the_url, headers=h, data=m)

        return r


    def get_training_status(self, model_id, token=None, url=API_TRAIN_MODEL):
        """ Gets status on the training process once you create a model
            :param model_id: string, id of the model to check
            returns: requests object
        """
        auth = 'Bearer ' + self.check_for_token(token)
        h = {'Authorization': auth, 'Cache-Control':'no-cache'}
        the_url = url + '/' + model_id
        r = requests.get(the_url, headers=h)

        return r


    def get_models_info_for_dataset(self, dataset_id, token=None, url=API_GET_MODELS):
        """ Gets metadata on all models available for given dataset id
            :param dataset_id: string, previously obtained dataset id
            warning: if providing your own url here, also include the dataset_id in the right place
            as this method will not include it for you. Otherwise use the dataset_id attribute as 
            per usual
            returns: a requests object
        """
        auth = 'Bearer ' + self.check_for_token(token)
        h = {'Authorization': auth, 'Cache-Control':'no-cache'}
        if url != API_GET_MODELS:
            r = requests.get(the_url, headers=h)
            return r

        the_url = url.replace('<dataset_id>', dataset_id)
        r = requests.get(the_url, headers=h)

        return r

    
    #TODO: Something I did when outputting the file failed and I just repeated the same row over and over again.
    def parse_rectlabel_app_output(self):
        # get json files only
        files = []
        files = [f for f in os.listdir() if f[-5:] == '.json']

        if len(files) == 0:
            print('No json files found in this directory')
            return None

        max_boxes = 0        
        rows = []

        for each_file in files:
            f = open(each_file, 'r')
            j = f.read()            
            j = json.loads(j)            
            f.close()

            # running count of the # of boxes.
            if len(j['objects']) > max_boxes:
                max_boxes = len(j['objects'])

            # Each json file will end up being a row
            # set labels
            row = []

            for o in j['objects']:
                labels = {}
                labels['label'] = o['label']
                labels['x'] = o['x_y_w_h'][0]
                labels['y'] = o['x_y_w_h'][1]
                labels['width'] = o['x_y_w_h'][2]
                labels['height'] = o['x_y_w_h'][3]

                # String manipulation for csv
                labels_right_format = '\"' + json.dumps(labels).replace('"', '\"\"') + '\"'

                row.append(labels_right_format)

            row.insert(0, '\"' + j['filename'] + '\"')        

            rows.append(row)

        # on array element per row
        rows = [','.join(i) for i in rows]

        header = '\"image\"'
        
        for box_num in range(0, max_boxes):
            header += ', \"box\"' + str(box_num)

        rows.insert(0, header)
        return rows

    def save_parsed_data_to_csv(self, output_filename='output.csv'):
        result = self.parse_rectlabel_app_output()

        ff = open(output_filename, 'w', encoding='utf8')

        for line in result:
            ff.write(line + '\n')

        ff.close()
