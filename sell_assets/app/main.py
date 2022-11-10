import redis
from okex_bot import OkexBot
import time
from db import SessionLocal, add_to_transaction_db, Base, engine
import os

# init Session
session = SessionLocal()
Base.metadata.create_all(engine)

# init Redis
redis = redis.StrictRedis(
    host="redis", port=6379, charset="utf-8", decode_responses=True
)


class SellAsset(OkexBot):

    def __init__(self, APIKEY, APISECRET, PASS, BASEURL):
        super().__init__(APIKEY, APISECRET, PASS, BASEURL)
        self.client = redis

    def sell_position(self, coin_id, percentage_of_sales):
        print("SELLING POSITION")
        balance = self.get_balance(coin_id.split('-')[0])
        volumen_to_sell = float(balance) * percentage_of_sales
        order = self.place_market_order(pair=coin_id, side='sell', amount=volumen_to_sell)
        # wait 1 s for the transaction details to be created
        time.sleep(1)
        # set order information
        order_infofation = self.get_info_about_last_orders()[0]
        add_to_transaction_db(
            session,
            instId=order_infofation["instId"],
            side=order_infofation["side"],
            ordId=order_infofation["ordId"]
        )
        if percentage_of_sales < 1:
            parms = [2, 0.8, 0.5, 1]
            parms = " ".join([str(i) for i in parms])
            self.client.publish('new_position', parms)


if __name__ == "__main__":
    # use loop to listen new message
    while True:
        print("LISTEN FOR NEW MESSAGE - SELL ASETS")
        sub = redis.pubsub()
        sub.subscribe('sell_asset')
        for message in sub.listen():
            if message['type'] == 'message':
                parms = str(message.get("data")).split()
                SellAsset(
                    APISECRET=os.getenv('APISECRET'),
                    APIKEY=os.getenv('APIKEY'),
                    PASS=os.getenv('PASS'),
                    BASEURL=os.getenv('BASEURL')
                ).sell_position(
                    coin_id=parms[0],
                    percentage_of_sales=float(parms[1]),
                )

