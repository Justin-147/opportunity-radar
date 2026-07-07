from pathlib import Path

from opportunity_radar.pipeline.validate_inputs import validate_input_dir

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_validate_sample_inputs_has_no_errors():
    issues = validate_input_dir(PROJECT_ROOT / "examples" / "sample_inputs")

    assert not [issue for issue in issues if issue.level == "error"]


def test_validate_missing_title_fails(tmp_path):
    input_dir = tmp_path / "inputs"
    input_dir.mkdir()
    (input_dir / "bad.csv").write_text(
        "title,url,published_at,category\n,https://example.org,2026-07-01,job\n",
        encoding="utf-8",
    )

    issues = validate_input_dir(input_dir)

    assert any(issue.level == "error" and issue.field == "title" for issue in issues)


def test_validate_rejects_invalid_url_and_category(tmp_path):
    input_dir = tmp_path / "inputs"
    input_dir.mkdir()
    (input_dir / "bad.yaml").write_text(
        """
items:
  - title: Bad item
    category: unknown
    url: javascript:alert(1)
    published_at: 2026-07-01
""".strip(),
        encoding="utf-8",
    )

    issues = validate_input_dir(input_dir)
    error_fields = {issue.field for issue in issues if issue.level == "error"}

    assert {"category", "url"}.issubset(error_fields)
