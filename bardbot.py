import discord
from discord.ext import commands
from discord import app_commands
import random
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

MESA_OBJETIVO = "⚔️ Derrotar o necromante das Terras Sombrias antes que ele invoque o Deus da Morte! 💀"

INSPIRACOES = [
    "🛡️ *A sorte favorece os corajosos!*",
    "🌟 *Você é mais forte do que pensa. Role os dados e descubra!*",
    "🔥 *Nunca subestime um grupo de aventureiros motivados!*",
    "✨ *Mesmo no escuro, a esperança pode brilhar.*",
    "🎯 *Hoje pode ser o dia do seu crítico natural!*"
]

CONDICOES = {
    "😵 Atordoado": "Você perde ações e tem desvantagem em jogadas de ataque.",
    "😢 Envenenado": "Você tem desvantagem em testes de resistência e ataque.",
    "🙈 Cego": "Você não enxerga nada e falha automaticamente em testes que dependem da visão.",
    "🧊 Paralisado": "Você não pode se mover nem agir.",
    "😴 Adormecido": "Você está inconsciente até ser acordado ou levar dano.",
    "🪦 Morto-vivo": "Você não está exatamente 'vivo'... mas ainda pode ser uma dor de cabeça para o grupo."
}

@bot.event
async def on_ready():
    print(f'Bot online! Logado como {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f'Sincronizado {len(synced)} comandos slash.')
    except Exception as e:
        print(f'Erro ao sincronizar comandos: {e}')

@bot.tree.command(name="roll", description="🎲 Rola um dado: d6, d10 ou d20")
@app_commands.describe(dado="Qual dado você quer rolar? Ex: d6, d10, d20")
async def roll(interaction: discord.Interaction, dado: str):
    dado = dado.lower()
    if dado not in ['6', '10', '20']:
        await interaction.response.send_message("⚠️ Só aceito d6, d10 ou d20, beleza?", ephemeral=True)
        return

    max_val = int(dado[1:])
    resultado = random.randint(1, max_val)
    await interaction.response.send_message(f'🎲 Você rolou um {dado.upper()} e tirou: **{resultado}**!')

@bot.tree.command(name="goal", description="🎯 Mostra o objetivo atual da mesa de RPG")
async def goal(interaction: discord.Interaction):
    await interaction.response.send_message(f'📜 **Missão Atual:**\n{MESA_OBJETIVO}')

@bot.tree.command(name="help", description="📖 Mostra os comandos disponíveis do bot")
async def help_command(interaction: discord.Interaction):
    help_text = (
        "🧙‍♂️ **Comandos do Bot RPG**\n"
        "===========================\n"
        "🎲 `/roll [d6|d10|d20]` → Rola um dado.\n"
        "📜 `/goal` → Mostra o objetivo da mesa.\n"
        "📘 `/stats` → Mostra os atributos básicos do RPG.\n"
        "✨ `/inspiration` → Receba uma frase inspiradora!\n"
        "☠️ `/conditions` → Veja efeitos negativos e condições.\n"
    )
    await interaction.response.send_message(help_text, ephemeral=True)

@bot.tree.command(name="stats", description="📘 Mostra os atributos básicos do RPG")
async def stats(interaction: discord.Interaction):
    texto = (
        "**📊 Atributos do RPG:**\n"
        "- 💪 **Vigor:** Saúde e força física.\n"
        "- 🧠 **Intelecto:** Conhecimento, lógica e magia.\n"
        "- 😎 **Presença:** Carisma e influência.\n"
        "- 🌀 **Éter:** Ligação com forças sobrenaturais.\n"
    )
    await interaction.response.send_message(texto)

@bot.tree.command(name="inspiration", description="✨ Receba uma frase inspiradora")
async def inspiration(interaction: discord.Interaction):
    frase = random.choice(INSPIRACOES)
    await interaction.response.send_message(frase)

@bot.tree.command(name="conditions", description="☠️ Lista de condições comuns no RPG")
async def conditions(interaction: discord.Interaction):
    resposta = "**☠️ Condições e Efeitos Comuns:**\n"
    for nome, desc in CONDICOES.items():
        resposta += f"- {nome}: {desc}\n"
    await interaction.response.send_message(resposta)

bot.run(TOKEN)
