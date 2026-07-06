from __future__ import annotations

import argparse
import shutil
from datetime import datetime, timezone
from pathlib import Path

from opportunity_radar.config import get_project_root, load_profile, load_scoring_rules, load_sources
from opportunity_radar.pipeline.build_context import build_report
from opportunity_radar.pipeline.classify import classify_item
from opportunity_radar.pipeline.deduplicate import deduplicate_items
from opportunity_radar.pipeline.generate_mock_data import generate_learning_items
from opportunity_radar.pipeline.import_manual import load_manual_inputs, load_records_from_sources
from opportunity_radar.pipeline.normalize import normalize_records
from opportunity_radar.pipeline.score import score_items
from opportunity_radar.writers.html_writer import write_html_report
from opportunity_radar.writers.json_writer import write_json_report
from opportunity_radar.writers.markdown_writer import render_markdown, write_markdown_report


def generate_report(
    profile_id: str,
    use_mock: bool = False,
    input_dir: str | Path | None = None,
    project_root: Path | None = None,
) -> dict[str, Path | int]:
    root = project_root or get_project_root()
    generated_at = datetime.now(timezone.utc).replace(tzinfo=None)
    date_label = generated_at.date().isoformat()
    profile = load_profile(profile_id, root)

    if use_mock or input_dir is None:
        records = load_records_from_sources(load_sources(root), root)
    else:
        resolved_input_dir = Path(input_dir)
        if not resolved_input_dir.is_absolute():
            resolved_input_dir = root / resolved_input_dir
        records = load_manual_inputs(resolved_input_dir)

    items = normalize_records(records)
    items = [classify_item(item) for item in items]
    items.extend(generate_learning_items(profile, generated_at))
    items = deduplicate_items(items)
    scored_items = score_items(items, profile, load_scoring_rules(root), generated_at)
    report = build_report(profile, scored_items, generated_at)

    stem = f"{date_label}_{profile_id}"
    processed_path = root / "data" / "processed" / f"{stem}.json"
    report_json_path = root / "reports" / "json" / f"{stem}.json"
    markdown_en_path = root / "reports" / "markdown" / f"{stem}_en.md"
    markdown_zh_path = root / "reports" / "markdown" / f"{stem}_zh.md"
    html_en_path = root / "reports" / "html" / f"{stem}_en.html"
    html_zh_path = root / "reports" / "html" / f"{stem}_zh.html"

    write_json_report(report, processed_path)
    write_json_report(report, report_json_path)
    write_markdown_report(report, markdown_en_path, "en")
    write_markdown_report(report, markdown_zh_path, "zh")

    markdown_en = render_markdown(report, "en")
    markdown_zh = render_markdown(report, "zh")
    write_html_report(markdown_en, html_en_path, report.title, "en")
    write_html_report(markdown_zh, html_zh_path, report.title, "zh")

    return {
        "processed": processed_path,
        "report_json": report_json_path,
        "markdown_en": markdown_en_path,
        "markdown_zh": markdown_zh_path,
        "html_en": html_en_path,
        "html_zh": html_zh_path,
        "top_opportunities": len(report.top_opportunities),
    }


def copy_sample_artifacts(outputs: dict[str, Path | int], project_root: Path | None = None) -> None:
    root = project_root or get_project_root()
    sample_reports = root / "examples" / "sample_reports"
    sample_outputs = root / "examples" / "sample_outputs"
    sample_reports.mkdir(parents=True, exist_ok=True)
    sample_outputs.mkdir(parents=True, exist_ok=True)

    shutil.copyfile(outputs["markdown_en"], sample_reports / "weekly_opportunity_radar_en.md")
    shutil.copyfile(outputs["markdown_zh"], sample_reports / "weekly_opportunity_radar_zh.md")
    shutil.copyfile(outputs["processed"], sample_outputs / "weekly_opportunity_radar.json")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Opportunity Radar CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    generate = subparsers.add_parser("generate", help="Generate opportunity intelligence report")
    generate.add_argument("--profile", default="singapore_ai_fintech")
    generate.add_argument("--mock", action="store_true", help="Use bundled synthetic sample inputs")
    generate.add_argument("--input-dir", help="Manual input directory containing CSV/YAML files")
    generate.add_argument(
        "--copy-samples",
        action="store_true",
        help="Copy generated outputs into examples/sample_reports and examples/sample_outputs",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "generate":
        outputs = generate_report(
            profile_id=args.profile,
            use_mock=args.mock,
            input_dir=args.input_dir,
        )
        if args.copy_samples:
            copy_sample_artifacts(outputs)
        for key in ["processed", "markdown_en", "markdown_zh", "html_en", "html_zh"]:
            print(f"{key}: {outputs[key]}")
        print(f"top_opportunities: {outputs['top_opportunities']}")
        return 0

    parser.error(f"Unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
