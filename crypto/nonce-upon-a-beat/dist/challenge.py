import json
import secrets
from hashlib import sha256

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
GX = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
GY = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
G = (GX, GY)


def point_add(left, right):
    if left is None:
        return right
    if right is None:
        return left

    x1, y1 = left
    x2, y2 = right

    if x1 == x2 and (y1 + y2) % P == 0:
        return None

    if left == right:
        slope = 3 * x1 * x1 * pow(2 * y1, -1, P)
    else:
        slope = (y2 - y1) * pow(x2 - x1, -1, P)

    slope %= P
    x3 = (slope * slope - x1 - x2) % P
    y3 = (slope * (x1 - x3) - y1) % P
    return x3, y3


def scalar_mul(value, point=G):
    result = None
    current = point

    while value:
        if value & 1:
            result = point_add(result, current)
        current = point_add(current, current)
        value >>= 1

    return result


def hash_message(message):
    return int.from_bytes(sha256(message).digest(), "big")


def sign(message, private_key, nonce):
    nonce_point = scalar_mul(nonce)
    if nonce_point is None:
        raise ValueError("invalid nonce")

    r = nonce_point[0] % N
    s = pow(nonce, -1, N) * (hash_message(message) + r * private_key) % N

    if r == 0 or s == 0:
        raise ValueError("invalid signature")

    return r, s


class BeatGrid:
    def __init__(self, secret):
        self.secret = secret.to_bytes(32, "big")
        self.slots = {}

    def nonce_for(self, bpm, bar):
        slot = f"{bpm}:{bar // 16}".encode()
        if slot not in self.slots:
            digest = sha256(self.secret + slot).digest()
            self.slots[slot] = int.from_bytes(digest, "big") % (N - 1) + 1
        return self.slots[slot]


def aes_ctr(data, key, iv):
    encryptor = Cipher(algorithms.AES(key), modes.CTR(iv)).encryptor()
    return encryptor.update(data) + encryptor.finalize()


def build_challenge(flag, private_key=None, beat_secret=None, ctr_iv=None):
    private_key = private_key or secrets.randbelow(N - 1) + 1
    beat_secret = beat_secret or secrets.randbelow(N - 1) + 1
    ctr_iv = ctr_iv or secrets.token_bytes(16)

    tracks = [
        ("midnight_modulus.wav", 128, 64),
        ("elliptic_echoes.wav", 128, 71),
    ]

    grid = BeatGrid(beat_secret)
    signed_tracks = []

    for title, bpm, bar in tracks:
        message = f"track={title}|artist=DJ Curve|bpm={bpm}|bar={bar}".encode()
        nonce = grid.nonce_for(bpm, bar)
        r, s = sign(message, private_key, nonce)
        signed_tracks.append(
            {
                "message": message.decode(),
                "r": hex(r),
                "s": hex(s),
            }
        )

    public_key = scalar_mul(private_key)
    key = sha256(private_key.to_bytes(32, "big") + b"encore-key").digest()
    ciphertext = aes_ctr(flag, key, ctr_iv)

    return {
        "curve": "secp256k1",
        "public_key": {
            "x": hex(public_key[0]),
            "y": hex(public_key[1]),
        },
        "tracks": signed_tracks,
        "encore": {
            "iv": ctr_iv.hex(),
            "ciphertext": ciphertext.hex(),
        },
    }


def main():
    from secret import FLAG

    print(json.dumps(build_challenge(FLAG), indent=2))


if __name__ == "__main__":
    main()
