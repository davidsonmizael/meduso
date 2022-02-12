from flask import Flask
from backend.communicator import comm_blueprint
from backend.manage import manage_blueprint
from frontend.views.urls import dash_blueprint

app = Flask(__name__)

app.register_blueprint(dash_blueprint, url_prefix='/panel')
app.register_blueprint(comm_blueprint, url_prefix='/api/v1.0')
app.register_blueprint(manage_blueprint, url_prefix='/api/v1.0/manage')

if __name__ == '__main__':
    
    print("Listing all URLs:")
    for url in app.url_map.iter_rules():
        if url.endpoint != 'static':
            print(" - " + str(url))

    app.run(debug=True)