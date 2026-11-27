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
    "router, scheduler or runner",
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

    def test_install_example_matches_published_release(self):
        # The pinned example must name the latest PUBLISHED release, not the
        # current candidate on dev. Derive it from docs/releases/*.md so a
        # release PR is never gated on a stale hardcoded string (A01).
        versions = []
        for path in (ROOT / "docs" / "releases").glob("v*.md"):
            match = re.match(r"v(\d+)\.(\d+)\.(\d+)", path.name)
            if match and "**Status:** published" in path.read_text(encoding="utf-8"):
                versions.append((tuple(int(x) for x in match.groups()), match.group(0)))
        self.assertTrue(versions, "no published release notes found")
        published = max(versions)[1]
        update = read("docs/how-to-update.md")
        self.assertIn(f"git -C .ads checkout {published}", update)
        self.assertIn(f"`{published}` above is an example **published release**", update)


class V081ExecutionLivenessTests(unittest.TestCase):
    def test_liveness_concepts_parity_across_entries(self):
        standard = read("STANDARD.md").lower()
        template = read("templates/AGENTS.md").lower()
        for concept in LIVENESS_CONCEPTS:
            self.assertIn(concept, standard, f"pinned entry missing: {concept}")
            self.assertIn(concept, template, f"standalone entry missing: {concept}")

    def test_retry_budget_consistent_with_stop_rule(self):
        for rel in ("STANDARD.md", "templates/AGENTS.md"):
            self.assertIn("at most three unsuccessful", read(rel).lower(), rel)

    def test_no_invented_infrastructure(self):
        template = read("templates/AGENTS.md").lower()
        self.assertIn("never invent a router, scheduler or runner", template)


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
        normalized = re.sub(r"\s+", " ", doc)
        self.assertIn(
            "installation → host discovery → explicit read → recommendation applied → behavioral adoption",
            normalized,
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
        doc = read("docs/agent-adoption.md").replace("*", "")
        self.assertIn(
            "ADS adds no loading protocol, registry, lockfile schema or router of its own",
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


class V081RequirementAuthorityTests(unittest.TestCase):
    def test_standard_requirement_authority(self):
        doc = read("STANDARD.md")
        self.assertIn("does not authorize every requirement", doc)
        self.assertIn("not new Owner authorization", doc)
        self.assertIn("forwarded reports", doc)
        self.assertIn("does not approve its proposals", doc)
        self.assertIn("latest actual Owner scope decision", doc)
        self.assertIn("do not silently drop Owner-approved scope", doc)
        self.assertIn("keep genuine product, security and required-CI obligations", doc)

    def test_standalone_template_requirement_authority_parity(self):
        doc = read("templates/AGENTS.md")
        self.assertIn("format does not authorize every requirement", doc)
        self.assertIn("forwarded reports", doc)
        self.assertIn("do not silently drop Owner-approved scope", doc)
        self.assertIn("retire the rejected obligation", doc)

    def test_supervision_challenges_unsupported_work(self):
        doc = read("STANDARD.md")
        self.assertIn("derive Acceptance from the authorized objective", doc)
        self.assertIn("challenge unsupported or disproportionate work", doc)
        self.assertIn("rather than returning to the Owner as a scheduler", doc)


class V081AcceptanceIntegrityTests(unittest.TestCase):
    def test_quality_matches_acceptance_to_execution_path(self):
        doc = read("QUALITY.md")
        self.assertIn("match the claimed acceptance scope to the execution path", doc)
        self.assertIn("substituted adapter/test double proves only that scope", doc)
        self.assertIn("never perform an unapproved live mutation solely to obtain evidence", doc)

    def test_quality_partial_external_effects(self):
        doc = read("QUALITY.md")
        self.assertIn("failed composite operation may already have changed external state", doc)
        self.assertIn("completed-step list", doc)
        self.assertIn("reconcile material side effects before retrying", doc)

    def test_template_carries_acceptance_scope_and_partial_effects(self):
        doc = read("templates/AGENTS.md")
        self.assertIn("Match the tested journey to the claimed scope", doc)
        self.assertIn("possibly present until reconciled", doc)


class V081PolicyMigrationTests(unittest.TestCase):
    def test_update_guidance_distinguishes_pin_from_migration(self):
        doc = read("docs/how-to-update.md")
        self.assertIn("A pin advance is not a policy migration", doc)
        self.assertIn("retire superseded ADS-derived procedures", doc)
        self.assertIn("distinguish historical records from current obligations", doc)
        self.assertIn("A pin-only refresh with no applicable policy change needs no migration exercise", doc)

    def test_reviewed_checks_and_production_boundaries_preserved(self):
        doc = read("docs/how-to-update.md")
        self.assertIn("reviewed required-check configuration or production boundaries stay untouched", doc)


class V081CapabilitySelectionTests(unittest.TestCase):
    def test_route_chosen_by_fit_in_both_entries(self):
        for rel in ("STANDARD.md", "templates/AGENTS.md"):
            doc = read(rel)
            self.assertIn("task fit", doc, rel)
            self.assertIn("rather than host lock-in", doc, rel)

    def test_sufficient_equivalent_evidence_in_both_entries(self):
        for rel in ("STANDARD.md", "templates/AGENTS.md"):
            doc = read(rel)
            self.assertIn("sufficient equivalent independent evidence", doc, rel)
            self.assertIn("mandatory gate stays binding", doc, rel)


class V081AuthorizationProvenanceTests(unittest.TestCase):
    def test_safety_identity_is_not_authorization(self):
        doc = read("SAFETY.md")
        self.assertIn("never grant authority", doc)
        self.assertIn("does not by itself authorize an operation", doc)
        self.assertIn("comes from the actual task and its real impact", doc)
        self.assertIn("neither weakens an existing configured protection", doc)


if __name__ == "__main__":
    unittest.main()
