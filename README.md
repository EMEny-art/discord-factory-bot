# Discord Factory Bot

Questo progetto crea un master bot Discord con un comando slash `/crea-bot` che genera un bot figlio reale in Python, lo salva in `bots.json` e lo avvia automaticamente su hosting esterno.

Funzioni principali:
- `discord.py` 2.3
- master bot con comando `/crea-bot`
- 6 categorie con i conteggi richiesti
- file Python generato per ogni bot figlio
- URL di invito Discord generato da `client_id`
- hosting pronto per Bothosting, VPS, Render e altri host Linux
- i bot figli usano comandi prefix `!` invece di slash command per rispettare i limiti reali di Discord

Categorie supportate:
- TICKET AVANZATI = 200 comandi
- MODERAZIONE AVANZATA = 200 comandi
- CONFIGURAZIONE AVANZATA = 150 comandi
- GIVEAWAY ED ECONOMIA = 150 comandi
- MUSICA E FUN = 200 comandi
- TUTTO = 900 comandi

Comando master:
`/crea-bot token_bot:string categoria_1 categoria_2 categoria_3 nome_bot:optional client_id:optional`

Esempi:
- `/crea-bot token_bot:ABC123 TICKET AVANZATI "" ""`
- `/crea-bot token_bot:ABC123 MODERAZIONE AVANZATA CONFIGURAZIONE AVANZATA "" ""`
- `/crea-bot token_bot:ABC123 TUTTO "" "" "example-bot" 123456789012345678`

Nota importante:
- `token_bot` = token del bot figlio
- `client_id` = ID dell'app Discord (non il token)
- per creare un'app Discord vera e propria serve il Developer Portal di Discord
- i bot generati usano comandi `!` in modo realistico perché Discord limita fortemente le slash command

Variabili d'ambiente:
- `DISCORD_TOKEN` = token del master bot

Avvio locale:
```bash
pip install -r requirements.txt
export DISCORD_TOKEN="TUO_TOKEN_MASTER"
python app.py
```

Hosting:
- crea un file `.env` con `DISCORD_TOKEN=...`
- avvia il processo su Bothosting/VPS/Render con `python app.py`
- il master bot resta online e avvia i bot figli da `generated_bots/`

La piattaforma non può creare un’app Discord da zero senza il Developer Portal, ma il sistema qui genera e avvia i bot figli correttamente dopo che l’app esiste.
