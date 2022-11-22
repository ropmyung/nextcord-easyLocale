from module import BotContent # the class you can use for easier locale
from nextcord import *

# ping command
@BOT.slash_command(
    name="ping",
    name_localizations={Locale.ko: "핑"},
    description="🤖 Checks how long does it takes to respond.",
    description_localizations={Locale.ko: "🤖 응답시간을 확인해요."}
)
async def ping(inte: Interaction):
    txt = BotContent({
            Locale.ko: [" 응답속도 ".center(12, '━'), "퐁! `{:.2f}ms` 🏓"],
            Locale.en_US: ["Pong!",'🏓 `{:.2f}ms`']
        }, inte)
    await inte.send(embed=Embed(title=txt.get(), description=txt.get().format(BOT.latency * 1000)))

# Example of divide method use
@BOT.slash_command(
    name="test",
    description="test",
)
async def test(inte: Interaction):
    txt = BotContent({
            Locale.ko: [
              "ABC",
              "DEF
            ],
            Locale.en_US: [
              "가나다",
              "마바사"
            ]
        }, inte)
    txt.divde(1) # Divides the list at index 1.
    if True: # If the given statement is True,
      await inte.send(txt.get(0)) # The first content ("ABC" or "가나다") is returend.
    else: # If the given statement is False,
      await inte.send(txt.get(1)) # The second content ("DEF" or "마바사") is returned.
