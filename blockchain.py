import hashlib, json, time


class Blockchain(object):

    def __init__(self):
        self.chain = []
        self.memPool = []
        self.createGenesisBlock()

    def createGenesisBlock(self):
    	self.createBlock()

    def createBlock(self):
    	if self.chain:
    		previous_block = self.chain[-1]
    		previous_block.pop('transactions')
    		previousHash = self.generateHash(previous_block)
    	else:
    		previousHash = '0000000000000000000000000000000000000000000000000000000000000000' 

    	block = {
    		'index': len(self.chain),
    		'timestamp': int(time.time()),
    		'nonce': 0,
    		'merkleRoot': 0,
    		'previousHash': previousHash,
    		'transactions': []
    	}

    	self.chain.append(block)

    	return block

    @staticmethod
    def generateHash(data):
        blkSerial = json.dumps(data, sort_keys=True).encode()
        return hashlib.sha256(blkSerial).hexdigest()

    def printChain(self):
    	for block in reversed(self.chain):
    		# block.pop('transactions')
    		selfhash = self.generateHash(block)
    		print('===================================== %s° BLOCK ====================================' % block['index'])
    		# print('Self Hash: ', selfhash)
    		print('Timestamp: ', block['timestamp'])
    		print('Nonce: ', block['nonce'])
    		print('merkleRoot: ', block['merkleRoot'])
    		print('previousHash: ', block['previousHash'])
    		print('====================================================================================\n\n')

# Teste
blockchain = Blockchain()
for x in range(0, 13): blockchain.createBlock()
blockchain.printChain()