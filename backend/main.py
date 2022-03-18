from Bot.bot import runBot
from routes import runFlask
from threading import Thread


if __name__ == "__main__":
    print("Initializing Bot")
    botThr = Thread(target=runBot, daemon=True)
    botThr.start()
    print("initializing Server")
    runFlask()
