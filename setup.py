from distutils.core import setup
setup(
  name = 'EinsteinVision',
  packages = ['EinsteinVision'], # this must be the same as the name above
  version = '0.4',
  description = 'Wrapper for Salesforce\'s Einstein Predictive Vision API',
  author = 'Felipe Ryan',
  author_email = 'feliperyan@gmail.com',
  url = 'https://github.com/feliperyan/EinsteinVisionPython', # use the URL to the github repo
  download_url = 'https://github.com/feliperyan/EinsteinVisionPython/archive/0.4.tar.gz', # I'll explain this in a second
  keywords = ['api', 'einsteinpredictivevision', 'metamind', 'salesforce'], # arbitrary keywords
  classifiers = [],
  install_requires=[
          'requests',
          'requests_toolbelt',
          'cryptography',
          'PyJWT'
      ],
)
