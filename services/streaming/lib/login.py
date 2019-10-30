from telethon import TelegramClient

def send_code(api_id, api_hash, phone):
    with TelegramClient('streaming_analytics', api_id, api_hash) as client:
        return await client.send_code_request(phone)

def authenticate_session(api_id, api_hash, phone, code):
    with TelegramClient('streaming_analytics', api_id, api_hash) as client:
        return await client.sign_in(phone, code)
