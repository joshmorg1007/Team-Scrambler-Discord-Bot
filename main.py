import discord
from discord import ChannelType
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
async def voiceScramble(ctx, *args):
    if int(len(args)) >= 10:
        await ctx.send("No more than 10 teams, ask Rob why")
        return

    if len(args) >= 100:
        await ctx.send("No more than 100 players, ask Rob why")
        return

    team_count = 0
    team_channel_list = []

    calling_member = ctx.author
    calling_channel = None
    player_list = []
    channel_list = []

    for c in ctx.guild.channels:
        if c.type == ChannelType.voice:
            channel_list.append(c)

    for channel in channel_list:
        for member in channel.members:
            if (calling_member.id == member.id):
                calling_channel = channel

    if calling_channel is None:
        await ctx.send("You must be in a voice channel to call this command")
        return

    for arg in args:
        team_count += 1
        current = discord.utils.get(
                ctx.guild.channels, name=args[team_count-1])
        team_channel_list.append(current)

        try:
            print(current.id)
        except:
            print(
                "Could not find voice channel with name '{args[team_count]}'")
            await ctx.send("Could not find voice channel with name '" + args[team_count-1] + "'")

    for member in calling_channel.members:
        player_list.append(member)

    if (len(player_list) % int(team_count) != 0):
        await ctx.send("Not able to make teams with even numbers")
        return

    player_in_team = len(player_list) / int(len(args))

    teams = list()
    for i in range(0, int(team_count)):
        temp_team = list()
        for x in range(0, int(player_in_team)):
            temp_team.append(player_list.pop(
                random.randrange(0, len(player_list))))
        teams.append(temp_team)

    number = 0
    for team in teams:
        for member in team:
            await member.move_to(team_channel_list.pop(0))
        number += 1


@bot.command()
async def test(ctx, *args):
    channel = discord.utils.get(ctx.guild.channels, name=args[0])
    calling_member = ctx.author
    members = []
    members.append(calling_member)
    for member in channel.members:
        members.append(member)
    print(members)
    print(channel.id)
    for member in members:
        await member.move_to(channel)
        return
    print("Testing")

token = os.getenv("TOKEN")
bot.run(token)
#bot.run("Insert Token when testing")
sys.stdout.flush()
