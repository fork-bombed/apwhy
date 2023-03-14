import argparse
import apwhy.console.cli as console
from apwhy.recon import enumerator
from apwhy.api import Api


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="apwhy", description="API enumeration and pentesting tool"
    )
    parser.add_argument("url", help="target URL")
    parser.add_argument(
        "-w", "--wordlist", required=True, help="wordlist to enumerate API endpoints"
    )
    parser.add_argument("-l", "--limit", type=int, default=50, help="parallel request limit (default 50)")
    parser.add_argument("--hc", "--hidecodes", type=list, help="response codes to hide")
    parser.add_argument("--sc", "--showcodes", type=list, help="response codes to show")
    return parser.parse_args()


def run():
    args = parse_arguments()
    console.display_splash_screen()
    api = Api(args.url)
    console.output(f"Target: {api.get_url()}")
    try:
        enumerator.run(api, args.wordlist, args.limit)
    except KeyboardInterrupt:
        console.warn("Enumeration stopped")


if __name__ == "__main__":
    try:
        run()
        console.info("Execution finished")
    except KeyboardInterrupt:
        console.error("Quitting...")
