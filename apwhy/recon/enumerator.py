from apwhy.api import Endpoint, Api
import apwhy.console.cli as console


class Wordlist:
    def __init__(self, path: str):
        self.path = path
        self.size = 0
        self.words = []
        self._process_wordlist()

    def _read_file_chunk(self, file, chunk_size: int = 65536) -> int:
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            yield chunk

    def _process_wordlist(self) -> None:
        self.size = 0
        self.words = []
        try:
            with open(self.path, "r", encoding="utf-8", errors="ignore") as f:
                for chunk in self._read_file_chunk(f):
                    chunk_words = chunk.split("\n")
                    self.words += chunk_words
                    self.size += len(chunk_words)
        except FileNotFoundError:
            console.error(f"Wordlist '{self.path}' not found")

    def get_size(self) -> int:
        return self.size

    def get_words(self) -> list[str]:
        return self.words


def run(api: Api, wordlist_path: str, threads: int) -> None:
    wordlist = Wordlist(wordlist_path)
    console.output(f"Fuzzing {wordlist.get_size()} endpoint(s)")
    words = wordlist.get_words()
    for word in words:
        endpoint = Endpoint(api, word)
        response = endpoint.probe()
        output_columns = [endpoint.get_url(), response.status_code]
        output_text = "".join(column.ljust(50) for column in map(str, output_columns))
        if response.status_code == 404:
            console.output_bad(output_text)
            continue
        console.output_good(output_text)
    console.output("Fuzz complete")
