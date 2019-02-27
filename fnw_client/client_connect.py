from telethon import TelegramClient, events, sync

class ClientAdapter:
    """
    A client that connects to Telegram.
    """

    def __init__(self, api_id, api_hash):

        self.__api_id = api_id
        self.__api_hash = api_hash

        self.__client = TelegramClient('session_name', api_id, api_hash)
        self.__client.start()

    def __del__(self):
        client.disconnect()

    def get_all_message_times(self, username):
        for message in self.__client.iter_messages(username):
            print(utils.get_display_name(message.sender), message.message)
