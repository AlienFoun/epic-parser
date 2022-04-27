# <p align="center">Epic Games Parser</p>
<p align="center"><img alt="GitHub Madeby" src="https://img.shields.io/badge/made%20by-AlienFoun-blue"> <img alt="GitHub repo size" src="https://img.shields.io/github/repo-size/AlienFoun/epic_games_parser"> <img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/Alienfoun/epic_games_parser?style=social"> <img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/AlienFoun/epic_games_parser"> </p>

# About
**The program allows you to get information about free game giveaways on the Epic Games Store**


# Project structure
The project is structured for better scaling. In general, files names reflect their essence
* bot - contains the main script code
* config - contains the data necessary for the program to work
* get_free_games - contains a function for getting information about free games from the Epic Games Store using the API
* helper - contains the functions necessary for the program to work
* sql_funcs - contains the functions necessary for the program to work with PostgreSQL database
* keyboards - contains the necessary keyboards for telegram

# Selected libraries
* Aiogram
* APScheduler
* loguru
* psycopg2
* asyncio
* requests

# Installation
Download Python 3.8 or higher

```
git clone https://github.com/AlienFoun/happy_birthday-script
cd happy_birthday-script

for pip: pip install -r requirements.txt

for poetry:
  poetry install
  poetry update
```

Fill in the data to connect to the Telegram and PostgreSQL database in the file `config.py`. You can also fill in information about the launch time of the newsletter:

```Python
BOT_TOKEN = 'your_token'
host = 'your_host'
user = 'your_user'
password = 'your_password'
db_name = 'your_database'
hour = 20
minute = 0
```

# Usage

Open the terminal and go to the folder with the project, then start the script using the command `python bot.py`.

# How it works?

After turning it on, the bot will be available in Telegram. After that you will be able to send messages in a dialog with the bot. 

Available commands:

```Python
/start - Connect to send notifications of new free games
/stop - Unsubscribe
```

After entering the /start command, the user is checked to see if he is in the database using fuction

```Python
def sql_check_user(user_id: int) -> bool:
    cursor.execute(f "SELECT user_id FROM user_base WHERE user_id = '{user_id}'")
    rows = cursor.fetchall()
    for rows:
        if user_id in row:
            return True
    return False
```

If the user is not found in the database, he will be asked to subscribe to the mailing list; if the user agrees, he will be added to the database. If so, you will be informed at the time specified in `config.py`.

In case of refusal, the user will be offered to apply in the future. If a user enters the /stop command, he will be removed from the database and unsubscribed.

At the specified time the get_free_games script sends a request to the Epic Games Store API, after which we get information about the game name, description, original price, as well as the start and end date of the giveaway.

If we cannot get information about the start date of the game, it means that the game is being distributed at the moment.

After getting information about those games that are given away for free, all the information is formatted according to the pattern:

```Python
Game name:
Regular price:
Plot:
Link:
```
And this information is sent to users from the database.

Example:

```
The games are currently available:

Title: Amnesia: Rebirth
Regular price: 515 rubles.
Plot: In Amnesia: Rebirth, from the creators of the cult series, you will experience a new plunge into darkness. As you grapple with despair and hopelessness, your ability to endure suffering will be put to the test.
Link: https://store.epicgames.com/ru/p/amnesia-rebirth
The game is available for free RIGHT NOW

Title: Just Die Already
Regular price: 360 rubles
Plot: The creators of Goat Simulator present the adventures of old men in Just Die Already! You're old and mean, and you've just been kicked out of the nursing home. How do you survive when everyone's just waiting for you to die?
Link: https://store.epicgames.com/ru/p/just-die-already
The game will be free on April 28, 2022 3:00pm - May 05, 2022 3:00pm

Title: Riverbond
Regular Price: 549 rubles
Plot: The game Riverbond is a frantic voxel adventure, which can take part from 1 to 4 players. Embark on a heroic journey: complete quests, fight cool opponents and smash everything around in small dice!
Link: https://store.epicgames.com/ru/p/riverbond-782aa4
The game is available for free RIGHT NOW

Title: Paradigm
Regular Price: 349 rubles
Plot: Paradigm is a surreal adventure game set in the strange and post apocalyptic Eastern European country of Krusz. Play as the handsome mutant, Paradigm, whose past comes back to haunt him in the form of a genetically engineered sloth that vomits candy.
Link: https://store.epicgames.com/ru/p/paradigm-875c5c
The game will be free on April 28, 2022 3:00pm - May 05, 2022 3:00pm
```

The project uses a logging system to get information about what happens while the program is running. The command for logging starts with "logger".
Logger configuration information:
```Python
logger.add(f"{__file__[:3]}.log", format="{time} {level} {message}", level="DEBUG",
           rotation='100 KB', compression='zip')
```

# Contributions

You can contribute to project in the following ways:

* [Submit new feature ideas](https://github.com/AlienFoun/happy_birthday-script/issues)
* [Report bugs as issues](https://github.com/AlienFoun/happy_birthday-script/issues)
* Star ⭐ this repository
* Spread the word about this project

Do you have an idea for an amazing new feature? Did you find a bug you want to fix? Great! Please submit an issue for discussion before making a pull request.
