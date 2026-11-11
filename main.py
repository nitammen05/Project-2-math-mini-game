"""Start Math Quest from the terminal.

Usage:
    python3 main.py                      # uses problems.txt, port 8000
    python3 main.py --port 8080 --problems my_problems.txt
"""

import argparse
import os
import sys
import webbrowser

from problems import load_problems
from web import make_server

HERE = os.path.dirname(os.path.abspath(__file__))


def parse_args(argv):
    parser = argparse.ArgumentParser(description="Math Quest: a math RPG in your browser.")
    parser.add_argument("--problems", default=os.path.join(HERE, "problems.txt"),
                        help="path to the problems file (default: problems.txt)")
    parser.add_argument("--port", type=int, default=8000, help="port to serve on (default: 8000)")
    parser.add_argument("--no-browser", action="store_true", help="don't open a browser automatically")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(sys.argv[1:] if argv is None else argv)
    try:
        problems = load_problems(args.problems)
    except (OSError, ValueError) as err:
        print(f"Could not load problems: {err}", file=sys.stderr)
        return 1
    server = make_server(problems, port=args.port)
    url = f"http://127.0.0.1:{server.server_address[1]}/"
    print(f"Math Quest is running at {url}  (press Ctrl+C to stop)")
    if not args.no_browser:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nGoodbye, hero!")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
