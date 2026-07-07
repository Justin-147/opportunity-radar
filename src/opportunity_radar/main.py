from __future__ import annotations

import argparse
import shutil
from datetime import UTC, datetime
from pathlib import Path
from typing import cast

from opportunity_radar.config import (
    get_project_root,
    load_profile,
    load_scoring_rules,
    load_sources,
)
from opportunity_radar.pipeline.build_context import build_report
from opportunity_radar.pipeline.classify import classify_item
from opportunity_radar.pipeline.deduplicate import deduplicate_items
from opportunity_radar.pipeline.generate_mock_data import generate_learning_items
from opportunity_radar.pipeline.import_manual import load_manual_inputs, load_records_from_sources
from opportunity_radar.pipeline.normalize import normalize_records
from opportunity_radar.pipeline.score import score_items
from opportunity_radar.pipeline.validate_inputs import ValidationIssue, validate_input_dir
from opportunity_radar.writers.html_writer import write_html_report
from opportunity_radar.writers.json_writer import write_json_report
from opportunity_radar.writers.markdown_writer import render_markdown, write_markdown_report


def _naive_utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value
    return value.astimezone(UTC).replace(tzinfo=None)


def parse_as_of(value: str | None) -> datetime | None:
    if not value:
        return None
    text = value.strip()
    normalized = text[:-1] + "+00:00" if text.endswith("Z") else text
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise ValueError(
            f"Invalid --as-of value '{value}'. Use YYYY-MM-DD or ISO datetime."
        ) from exc
    return _naive_utc(parsed)


def resolve_path_against_root(path: str | Path, root: Path) -> Path:
    resolved = Path(path)
    if not resolved.is_absolute():
        resolved = root / resolved
    return resolved


def summarize_validation(issues: list[ValidationIssue]) -> tuple[int, int]:
    errors = sum(1 for issue in issues if issue.level == "error")
    warnings = sum(1 for issue in issues if issue.level == "warning")
    return errors, warnings


def print_validation_result(issues: list[ValidationIssue]) -> None:
    errors, warnings = summarize_validation(issues)
    for issue in issues:
        print(f"{issue.level}: {issue.location} {issue.field}: {issue.message}")
    print(f"validation_errors: {errors}")
    print(f"validation_warnings: {warnings}")
    print(f"status: {'failed' if errors else 'passed'}")


def generate_report(
    profile_id: str,
    use_mock: bool = False,
    input_dir: str | Path | None = None,
    project_root: Path | None = None,
    output_root: str | Path | None = None,
    generated_at: datetime | None = None,
) -> dict[str, Path | int]:
    root = project_root or get_project_root()
    output_base = resolve_path_against_root(output_root, root) if output_root else root
    generated_at = generated_at or datetime.now(UTC).replace(tzinfo=None)
    date_label = generated_at.date().isoformat()
    profile = load_profile(profile_id, root)

    if use_mock or input_dir is None:
        records = load_records_from_sources(load_sources(root), root)
    else:
        resolved_input_dir = resolve_path_against_root(input_dir, root)
        records = load_manual_inputs(resolved_input_dir)

    items = normalize_records(records)
    items = [classify_item(item) for item in items]
    items.extend(generate_learning_items(profile, generated_at))
    items = deduplicate_items(items)
    scored_items = score_items(items, profile, load_scoring_rules(root), generated_at)
    report = build_report(profile, scored_items, generated_at)

    stem = f"{date_label}_{profile_id}"
    processed_path = output_base / "data" / "processed" / f"{stem}.json"
    report_json_path = output_base / "reports" / "json" / f"{stem}.json"
    markdown_en_path = output_base / "reports" / "markdown" / f"{stem}_en.md"
    markdown_zh_path = output_base / "reports" / "markdown" / f"{stem}_zh.md"
    html_en_path = output_base / "reports" / "html" / f"{stem}_en.html"
    html_zh_path = output_base / "reports" / "html" / f"{stem}_zh.html"

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

    shutil.copyfile(
        cast(Path, outputs["markdown_en"]),
        sample_reports / "weekly_opportunity_radar_en.md",
    )
    shutil.copyfile(
        cast(Path, outputs["markdown_zh"]),
        sample_reports / "weekly_opportunity_radar_zh.md",
    )
    shutil.copyfile(
        cast(Path, outputs["processed"]),
        sample_outputs / "weekly_opportunity_radar.json",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Opportunity Radar CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    generate = subparsers.add_parser("generate", help="Generate opportunity intelligence report")
    generate.add_argument("--profile", default="singapore_ai_fintech")
    generate.add_argument("--mock", action="store_true", help="Use bundled synthetic sample inputs")
    generate.add_argument("--input-dir", help="Manual input directory containing CSV/YAML files")
    generate.add_argument("--as-of", help="Generate as of YYYY-MM-DD or ISO datetime")
    generate.add_argument("--output-root", help="Write runtime outputs under this directory")
    generate.add_argument(
        "--strict-validation",
        action="store_true",
        help="Validate inputs before generation and fail on validation errors",
    )
    generate.add_argument(
        "--copy-samples",
        action="store_true",
        help="Copy generated outputs into examples/sample_reports and examples/sample_outputs",
    )

    validate = subparsers.add_parser("validate", help="Validate manual CSV/YAML inputs")
    validate.add_argument(
        "--input-dir", required=True, help="Input directory containing CSV/YAML files"
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "generate":
        try:
            generated_at = parse_as_of(args.as_of)
        except ValueError as exc:
            parser.error(str(exc))
            return 2

        root = get_project_root()
        if args.strict_validation:
            validation_dir = args.input_dir or root / "examples" / "sample_inputs"
            resolved_validation_dir = resolve_path_against_root(validation_dir, root)
            issues = validate_input_dir(resolved_validation_dir)
            print_validation_result(issues)
            errors, _warnings = summarize_validation(issues)
            if errors:
                return 1

        outputs = generate_report(
            profile_id=args.profile,
            use_mock=args.mock,
            input_dir=args.input_dir,
            output_root=args.output_root,
            generated_at=generated_at,
        )
        if args.copy_samples:
            copy_sample_artifacts(outputs)
        for key in ["processed", "markdown_en", "markdown_zh", "html_en", "html_zh"]:
            print(f"{key}: {outputs[key]}")
        print(f"top_opportunities: {outputs['top_opportunities']}")
        return 0

    if args.command == "validate":
        root = get_project_root()
        input_dir = resolve_path_against_root(args.input_dir, root)
        issues = validate_input_dir(input_dir)
        print_validation_result(issues)
        errors, _warnings = summarize_validation(issues)
        return 1 if errors else 0

    parser.error(f"Unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
