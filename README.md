# attentionalamoussebot
Funny personal bot which says 'ATTENTION A LA MOUSSE' and other bullshit.

## Setting up
First, create a ``.env`` file at the root of the repository containing the following values:
```
chat_id=<your chat_id>
bot_token=<your bot token>
admin_userid=<your user id>
```

Once this file has correctly filled and created, you can run the following command at the root of the repository:
```bash
docker-compose up -d
```