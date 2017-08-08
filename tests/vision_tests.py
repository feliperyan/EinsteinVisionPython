import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

print(sys.path)

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
#    
#
    def test_init_and_pem_file(self):
        with patch('EinsteinVision.EinsteinVision.open', mock_open(read_data='some pem file data')) as m:
            genius = EinsteinVisionService(email='f@f.com', pem_file='aloha.pem')            
        
        self.assertTrue(genius is not None)
        self.assertTrue(genius.private_key == 'some pem file data')
#
#
    @patch('EinsteinVision.EinsteinVision.requests.post')
    def test_get_token(self, mock_post):        

        mock_post.return_value.status_code = 200
        mock_post.return_value.json = lambda : {'access_token':'aloha'}

        self.assertTrue(self.genius.token is None)
        self.genius.get_token()
        print('this is the token: ' + str(self.genius.token))
        self.assertTrue(self.genius.token is not None)
#
#
if __name__ == '__main__':
    unittest.main()