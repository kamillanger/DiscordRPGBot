import discord
from Functions import CharacterFunctions as char, MoneyFunctions as mon, QuestFunctions as questFunc
from discord.ext import commands
import os
#Tested by Szymon Skarzyński (szymon.skarzynski@outlook.com)

bot = commands.Bot(command_prefix='!', case_insensitive=True)
bot.remove_command('help')
token = open("botToken.txt", "r").readline()

@bot.command(aliases = ['commands'])
async def help(ctx):
    embed = discord.Embed(title="Help", description="What commands exist", color=0xf35ff0)
    embed.set_author(name="Kamil Langer")

    embed.add_field(name="!help, !commands", value="Displays the command window.", inline=False)
    embed.add_field(name="!character", value="Displays information about your character or creates it if you "
                                             "don't have one already.", inline=False)
    embed.add_field(name="!quest", value="Sends your character on a quest.", inline=False)
    embed.add_field(name="!casino", value="Lets you gamble your hard earned money.", inline=False)

    embed.set_footer(text="Bot was created for fun.")

    await ctx.send(embed=embed)


@bot.command()
async def character(ctx, name = None):
    if await char.checkIfCharacterExists(str(ctx.message.author.id)):
        characterData = await char.getCharacterInfo(ctx.message.author.id)
        embed = await char.displayCharacterInfo(characterData)
        await ctx.send(embed=embed)
    else:
        if name is None:
            embed = discord.Embed(
                title="You haven't created a character yet",
                color=0xf35ff0
            )
            embed.add_field(name="To create your character type:", value='!character "character name"', inline=False)
            await ctx.send(embed=embed)

        else:
            if len(name) > 50:
                await ctx.send("Character name is too long. Maximum length is 50.")
            else:
                await char.createCharacter(str(ctx.message.author.id), name)
                await ctx.send("Your character has been created! <:BloodTrail:643083316228259870>")


@bot.command()
async def casino(ctx, game = None, bet = None, amount = None):
    if await char.checkIfCharacterExists(str(ctx.message.author.id)):
        if game is None:
            await ctx.send(embed = await mon.showCasinoInformation())
        else:
            game = game.lower()
            if game == "dice":
                if amount is None:
                    await ctx.send("You need to provide the amount you want to gamble.")
                else:
                    if await mon.checkIfAmountIsCorrect(amount):
                        await mon.gambleDice(ctx, ctx.message.author.id, amount, bet)
                    else:
                        await ctx.send("Provided bet amount is not a whole and positive number.")
            elif game == "even/odd":
                if amount is None:
                    await ctx.send("You need to provide the amount you want to gamble.")
                else:
                    if await mon.checkIfAmountIsCorrect(amount):
                        await mon.gambleEvenOdd(ctx, ctx.message.author.id, amount, bet)
                    else:
                        await ctx.send("Provided bet amount is not a whole and positive number.")
            else:
                await ctx.send("I don't know this casino game.")
    else:
        await ctx.send("You need a character to gamble.")


@bot.command()
async def quest(ctx, level = None):
    clientId = str(ctx.message.author.id)
    if await char.checkIfCharacterExists(clientId):
        if level is None:
            if await char.checkIfCharacterIsOnQuest(clientId):
                if await char.checkIfCharacterHasFinishedQuest(clientId):
                    await char.finishCharacterQuest(ctx, clientId)
                else:
                    await questFunc.showQuestRemainingTimeInfo(ctx, clientId)
            else:
                await ctx.send(embed = await questFunc.showQuestInformation())
        else:
            if await char.checkIfCharacterIsOnQuest(clientId):
                if await char.checkIfCharacterHasFinishedQuest(clientId):
                    await char.finishCharacterQuest(ctx, clientId)
                else:
                    await questFunc.showQuestRemainingTimeInfo(ctx, clientId)
            elif await questFunc.checkIfQuestExists(level):
                await questFunc.sendCharacterOnQuest(clientId, level)
                await ctx.send(f'Your character has been sent on a quest: {level}')
            else:
                await ctx.send('It seems that this quest does not exist. Check available quests with "!quest"')
    else:
        await ctx.send("You need a character to send it on a quest.")

for cog in os.listdir(".\\cogs"):
    if cog.endswith(".py") and not cog.startswith("_"):
        try:
            cog = f"cogs.{cog.replace('.py', '')}"
            bot.load_extension(cog)
        except Exception as e:
            print(f"{cog} can't be loaded:")
            raise e


@bot.event
async def on_ready():
    print("Bot is ready.")


bot.run(token)
