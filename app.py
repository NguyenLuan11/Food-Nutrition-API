from lib import create_app, register_mdns_service, get_local_ip
import os
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    register_mdns_service()
    app = create_app()
    host_ip = get_local_ip()

    app.run(host=host_ip, port=os.environ.get("PORT"), debug=True)
