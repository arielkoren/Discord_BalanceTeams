from config import *
log = logging.getLogger(__name__)
import os
import sqlite3
from riotwatcher import LolWatcher, ApiError

watcher = LolWatcher(RIOT_API_KEY)
def get_summoner_info(region, name):
    try:
        summoner = watcher.summoner.by_name(region, name)
        log.debug(summoner)
        ranks_data = watcher.league.by_summoner(region, summoner["id"])
        log.debug(ranks_data)

        rank_result = {}
        for rank in ranks_data:
            if "RANKED_SOLO_5x5" != rank.get("queueType"):
                continue

            tier, rank = rank.get("tier"), rank.get("rank")
            local_mmr = tier_translation.get(tier.lower(), 0)
            local_mmr += rank_translation.get(rank.lower(), 0)
            rank_result["tier"] = tier
            rank_result["rank"] = rank
            rank_result["local_mmr"] = local_mmr
            log.info(rank_result)
            return rank_result

    except ApiError as e:
        log.error(e)
        return {}





try:
    watcher.summoner.by_name("euw1", "a")
except ApiError as e:
    print("ERROR")
    print(e)
    err = e

def generate_db():
    log.debug("generate_db")
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("""
              CREATE TABLE IF NOT EXISTS users
              ([id] INTEGER PRIMARY KEY AUTOINCREMENT, [user_discord_id] text, [eune] text, [euw] text, [mmr] INTEGER)
              """)
    conn.commit()

def verify_db(func, *args, **kwargs):
    log.debug("verify_db")
    def wrapper(*args, **kwargs):
        if not os.path.exists(DATABASE_NAME):
            generate_db()
        return func(*args, **kwargs)
    return wrapper

@verify_db
def get_user_data(user_discord_id):
    log.debug("get_user_data(%s)" % user_discord_id)
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row

    c = conn.cursor()
    c.execute(f"""
              SELECT * from users where user_discord_id = "{user_discord_id}"
              """)
    result = list(c.fetchall())
    if len(result) > 0:
        return dict(result[0])
    return {}

@verify_db
def add_user_data(user_discord_id, data, mmr):
    log.debug("add_user_data")
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    # Verify data
    eune_cmd = "\"%s\"" % data.get("eune", "")
    log.debug("eune_cmd: [%s]" % eune_cmd)
    if "\"\"" == eune_cmd:
        eune_cmd = f"(SELECT eune from users where user_discord_id = \"{user_discord_id}\")"

    euw_cmd = "\"%s\"" % data.get("euw", "")
    log.debug("euw_cmd: [%s]" % euw_cmd)
    if "\"\"" == euw_cmd:
        euw_cmd = f"(SELECT euw from users where user_discord_id = \"{user_discord_id}\")"

    # Check existing MMR first
    c.execute(f"SELECT mmr from users where user_discord_id = \"{user_discord_id}\"")
    results = c.fetchall()

    log.debug(results)

    # Verify mmr exists
    db_mmr = 0
    if len(results) != 0:
        db_mmr = results[0][0]
    mmr = max(db_mmr, mmr)

    # Insert
    exec_command = f"""INSERT or REPLACE INTO users (id, user_discord_id, eune, euw, mmr)
                    VALUES
                    ((SELECT id from users where user_discord_id=\"{user_discord_id}\"), \"{user_discord_id}\", {eune_cmd}, {euw_cmd}, {mmr})
              """
    log.info(exec_command)

    c.execute(exec_command)
    conn.commit()