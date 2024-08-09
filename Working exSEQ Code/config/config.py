import yaml


def getConfig(*,path = './config/config.yaml'):
    with open(path,'r') as config_file:
        config = yaml.safe_load(config_file)
    return config

def setConfig(data:dict,*,path = './config/config.yaml'):
    with open(path, 'w') as config_file:
        yaml.safe_dump(data,config_file)

if __name__ == '__main__':
    print(getConfig())
    setConfig({'hello':'world'},path = './test_config.yml')