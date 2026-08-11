#![allow(clippy::unwrap_used, clippy::expect_used, clippy::panic)]
//! Characterization tests for the integrity coverage of `AuditEntry::violations`.
//!
//! # CURRENT BEHAVIOUR ≠ NORMATIVE REQUIREMENT
//!
//! Every assertion in this file records what the code does **today**. None of
//! them asserts what the code **ought** to do. If a future authorized design
//! decision changes the digest input, these tests are expected to fail, and
//! that failure is the intended signal — not a regression to be silenced by
//! weakening the assertion.
//!
//! Do not cite this file as evidence that the recorded behaviour is correct,
//! required, approved, or specified. The question of what the required
//! behaviour is remains open; see `GUARD-G1_INTEGRITY_DESIGN_BRIEF.md` §12
//! (decisions D1–D8), none of which is decided.
//!
//! ## What is recorded here
//!
//! `chain_hash` is computed from nine fields (`src/chain.rs:36-48`).
//! `violations` is not one of them. Merkle leaves are built from `chain_hash`
//! alone (`src/segment.rs:141-147`), so the segment layer inherits the same
//! coverage. These tests pin that state so any change to it becomes visible.
//!
//! * `t_0a_*` — a mutated `violations` field still passes `verify_chain`.
//! * `t_0b_*` — a mutated `violations` field still passes segment verification.
//! * `t_0c_*` — known-answer vector for the current nine-field digest preimage.

use aura_guard::chain::{compute_chain_hash, verify_chain};
use aura_guard::crypto::genesis_hash;
use aura_guard::log_writer::{read_all_entries, LogWriter};
use aura_guard::models::{AuditEntry, Violation};
use aura_guard::segment::{build_manifest, verify_manifest_against_entries};

// ---------------------------------------------------------------------------
// Fixtures — synthetic, fixed, obviously not production data.
// ---------------------------------------------------------------------------

const FIXED_TIMESTAMP: &str = "2026-01-01T00:00:00+00:00";
const FIXED_AUDIT_ID: &str = "00000000-0000-4000-8000-000000000000";
const POLICY_HASH: &str = "aa\
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa";
const INPUT_HASH: &str = "bb\
bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb";
const SHADOW_HASH: &str = "cc\
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc";

/// A violation carrying the kind of detail an auditor would rely on.
fn substantive_violation() -> Violation {
    Violation {
        rule: "cc-luhn".to_string(),
        action: "deny".to_string(),
        confidence: 0.99,
        validator: Some("luhn_ok".to_string()),
    }
}

/// Build one entry whose `chain_hash` is computed by the production function.
fn entry_with(seq: u64, prev_hash: &str, violations: Vec<Violation>) -> AuditEntry {
    let decision = "DENY".to_string();
    let policy_set = "finance-v1".to_string();
    let context = "Finance Bot".to_string();

    let chain_hash = compute_chain_hash(
        prev_hash,
        &decision,
        &policy_set,
        POLICY_HASH,
        &context,
        INPUT_HASH,
        SHADOW_HASH,
        seq,
        FIXED_TIMESTAMP,
    );

    AuditEntry {
        schema: "aura-guard.audit.v1".to_string(),
        seq,
        audit_id: FIXED_AUDIT_ID.to_string(),
        request_id: None,
        timestamp: FIXED_TIMESTAMP.to_string(),
        decision,
        policy_set,
        policy_hash: POLICY_HASH.to_string(),
        context,
        input_hash: INPUT_HASH.to_string(),
        shadow_hash: SHADOW_HASH.to_string(),
        violations,
        prev_hash: prev_hash.to_string(),
        chain_hash,
    }
}

/// Two linked entries, the first carrying a substantive violation.
fn two_linked_entries() -> Vec<AuditEntry> {
    let e0 = entry_with(0, &genesis_hash(), vec![substantive_violation()]);
    let e1 = entry_with(1, &e0.chain_hash, vec![]);
    vec![e0, e1]
}

/// Write entries through the production `LogWriter`, returning the log path.
fn write_log(dir: &std::path::Path, entries: &[AuditEntry]) -> std::path::PathBuf {
    let path = dir.join("audit.jsonl");
    let writer = LogWriter::open(path.clone(), &genesis_hash()).expect("log opens");
    for e in entries {
        writer.append(e).expect("entry appends");
    }
    path
}

/// Rewrite the persisted `violations` array of the first line, leaving every
/// other byte of the record untouched.
///
/// This models an operator with write access to `logs/audit.jsonl`. It does
/// not use any production code path — that is the point.
fn tamper_first_line_violations(path: &std::path::Path, replacement: &str) {
    let raw = std::fs::read_to_string(path).expect("log is readable");
    let mut lines: Vec<String> = raw.lines().map(str::to_string).collect();

    let first = &lines[0];
    let start = first
        .find("\"violations\":[")
        .expect("violations array present");
    let open = start + "\"violations\":".len();
    let close = first[open..].find(']').expect("array closes") + open;

    let tampered = format!("{}{}{}", &first[..open], replacement, &first[close + 1..]);
    lines[0] = tampered;

    std::fs::write(path, format!("{}\n", lines.join("\n"))).expect("log is writable");
}

// ---------------------------------------------------------------------------
// T-0a — chain verification is unaffected by mutation of `violations`
// ---------------------------------------------------------------------------

/// CURRENT BEHAVIOUR: emptying the `violations` array of a persisted entry
/// does not break the hash chain. `verify_chain` returns `Ok`.
///
/// NOT A NORMATIVE REQUIREMENT. Whether this ought to be detected is decision
/// D1, undecided.
#[test]
fn t_0a_chain_verifies_after_violations_emptied() {
    let dir = tempfile::tempdir().expect("tempdir");
    let entries = two_linked_entries();
    let path = write_log(dir.path(), &entries);

    // Precondition: the untampered log verifies.
    let before = read_all_entries(&path).expect("log parses");
    assert!(
        verify_chain(&before).is_ok(),
        "precondition: untampered log must verify"
    );
    assert_eq!(before[0].violations.len(), 1, "fixture carries a violation");

    tamper_first_line_violations(&path, "[]");

    let after = read_all_entries(&path).expect("tampered log still parses");
    assert!(
        after[0].violations.is_empty(),
        "the mutation reached the persisted record"
    );

    // RECORDED: the chain still verifies. The evidentiary detail is gone and
    // no verification step notices.
    assert!(
        verify_chain(&after).is_ok(),
        "CURRENT BEHAVIOUR: violations are outside the chain digest, so \
         emptying them does not break verification. If this assertion begins \
         to fail, the digest input has changed — see GUARD-G1 brief §12."
    );
}

/// CURRENT BEHAVIOUR: rewriting the rule identifier, the declared action, the
/// confidence and the validator outcome does not break the hash chain.
///
/// NOT A NORMATIVE REQUIREMENT.
#[test]
fn t_0a_chain_verifies_after_violation_content_rewritten() {
    let dir = tempfile::tempdir().expect("tempdir");
    let entries = two_linked_entries();
    let path = write_log(dir.path(), &entries);

    tamper_first_line_violations(
        &path,
        r#"[{"rule":"benign-match","action":"allow","confidence":0.01,"validator":"none"}]"#,
    );

    let after = read_all_entries(&path).expect("tampered log still parses");
    assert_eq!(after[0].violations[0].rule, "benign-match");
    assert_eq!(after[0].violations[0].action, "allow");

    // RECORDED: a DENY decision now carries an `allow` violation, and the
    // chain still verifies. The record is internally inconsistent; nothing
    // automated detects that.
    assert_eq!(
        after[0].decision, "DENY",
        "decision field is covered, unchanged"
    );
    assert!(
        verify_chain(&after).is_ok(),
        "CURRENT BEHAVIOUR: violation content is outside the chain digest."
    );
}

/// CURRENT BEHAVIOUR: injecting a violation that never occurred does not break
/// the hash chain.
///
/// NOT A NORMATIVE REQUIREMENT.
#[test]
fn t_0a_chain_verifies_after_violation_fabricated() {
    let dir = tempfile::tempdir().expect("tempdir");
    let entries = two_linked_entries();
    let path = write_log(dir.path(), &entries);

    tamper_first_line_violations(
        &path,
        r#"[{"rule":"cc-luhn","action":"deny","confidence":0.99,"validator":"luhn_ok"},{"rule":"fabricated-rule","action":"deny","confidence":1.0}]"#,
    );

    let after = read_all_entries(&path).expect("tampered log still parses");
    assert_eq!(after[0].violations.len(), 2, "a violation was injected");
    assert_eq!(after[0].violations[1].rule, "fabricated-rule");

    // RECORDED: the chain still verifies.
    assert!(
        verify_chain(&after).is_ok(),
        "CURRENT BEHAVIOUR: fabricated violations are outside the chain digest."
    );
}

/// CONTROL — establishes that the tampering harness and the chain check are
/// both working: mutating a field that *is* covered does break verification.
///
/// This is what makes the three assertions above meaningful rather than
/// vacuous.
#[test]
fn t_0a_control_covered_field_mutation_breaks_chain() {
    let dir = tempfile::tempdir().expect("tempdir");
    let entries = two_linked_entries();
    let path = write_log(dir.path(), &entries);

    let raw = std::fs::read_to_string(&path).expect("readable");
    let tampered = raw.replacen(r#""decision":"DENY""#, r#""decision":"ALLOW""#, 1);
    assert_ne!(raw, tampered, "control mutation applied");
    std::fs::write(&path, tampered).expect("writable");

    let after = read_all_entries(&path).expect("parses");
    assert!(
        verify_chain(&after).is_err(),
        "CONTROL: `decision` is one of the nine digested fields, so mutating \
         it must break the chain. If this passes, the harness is broken and \
         the other assertions in this file prove nothing."
    );
}

// ---------------------------------------------------------------------------
// T-0b — segment verification is unaffected by mutation of `violations`
// ---------------------------------------------------------------------------

/// CURRENT BEHAVIOUR: a segment manifest built over entries still verifies
/// after the `violations` of a covered entry are rewritten, because Merkle
/// leaves are derived from `chain_hash` alone.
///
/// NOT A NORMATIVE REQUIREMENT.
#[test]
fn t_0b_segment_manifest_verifies_after_violations_mutated() {
    let entries = two_linked_entries();

    let manifest = build_manifest(1, &entries, None, FIXED_TIMESTAMP).expect("manifest builds");

    // Precondition: the manifest verifies against the untampered entries.
    assert!(
        verify_manifest_against_entries(&manifest, &entries).is_ok(),
        "precondition: untampered entries must verify against their manifest"
    );

    // Apply the same class of mutation, in memory this time.
    let mut tampered = entries.clone();
    tampered[0].violations = vec![];

    // RECORDED: the manifest still verifies. The Merkle root, the segment
    // chain hash and any RFC 3161 imprint derived from them are unchanged.
    assert!(
        verify_manifest_against_entries(&manifest, &tampered).is_ok(),
        "CURRENT BEHAVIOUR: Merkle leaves are built from chain_hash only \
         (src/segment.rs:141-147), so violations are outside segment coverage."
    );
}

/// CONTROL — mutating a covered field changes `chain_hash`, which changes the
/// Merkle leaf, which breaks manifest verification.
#[test]
fn t_0b_control_covered_field_mutation_breaks_manifest() {
    let entries = two_linked_entries();
    let manifest = build_manifest(1, &entries, None, FIXED_TIMESTAMP).expect("manifest builds");

    let mut tampered = entries.clone();
    tampered[0].chain_hash = compute_chain_hash(
        &tampered[0].prev_hash,
        "ALLOW", // covered field changed
        &tampered[0].policy_set,
        &tampered[0].policy_hash,
        &tampered[0].context,
        &tampered[0].input_hash,
        &tampered[0].shadow_hash,
        tampered[0].seq,
        &tampered[0].timestamp,
    );

    assert!(
        verify_manifest_against_entries(&manifest, &tampered).is_err(),
        "CONTROL: a changed chain_hash must change the Merkle leaf and break \
         manifest verification."
    );
}

// ---------------------------------------------------------------------------
// T-0c — known-answer vector for the current digest preimage
// ---------------------------------------------------------------------------

/// CURRENT BEHAVIOUR: `compute_chain_hash` digests exactly nine fields joined
/// by `|`. This pins the digest produced by the current implementation for a
/// fixed input.
///
/// # NOT A NORMATIVE REQUIREMENT
///
/// The constant below is **the value the code produces today**. It is not an
/// approved, specified, or required value. No normative material defines a
/// digest input for this record type. If an authorized decision (D1, D3, D5 in
/// the GUARD-G1 brief) changes the digest, this test is expected to fail and
/// the constant is expected to be replaced — deliberately, as part of that
/// change, never as incidental maintenance.
#[test]
fn t_0c_known_answer_vector_for_current_nine_field_digest() {
    // Value produced by the current implementation for the fixture inputs.
    // CURRENT BEHAVIOUR, not a specified constant.
    const CURRENT_DIGEST: &str = "17a13da4f21d5737c9459c2832e8ff1a823f75598b550797eb4ea159052ff49e";

    let actual = compute_chain_hash(
        &genesis_hash(),
        "DENY",
        "finance-v1",
        POLICY_HASH,
        "Finance Bot",
        INPUT_HASH,
        SHADOW_HASH,
        0,
        FIXED_TIMESTAMP,
    );

    assert_eq!(
        actual, CURRENT_DIGEST,
        "CURRENT BEHAVIOUR: the nine-field digest changed. If this was \
         intentional, the digest input was redefined — record the authorizing \
         decision and update this constant deliberately. If it was not \
         intentional, the digest input changed by accident."
    );
}

/// CURRENT BEHAVIOUR: the digest is invariant under any change to
/// `violations`, because the function has no access to the field.
///
/// This is the structural counterpart to `t_0c_known_answer_vector...`: it
/// records *why* the T-0a and T-0b results hold, rather than just that they do.
///
/// NOT A NORMATIVE REQUIREMENT.
#[test]
fn t_0c_digest_is_independent_of_violations_by_construction() {
    let with_violation = entry_with(0, &genesis_hash(), vec![substantive_violation()]);
    let without_violation = entry_with(0, &genesis_hash(), vec![]);
    let with_many = entry_with(
        0,
        &genesis_hash(),
        vec![substantive_violation(), substantive_violation()],
    );

    // RECORDED: three entries differing only in `violations` share one digest.
    assert_eq!(
        with_violation.chain_hash, without_violation.chain_hash,
        "CURRENT BEHAVIOUR: violations do not enter the digest."
    );
    assert_eq!(
        with_violation.chain_hash, with_many.chain_hash,
        "CURRENT BEHAVIOUR: violation count does not enter the digest."
    );
}
