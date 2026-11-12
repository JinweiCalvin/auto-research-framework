import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def load_tool(name):
    path = ROOT / "tools" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class WorkflowToolsTest(unittest.TestCase):
    def test_create_project_scaffolds_and_refuses_overwrite(self):
        tool = load_tool("create_research_project")
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "study"
            tool.create(project)
            self.assertTrue((project / "RESEARCH_BRIEF.md").is_file())
            self.assertTrue((project / "experiments").is_dir())
            self.assertTrue((project / "decisions").is_dir())
            self.assertTrue((project / "literature").is_dir())
            with self.assertRaises(ValueError):
                tool.create(project)

    def test_package_snapshots_artifacts_and_manifest(self):
        tool = load_tool("package_idea2paper")
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            source = tmp_path / "output"
            source.mkdir()
            story = {"title": "Test idea", "innovation_claims": ["candidate claim"]}
            result = {"success": True, "review_history": []}
            (source / "final_story.json").write_text(json.dumps(story), encoding="utf-8")
            (source / "pipeline_result.json").write_text(json.dumps(result), encoding="utf-8")
            project = tmp_path / "project"
            project.mkdir()
            (project / "RESEARCH_BRIEF.md").write_text("# Research Brief\n", encoding="utf-8")
            tool.OUTPUT = source
            tool.I2P_ROOT = tmp_path
            packet = tool.package(project, "test prompt", "run-001")
            manifest = json.loads((packet / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["title"], "Test idea")
            self.assertEqual(len(manifest["artifacts"]["final_story.json"]["sha256"]), 64)
            self.assertTrue((packet / "ARIS_HANDOFF.md").is_file())
            with self.assertRaises(ValueError):
                tool.package(project, None, "run-001")

    def test_package_rejects_invalid_story(self):
        tool = load_tool("package_idea2paper")
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            source = tmp_path / "output"
            source.mkdir()
            (source / "final_story.json").write_text("{}", encoding="utf-8")
            (source / "pipeline_result.json").write_text("{}", encoding="utf-8")
            project = tmp_path / "project"
            project.mkdir()
            (project / "RESEARCH_BRIEF.md").write_text("# Research Brief\n", encoding="utf-8")
            tool.OUTPUT = source
            with self.assertRaises(ValueError):
                tool.package(project, None, "run-001")


if __name__ == "__main__":
    unittest.main()
