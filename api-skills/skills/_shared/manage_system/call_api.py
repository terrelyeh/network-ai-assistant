#!/usr/bin/env python3
"""Manage System HTTP API caller for published skill fallback scripts."""

from __future__ import annotations

import argparse
import json
import sys

import requests

from ..common.json_args import parse_json_arg
from .client import run


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--operation-id", required=True)
    parser.add_argument("--path-params", default="{}")
    parser.add_argument("--query-params", default="{}")
    parser.add_argument("--body", default="{}")
    parser.add_argument("--headers", default="{}")
    parser.add_argument("--timeout", type=int, default=30)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    try:
        path_params = parse_json_arg(args.path_params, "--path-params", require_object=True)
        query_params = parse_json_arg(args.query_params, "--query-params", require_object=True)
        body = parse_json_arg(args.body, "--body", require_object=False)
        headers = parse_json_arg(args.headers, "--headers", require_object=True)
    except ValueError as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        raise SystemExit(1) from exc

    try:
        result = run(
            operation_id=args.operation_id,
            path_params=path_params,
            query_params=query_params,
            body=body,
            extra_headers=headers,
            timeout=args.timeout,
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except requests.HTTPError as exc:
        print(json.dumps({"error": f"HTTP {exc.response.status_code}", "detail": exc.response.text}), file=sys.stderr)
        raise SystemExit(1) from exc
    except ValueError as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
