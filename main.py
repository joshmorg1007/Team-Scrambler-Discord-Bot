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

    teams = divide_players_into_teams(number_of_teams, player_in_team)

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

        if not current.id:
            print(
                "Could not find voice channel with name '{args[team_count]}'")
            await ctx.send("Could not find voice channel with name '" + args[team_count-1] + "'")
            return

    for member in calling_channel.members:
        player_list.append(member)

    if (len(player_list) % int(team_count) != 0):
        await ctx.send("Not able to make teams with even numbers")
        return

    teams = divide_players_into_teams(team_count, player_list)

    for team in teams:
        this_teams_channel = team_channel_list.pop(0)
        for member in team:
            await member.move_to(this_teams_channel)


@bot.command()
async def recall(ctx, *args):
    calling_member = ctx.author

    channel_list = []
    for c in ctx.guild.channels:
        if c.type == ChannelType.voice:
            channel_list.append(c)

    calling_channel = None
    for channel in channel_list:
        for member in channel.members:
            if (calling_member.id == member.id):
                calling_channel = channel

    if calling_channel is None:
        await ctx.send("You must be in a voice channel to call this command")
        return

    for channel in channel_list:
        for member in channel.members:
            await member.move_to(calling_channel)


def divide_players_into_teams(num_of_teams, list_of_players):
    player_in_team = len(list_of_players) / len(num_of_teams)
    teams = list()
    for i in range(0, int(num_of_teams)):
        temp_team = list()
        for x in range(0, int(player_in_team)):
            temp_team.append(list_of_players.pop(
                random.randrange(0, len(list_of_players))))
        teams.append(temp_team)
    return teams


token = os.getenv("TOKEN")
bot.run(token)
#bot.run("Insert Token Here When Testing")
sys.stdout.flush()
