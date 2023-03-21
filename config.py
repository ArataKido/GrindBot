from dotenv import dotenv_values

config = dotenv_values('.env')
#TODO remove global instates, prob put them in a class
PROD_URL = config['PROD_URL']
DEMO_URL = config['DEMO_URL']
APP_TOKEN = config['APP_TOKEN']
USER_TOKEN = config['USER_TOKEN']
