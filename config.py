import logging
global_log = logging.getLogger(__name__)
format = """[%(asctime)s][%(levelname)-6s][%(name)-10s] - %(message)s"""
logging.basicConfig(level=logging.DEBUG, format=format) #filename=...
global_log.setLevel(logging.DEBUG)


#CLIENT_SECRET = "VRHXpjPQC5YV1JLjXHddriqTQWINKl9d"
TOKEN = "OTkxNjIyNTA0NjkzMTA4NzM3.GMMybY.VUfGS3q529Vu4qHk1V4Xz-KW11vkAIuhQQSu2Q"

VOICE_CHANNEL_GENERAL = 622893903829532691
GUILD_ID = 622893903002992670

RIOT_API_KEY = "RGAPI-860316b7-7800-4cb1-a8c4-3410838aefb5"

REGION_EUNE = "eun1"
REGION_EUW = "euw1"

#USER_INFO_PATH = "./users/"
DATABASE_NAME = "users.sqlite3"


WELCOME_MESSAGE = """
```
+-------------------------------------------------------------------------------+
| Welcome message from BalanceBot                                               |
+-------------------------------------------------------------------------------+
  Hello {ctx.author}, we will now initialize you for the Balance Teams bot!     
  I'm going to save your user_id({ctx.author.id}) so I can remember you         
+-----------------+--------------------------+----------------------------------+
| EUNE server     | !eune <InGameName>       | For example: !eune CutDown       |
+-----------------+--------------------------+----------------------------------+
| EUW server      | !euw <InGameName>        | For example: !euw CutDown2       |
+-----------------+--------------------------+----------------------------------+
```
"""

GET_RANK_MESSAGE = """
```
Oh wow, maybe you are not a pisslow after all!
It seems that your rank is {rank_data[tier]} {rank_data[rank]}!
your balancebot mmr is: {rank_data[local_mmr]}
```
"""

tier_translation = {
    "iron": 0,
    "bronze": 500,
    "silver": 1000,
    "gold": 1500,
    "platinum": 2000,
    "diamond": 2500,
    "master": 3000,
    "grandmaster": 3500,
    "challenger": 4000
}
rank_translation = {
    "iv": 0,
    "iii": 100,
    "ii": 200,
    "i": 300,
}

STATUS_MESSAGE = """
Your current information is:
```
EUNE: {summoner_data[eune]}
EUW : {summoner_data[euw]}
MMR : {summoner_data[mmr]}
```
"""

TEAM_MESSAGE = """| <@{member_a[user_discord_id]}> : {member_a[mmr]}{pad:<20} | <@{member_b[user_discord_id]}> : {member_a[mmr]}\n"""
#TEAM_MESSAGE = "{team} - <@{member[user_discord_id]}>"