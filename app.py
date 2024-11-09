from lib import create_app, register_mdns_service, get_local_ip
import os
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    register_mdns_service()
    app = create_app()
    host_ip = get_local_ip()

    if not os.path.exists(app.config['UPLOAD_FOLDER_ADMIN']):
        os.makedirs(app.config['UPLOAD_FOLDER_ADMIN'])
    if not os.path.exists(app.config['UPLOAD_FOLDER_USERS']):
        os.makedirs(app.config['UPLOAD_FOLDER_USERS'])
    if not os.path.exists(app.config['UPLOAD_FOLDER_FOODS']):
        os.makedirs(app.config['UPLOAD_FOLDER_FOODS'])
    if not os.path.exists(app.config['UPLOAD_FOLDER_ARTICLES']):
        os.makedirs(app.config['UPLOAD_FOLDER_ARTICLES'])

    app.run(host=host_ip, port=os.environ.get("PORT"), debug=True)
