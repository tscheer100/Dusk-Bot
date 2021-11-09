# Dusk Bot
A general purpose custom Discord bot that adds useful features as well as fun little tricks to keep members entertained.  

# requirements:
- [discord.py](https://github.com/Rapptz/discord.py)
- A bot token. must authorize [here](https://discord.com/developers/applications)
- [.env](https://pypi.org/project/python-dotenv/)
- [Motor](https://github.com/mongodb/motor)
- pymongo
- Python 3.x

## Setup
To set up locally, first pull the repo
```sh
git clone https://github.com/tscheer100/Dusk-Bot.git
```
then create a `.env` file within the root folder of the repo.
```sh
touch .env
```
edit the `.env` file 
```sh
nano .env
```
once in the file, add your discord token with the following syntax
```
DISCORD_TOKEN="U2OTA3MTQ3ODk5Njkjkz.X2Yqtg.FSGfvEqZILo"
```
also, to make the economy work correctly, make a `bank.json` file.
```sh
touch bank.json
```
then `nano` into the file to edit it like before and add an empty curly brace backet.
```json
{

}
```
run the bot using python
```sh
python3 dusk.py
```


### What I've learned from this project:
- Tenerary Operators and how to use them to circumnavigate Discord embed's lack of support for regular `if-else` statements.
- Familiarized myself with `.gitignore` as not to leak data to the public.
- learned about `.env` and how it can be used to seperate data from the rest of the code.
- Strengthened knowledge on Discord's API with `discord.py`
- Dipped my toes in the difference between handling discord specific errors and python errors. the discord specific errors can be found [here](https://discordpy.readthedocs.io/en/latest/api.html#discord.DiscordException) 
- Dealt with SSH and raspberry pi. learned that pi zeros only support 2.4ghz band.
- Learned about embed editing.
- Got more experience integrating JSON into Python.
- Gained more understanding as to when to use the `self` command to call other methods within a class.
- learned about MongoDB and how it is not good with discord.py and rather to use Motor to stop with blocking
- learned the basics of database manipulation
- learned how to call a method from one cog to another
- learned about the `reversed` command
