import sys
from termcolor import colored
from apwhy.console import splash


def get_splash_screen() -> str:
    return colored(splash.logo, "light_yellow")


def display_splash_screen() -> None:
    print(get_splash_screen() + "\n")


def output(text: str) -> None:
    print(text)


def output_good(text: str) -> None:
    plus = colored("+", "light_green")
    out = f"[{plus}] {text}"
    output(out)


def output_bad(text: str) -> None:
    cross = colored("x", "light_red")
    out = f"[{cross}] {text}"
    output(out)


def error(text: str) -> None:
    error_text = colored("ERROR", "light_red")
    output(f"[{error_text}] {text}")
    exit()


def info(text: str) -> None:
    info_text = colored("INFO", "light_blue")
    output(f"[{info_text}] {text}")


def warn(text: str) -> None:
    warn_text = colored("WARN", "light_yellow")
    output(f"[{warn_text}] {text}")


def output_row(columns: list[str | int], color=None) -> None:
    # TODO: Make this more modular lol :/
    offset1 = 8
    offset2 = 35
    offset3 = 10
    columns = list(map(str, columns))
    if color is not None:
        colored_columns = [colored(column, color=color) for column in columns]
        offset1 += len(colored_columns[0]) - len(columns[0])
        offset2 += len(colored_columns[1]) - len(columns[1])
        offset3 += len(colored_columns[2]) - len(columns[2])
        columns = colored_columns
    output(f"{{0:<{offset1}}} {{1:<{offset2}}} {{2:<{offset3}}} {{3}}".format(*columns))


def overwrite_last_line() -> None:
    sys.stdout.write("\033[F\033[K")
