"""Smoke tests for ml-automation-gcp — validate plugin layout invariants."""
import json
from pathlib import Path
import pytest


PLUGIN_ROOT = Path(__file__).resolve().parent.parent


class TestManifestValidity:
    """Test that plugin manifest is valid and well-formed."""

    def test_manifest_exists(self) -> None:
        """Manifest file must exist at .cortex-plugin/plugin.json."""
        manifest_path = PLUGIN_ROOT / ".cortex-plugin" / "plugin.json"
        assert manifest_path.exists(), f"Manifest not found at {manifest_path}"

    def test_manifest_parses_as_json(self) -> None:
        """Manifest must be valid JSON."""
        manifest_path = PLUGIN_ROOT / ".cortex-plugin" / "plugin.json"
        with open(manifest_path) as f:
            manifest = json.load(f)
        assert isinstance(manifest, dict), "Manifest must be a JSON object"

    def test_manifest_has_required_fields(self) -> None:
        """Manifest must include name, version, description, cortex.agents_dir."""
        manifest_path = PLUGIN_ROOT / ".cortex-plugin" / "plugin.json"
        with open(manifest_path) as f:
            manifest = json.load(f)

        required = ["name", "version", "description"]
        for field in required:
            assert field in manifest, f"Manifest missing required field: {field}"

        assert "cortex" in manifest, "Manifest missing 'cortex' section"
        cortex = manifest["cortex"]
        cortex_required = ["agents_dir", "skills_dir", "commands_dir", "hooks_dir"]
        for field in cortex_required:
            assert field in cortex, f"Manifest.cortex missing required field: {field}"


class TestAgentsAndSkillsReferentialIntegrity:
    """Test that AGENTS.md referential integrity matches agents/ and skills/ dirs."""

    def test_agents_md_exists(self) -> None:
        """AGENTS.md must exist."""
        agents_md = PLUGIN_ROOT / "AGENTS.md"
        assert agents_md.exists(), f"AGENTS.md not found at {agents_md}"

    def test_agents_dir_exists(self) -> None:
        """agents/ directory must exist."""
        agents_dir = PLUGIN_ROOT / "agents"
        assert agents_dir.is_dir(), f"agents/ directory not found at {agents_dir}"

    def test_skills_dir_exists(self) -> None:
        """skills/ directory must exist."""
        skills_dir = PLUGIN_ROOT / "skills"
        assert skills_dir.is_dir(), f"skills/ directory not found at {skills_dir}"

    def test_agents_md_agents_have_implementations(self) -> None:
        """Every agent listed in AGENTS.md must have a .md file in agents/."""
        agents_md = PLUGIN_ROOT / "AGENTS.md"
        with open(agents_md) as f:
            content = f.read()

        # Extract agent names from "Available Agents" table
        agents_dir = PLUGIN_ROOT / "agents"

        # Parse "Available Agents" section explicitly
        if "## Available Agents" in content:
            agents_section = content.split("## Available Agents")[1]
            # Find where next section starts
            if "## Available Skills" in agents_section:
                agents_section = agents_section.split("## Available Skills")[0]

            for line in agents_section.split("\n"):
                # Table rows have | at start, contain backticks, and are not separators
                if line.startswith("| `") and "|" in line and not line.startswith("|---|"):
                    # Extract agent name from | `agent-name` | description |
                    parts = line.split("`")
                    if len(parts) >= 2:
                        agent_name = parts[1].strip()
                        if agent_name:
                            agent_file = agents_dir / f"{agent_name}.md"
                            assert (
                                agent_file.exists()
                            ), f"Agent '{agent_name}' listed in AGENTS.md but missing {agent_file}"

    def test_agents_md_skills_have_implementations(self) -> None:
        """Every skill listed in AGENTS.md must have a directory in skills/."""
        agents_md = PLUGIN_ROOT / "AGENTS.md"
        with open(agents_md) as f:
            content = f.read()

        skills_dir = PLUGIN_ROOT / "skills"

        # Parse "Available Skills" section explicitly
        if "## Available Skills" in content:
            skills_section = content.split("## Available Skills")[1]
            # Find where next section starts
            if "## Routing" in skills_section:
                skills_section = skills_section.split("## Routing")[0]

            for line in skills_section.split("\n"):
                # Table rows have | at start, contain backticks with slash, not separators
                if line.startswith("| `/") and "|" in line and not line.startswith("|---|"):
                    # Extract skill name from | `/skill-name` | trigger |
                    parts = line.split("`")
                    if len(parts) >= 2:
                        skill_name = parts[1].lstrip("/").strip()
                        if skill_name:
                            skill_dir = skills_dir / skill_name
                            assert (
                                skill_dir.is_dir()
                            ), f"Skill '{skill_name}' listed in AGENTS.md but missing directory {skill_dir}"

    def test_no_orphan_agents(self) -> None:
        """Every agent .md file in agents/ must be listed in AGENTS.md."""
        agents_md = PLUGIN_ROOT / "AGENTS.md"
        with open(agents_md) as f:
            agents_content = f.read()

        agents_dir = PLUGIN_ROOT / "agents"
        for agent_file in agents_dir.glob("*.md"):
            agent_name = agent_file.stem
            assert (
                f"`{agent_name}`" in agents_content
            ), f"Agent '{agent_name}' in agents/ but not referenced in AGENTS.md"

    def test_no_orphan_skills(self) -> None:
        """Every skill directory in skills/ must be listed in AGENTS.md."""
        agents_md = PLUGIN_ROOT / "AGENTS.md"
        with open(agents_md) as f:
            agents_content = f.read()

        skills_dir = PLUGIN_ROOT / "skills"
        for skill_subdir in skills_dir.iterdir():
            if skill_subdir.is_dir():
                skill_name = skill_subdir.name
                assert (
                    f"`/{skill_name}`" in agents_content
                ), f"Skill '{skill_name}' in skills/ but not referenced in AGENTS.md"
