"""Contract tests for v0.8.1 Refine, Don't Reinvent (#143): dual-entry adoption,
standalone provenance, execution-liveness guidance, optional third-party Skills
advisory, archive-sole-custody recoverability, and reachability-first pin wording."""
import re
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


# Concepts required in BOTH adoption entries (STANDARD.md = pinned, templates/AGENTS.md
# = standalone). Plain phrases only, so Markdown emphasis may be restyled freely.
LIVENESS_CONCEPTS = (
    "finished is not succeeded",
    "never widens authorization",
    "scheduler",
    "model switch",
    "independent review",
)


class V081AdoptionEntryTests(unittest.TestCase):
    def test_agent_adoption_offers_both_entries(self):
        doc = read("docs/agent-adoption.md")
        self.assertIn("choose **one** entry intentionally", doc)
        self.assertIn("Standalone:", doc)
        self.assertIn("Pinned:", doc)
        # The old unconditional submodule step must not return.
        self.assertNotIn("2. Add ADS as a pinned Git submodule", doc)

    def test_standalone_records_adopted_revision(self):
        template = read("templates/AGENTS.md")
        self.assertIn("adopted revision", template)
        self.assertIn("full ADS commit SHA (required)", template)
        update = read("docs/how-to-update.md")
        self.assertIn("adopted ADS full source commit SHA (required)", update)
        adoption = read("docs/agent-adoption.md")
        self.assertIn("adopted ADS full source commit SHA (required)", adoption)
        # SHA-only (pilot) adoption must remain satisfiable: tag is conditional.
        for doc in (update, adoption, template):
            self.assertIn("when the copy came from a tagged release", doc)

    def test_install_example_matches_declared_release(self):
        # Derive the version from the declared release instead of hardcoding it:
        # a future release PR must not be gated on a stale example string (A01).
        declared = re.search(r"v\d+\.\d+\.\d+", read("STANDARD.md"))
        self.assertIsNotNone(declared, "STANDARD.md must declare a released version")
        update = read("docs/how-to-update.md")
        self.assertIn(f"git -C .ads checkout {declared.group(0)}", update)


class V081ExecutionLivenessTests(unittest.TestCase):
    def test_liveness_concepts_parity_across_entries(self):
        standard = read("STANDARD.md").lower()
        template = read("templates/AGENTS.md").lower()
        for concept in LIVENESS_CONCEPTS:
            self.assertIn(concept, standard, f"pinned entry missing: {concept}")
            self.assertIn(concept, template, f"standalone entry missing: {concept}")

    def test_retry_budget_consistent_with_stop_rule(self):
        standard = read("STANDARD.md").lower()
        self.assertIn("three unsuccessful related attempts", standard)

    def test_no_invented_infrastructure(self):
        template = read("templates/AGENTS.md").lower()
        self.assertIn("never invent a scheduler or router", template)


class V081SkillsAdvisoryTests(unittest.TestCase):
    def test_third_party_skills_section_is_advisory_only(self):
        doc = read("docs/agent-adoption.md")
        self.assertIn("## Optional third-party Skills (advisory, never required)", doc)
        self.assertIn("Agent Skills specification", doc)
        self.assertIn("skills-lock.json", doc)
        self.assertIn("DISABLE_TELEMETRY=1", doc)
        self.assertIn("Nothing here is mandatory", doc)
        self.assertIn("passive interop, not native support", doc.lower())
        self.assertNotIn("must install", doc.lower())

    def test_five_level_evidence_ladder_ordered(self):
        doc = read("docs/agent-adoption.md").lower()
        self.assertIn(
            "installation → host discovery → explicit read "
            "→ recommendation applied → behavioral adoption",
            doc.replace("\n", " "),
        )

    def test_effective_external_reference_guidance(self):
        doc = read("docs/agent-adoption.md")
        self.assertIn("Effective external references", doc)
        self.assertIn("does not pin its external rule references", doc)

    def test_ads_owned_skills_standalone_boundary(self):
        doc = read("docs/agent-adoption.md")
        self.assertIn("do not claim standalone installation of ADS's own Skills", doc)
        lite = read("docs/lite-adoption.md")
        self.assertIn("only if you also vendor the paths they reference", lite)

    def test_no_ads_proprietary_lockfile_or_registry(self):
        doc = read("docs/agent-adoption.md")
        self.assertIn(
            "ADS adds **no** loading protocol, registry, lockfile schema or router of its own",
            doc,
        )


class V081WorkspaceAndPinTests(unittest.TestCase):
    def test_archive_sole_custody_recoverability(self):
        doc = read("docs/git-governance.md").lower()
        self.assertIn("sole custody", doc)
        self.assertIn("disaster recovery", doc)
        self.assertIn("retain when recoverability is unproven", doc)
        # Must not invalidate the provider-retained archival-tag custody model (#133).
        self.assertIn("archival tag kept after a ref retirement", doc)

    def test_reachability_first_pin_validation(self):
        doc = read("docs/how-to-update.md").lower()
        self.assertIn("reachability", doc)
        self.assertIn("never bootstrap or validation preconditions", doc)


if __name__ == "__main__":
    unittest.main()
