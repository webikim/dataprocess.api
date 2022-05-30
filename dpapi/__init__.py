import os.path

import toml
from fastapi.security import OAuth2PasswordBearer

base_path = os.path.dirname(__file__)
config_path = os.path.join(base_path, '../config')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

config = toml.load(os.path.join(config_path, 'dataprocess.toml'))

anno_config = config['annotation']
image_path = anno_config.get('IMAGE_PATH')
label_path = anno_config.get('LABEL_PATH')
out_path = anno_config.get('OUT_PATH')
if not os.path.isdir(out_path):
    os.mkdir(out_path)
