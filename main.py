import os
import discord
from discord.ext import commands
import re  
import asyncio  
import myserver


bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())


@bot.event
async def on_ready():
    print("Bot Is Online")

# Modal สำหรับกรอกลิ้ง TrueMoney
class LinkModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="กรอกลิ้ง TrueMoney")
        self.link_input = discord.ui.InputText(label="กรอกลิ้ง TrueMoney", style=discord.InputTextStyle.long)
        self.add_item(self.link_input)

    async def callback(self, interaction: discord.Interaction):
        link = self.link_input.value

        # ตรวจสอบลิงก์ทรูมันนี่
        if re.match(r'https://gift\.truemoney\.com/campaign/\?v=[a-zA-Z0-9]{18}', link):
            # ส่งลิ้งค์ไปยังห้องที่กำหนดในรูปแบบ Embed
            channel_id = 1297442144289689643  # แทนที่ด้วย ID ของ Channel ที่ต้องการส่ง
            channel = bot.get_channel(channel_id)
            embed = discord.Embed(title="ลิงก์ TrueMoney ที่กรอก", description=f"{link}", color=discord.Color.green())
            await channel.send(embed=embed)
            await interaction.response.send_message("ลิงก์ถูกต้องและส่งไปยังห้องที่กำหนดแล้ว!", ephemeral=True)
        else:
            await interaction.response.send_message("ลิงก์ทรูมันนี่ไม่ถูกต้อง กรุณากรอกใหม่!", ephemeral=True)

# Modal สำหรับกรอกข้อมูลเพิ่มเติม
class InfoModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="กรอกข้อมูลเพิ่มเติม")
        self.info_input = discord.ui.InputText(label="ข้อมูลเพิ่มเติม", style=discord.InputTextStyle.long)
        self.add_item(self.info_input)

    async def callback(self, interaction: discord.Interaction):
        info = self.info_input.value

        # ส่งข้อมูลไปยังห้องที่กำหนดในรูปแบบ Embed
        channel_id = 1297442144289689643  # แทนที่ด้วย ID ของ Channel ที่ต้องการส่ง
        channel = bot.get_channel(channel_id)
        embed = discord.Embed(title="ข้อมูลเพิ่มเติม", description=f"{info}", color=discord.Color.blue())
        await channel.send(embed=embed)

        await interaction.response.send_message("ข้อมูลเพิ่มเติมถูกส่งไปยังห้องที่กำหนดแล้ว!", ephemeral=True)

@bot.command()
async def robux(ctx):
    # สร้าง Embed
    embed = discord.Embed(title="เลือกตัวเลือก", description="กรุณาเลือกตัวเลือกที่ต้องการ:", color=discord.Color.green())

    # ปุ่มสำหรับกรอกลิ้ง TrueMoney
    button1 = discord.ui.Button(label="กรอกลิ้ง TrueMoney", style=discord.ButtonStyle.primary)
    async def button1_callback(interaction: discord.Interaction):
        modal = LinkModal()
        await interaction.response.send_modal(modal)
    button1.callback = button1_callback

    # ปุ่มสำหรับกรอกข้อมูลเพิ่มเติม
    button2 = discord.ui.Button(label="กรอกข้อมูลเพิ่มเติม", style=discord.ButtonStyle.secondary)
    async def button2_callback(interaction: discord.Interaction):
        modal = InfoModal()
        await interaction.response.send_modal(modal)
    button2.callback = button2_callback

    # ปุ่ม Callback
    button3 = discord.ui.Button(label="Callback", style=discord.ButtonStyle.success)
    async def button3_callback(interaction: discord.Interaction):
        await interaction.response.send_message("นี่คือการตอบสนองจาก Callback", ephemeral=True)
    button3.callback = button3_callback

    # เพิ่มปุ่มลงใน View
    view = discord.ui.View()
    view.add_item(button1)
    view.add_item(button2)
    view.add_item(button3)

    await ctx.send(embed=embed, view=view)

server_on()

bot.run(os.getenv('Token'))
