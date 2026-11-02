# Discord Factory Bot Real

Questo progetto è una versione avanzata e reale di un factory bot Discord basato su `discord.py 2.3`.

Funzioni principali:
- Master bot con slash command `/crea-bot`
- Generazione reale di script Python per ogni bot creato
- Tutte le categorie richieste in comandi dinamici
- Salvataggio e ricaricamento automatico da `bots.json`
- Generazione automatica dell'URL di invito Discord quando hai il `client_id`
- Pronto per host esterni: Bothosting, VPS, Linux

Comando master:
`/crea-bot token_bot:string categoria_1 categoria_2 categoria_3 bot_name:optional client_id:optional`

Esempio:
`/crea-bot token_bot:ABC123 TICKET AVANZATI MODERAZIONE AVANZATA "" ""`

Categorie supportate:
- TICKET AVANZATI = 200 comandi
- MODERAZIONE AVANZATA = 200 comandi
- CONFIGURAZIONE AVANZATA = 150 comandi
- GIVEAWAY ED ECONOMIA = 150 comandi
- MUSICA E FUN = 200 comandi
- TUTTO = 900 comandi totali

Nota importante sul bot reale:
Per creare un invito Discord reale, Discord richiede il `client_id` dell'app bot dal Developer Portal. Il token è diverso dal client ID. Il comando genera l'URL di invito automaticamente appena inserisci il client_id.

Variabili d'ambiente:
- `DISCORD_TOKEN` = token del master bot

Esecuzione:
```bash
pip install -r requirements.txt
python app.py
```

Hosting Linux / Bothosting:
- crea un file `.env` con `DISCORD_TOKEN=...`
- avvia il processo con `python app.py`
- la factory genera i bot reali dentro `generated_bots/`

I bot creati vengono avviati automaticamente all'avvio del master, se presenti in `bots.json`.
