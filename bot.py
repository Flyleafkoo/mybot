from bot_runner import BotRunner
from config import TOKEN, GROUP_IDS, SPECIFIC_GROUP_ID, SPECIFIC_GROUP_ID2
if __name__ == "__main__":
    TOKEN = TOKEN
    GROUP_IDS = GROUP_IDS
    SPECIFIC_GROUP_ID = SPECIFIC_GROUP_ID
    SPECIFIC_GROUP_ID2 = SPECIFIC_GROUP_ID2
    bot_runner = BotRunner(TOKEN, GROUP_IDS, SPECIFIC_GROUP_ID)
    bot_runner.start()
