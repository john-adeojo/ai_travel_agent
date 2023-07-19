import yaml
import os

def read_config():
    # Get the directory of the current script
    script_dir = "../src/"

    # Construct the full path to the configuration file
    file_path = os.path.join(script_dir, "apikeys.yml")

    with open(file_path, 'r') as stream:
        try:
            configs = yaml.safe_load(stream)
            api_key = configs['amadeues_flights']['api_key']
            api_secret = configs['amadeues_flights']['api_secret']
            openai_key = configs['openai']['openai_key']
            hugging_api_key = configs['huggingfacehub']['hugging_api_key']
            return api_key, api_secret, openai_key, hugging_api_key
        except yaml.YAMLError as exc:
            print(exc)
            
    return api_key, api_secret, openai_key

class SingletonToken:
    __token = None

    @classmethod
    def set_token(cls, token):
        cls.__token = token

    @classmethod
    def get_token(cls):
        return cls.__token