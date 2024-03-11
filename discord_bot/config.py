import os
import environ  # pip install django-environ

configPath = os.path.dirname(os.path.abspath(__file__))

env = environ.Env(DEBUG=(bool, True))

envPath = os.path.join(configPath, '.prod.env')

environ.Env.read_env(env_file=envPath)
