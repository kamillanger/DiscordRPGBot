import os.path
import json
import discord
import random
from datetime import datetime


async def checkIfCharacterExists(clientId):
    return os.path.isfile(f'characters/{clientId}.json')


async def displayCharacterInfo(characterData):
    embed = discord.Embed(title=characterData['name'], color=0xf35ff0)

    embed.add_field(name="Your level:", value=characterData['level'], inline=False)
    embed.add_field(name="Experience:", value=characterData['experience'], inline=False)
    embed.add_field(name="Money:", value=characterData['money'], inline=False)
    if characterData['onQuest'] is False:
        questInfo = 'Your character is currently not doing any quest.'
    else:
        questInfo = f'Your character is currently doing a quest: {characterData["questInfo"]["name"]}.'

    embed.add_field(name="Quest info:", value=questInfo, inline=False)

    embed.set_footer(text="Your character info.")

    return embed


async def createCharacter(clientId, characterName):
    newCharacterData = {
        "name": f"{characterName}",
        "level": 1,
        "experience": 0,
        "money": 0,
        "onQuest": False,
        "questInfo": None,
        "equipment": {
            "armor": None,
            "weapon": None,
            "shield": None
        }
    }

    with open(f'characters/{clientId}.json', 'w') as json_file:
        json.dump(newCharacterData, json_file)


async def getCharacterInfo(clientId):
    with open(f'characters/{clientId}.json') as output:
        characterData = json.load(output)

    return characterData


async def getCharacterMoney(clientId):
    with open(f'characters/{clientId}.json') as character:
        characterInfo = json.load(character)

    return characterInfo['money']


async def addMoneyToCharacter(clientId, amount):
    with open(f"characters/{clientId}.json", "r") as character:
        characterData = json.load(character)

    currentCharacterMoneyAmount = int(characterData["money"])
    newCharacterMoneyAmount = int(currentCharacterMoneyAmount) + int(amount)
    characterData["money"] = int(newCharacterMoneyAmount)

    with open(f"characters/{clientId}.json", "w") as character:
        json.dump(characterData, character)


async def removeMoneyFromCharacter(clientId, amount):
    with open(f"characters/{clientId}.json", "r") as character:
        characterData = json.load(character)

    currentCharacterMoneyAmount = int(characterData["money"])
    newCharacterMoneyAmount = int(currentCharacterMoneyAmount) - int(amount)
    characterData["money"] = int(newCharacterMoneyAmount)

    with open(f"characters/{clientId}.json", "w") as character:
        json.dump(characterData, character)


async def checkIfCharacterHasFinishedQuest(clientId):
    with open(f'characters/{clientId}.json') as char:
        characterData = json.load(char)

    finishTime = datetime.strptime(str(characterData['questInfo']['finishTime']), '%Y-%m-%d %H:%M:%S.%f')

    return datetime.now() > finishTime


async def finishCharacterQuest(ctx, clientId):
    with open(f'characters/{clientId}.json') as char:
        characterData = json.load(char)

    levelName = characterData['questInfo']['name']
    with open(f'Quests/{levelName}.json') as quest:
        questInfo = json.load(quest)

    moneyReward = random.randint(questInfo['goldReward']['min'], questInfo['goldReward']['max'])

    await addMoneyToCharacter(clientId, moneyReward)
    await ctx.send(f"Congratulations, from finishing this quest you've earned {moneyReward} gold.")

    xpReward = questInfo['xpReward']
    currentCharXp = characterData['experience']
    newCharXp = currentCharXp + xpReward
    if newCharXp > 100:
        characterData['level'] += 1
        newCharXp -= 100
        characterData['experience'] = newCharXp
        await ctx.send(f"Congratulations, you've leveled up! You're now on {characterData['level']} level")
    else:
        characterData['experience'] = newCharXp

    characterData['onQuest'] = False
    characterData['questInfo'] = None
    with open(f'characters/{clientId}.json', 'w') as char:
        json.dump(characterData, char)


async def checkIfCharacterIsOnQuest(clientId):
    with open(f'characters/{clientId}.json') as char:
        characterData = json.load(char)

    return characterData['onQuest']
