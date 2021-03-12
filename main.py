import discord
import random
import sys
from discord.ext import commands
import os

bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
  print("we have logged in as {0.user}".format(bot))

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


  for i in range(1,len(args)):
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

  team_number = 1
  for team in teams:
    team_string = "**Team** " + str(team_number) + "\n"

    for member in team:
      team_string += member + "\n"
    number += 1
      team_string += "\n\n"
    await ctx.send(team_string)

bot.run(os.getenv("TOKEN"))
sys.stdout.flush()
