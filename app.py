from lib import create_app
import os
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    app = create_app()
    app.run(host=os.environ.get("HOST"), port=os.environ.get("PORT"), debug=True)
