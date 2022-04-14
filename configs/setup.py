import json


print("Hello! We are now going to configure some basic settings. If you want to leave the default option just press enter\n")
host = input("Enter your IP address or NDS route (default: localhost)")
if host == "":
  host = "localhost"
while True:
  backport = input("Enter the port for the bot server (default: 12546)")
  if backport == "":
    backport = 12546
    break
  else:
    try:
      backport = int(backport)
      if backport < 1024 or backport > 49151:
        print("Invalid port number, must be between 1024 and 49151 (not included)")
        continue
      break
    except ValueError:
      print("Ports must be numbers between 1024 and 49151 (not included)")
while True:
  frontport = input("Enter the port for the webpage (default: 12547)")
  if frontport == "":
    frontport = 12547
    break
  else:
    try:
      frontport = int(frontport)
      if frontport < 1024 or frontport > 49151 or frontport == backport:
        print("Invalid port number, must be between 1024 and 49151 (not included) and must be different from the bot server port")
        continue
      break
    except ValueError:
      print("Ports must be numbers between 1024 and 49151 (not included) and must be different from the bot server port")
listen = "Which IPs do you want the bot server to listen to? (Default: 0.0.0.0)"

with open("config.json", "w") as file:
  json.dump({
    "rootAddr": host,
    "backListen": listen,
    "frontPort": frontport,
    "backPort": backport
  })

secret = input("Enter the client secret of your oauth2 app (found in the Discord Developer Portal -> your app -> oauth2 -> general)")
ID = input("Enter the client ID of your oauth2 app (found in the Discord Developer Portal -> your app -> OAuth2 -> General)")
token = input("Enter the token of your bot (found in the Discord Developer Portal -> your app -> Bot)")

yml = "token: '{}'\nclientID: {}\nclientSecret: '{}'".format(token, ID, secret)

with open("Bot/bot.yaml", "w") as file:
  file.write(yml)