import hashlib, json


class Blockchain(object):

    @staticmethod
    def generate_hash(data):
        data_byte = json.dumps(data).encode()
        return hashlib.sha256(data_byte).hexdigest()


var1 = {
            'nome': "Jon Snow",
            'idade': 18,
        }
expected_hash1 = "4145c81419ee987c94f741936c3277e9b281e2ffc9faa3edb5693128e1ee65c1"
var1_hash = Blockchain.generate_hash(var1)
print('Dados: {}'.format(var1))
print('Hash   gerado: {}'.format(var1_hash))
print('Hash esperado: {}'.format(expected_hash1))
print('Iguais? {}\n'.format(expected_hash1==var1_hash))
