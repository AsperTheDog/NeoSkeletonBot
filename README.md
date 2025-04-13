# NeoSkeletonBot

![image](https://github.com/user-attachments/assets/78b1e92f-2249-4364-82e5-5a1ecaf2afe9)

SkeletonBot is a discord bot made to help people create their own custom bots without having to know how to program in a fully fledged programming language. 

Because the possibilities of this bot are completely outside of what a normal host would be able to control **I am not able to host a public version of this**. Thus it's made to be self-hosted. Below you can find instructions to install it.

## How it works

SkeletonBot comes with a compiler and a web server. This allows you to access the controls from the web browser as if you were accessing a webpage, in there you will be able to create scripts for the bot using the visual design based on state machines. The system is made to be safe and intuitive but powerful.

Programmers with experience can expand their capabilities making custom actions if they wish so, the system is made so new action classes are detected and added automatically as long as the template is followed.  

## Installation

**This is the windows installation guide.** Linux installation has not been tested but it should be possible unless Angular uses an npm package that is not compatible (I don't think so though). Nonetheless if you want to install this on linux you will have to do the configuration by yourself until Im able to create a setup guide done.

Before doing anything. Make sure you install these two programs:

 - [Python 3 (***WHEN YOU INSTALL TICK THE OPTION THAT SAYS 'add python to PATH' THIS IS VERY IMPORTANT.***)](https://www.python.org/downloads/)  
> Make sure you download the correct version for your operating system in the *files* section.  


 - [Node.js](https://nodejs.org/en/download/)  
> Simply select the correct operating system in the **LTS** tab  


## Configuration

In order to get the bot working a discord bot must be made. Follow [these](https://dsharpplus.github.io/articles/basics/bot_account.html) instructions to create a bot.

Make sure you activate the following options in the Bot section of the app

 - presence intent
 - server members intent
 - message content intent

<ins>NOTE: You may want to setup a [ddns](https://www.noip.com) if you plan on allowing other people to access from their homes<ins>

First, simply run the file *setup.bat* you will find inside the downloaded folder.  
 
 <details>
  <summary>You will have to fill out some data</summary>
   - Your IP or DNS route will be the main body of the url (it's basically the "something.com" part of a URL), most likely you won't have any. If you plan to use this locally then "localhost" will do the trick just fine, but if you plan on having this publicly then you will either need a ddns (noted before) or your public IP (most IPs change from time to time, so if you choose this then it will probably break eventually). To get your IP simply look up in google "what is my IP" and you will be shown something in the format of x.x.x.x (e.g 123.456.78.9).  <br> <br> 
   - The bot server port is the number the bot app "binds" to. If you don't know what this is then just leave the default.  <br> <br> 
   - The website port is the number the website "binds" to. As with the bot port, if you don't know what it is then just leave it as default.  <br> <br> 
   - The listen port is the IPs that the bot will be listening to. 0.0.0.0 means it will listen to everything. If you are going to run this locally you can change this to 127.0.0.1 so it only listens to your own pc, but this is not necessary and 0.0.0.0 will work just fine.  <br> <br> 
   - the https option will just let the program know better how to generate the login URL (details about this below). This will not have any effect in the configuration of the system onwards.  <br> <br> 
   - The Client secret is a code provided by Discord in order to connect with them. Do not share this code with anyone. This should be given in the Discord Developer Portal app, just follow the path given in the terminal.  <br> <br> 
   - The Client ID is the id of the user created for your bot in discord. Follow the path given in the terminal.  <br> <br> 
   - The token is a secret code that lets Discord know that bot is yours. Do not share this code with anyone. Can be found in the path given by the terminal.  <br> <br> 
 </details>
 
 Once everything has been filled the system will generate the configuration files for you. You can edit these manually if you have done something wrong (or just rerun the setup.bat file and introduce the data again). The routes of the relevant files are *configs/config.json* and *backend/Bot/bot.yaml*
 
You will be given a login URL, this is important, so make sure to save it somewhere before continuing.
 
---
 
Next, if you want your page to be remotely available you have to open the ports shown in the fields **frontPort** and **backPort**, by default these are 12547 and 12546 respectively. The process of opening ports may be different depending on your ISP, but [this guide](https://nordvpn.com/es/blog/open-ports-on-router/) should work as a general guideline.
 
**Remember this step is not needed if you plan to use the system locally (if you are the only one that will be accessing your webpage)**  
 
---
 
Next, we have to tell discord we trust this URL. In the Discord Developer Portal move to your application and go to the section called **oauth2 -> general**. There you should see a button called *add redirect*. Click in there and add the URL the setup file should have given you. Don't forget to save!

## Running

**Make sure you've gone through intallation and configuration sections before trying to run anything!!**

Just run the file *runHTTPS.bat* inside the downloaded folder if you want the webpage to work over HTTPS or *runHTTP.bat* if you want it to work over HTTP (you can change at any time, just make sure you reconfigure the Discord Developer Portal accordingly). It will open two terminals: One for the webpage, and the other one for the bot.

If you don't want to start any process regarding the webpage and just execute the discord bot run the file *runBot.bat*, this will not start the webserver. This could be useful if you no longer have to make any changes to your custom scripts and just want the bot to work as it is. Take into account the webpage is the only way of customizing the behaviour of the bot, so you will have to restart the bot and reload the program with the web if you want to change anything.
