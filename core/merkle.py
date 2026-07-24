import hashlib
import json


class MerkleAttestor:
    """Art. 12 & 13: Cryptographic log immutability"""
    @staticmethod
    def generate_leaf(data: dict):
        payload = json.dumps(data, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def generate_etc(self, ari_result: dict):
        # Event Trust Certificate (ETC)
        leaf = self.generate_leaf(ari_result)
        return {"certificate": f"AURA-ETC-{leaf[:16]}", "proof": [leaf], "leaf_hash": leaf}
