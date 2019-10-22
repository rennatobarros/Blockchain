import hashlib
import json
from time import time
import copy
import random
import requests

from bitcoin.wallet import CBitcoinSecret
from bitcoin.signmessage import BitcoinMessage, VerifyMessage, SignMessage

DIFFICULTY = 3 # Quantidade de zeros (em hex) iniciais no hash valido.

class Blockchain(object):

    def __init__(self):
        self.chain = []
        self.memPool = []
        self.nodes = set()
        self.createGenesisBlock()


    def createGenesisBlock(self):
        self.createBlock(previousHash='0'*64, nonce=0)
        self.mineProofOfWork(self.prevBlock)


    def createBlock(self, nonce=0, previousHash=None):
        if (previousHash == None):
            previousBlock = self.chain[-1]
            previousBlockCopy = copy.copy(previousBlock)
            previousBlockCopy.pop("transactions", None)

        copy_mempool = Blockchain.getTxHashes(self.memPool)

        block = {
            'index': len(self.chain) + 1,
            'timestamp': int(time()),
            'transactions': self.memPool,
            'merkleRoot': self.generateMerkleRoot(copy_mempool),
            'nonce': nonce,
            'previousHash': previousHash or self.generateHash(previousBlockCopy),
        }

        self.memPool = []
        self.chain.append(block)

        return block


    def mineProofOfWork(self, prevBlock):
        nonce = 0
        while self.isValidProof(prevBlock, nonce) is False:
            nonce += 1

        return nonce


    def createTransaction(self, sender, recipient, amount, timestamp, privKey):
        transaction = {
            "sender": sender,
            "recipient": recipient,
            "amount": amount,
            "timestamp": timestamp,
        }

        signature = hashlib.sha256(Blockchain.sign(privKey, json.dumps(transaction, sort_keys=True))).hexdigest()
        transaction["signature"] = signature


        self.memPool.append(transaction)

        return True


    @staticmethod
    def generateMerkleRoot(transactions):
        copy_transactions = []

        if len(transactions) == 0:
            return '0' * 64
        elif len(transactions) == 1:
            return transactions[0]
        elif len(transactions)%2 != 0:
            transactions.append(transactions[-1])

        for i in range(0, len(transactions), 2):
            hash = Blockchain.generateHash(transactions[i] + transactions[i+1])
            copy_transactions.append(hash)

        return Blockchain.generateMerkleRoot(copy_transactions)


    @staticmethod
    def isValidProof(block, nonce):
        block['nonce'] = nonce
        guessHash = Blockchain.getBlockID(block)
        return guessHash[:DIFFICULTY] == '0' * DIFFICULTY


    @staticmethod
    def generateHash(data):
        blkSerial = json.dumps(data, sort_keys=True).encode()
        return hashlib.sha256(blkSerial).hexdigest()


    @staticmethod
    def getBlockID(block):
        blockCopy = copy.copy(block)
        blockCopy.pop("transactions", None)
        return Blockchain.generateHash(blockCopy)


    def printChain(self):
        for block in reversed(self.chain):
            selfhash = Blockchain.getBlockID(block)

            print(hex(int(selfhash, 16)))
            print('\t\t\t\t\tA')
            print('\t\t\t\t\t|\n')
            print(' =================================== %s BLOCK ==================================' % block['index'])
            print('| Self Hash: ', selfhash)
            print('| Timestamp: ', block['timestamp'])
            print('| Nonce: ', block['nonce'])
            print('| transactions: ', block['transactions'])
            print('| merkleRoot: ', block['merkleRoot'])
            print('| previousHash: ', block['previousHash'])
            print(' ================================================================================')


    @property
    def prevBlock(self):
        return self.chain[-1]


    @staticmethod
    def sign(privKey, message):
        secret = CBitcoinSecret(privKey)
        msg = BitcoinMessage(message)
        return SignMessage(secret, msg)


    @staticmethod
    def verifySignature(address, signature, message):
        msg = BitcoinMessage(message)
        return VerifyMessage(address, msg, signature)


    def isValidChain(self, chain):
        for i, block in enumerate(chain):
            valid_proof = Blockchain.isValidProof(block, block['nonce'])

            if not valid_proof:
                return False

            if i != 0:
                header_prev_hash = block['previousHash']
                prev_block = copy.copy(chain[i-1])
                prev_block.pop('transactions')

                block_prev_hash = Blockchain.generateHash(prev_block)

                if header_prev_hash != block_prev_hash:
                    # print(header_prev_hash)
                    # print(block_prev_hash)
                    print("Bloco invalido! Hash do bloco anterior invalido.")
                    return False

                block_merkle_root = block['merkleRoot']
                copy_mempool = Blockchain.getTxHashes(block['transactions'])

                transactions_merkle_root = Blockchain.generateMerkleRoot(copy_mempool)

                if block_merkle_root != transactions_merkle_root:
                    # print("Block merkle = " + block_merkle_root)
                    # print("transactions merkle = " + transactions_merkle_root)
                    print("Bloco invalido! merkleRoot invalido.")
                    return False

            print("Bloco %d valido " % i)

        return True

    @staticmethod
    def getTxHashes(data):
        aux = []
        for i in range(len(data)):
            hash = Blockchain.generateHash(data[i])
            aux.append(hash)

        return aux

    def resolveConflicts(self):
        for node in nodes:
            response = requests.get("http://%s/chain" % node)
            


# Teste
# #blockchain = Blockchain()

# sender = '19sXoSbfcQD9K66f5hwP5vLwsaRyKLPgXF'
# recipient = '1MxTkeEP2PmHSMze5tUZ1hAV3YTKu2Gh1N'

# # Cria 5 blocos, incluindo o Genesis, contendo de 1-4 transacoes cada, com valores aleatorios, entre os enderecos indicados em sender e recipient.
# for x in range(0, 4):
#     for y in range(0, random.randint(1,4)):
#         timestamp = int(time())
#         amount = random.uniform(0.00000001, 100)
#         blockchain.createTransaction(sender, recipient, amount, timestamp, 'L1US57sChKZeyXrev9q7tFm2dgA2ktJe2NP3xzXRv6wizom5MN1U')
#     blockchain.createBlock()
#     blockchain.mineProofOfWork(blockchain.prevBlock)

# blockchain.printChain()

# print(blockchain.isValidChain(blockchain.chain))
