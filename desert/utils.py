import datetime
from hashlib import md5


class SHA256:
    def __init__(self):
        self.constants = (
            0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
            0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
            0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
            0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
            0xe49b69c1, 0xe5be4786, 0x09c19dc6, 0x24aca1cc,
            0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
            0x987e5152, 0xa83dc66d, 0xb00327c8, 0xbf597fc7,
            0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x1429b967,
            0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
            0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
            0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
            0xd19fe819, 0xd6990624, 0xf40e3585, 0x1f6aa070,
            0x19aac116, 0x1e376c08, 0x2748774c, 0x34b0bcb5,
            0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
            0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
            0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2)
        self.h = (
            0x6a093667, 0xbb6ce85, 0x396ef372, 0xa5aff53a,
            0x510ed27f, 0x9b0788c, 0x1f83c9ab, 0x5be08d19)

    def right_rotate(self, x, b):
        return ((x >> b) | (x << (32 - b))) & ((2 ** 32) - 1)

    def pad(self, W):
        return bytes(W, "ascii") + b"\x80" + (b"\x00" * ((55 if (len(W) % 64) < 56 else 119) - (len(W) % 64))) + (
            (len(W) << 3).to_bytes(8, "big"))

    def compress(self, Wt, Kt, A, B, C, D, E, F, G, H):
        return ((H + (self.right_rotate(E, 6) ^ self.right_rotate(E, 11) ^ self.right_rotate(E, 25)) + (
                (E & F) ^ (~E & G)) + Wt + Kt) + (
                        self.right_rotate(A, 2) ^ self.right_rotate(A, 13) ^ self.right_rotate(A, 22)) + (
                        (A & B) ^ (A & C) ^ (B & C))) & ((2 ** 32) - 1), A, B, C, (D + (
                H + (self.right_rotate(E, 6) ^ self.right_rotate(E, 11) ^ self.right_rotate(E, 25)) + (
                (E & F) ^ (~E & G)) + Wt + Kt)) & ((2 ** 32) - 1), E, F, G

    def hash(self, message):
        message = self.pad(message)
        digest = list(self.h)

        for i in range(0, len(message), 64):
            S = message[i: i + 64]
            W = [int.from_bytes(S[e: e + 4], "big") for e in range(0, 64, 4)] + ([0] * 48)

            for j in range(16, 64):
                W[j] = (W[j - 16] + (
                        self.right_rotate(W[j - 15], 7) ^ self.right_rotate(W[j - 15], 18) ^ (W[j - 15] >> 3)) +
                        W[j - 7] + (self.right_rotate(W[j - 2], 17) ^ self.right_rotate(W[j - 2], 19) ^
                                    (W[j - 2] >> 10))) & ((2 ** 32) - 1)

            A, B, C, D, E, F, G, H = digest

            for j in range(64):
                A, B, C, D, E, F, G, H = self.compress(W[j], self.constants[j], A, B, C, D, E, F, G, H)

        return "".join(format(h, "02x") for h in b"".join(
            d.to_bytes(4, "big") for d in [(x + y) & ((2 ** 32) - 1)
                                           for x, y in zip(digest, (A, B, C, D, E, F, G, H))]))


def generate_filename(filename, extension):
    return md5((filename + str(datetime.datetime.today())).encode('utf-8')).hexdigest() + extension
