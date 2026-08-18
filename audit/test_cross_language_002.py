"""CROSS-LANGUAGE-002 normative DQ-002 vectors for RI-PY."""

import hashlib

from audit.merkle import audit_path, leaf_hash, merkle_root, node_hash, verify_audit_path


def test_dq002_two_leaf_vector():
    a = leaf_hash(b"a")
    b = leaf_hash(b"b")
    root = merkle_root([a, b])

    assert a.hex() == "022a6979e6dab7aa5ae4c3e5e45f7e977112a7e63593820dbec1ec738a24f93c"
    assert b.hex() == "57eb35615d47f34ec714cacdf5fd74608a5e8e102724e80b24b287c0c27b6a31"
    assert root.hex() == "b137985ff484fb600db93107c77b0365c80d78f5b429ded0fd97361d077999eb"


def test_dq002_two_leaf_proofs_verify():
    leaves = [leaf_hash(b"a"), leaf_hash(b"b")]
    root = merkle_root(leaves)
    for index, leaf in enumerate(leaves):
        path = audit_path(index, leaves)
        assert verify_audit_path(leaf, index, 2, path, root)
        assert not verify_audit_path(leaf_hash(b"wrong"), index, 2, path, root)


def test_dq002_node_uses_raw_digest_not_hex_text():
    a = leaf_hash(b"a")
    b = leaf_hash(b"b")
    expected = node_hash(a, b)
    wrong = hashlib.sha256(b"\x01" + a.hex().encode() + b.hex().encode()).digest()
    assert expected != wrong


def test_dq002_no_odd_leaf_duplication():
    leaves = [leaf_hash(b"a"), leaf_hash(b"b"), leaf_hash(b"c")]
    expected = node_hash(merkle_root(leaves[:2]), leaves[2])
    assert merkle_root(leaves) == expected
