import requests
import redis
from db import SessionLocal, add_to_new_token_db, engine, Base


# init Redis
redis = redis.Redis(host="localhost", port=6379)

# OKX API URL
url = "https://www.okx.com/priapi/v5/rubik/app/public/new-coin-rank?t=1661446882241&type=USDT"

# init Session
session = SessionLocal()
Base.metadata.create_all(engine)


def stream_listener():
    """Function to listen for OKEX API and to catch new tokens"""
    # actual list of tokens on OKEX
    list_of_coins = requests.get(url).json()["data"][0]["online"]
    # number of tokens on OKEX
    len_list_of_coins = len(list_of_coins)

    # Test variable
    counter = 0

    while True:
        # condition that check if there is new token
        # if len(requests.get(url).json()["data"][0]["online"]) > len_list_of_coins:
        # temp solutions to check if evrything works (redis and pgsql docker)
        if counter > 100:
            # set new token ID
            # new_coin = [
            #     x
            #     for x in requests.get(url).json()["data"][0]["online"]
            #     if x not in list_of_coins
            # ][0]["instId"]
            new_coin = 'XD-USDT'
            # publish to redis information about new token
            redis.publish("token_id", new_coin)
            # post to db inforamtion
            add_to_new_token_db(session, instId=new_coin, market="okex")
            # update the following variables with new data
            list_of_coins = requests.get(url).json()["data"][0]["online"]
            len_list_of_coins = len(requests.get(url).json()["data"][0]["online"])

        print(f"Checking for new coin...{counter}")

        counter += 1


if __name__ == "__main__":
    stream_listener()

