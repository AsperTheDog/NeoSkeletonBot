# NeoSkeletonBot

SkeletonBot is a discord bot made to allow people to create their own custom bots without having to know how to program in a fully fledged programming language. 

Because the possibilities of this bot are completely outside of what a normal host would be able to control **I am not able to host a public version of this**. Thus it's made to be self-hosted. Below you can find instructions to install it.

## How it works

SkeletonBot comes with a compiler and a web server. This allows you to access the controls from the web browser as if you were accessing a webpage, in there you will be able to create scripts for the bot using the visual design based on state machines. The system is made to be safe and intuitive but powerful.

Programmers with experience can expand their capabilities making custom actions if they wish so, the system is made so new action classes are detected and added automatically as long as the template is followed.  
**TODO: WIKI!!**

## Instalation

Before doing anything. Make sure you install these two programs:

 - [Python 3.10](https://www.python.org/downloads/release/python-3104/)  
> Make sure you download the correct version for your operating system in the *files* section.  
> ***WHEN YOU INSTALL TICK THE OPTION THAT SAYS 'add python to PATH' THIS IS VERY IMPORTANT.***


 - [Node.js](https://nodejs.org/en/download/)  
> Simply select the correct operating system in the **LTS** tab  

---

Once that has been dealt with, simply run the file *setup.bat* you will find inside the downloaded folder.

## Configuration

In order to get the bot working a discord bot must be made. Follow these instructions to create a bot.
Once you have installed everything correctly and you have your bot created. Get your bot Token from the webpage (under the bot section of your application in the Discord Developer Portal) you just have to create a file in *backend/Bot* called *Bot.yaml*. You should see a file called *Bot.yaml.example* in there, you can just go ahead and remove the *.example* from it and open it. Inside you will have to put the token as the example indicates. In the end, if your code was *BcQp2WlVivPlWQU4x4wnZg* your file should look like this:

```
TOKEN: BcQp2WlVivPlWQU4x4wnZg
```

Now you have to create the file called *config.json*. In the downloaded folder, you will find a file called *config.json.example*, as with the *bot.yaml* process, simply remove the *.example* part of the name and open it. Once inside you will see there's a field called **rootAddr**, this is what you have to change.
You will have to put your public IP in there. If you don't know how to get your public IP, just look up in google "what is my IP" and you'll be shown a code in the format **x.x.x.x**. That is what you want.
Imagining your IP is **123.456.78.9** our file should ultimately look like this:

```
{
  "rootAddr": "123.456.78.9",
  "backListen": "0.0.0.0",
  "frontPort": 12547,
  "backPort": 12546
}
```

<ins>NOTE: You may want to setup a [ddns](https://www.noip.com) if you plan on allowing other people to access from their homes<ins>

Before moving on, you have to open the ports shown in the fields **frontPort** and **backPort**, by default these are 12547 and 12546 respectively. Opening ports may be different depending on your ISP, but [this guide](https://nordvpn.com/es/blog/open-ports-on-router/) should work as a general guideline. **(hint: your router's IP is the IP we just looked for before)**

Then, we have to figure out what the URL of the future page login is. If we look at the fields in the config.json found above we can easily figure it out.
What we want to do is pick this template and substitute the values with the corresponding fields:

> `https://<rootAddr>:<backPort>/login`

In the case of our example, this would be

> `https://123.456.78.9:12546/login`

**IMPORTANT** If you plan to run this over http instead, then change the *https* part into *http*. Otherwise the process is exactly the same

The /login part is not part of the actual URL we will be using but is necessary for the next step, so just bear with me.
Next, we have to tell discord we trust this URL. In the Discord Developer Portal move to your application and go to the section called **oauth2 -> general**. There you should see a button called *add redirect*. Click in there and add the URL we just figured out. Then make sure to save.

## Running

Make sure you've gone through intallation and configuration sections before trying to run anything!!

Just run the file *runHTTPS.bat* inside the downloaded folder if you want the webpage to work over HTTPS or *runHTTP.bat* if you want it to work over HTTP (you can change at any time, just make sure you reconfigure the Discord Developer Portal accordingly). It will open two terminals: One for the webpage, and the other one for the bot.
