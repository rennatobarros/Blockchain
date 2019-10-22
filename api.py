from flask import Flask
import blockchain

blockchain = Blockchain()

app = Flask(__name__)

@app.route('/transactions/create')


def create_transaction():
    pass

if __name__ == '__main__':
    app.run()