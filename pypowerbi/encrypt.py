import base64

from Crypto.PublicKey.RSA import construct
from Crypto.Cipher import PKCS1_OAEP

CHUNK_LENGTH = 85


class PublicKey():

    def __init__(self, public_key):
        self.exponent = self._from_base64_string(public_key["exponent"])
        self.modulus = self._from_base64_string(public_key["modulus"])

    def encrypt(self, plain_text):
        return base64.b64encode(
            b''.join(self._get_encrypted_chunks(
                bytes_to_encrypt=plain_text.encode()
            ))
        ).decode()

    def _get_encrypted_chunks(self, bytes_to_encrypt):
        return [
            self._rsa_encryptor.encrypt(x)
            for x in self._chunks(bytes_to_encrypt, CHUNK_LENGTH)
        ]

    @staticmethod
    def _from_base64_string(base64_string):
        return int.from_bytes(
            base64.b64decode(base64_string), 'big'
        )

    @staticmethod
    def _chunks(l, n):
        """Yield successive n-sized chunks from l."""
        for i in range(0, len(l), n):
            yield l[i:i + n]

    @property
    def _rsa_encryptor(self):
        return PKCS1_OAEP.new(
            construct((self.modulus, self.exponent))
        )
