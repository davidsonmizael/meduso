import yaml
from run import app

#loading project settings
config = {}
with open('config/project_settings.yml') as fs:
    try:
        config = yaml.safe_load(fs)
    except yaml.YAMLError:
        print('Failed to load project settings yaml file.')
        exit()
    
if __name__ == '__main__':
    host_ip = config['flask']['host']
    host_port = config['flask']['port']
    app.run(host=host_ip, port=host_port)