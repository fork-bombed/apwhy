import os
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
