import argparse
import json
import subprocess
import sys

from surety.scaffold import extract_from_json


def _copy_to_clipboard(text: str) -> bool:
    try:
        subprocess.run(['pbcopy'], input=text.encode(), check=True)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        pass

    try:
        subprocess.run(['xclip', '-selection', 'clipboard'],
                       input=text.encode(), check=True)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        pass

    try:
        subprocess.run(['xdotool', 'type', '--clearmodifiers', '--', text],
                       check=True)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        pass

    return False


def main():
    parser = argparse.ArgumentParser(
        prog='surety-scaffold',
        description='Generate surety Dictionary classes from a JSON payload.',
    )
    parser.add_argument(
        'json',
        nargs='?',
        help='JSON string to extract from. Reads from stdin if omitted.',
    )
    parser.add_argument(
        '--class-name', '-c',
        default='Schema',
        help='Name for the top-level generated class (default: Schema).',
    )
    parser.add_argument(
        '--no-clipboard',
        action='store_true',
        help='Do not copy the result to the clipboard.',
    )
    args = parser.parse_args()

    raw = args.json if args.json else sys.stdin.read()

    try:
        json.loads(raw)
    except json.JSONDecodeError as e:
        print(f'Error: invalid JSON — {e}', file=sys.stderr)
        sys.exit(1)

    result = extract_from_json(raw, class_name=args.class_name)

    print(result)

    if not args.no_clipboard:
        if _copy_to_clipboard(result):
            print('\n# Copied to clipboard.', file=sys.stderr)
        else:
            print('\n# Could not copy to clipboard (no pbcopy/xclip found).',
                  file=sys.stderr)
