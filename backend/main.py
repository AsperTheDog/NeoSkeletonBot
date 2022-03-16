from Bot.bot import runBot
from routes import app


if __name__ == "__main__":
    print("Initializing Bot")
    runBot(app.run_task(debug=True, host="0.0.0.0", port=12546, certfile='cert/cert.pem', keyfile='cert/key.pem'))
