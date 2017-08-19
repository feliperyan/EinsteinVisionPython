[![codecov](https://codecov.io/gh/feliperyan/EinsteinVisionPython/branch/master/graph/badge.svg)](https://codecov.io/gh/feliperyan/EinsteinVisionPython)
# EinsteinVisionPython

### Very much a work in progress Python Wrapper for the [Einstein Predictive Vision API service](https://devcenter.heroku.com/articles/einstein-vision)

2017-08-16 At the moment you can use this to:
1. Read a .pem file
2. Generate an Auth Token
3. Send an image URL and a modelId (GeneralImageClassifier if you want) and get a prediction
4. Upload an image file as base64 for prediction
5. Create a dataset from an accessible zip url
6. Train a model given a dataset id
7. Check on status of training
