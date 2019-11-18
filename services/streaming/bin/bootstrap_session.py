from telethon.sync import TelegramClient
from telethon.sessions import StringSession

from services.streaming.config import collect_env_vars


def get_session(api_id, api_hash):

    with TelegramClient(api_id, api_hash) as client:

        string = StringSession.save(client.session)
        print(string)


if __name__ == "__main__":
    creds = collect_env_vars("API_ID", "API_HASH")
    get_session(**creds)