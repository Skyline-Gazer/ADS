"""Contract tests for v0.8.1 Refine, Don't Reinvent (#143): dual-entry adoption,
standalone provenance, execution-liveness guidance, optional third-party Skills
advisory, archive-sole-custody recoverability, and reachability-first pin wording."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


class V081AdoptionEntryTests(unittest.TestCase):
    def test_agent_adoption_offers_both_entries(self):
        doc = read("docs/agent-adoption.md")
        self.assertIn("choose **one** entry intentionally", doc)
        self.assertIn("**Standalone:**", doc)
        self.assertIn("**Pinned:**", doc)
        # The old mandatory-submodule step must not return.
        self.assertNotIn("2. Add ADS as a pinned Git submodule", doc)

    def test_standalone_records_adopted_revision(self):
        template = read("templates/AGENTS.md")
        self.assertIn("adopted revision", template)
        self.assertIn("full ADS commit SHA", template)
        update = read("docs/how-to-update.md")
        self.assertIn("adopted ADS release tag and full source commit SHA", update)

    def test_install_example_is_current(self):
        update = read("docs/how-to-update.md")
        self.assertIn("git -C .ads checkout v0.8.0", update)
        self.assertNotIn("git -C .ads checkout v0.7.0", update)


class V081ExecutionLivenessTests(unittest.TestCase):
    def test_pinned_entry_has_resilience_rule(self):
        doc = read("STANDARD.md").lower()
        self.assertIn("already-authorized native recovery", doc)
        self.assertIn("finished is not succeeded", doc)
        self.assertIn("never widens authorization", doc)

    def test_standalone_entry_carries_same_guidance(self):
        template = read("templates/AGENTS.md").lower()
        self.assertIn("execution liveness is host-first", template)
        self.assertIn("finished is not succeeded", template)
        # No invented scheduler: the rule forbids compensating infrastructure.
        self.assertIn("never invent a scheduler or router", template)


class V081SkillsAdvisoryTests(unittest.TestCase):
    def test_third_party_skills_section_is_advisory_only(self):
        doc = read("docs/agent-adoption.md")
        self.assertIn("## Optional third-party Skills (advisory, never required)", doc)
        self.assertIn("Agent Skills specification", doc)
        self.assertIn("skills-lock.json", doc)
        self.assertIn("DISABLE_TELEMETRY=1", doc)
        lowered = doc.lower()
        self.assertIn("passive interop, not native support", lowered)
        self.assertNotIn("you must install", lowered)
        self.assertNotIn("mandatory skill", lowered)

    def test_five_level_evidence_ladder(self):
        doc = read("docs/agent-adoption.md").lower()
        for level in (
            "installation",
            "host discovery",
            "explicit read",
            "recommendation applied",
            "behavioral adoption",
        ):
            self.assertIn(level, doc)

    def test_effective_external_reference_guidance(self):
        doc = read("docs/agent-adoption.md")
        self.assertIn("Effective external references", doc)
        self.assertIn("does not pin its external rule references", doc)

    def test_ads_owned_skills_standalone_boundary(self):
        doc = read("docs/agent-adoption.md")
        self.assertIn("do not claim standalone installation of ADS's own Skills", doc)

    def test_no_ads_proprietary_lockfile_or_registry(self):
        doc = read("docs/agent-adoption.md")
        self.assertIn(
            "ADS adds **no** loading protocol, registry, lockfile schema or router of its own", doc
        )


class V081WorkspaceAndPinTests(unittest.TestCase):
    def test_archive_sole_custody_recoverability(self):
        doc = read("docs/git-governance.md").lower()
        self.assertIn("sole custody", doc)
        self.assertIn("disaster recovery", doc)
        self.assertIn("retain when recoverability is unproven", doc)

    def test_reachability_first_pin_validation(self):
        doc = read("docs/how-to-update.md").lower()
        self.assertIn("pinned commit's **reachability**".lower(), doc)
        self.assertIn("never bootstrap or validation preconditions", doc)


if __name__ == "__main__":
    unittest.main()
