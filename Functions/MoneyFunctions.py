import discord
import random
from Functions import CharacterFunctions as char


async def showCasinoInformation():
    embed = discord.Embed(
        title="Available casino games are:",
        color=0xf35ff0
    )
    embed.add_field(
        name='!casino dice "bet number" "amount to bet"',
        value="Choose a correct number 1-6 to win 5x of your entry.",
        inline=False
    )
    embed.add_field(
        name='!casino even/odd "your guess" "amount to bet"',
        value="Choose if a number 1-100 will be even or odd to win 2x entry.",
        inline=False
    )

    return embed


async def checkIfAmountIsCorrect(amount):
    return amount.isnumeric() and int(amount) > 0


async def gambleDice(ctx, clientId, amount, betNumber):
    if not int(betNumber) in range(1, 6):
        await ctx.send('Your bet number needs to be between 1 and 6.')
        return

    characterMoney = await char.getCharacterMoney(clientId)
    if await checkIfCharacterCanAffordToGamble(characterMoney, amount):
        randomNumber = random.randint(1, 6)
        betNumber = int(betNumber)
        if betNumber == randomNumber:
            await char.addMoneyToCharacter(clientId, int(amount)*4)
            await ctx.send(f'Rolled: {randomNumber}. Congratulations, you won {amount}.')
        else:
            await char.removeMoneyFromCharacter(clientId, amount)
            await ctx.send(f'Rolled: {randomNumber}. Sadly, you lost {amount}.')
    else:
        await ctx.send(f"Sorry, You can't afford to gamble {amount}.")


async def gambleEvenOdd(ctx, clientId, amount, betType):
    characterMoney = await char.getCharacterMoney(clientId)
    if await checkIfCharacterCanAffordToGamble(characterMoney, amount):
        randomNumber = random.randint(1, 100)
        if await checkIfEvenOddBetWasCorrect(betType, randomNumber):
            await char.addMoneyToCharacter(clientId, int(amount))
            await ctx.send(f'Rolled: {randomNumber}. Congratulations, You won {amount}.')
        else:
            await char.removeMoneyFromCharacter(clientId, amount)
            await ctx.send(f'Rolled: {randomNumber}. Sadly You lost {amount}.')
    else:
        await ctx.send(f"Sorry, You can't afford to gamble {amount}.")


async def checkIfCharacterCanAffordToGamble(characterMoney, amountToGamble):
    return int(characterMoney) >= int(amountToGamble)


async def checkIfEvenOddBetWasCorrect(betType, generatedNumber):
    betType = betType.lower()
    isEven = generatedNumber % 2 == 0

    if betType == 'even':
        if isEven:
            return True
        else:
            return False
    elif betType == 'odd':
        if isEven:
            return False
        else:
            return True
    else:
        return False
