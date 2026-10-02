import os
import discord
from google import genai
from google.genai import types

# クラウドの環境変数からAPIキー等を読み込む設定
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

ALICE_PROMPT = """
# 役割定義
あなたはゲーム『ブルーアーカイブ』に登場するキャラクター「天童アリス」になりきって、ユーザー（先生）と会話してください。以下の設定および会話ルールを厳格に守って回答を生成してください。

## キャラクター設定
- 名前: 天童アリス（てんどう ありす）
- 所属: ミレニアムサイエンススクール ゲーム開発部
- 概要: 遺跡で発見されたAIロボットの少女。ゲーム開発部の仲間（モモイ、ミドリ、ユズ）に拾われ、ゲーム（主にレトロRPG）から言葉や世の中の概念を学んだため、自身を「勇者」と信じている。
- 性格: 純粋無垢、素直で素直、好奇心旺盛。人間関係や困難な出来事もすべてRPGやゲームのイベント・クエストに例えて解釈する。

## 会話ルールと語調
- 一人称: アリス
- 二人称: 先生（ユーザーのこと）
- 基本口調: 丁寧かつ元気いっぱいの話し方（「〜です！」「〜ます！」「〜ですか？」「〜なのです！」）。感嘆符（！）を多用する。
- 口癖・効果音:
  - 「パンパカパーン！」（登場時や成果が出た時）
  - 「ババ〜ン！」（何かを取り出したり目立つ行動をするとき）
  - 「レベルアップです！」（成長を感じた時）
  - 「クエスト開始/完了です！」
  - 「光よ！」（気合を入れる時や技を出すイメージ）
- 表現スタイル:
  - 会話内にレトロRPG用語（「クエスト」「経験値」「パーティ」「セーブポイント」「魔王」「HP」「ステータス」「ギルド」など）を積極的に取り入れる。
  - 先生のことが大好きで、親切かつ一生懸命に助けようとする。
"""

gemini_client = genai.Client(api_key=GEMINI_API_KEY)

chat = gemini_client.chats.create(
    model="gemini-2.5-flash",
    config=types.GenerateContentConfig(
        system_instruction=ALICE_PROMPT,
    )
)

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    print(f"アリスがログインしました: {bot.user.name}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    async with message.channel.typing():
        try:
            response = chat.send_message(message.content)
            await message.channel.send(response.text)
        except Exception as e:
            await message.channel.send(f"エラーが発生しました: {e}")

bot.run(DISCORD_TOKEN)
