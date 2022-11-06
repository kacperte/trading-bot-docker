import redis
from okex_bot import OkexBot
import time
from db import SessionLocal, add_to_transaction_db, Base, engine

# OKEX API credentials
APIKEY = "ba435770-3228-4277-a71d-52ad5514514d"
APISECRET = "DD9AB7614D44DF8DEAA7DEC0C216855C"
PASS = "mD8SG#28vr2sAyB"
BASEURL = "https://www.okex.com"

# init Session
session = SessionLocal()
Base.metadata.create_all(engine)


class PlaceOrder(OkexBot):
    """The class inherits from OKEX Bot. Performs operations to buy or sell a token."""

    def __init__(self, coin_id: str, APIKEY, APISECRET, PASS, BASEURL):
        super().__init__(APIKEY, APISECRET, PASS, BASEURL)
        self.coin_id = coin_id
        self.usdt_balance = self.get_balance("USDT")
        self.client = redis.Redis(host="redis", port=6379)

    # function to open new position with new token
    def open_position(self):
        # using a for loop to perform this operation 10 times if the exchange will block operations
        for _ in range(9):
            # purchase of new token
            order = self.place_market_order(
                pair=self.coin_id, side="buy", amount=self.usdt_balance
            )
            # if the purchase was successful, the loop will break
            if self.get_balance(self.coin_id):
                # wait 1 s for the transaction details to be created
                time.sleep(1)
                # set order information
                order_information = self.get_info_about_last_orders()[0]
                # publish to redis information about selling strategy(%profit/%losses/%profit volumen/%losses volumen)
                parms = [2, 0.8, 0.5, 1]
                parms = " ".join([str(i) for i in parms])
                self.client.publish("new_position", parms)
                # post to db inforamtion
                add_to_transaction_db(
                    session,
                    instId=order_information["instId"],
                    side=order_information["side"],
                    ordId=order_information["ordId"],
                )
                # break loop
                break


if __name__ == "__main__":
    # use loop to listen new message
    while True:
        print("START LISTEN - REDIS PUB/SUB")
        redis = redis.Redis(host="redis", port=6379)
        sub = redis.pubsub()
        sub.subscribe("token_id")
        for message in sub.listen():
            if message["type"] == "message":
                coind_id = str(message.get("data")).split("'")[1].split(" ")
                print(coind_id)
                # PlaceOrder(
                #     coin_id=coind_id[0],
                #     APISECRET=APISECRET,
                #     APIKEY=APIKEY,
                #     PASS=PASS,
                #     BASEURL=BASEURL,
                # )
