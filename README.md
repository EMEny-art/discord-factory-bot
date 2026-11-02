# Discord Factory Bot

Questo progetto crea un master bot Discord con un comando slash `/crea-bot` che genera un bot figlio reale in Python e lo registra in `bots.json`.

Funzioni principali:
- `discord.py` 2.3
- master bot con comando `/crea-bot`
- 6 categorie e conteggi richiesti
- script Python generato per ogni bot figlio
- invito Discord creato da `client_id`
- file `generated_bots/` per i bot creati
- startup automatico dei bot figli
- pronto per hosting esterno su Bothosting/VPS/Linux

Categorie:
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

Importante:
- `token_bot` = token del bot figlio
- `client_id` = ID dell'app Discord, non il token
- il master bot non può creare un’app Discord da zero senza usare il Developer Portal di Discord

Variabili d'ambiente:
- `DISCORD_TOKEN` = token del master bot

Come avviare:
```bash
pip install -r requirements.txt
export DISCORD_TOKEN="TUO_TOKEN_MASTER"
python app.py
```
