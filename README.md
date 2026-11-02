# Discord Factory Bot

Questo progetto crea un bot master con comando slash `/crea-bot` e registra i bot creati in `bots.json`.

Caratteristiche:
- `discord.py` 2.3
- 6 categorie con conteggi richiesti
- Cogs separati in `cogs/`
- Autoreload dei bot registrati da `bots.json`
- file pronto per Render.com

Comando principale:
`/crea-bot token_bot:string categoria_1 categoria_2 categoria_3`

Categorie supportate:
- TICKET AVANZATI = 200 comandi
- MODERAZIONE AVANZATA = 200 comandi
- CONFIGURAZIONE AVANZATA = 150 comandi
- GIVEAWAY ED ECONOMIA = 150 comandi
- MUSICA E FUN = 200 comandi
- TUTTO = 900 comandi

Esempi:
- `/crea-bot token_bot:ABC123 TICKET AVANZATI "" ""`
- `/crea-bot token_bot:ABC123 MODERAZIONE AVANZATA CONFIGURAZIONE AVANZATA ""`
- `/crea-bot token_bot:ABC123 TUTTO "" ""`

Variabili d'ambiente:
- `DISCORD_TOKEN`

Render.com:
- usa il file `render.yaml`
- aggiungi il token del bot master come variabile d'ambiente

Licenza: MIT
