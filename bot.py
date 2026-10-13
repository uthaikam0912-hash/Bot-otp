
import os
import time
import secrets
import discord
from discord import app_commands

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# เก็บรหัสชั่วคราวในหน่วยความจำ
otp_data = {}
EXPIRY_SECONDS = 300
MAX_ATTEMPTS = 5


@tree.command(name="otp", description="สร้าง OTP จำลอง")
async def otp(interaction: discord.Interaction):
    user_id = interaction.user.id

        code = f"{secrets.randbelow(1_000_000):06d}"
            otp_data[user_id] = {
                    "code": code,
                            "expires": time.monotonic() + EXPIRY_SECONDS,
                                    "attempts": 0,
                                        }

                                            await interaction.response.send_message(
                                                    f"🧪 OTP จำลองของคุณคือ `{code}`\n"
                                                            "รหัสนี้ใช้ทดสอบเท่านั้น ไม่ใช่รหัส SMS จริง "
                                                                    "และหมดอายุใน 5 นาที",
                                                                            ephemeral=True,
                                                                                )


                                                                                @tree.command(name="verify", description="ตรวจสอบ OTP จำลอง")
                                                                                @app_commands.describe(code="รหัส 6 หลักที่ได้รับจาก /otp")
                                                                                async def verify(interaction: discord.Interaction, code: str):
                                                                                    user_id = interaction.user.id
                                                                                        data = otp_data.get(user_id)

                                                                                            if not data:
                                                                                                    await interaction.response.send_message(
                                                                                                                "ยังไม่มี OTP กรุณาใช้ /otp ก่อน",
                                                                                                                            ephemeral=True,
                                                                                                                                    )
                                                                                                                                            return

                                                                                                                                                if time.monotonic() >= data["expires"]:
                                                                                                                                                        otp_data.pop(user_id, None)
                                                                                                                                                                await interaction.response.send_message(
                                                                                                                                                                            "รหัสหมดอายุแล้ว กรุณาขอรหัสใหม่",
                                                                                                                                                                                        ephemeral=True,
                                                                                                                                                                                                )
                                                                                                                                                                                                        return

                                                                                                                                                                                                            data["attempts"] += 1

                                                                                                                                                                                                                if data["attempts"] > MAX_ATTEMPTS:
                                                                                                                                                                                                                        otp_data.pop(user_id, None)
                                                                                                                                                                                                                                await interaction.response.send_message(
                                                                                                                                                                                                                                            "เกินจำนวนครั้งที่อนุญาต กรุณาขอรหัสใหม่",
                                                                                                                                                                                                                                                        ephemeral=True,
                                                                                                                                                                                                                                                                )
                                                                                                                                                                                                                                                                        return

                                                                                                                                                                                                                                                                            if secrets.compare_digest(code, data["code"]):
                                                                                                                                                                                                                                                                                    otp_data.pop(user_id, None)
                                                                                                                                                                                                                                                                                            await interaction.response.send_message(
                                                                                                                                                                                                                                                                                                        "✅ ตรวจสอบ OTP จำลองสำเร็จ!",
                                                                                                                                                                                                                                                                                                                    ephemeral=True,
                                                                                                                                                                                                                                                                                                                            )
                                                                                                                                                                                                                                                                                                                                else:
                                                                                                                                                                                                                                                                                                                                        await interaction.response.send_message(
                                                                                                                                                                                                                                                                                                                                                    f"❌ รหัสไม่ถูกต้อง เหลือโอกาส "
                                                                                                                                                                                                                                                                                                                                                                f"{MAX_ATTEMPTS - data['attempts']} ครั้ง",
                                                                                                                                                                                                                                                                                                                                                                            ephemeral=True,
                                                                                                                                                                                                                                                                                                                                                                                    )


                                                                                                                                                                                                                                                                                                                                                                                    @client.event
                                                                                                                                                                                                                                                                                                                                                                                    async def on_ready():
                                                                                                                                                                                                                                                                                                                                                                                        await tree.sync()
                                                                                                                                                                                                                                                                                                                                                                                            print(f"Bot online: {client.user}")


                                                                                                                                                                                                                                                                                                                                                                                            if not TOKEN:
                                                                                                                                                                                                                                                                                                                                                                                                raise RuntimeError("กรุณาตั้งค่า DISCORD_TOKEN ก่อน")

                                                                                                                                                                                                                                                                                                                                                                                                client.run(TOKEN)
