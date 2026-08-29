#!/usr/bin/env python3
"""Search and compose prompts from the MJ Muse style catalog."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


CATALOG_PATH = Path(__file__).resolve().parent.parent / "references" / "style-catalog.json"
MODE_DEFAULTS = {
    "faithful": {"stylize": 140, "chaos": 0, "raw": True},
    "balanced": {"stylize": 300, "chaos": 0, "raw": False},
    "exploratory": {"stylize": 300, "chaos": 25, "raw": False},
}


def load_catalog() -> dict[str, Any]:
    with CATALOG_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def style_lookup(catalog: dict[str, Any], style_id: str) -> dict[str, Any]:
    needle = style_id.strip().lower()
    for style in catalog["styles"]:
        aliases = [str(value).lower() for value in style.get("aliases", [])]
        if style["id"].lower() == needle or needle in aliases:
            return style
    raise SystemExit(f"Unknown style: {style_id}")


def strip_controlled_flags(prompt: str) -> str:
    prompt = re.sub(
        r"\s+--(?:v|version|niji|ar|aspect|stylize|s|chaos|c|quality|q|weird|w|sref|sw|iw)\s+\S+",
        "",
        prompt,
        flags=re.IGNORECASE,
    )
    prompt = re.sub(r"\s+--style\s+raw\b|\s+--raw\b", "", prompt, flags=re.IGNORECASE)
    return prompt.strip()


def compose_prompt(subject: str, style: dict[str, Any]) -> str:
    clean_subject = strip_controlled_flags(subject)
    template = str(style.get("promptTemplate", "")).strip()
    if "{subject}" in template:
        prefix = template.split("{subject}", 1)[0]
        replacement = clean_subject
        if re.search(r"\b(?:a|an)(?:\s+[\w-]+){0,6}\s+$", prefix, flags=re.IGNORECASE):
            replacement = re.sub(r"^(?:a|an)\s+", "", replacement, flags=re.IGNORECASE)
        return template.replace("{subject}", replacement)
    return ", ".join(value for value in (clean_subject, template) if value)


def resolved_parameters(style: dict[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    mode = args.mode or style.get("creativityMode") or "balanced"
    params = dict(MODE_DEFAULTS[mode])
    params.update({key: value for key, value in style.get("parameters", {}).items() if value is not None})
    params["version"] = args.version or style.get("recommendedVersion") or "v8.2"
    overrides = {
        "aspectRatio": args.aspect_ratio,
        "stylize": args.stylize,
        "chaos": args.chaos,
        "weird": args.weird,
    }
    params.update({key: value for key, value in overrides.items() if value is not None})
    if args.raw is not None:
        params["raw"] = args.raw
    return params


def flags_for(params: dict[str, Any], negative: str | None) -> list[str]:
    flags: list[str] = []
    version = str(params.get("version", "v8.2")).lower()
    if version.startswith("niji"):
        flags.extend(["--niji", version.removeprefix("niji")])
    else:
        flags.extend(["--v", version.removeprefix("v")])
    if params.get("aspectRatio"):
        flags.extend(["--ar", str(params["aspectRatio"])])
    if params.get("stylize") is not None:
        flags.extend(["--stylize", str(round(float(params["stylize"])))])
    if params.get("chaos") is not None:
        flags.extend(["--chaos", str(round(float(params["chaos"])))])
    if params.get("weird"):
        flags.extend(["--weird", str(round(float(params["weird"])))])
    if params.get("raw"):
        flags.extend(["--style", "raw"])
    if negative:
        flags.extend(["--no", negative])
    return flags


def cmd_list(args: argparse.Namespace, catalog: dict[str, Any]) -> None:
    for style in catalog["styles"]:
        if args.category and style["category"] != args.category:
            continue
        if args.calibration and style["calibration"] != args.calibration:
            continue
        print(f"{style['id']}\t{style['name']}\t{style['category']}\t{style['calibration']}")


def cmd_search(args: argparse.Namespace, catalog: dict[str, Any]) -> None:
    terms = [term.lower() for term in re.split(r"\s+", args.query.strip()) if term]
    scored: list[tuple[int, dict[str, Any]]] = []
    for style in catalog["styles"]:
        text = " ".join(
            str(style.get(key, ""))
            for key in ("id", "name", "nameEn", "category", "visualDNA", "cameraLanguage", "promptTemplate")
        ).lower()
        score = sum(3 if term in style["id"].lower() or term in style["name"].lower() else 1 for term in terms if term in text)
        if score:
            scored.append((score, style))
    for score, style in sorted(scored, key=lambda pair: (-pair[0], pair[1]["id"]))[: args.limit]:
        print(f"{style['id']}\t{style['name']}\tscore={score}\t{style.get('visualDNA', '')}")


def cmd_show(args: argparse.Namespace, catalog: dict[str, Any]) -> None:
    print(json.dumps(style_lookup(catalog, args.style_id), ensure_ascii=False, indent=2))


def cmd_compose(args: argparse.Namespace, catalog: dict[str, Any]) -> None:
    style = style_lookup(catalog, args.style_id)
    prompt = compose_prompt(args.subject, style)
    params = resolved_parameters(style, args)
    negative = style.get("negativePrompt")
    command = " ".join([prompt, *flags_for(params, negative)])
    result = {
        "style": {"id": style["id"], "name": style["name"], "calibration": style["calibration"]},
        "prompt": prompt,
        "parameters": params,
        "negativePrompt": negative,
        "command": command,
    }
    if args.format == "command":
        print(command)
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list", help="List style presets")
    list_parser.add_argument("--category")
    list_parser.add_argument("--calibration", choices=("production-calibrated", "director-calibrated"))

    search_parser = subparsers.add_parser("search", help="Search style presets")
    search_parser.add_argument("query")
    search_parser.add_argument("--limit", type=int, default=8)

    show_parser = subparsers.add_parser("show", help="Show one style preset")
    show_parser.add_argument("style_id")

    compose_parser = subparsers.add_parser("compose", help="Compose a prompt from a style")
    compose_parser.add_argument("style_id")
    compose_parser.add_argument("subject")
    compose_parser.add_argument("--mode", choices=tuple(MODE_DEFAULTS))
    compose_parser.add_argument("--version")
    compose_parser.add_argument("--aspect-ratio")
    compose_parser.add_argument("--stylize", type=float)
    compose_parser.add_argument("--chaos", type=float)
    compose_parser.add_argument("--weird", type=float)
    raw_group = compose_parser.add_mutually_exclusive_group()
    raw_group.add_argument("--raw", dest="raw", action="store_true")
    raw_group.add_argument("--no-raw", dest="raw", action="store_false")
    compose_parser.set_defaults(raw=None)
    compose_parser.add_argument("--format", choices=("json", "command"), default="json")

    return parser


def main() -> None:
    args = build_parser().parse_args()
    catalog = load_catalog()
    {
        "list": cmd_list,
        "search": cmd_search,
        "show": cmd_show,
        "compose": cmd_compose,
    }[args.command](args, catalog)


if __name__ == "__main__":
    main()
