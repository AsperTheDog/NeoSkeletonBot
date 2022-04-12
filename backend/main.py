from Bot.bot import runBot
from routes import runFlask
from threading import Thread
import sys


if __name__ == "__main__":
    print("Initializing Bot")
    botThr = Thread(target=runBot, daemon=True)
    botThr.start()
    print("initializing Server")
    runFlask(sys.argv[1] if len(sys.argv) > 1 else None)
