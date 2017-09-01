import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

import unittest
from unittest.mock import patch, mock_open, MagicMock
from unittest import mock
from EinsteinVision.EinsteinVision import EinsteinVisionService
import json


FAKE_PEM = '''-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEAg2bJUmZ6z7O/BqJ55XgTjcUS+zGK8d6o+3XiIasXqRcd9Duv
N2qSNz6DYYQ0DZLwaMdz4TiiwfGSH/4UPMwwmemiu0O14JGx1mI5EO0ZH+w1WvSh
4VSEvTmsybUGIaAl5iW6f0UILadc2L6oIdeugYqNb5Uewl68swA3MHd3GujyCR2q
zZa6uD8o0ptG/gK/dRyGT75+J+pfSl+F5qOjOUYTX7yTmxzTUADEWLmX+LtXeQus
wKglek+4q1gkySn9A4fvchIeYwTVB4q7KLsQzYy+6CnDiRQF77PivBn9cLNmKgN2
z31KdbQFuk3vELvWHQnhIHE4FrMbUoGBXFvlxQIDAQABAoIBACNN0nlZH1X+rSxT
Kv0ELfzBHkBvJy2k7THikkcJeOntVBbykjkJYQ+GtDXXF0UuXXlJXVD9rnz9Mo11
7moHUmeH5jj6EDut6WH4MeziRwXUqOEvKO8pjiBpBouLH4KZTJVxPZJEMdZSSRfS
4cl18WTMnQOFxSXj3j8Zp7pV3qJT3K3VO7MJrYBiyTnMwpeoRQ6fHbs/FsPR7h//
KF1T2/ilrwBUrx3cqgxL+GRxJLPZSv7u2wMhUhuD9OGq1sY3Wsvv0mF+l6oscwjo
5MZNK9OhziZDVnSqlpL6xWgmJbpxnSAslgmbIAUPOkPOXiAc3mDGSg5FemdQw3Is
bIBvo2ECgYEA+ZwkJb5d/v3QDWv71KBBo7ZRuW2IgUyw1TX8dYmmYq1si92lOJei
P7gbeaD7rUCySCmf4wY0GOsIMNcRx1NYsJ6RYpP5KPrD1h0HTTZoD9cEKriyGBuC
tKMB02kGHzS8FdiY0xTxEWoPuLxCzb96hI0VWho1u6+1UwEGrumw0csCgYEAhsPy
hNKpbjw7jtSunp3MyYeZp2WwM3roypqmK4PGkTNQK+JXzLp/OvNYQUpjLYZmW5tY
VfhiSy5N7AHfbHLv35iRJtgJAddjHYtQZxiP628Q3oHLOn18rvcSPkWIrMsneQA0
7hPbheyZB0cxmdZjL93Qx2TqhhpL5zbYtEC19K8CgYEA0/j0fZUPr+cNkwhb4TKC
66t99ZF+NgfRuA7TqWFPCkeqgZClqcyjvab0tjKu6G+jt0KaBCqVfX/DAe7yqyot
jDfs0SFGm7VxL9iRBdIpRyJa6IjWvUBHnG09tLJgv4mCHK9HASKsohRG66P8u0tb
mUtSkaTmctABlU6uxUWxokcCgYBGgmTz64hsPaVnoI1QPf20f3b8J28eMDN2NZ21
bLfKpo9Otpj7a6Q/wqwtVO85FXWeflOkf1VmQm7QiVZNVoF8ekWPjj6AMSIRhh9m
IWrDYpPv5vbevmMq4+gunpDY313iqCIJYmhb1KNoNG6WL54roCGpAXrW+RE3gvG0
tZq9zwKBgQCC2oW1oYQ4eJm28zofbR483KCy7qaWhYA9n5UvWKV7zyOqco3hQ7Xy
qY+ihiK1RQhGMix6w0yAP9o6KTpvsNfiy4RvEsJSIoKW/0s7yoXNjB+aE/dfp0UE
D1+pHy9YT4pxD9ItIErxOw/mSrY0toauZJWXYQ9/SO66NS/BFg4uoQ==
-----END RSA PRIVATE KEY-----
'''

class TestStringMethods(unittest.TestCase):
    
    def setUp(self):
        with patch('EinsteinVision.EinsteinVision.open', mock_open(read_data=FAKE_PEM)) as m:
            self.genius = EinsteinVisionService(email='f@f.com', pem_file='aloha.pem')
   

    def test_init_and_pem_file(self):
        with patch('EinsteinVision.EinsteinVision.open', mock_open(read_data='some pem file data')) as m:
            genius = EinsteinVisionService(email='f@f.com', pem_file='aloha.pem')            
        
        self.assertTrue(genius is not None)
        self.assertTrue(genius.private_key == 'some pem file data')


    @patch('EinsteinVision.EinsteinVision.requests.post')
    def test_get_token(self, mock_post):

        mock_post.return_value.status_code = 200
        mock_post.return_value.json = lambda : {'access_token':'aloha'}

        self.assertTrue(self.genius.token is None)
        self.genius.get_token()
        print('this is the token: ' + str(self.genius.token))
        self.assertTrue(self.genius.token is not None)


    @patch('EinsteinVision.EinsteinVision.requests.get')
    def test_get_datasets_info(self, mock_get):

        mock_get.return_value.status_code = 200
        mock_get.return_value.json = lambda : {'object':'list', 'data':[]}

        self.genius.token = 'dummy token'

        self.assertTrue(self.genius.get_datasets_info().json() is not None)
        self.assertTrue('data' in self.genius.get_datasets_info().json().keys())
        self.assertTrue('object' in self.genius.get_datasets_info().json().keys())


    @patch('EinsteinVision.EinsteinVision.requests.get')
    def test_get_model_info(self, mock_get):

        mock_get.return_value.status_code = 200
        mock_get.return_value.json = lambda : {'metricsData':'list'}

        self.genius.token = 'dummy token'

        self.assertTrue(self.genius.get_model_info(model_id='dummy id').json() is not None)
        self.assertTrue('metricsData' in self.genius.get_model_info(model_id='dummy id').json().keys())

    def test_check_for_token(self):
        self.assertTrue(self.genius.check_for_token('ok') == 'ok')
        self.genius.token = 'dummy token'
        self.assertTrue(self.genius.check_for_token() == 'dummy token')


    @patch('EinsteinVision.EinsteinVision.requests.post')
    def test_get_url_image_prediction(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json = lambda : {'probabilities':'aloha', 'object':'predictresponse'}

        self.genius.token = 'dummy token'

        response = self.genius.get_url_image_prediction(model_id='dummy', picture_url='www.dummy.com/img.jpg')

        self.assertTrue(response.json() is not None)
        self.assertTrue('probabilities' in response.json().keys())
        self.assertTrue('object' in response.json().keys())

    
    @patch('EinsteinVision.EinsteinVision.requests.post')
    def test_get_fileb64_image_prediction(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json = lambda : {'probabilities':'aloha', 'object':'predictresponse'}
        self.genius.token = 'dummy token'

        with patch('EinsteinVision.EinsteinVision.open', mock_open(read_data=b'some binary picture file data')) as m:
            response = self.genius.get_fileb64_image_prediction(model_id='dummy', filename='dummyfile.jpg')            

        self.assertTrue(response.json() is not None)
        self.assertTrue('probabilities' in response.json().keys())
        self.assertTrue('object' in response.json().keys())

    
    @patch('EinsteinVision.EinsteinVision.requests.post')
    def test_create_dataset_synchronous(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json = lambda : {'probabilities':'aloha', 'object':'predictresponse'}
        self.genius.token = 'dummy token'

        response = self.genius.create_dataset_synchronous(file_url='dummy url')

        self.assertTrue(response.json() is not None)


    @patch('EinsteinVision.EinsteinVision.requests.post')
    def test_train_model(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json = lambda : {'datasetId':'51', 'status':'queued'}
        self.genius.token = 'dummy token'

        response = self.genius.train_model(dataset_id='123', model_name='model')

        self.assertTrue(response.json() is not None)


    @patch('EinsteinVision.EinsteinVision.requests.get')
    def test_get_training_status(self, mock_get):

        mock_get.return_value.status_code = 200
        mock_get.return_value.json = lambda : {'object':'list', 'data':[]}

        self.genius.token = 'dummy token'
        response = self.genius.get_training_status(model_id='1234').json()
        
        self.assertTrue(response is not None)        


    @patch('EinsteinVision.EinsteinVision.requests.get')
    def test_get_models_info_for_dataset(self, mock_get):

        mock_get.return_value.status_code = 200
        mock_get.return_value.json = lambda : {'object':'list', 'data':[]}

        self.genius.token = 'dummy token'
        response = self.genius.get_models_info_for_dataset(dataset_id='1234').json()
        
        self.assertTrue(response is not None)



if __name__ == '__main__':
    unittest.main()