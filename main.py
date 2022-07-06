from config import *
import discord
from discord.ext import commands
from riotwatcher import LolWatcher, ApiError
from utils import *
import random

log = logging.getLogger(__name__)

bot = commands.Bot(command_prefix='!')
client = discord.Client()
watcher = LolWatcher(RIOT_API_KEY)

def get_voice_channel_by_name(name):
    log.debug("get_voice_channel_by_name")
    for channel in bot.get_all_channels():
        if "voice" != str(channel.type):
            continue
        if channel.name.lower() == name:
            return channel

@bot.command(name="ping", help="helpong", brief="prints pong back to the channel")
async def test(ctx):
    log.debug("test")
    print(ctx)
    await ctx.send("pong")

@bot.command(name="teams")
async def balance_teams(ctx):
    log.debug("balance_teams")
    # Get all users from General channel

    current_guild = ctx.author.guild
    current_channel = ctx.author.voice.channel
    #guild = bot.get_guild(GUILD_ID)

    for index, channel in enumerate(current_guild.voice_channels):
        if channel == current_channel:
            team_a, team_b = current_guild.voice_channels[index+1:index+3]
            break

    log.debug("Handling channels: [%s] -> [%s]vs[%s]" % (current_channel.name, team_a.name, team_b.name))


    user_ids = [i for i in range(1001, 1010)]
    for user_id in current_channel.voice_states.keys():
        user_ids.append(user_id)

    # Sanity enough people
    if len(user_ids) < 10:
        await ctx.send("Found only [%d/10] members on room: [%s]" % (len(user_ids), ctx.author.voice.channel.name))
        return

    for index, user in enumerate(user_ids):
        res = get_user_data(user)
        if None == res:
            await ctx.send("Error handling user: [%s]" % user, delete_after=30)
        user_ids[index] = res

    def mmr(summoner):
        return summoner.get("mmr", 0)

    user_ids.sort(key=mmr)
    user_ids = user_ids[:10]

    # First get two randoms to each one of those
    member = user_ids.pop(random.randrange(len(user_ids)))
    team_a_members, team_a_mmr = [member], member["mmr"]

    member = user_ids.pop(random.randrange(len(user_ids)))
    team_b_members, team_b_mmr = [member], member["mmr"]

    # After randomization, make as equal as possible

    while 0 != len(user_ids):
        member = user_ids.pop(0)

        if team_b_mmr > team_a_mmr:
            team_a_mmr += member["mmr"]
            team_a_members.append(member)
            continue
        team_b_mmr += member["mmr"]
        team_b_members.append(member)

    log.info("Team a:")
    log.info(team_a_mmr)
    log.info(team_a_members)

    log.info("Team b:")
    log.info(team_b_mmr)
    log.info(team_b_members)

    team_a_str = ""
    team = "Team 1"
    for member in team_a_members:
        team_a_str += "<@%s> : %s\n" % (member["user_discord_id"], member["mmr"])

    team = "Team 2"
    team_b_str = ""
    for member in team_b_members:
        team_b_str += "<@%s> : %s\n" % (member["user_discord_id"], member["mmr"])

    teams_str = ""
    for member_a, member_b in zip(team_a_members, team_b_members):
        log.info(member_a["user_discord_id"])
        log.info(member_b["user_discord_id"])
        pad = " "
        teams_str += TEAM_MESSAGE.format(**locals())
    teams_str += ""

    embedVar = discord.Embed(title="Balance teams", description="", color=0x74E18B)
    embedVar.add_field(name="TeamA - [%s]" % team_a_mmr, value=team_a_str, inline=True)
    embedVar.add_field(name="TeamB - [%s]" % team_b_mmr, value=team_b_str, inline=True)
    await ctx.send(embed=embedVar, delete_after=120)

    #print(teams_str)
    #await ctx.send(teams_str)

    print("Done")


@bot.command(name="move")
async def move_to(ctx, member : discord.Member, channel:discord.VoiceChannel):
    log.debug("move")
    await member.move_to(channel)

@bot.command(name="init")
async def init_user(ctx):
    log.debug("init")
    summoner_data = get_user_data(ctx.author.id)
    await ctx.author.send(WELCOME_MESSAGE.format(**locals()))

@bot.command(name="eune")
async def init_eune(ctx, name):
    log.debug("init_eune")
    rank_data = get_summoner_info(REGION_EUNE, name)

    await ctx.author.send(GET_RANK_MESSAGE.format(**locals()))

    add_user_data(ctx.author.id, {"eune": name}, rank_data["local_mmr"])


@bot.command(name="euw")
async def init_euw(ctx, name):
    log.debug("init_euw")
    rank_data = get_summoner_info(REGION_EUW, name)

    log.debug(rank_data)
    await ctx.author.send(GET_RANK_MESSAGE.format(**locals()))

    add_user_data(ctx.author.id, {"euw": name}, rank_data["local_mmr"])

@bot.command(name="status")
async def check_status(ctx):
    log.debug("check_status")

    summoner_data = get_user_data(ctx.author.id)

    await ctx.author.send(STATUS_MESSAGE.format(**locals()))

@bot.command(name="update_db")
async def update_db(ctx):
    log.debug("update_db")

log.info("running bot")
bot.run(TOKEN)