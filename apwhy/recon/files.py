import apwhy.console.cli as console


class Wordlist:
    def __init__(self, path: str):
        self.path = path
        self.words = []

    def read(self) -> None:
        try:
            with open(self.path, "r", encoding="utf-8", errors="ignore") as f:
                self.words = set(f.read().split('\n'))
        except FileNotFoundError:
            console.error(f"Wordlist '{self.path}' not found")

    def get_size(self) -> int:
        return len(self.words)

    def get_words(self) -> list[str]:
        return self.words
