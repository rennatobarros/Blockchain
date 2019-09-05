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

		self.mineProofOfWork(block)

		self.chain.append(block)

		return block


	def mineProofOfWork(self, prevBlock):
		nonce = 0
		while True:
			nonce += 1
			valid = Blockchain.isValidProof(prevBlock, nonce)
			if valid:
				break


	@staticmethod
	def generateHash(data):
		blkSerial = json.dumps(data, sort_keys=True).encode()
		return hashlib.sha256(blkSerial).hexdigest()


	@staticmethod
	def getBlockID(block):
		b = copy.deepcopy(block)
		b.pop('transactions')
		return Blockchain.generateHash(b)


	@staticmethod
	def isValidProof(block, nonce):
		meta = str('0'*(DIFFICULTY-1)+'1'+'0'*(64-DIFFICULTY-1))

		block['nonce'] = nonce
		block_hash = Blockchain.getBlockID(block)

		return (block_hash < meta)


	def printChain(self):
		for block in reversed(self.chain):
			selfhash = Blockchain.getBlockID(block)

			print(hex(int(selfhash, 16)))
			print('\t\t\t\t\tA')
			print('\t\t\t\t\t|\n')
			print(' =================================== %s° BLOCK ==================================' % block['index'])
			print('| Self Hash: ', selfhash)
			print('| Timestamp: ', block['timestamp'])
			print('| Nonce: ', block['nonce'])
			print('| merkleRoot: ', block['merkleRoot'])
			print('| previousHash: ', block['previousHash'])
			print(' ================================================================================')


blockchain = Blockchain()
for x in range(0, 8): blockchain.createBlock()
# blockchain.printChain()

for x in blockchain.chain :
    print('[Bloco #{} : {}] Nonce: {} | É válido? {}'.format(x['index'], Blockchain.getBlockID(x), x['nonce'], Blockchain.isValidProof(x, x['nonce'])))
