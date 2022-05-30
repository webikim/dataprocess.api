import os.path

import toml
from fastapi.security import OAuth2PasswordBearer

base_path = os.path.dirname(__file__)
config_path = os.path.join(base_path, '../config')

config = toml.load(os.path.join(config_path, 'dataprocess.toml'))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
