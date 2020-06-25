async def addEmbedField(embed, name, value, inline):
    embed.add_field(
        name=name,
        value=value,
        inline=inline
    )

    return embed


async def addEmptyEmbedField(embed, inline):
    embed.add_field(
        name="\u200b",
        value="\u200b",
        inline=inline
    )

    return embed
