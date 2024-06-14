from typing import List, Dict
import json
from websocket import create_connection

class KrakenWebsocketAPI():

    URL = "wss://ws.kraken.com/v2"

    def __init__(self,
                 product_id: str
                 ):
        self.product_id = product_id

        self._ws = create_connection(self.URL)


        print("Connection established!")

        self._subscribe(product_id)

    def _subscribe(self, product_id: str):
        """"
            Establishes a remote connection to Kraken API
            and subscribes to trades for given product_id
        """

        print(f"Subscribing to trades for {product_id}")
        # Sending Kraken API subscription request
        msg = {
            "method": "subscribe",
            "params": {
                        "channel": "trade",
                        "symbol": [product_id],
                        "snapshot": False
                    }
        }

        self._ws.send(json.dumps(msg))

        print("Subscription success!")

        # Dumping heartbeat messages from _ws
        _ = self._ws.recv()
        _ = self._ws.recv()


    def get_trades(self) -> List[Dict]:
            
            
        # mock_trades =[ 
        #                 {
        #                     "product_id": 'BTC/USD',
        #                     "price":  60000,
        #                     "volume":  0.01,
        #                     "timestamp": 163000000
        #                 },
        #                 {
        #                     "product_id": 'BTC/USD',
        #                     "price":  60300,
        #                     "volume":  0.11,
        #                     "timestamp": 165000000
        #                 }
        #             ]

        message = self._ws.recv()

        if 'heartbeat' in message:
            return []
        
        # Parse string as dictionary
        message = json.loads(message)

        trades = []

        # Extract trades from messages
        for trade in message['data']:
            trades.append({
                'product_id' : self.product_id,
                'price' : trade['price'],
                'volume' : trade['qty'],
                'timestamp': trade['timestamp']
            })

        #print("message received ", message)

        return trades

        #breakpoint()

       