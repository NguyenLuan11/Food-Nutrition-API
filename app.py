from lib import create_app

if __name__ == "__main__":
    app = create_app()
    app.run(host='127.0.143.145', port=7777, debug=True)
