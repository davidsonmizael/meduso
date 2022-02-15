#!/usr/bin/env python3
import os
import logging
import logging.config
from app import init_app
import yaml
from dotenv import load_dotenv

logging.config.fileConfig('config/logger.conf', defaults={'logfilename': 'logs/main.log'})
logger = logging.getLogger('flaskApp')

#loading .env 
load_dotenv()

#loading project settings
config = {}
with open('config/project_settings.yml') as fs:
    try:
        config = yaml.safe_load(fs)
    except yaml.YAMLError:
        logger.exception('Failed to load project settings yaml file.')
        exit()

secret_key = os.getenv('APPLICATON_SECRET_KEY')
token_expiration_seconds = config['jwt']['token_expiration_seconds']
rtoken_expiration_seconds = config['jwt']['rtoken_expiration_seconds']

app = init_app(logger, secret_key, token_expiration_seconds, rtoken_expiration_seconds)

if __name__ == '__main__':
    
    logger.info("Listing all the available urls:")
    for url in app.url_map.iter_rules():
        if url.endpoint != 'static':
            logger.info(f" > {url}")

    app.run(host=config['flask']['host'], port=config['flask']['port'], debug=config['flask']['debug'])