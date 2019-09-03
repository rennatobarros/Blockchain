import hashlib, json, time, copy


DIFFICULTY = 4 # Quantidade de zeros (em hex) iniciais no hash válido.


class Blockchain(object):

	def __init__(self):
		self.chain = []
		self.memPool = []
		self.createGenesisBlock()


	def createGenesisBlock(self):
		self.createBlock()


	def createBlock(self):
		if self.chain:
			previous_block = copy.deepcopy(self.chain[-1])
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


	def mineProofOfWork(self, prevBlock):



		while True:
			prevBlock['nonce'] += 1
			prev_hash = Blockchain.generateHash(prevBlock)
			
			if 

		pass


	@staticmethod
	def generateHash(data):
		blkSerial = json.dumps(data, sort_keys=True).encode()
		return hashlib.sha256(blkSerial).hexdigest()


	@staticmethod
	def getBlockID(block):
		b = copy.deepcopy(block)
		b.pop('transactions')
		return Blockchain.generateHash(b)


	@property
	def prevBlock(self):
		return self.chain[-1]


	@staticmethod
	def isValidProof(block, nonce):
		


	def printChain(self):
		for block in reversed(self.chain):
			selfhash = Blockchain.getBlockID(block)


			print('\t\t\t\t\tA')
			print('\t\t\t\t\t|\n')
			print(' =================================== %s° BLOCK ==================================' % block['index'])
			print('| Self Hash: ', selfhash)
			print('| Timestamp: ', block['timestamp'])
			print('| Nonce: ', block['nonce'])
			print('| merkleRoot: ', block['merkleRoot'])
			print('| previousHash: ', block['previousHash'])
			print(' ================================================================================')


# Teste
blockchain = Blockchain()
for x in range(0, 13): blockchain.createBlock()
# blockchain.printChain()