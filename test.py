from flask import Flask,render_template
import config
from web3 import Web3
import ccxt
import time

app = Flask(__name__)
w3 = Web3(Web3.HTTPProvider(config.INFURA_URL))

def get_ethereum_price():
    binance = ccxt.binance()
    ethereum_price = binance.fetch_ticker('ETH/USDC')
    return ethereum_price
     
@app.route("/")
def index():
    
    ethereum_price = get_ethereum_price()
    latest_blocks = []
    for block_number in range(w3.eth.block_number, w3.eth.block_number-10, -1):
        block = w3.eth.get_block(block_number)
        latest_blocks.append(block)

    latest_transactions = []
    for tx in latest_blocks[-1]['transactions'][-10:]:
        transaction = w3.eth.get_transaction(tx)
        latest_transactions.append(transaction)

    current_time = time.time()
    return render_template("index.html",
                           miners = config.MINERS,
                           ethereum_price=ethereum_price, 
                           latest_blocks=latest_blocks, 
                           current_time=current_time,
                           latest_transactions=latest_transactions )

    
@app.route("/address/<addr>")
def address(addr):
    return render_template("address.html", addr=addr)
    
@app.route("/block/<block_number>")
def block(block_number):
    return render_template("block.html", block_number=block_number)

@app.route('/transaction/<hash>')
def transaction(hash):
    tx = w3.eth.get_transaction(hash)
    value = w3.fromWei(tx.value, 'ether')
    receipt = w3.eth.get_transaction_receipt(hash)
    ethereum_price = get_ethereum_price()

    gas_price = w3.fromWei(tx.gasPrice, 'ether')

    return render_template('transaction.html', tx=tx, value=value, receipt=receipt, gas_price=gas_price, ethereum_price=ethereum_price)


if __name__ == "__main__":
    app.debug = True

    app.run(debug=True)
