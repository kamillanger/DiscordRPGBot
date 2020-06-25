from discord.ext import commands


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        user = message.author
        msg = message.content
        print(f"{user} typed {msg}")

    @commands.Cog.listener()
    async def on_message_delete(self):
        print("Someone deleted a message.")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("I don't know this command.")
        if isinstance(error, commands.ExpectedClosingQuoteError):
            await ctx.send("You need to put parameters within closed quotation marks.")

        raise error


def setup(bot):
    bot.add_cog(Events(bot))
