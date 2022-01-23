import discord
import random
import sys
import os
from discord.ext import commands

bot = commands.Bot(command_prefix="!")


@bot.event
async def on_ready():
    print("we have logged in as {0.user}.format(client)")

@bot.command()
async def scramble(ctx, *args):

    if int(args[0]) > 10:
        await ctx.send("No more than 10 teams, ask Rob why")
        return

    if len(args) > 100:
        await ctx.send("No more than 100 players, ask Rob why")
        return

    number_of_teams = args[0]
    players = list()

    for i in range(1, len(args)):
        players.append(args[i])

    if (len(players) % int(number_of_teams) != 0):
        await ctx.send("Not able to make teams with even numbers")
        return

    player_in_team = len(players) / int(number_of_teams)

    teams = list()
    for i in range(0, int(number_of_teams)):
        temp_team = list()
        for x in range(0, int(player_in_team)):
            temp_team.append(players.pop(random.randrange(0, len(players))))
        teams.append(temp_team)

    number = 1
    for team in teams:
        team_string = "**Team** " + str(number) + "\n"

    for member in team:
        team_string += member + "\n"
    number += 1
    await ctx.send(team_string)


@bot.command()
async def test(ctx, *args):
    channel = discord.utils.get(ctx.guild.channels, name=args[0])
    channel2 = discord.utils.get(ctx.guild.channels, name=args[1])
    members = []
    for member in channel.members:
        members.append(member)
    print(members)
    print(channel.id)
    print(channel2.id)
    for member in members:
        await member.move_to(channel2)
        return
    print("Testing")

token = os.getenv("TOKEN")
bot.run(token)
sys.stdout.flush()
