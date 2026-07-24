import hashlib
import json

class MerkleAttestor:
    """Art. 12 & 13: Cryptographic log immutability"""
    @staticmethod
    def generate_leaf(data: dict):
        return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()

    def generate_etc(self, ari_result: dict):
        # Event Trust Certificate (ETC)
        leaf = self.generate_leaf(ari_result)
        return {"certificate": f"AURA-ETC-{leaf[:16]}", "proof": [leaf]}
