from __future__ import annotations
from hashlib import md5
from typing import Dict, List
import pickle


class HumanReadableIdManager:

    WORDS_FILENAME: str = "word_list.txt"
    WORDS: List[str]
    with open(WORDS_FILENAME, 'r', encoding='utf-8') as file:
        WORDS = [
            line.split("\t")[-1].strip()
            for line in file.readlines()[1:]
        ]
    WORD_AMOUNT: int = len(WORDS)
    MAX_64BIT: int = 0xffffffffffffffff
    MAX_32BIT: int = 0xffffffff
    ORIGINAL_ID_TYPE: type = str | int | bytes

    _seed: int | None
    _hash_counter: Dict[str, int]
    _original_to_human_readable: Dict[ORIGINAL_ID_TYPE, str]
    _human_readbale_to_original: Dict[str, ORIGINAL_ID_TYPE]

    @classmethod
    def load(cls, filename: str) -> HumanReadableIdManager:
        with open(filename, 'rb') as file:
            return pickle.load(file)

    def __init__(self, seed: int | None = None):
        self._seed = seed
        self._hash_counter = {}
        self._original_to_human_readable = {}
        self._human_readbale_to_original = {}

    def save(self, filename: str) -> None:
        with open(filename, 'wb') as file:
            pickle.dump(self, file)

    def _bytes_to_hash(self, value: ORIGINAL_ID_TYPE) -> bytes:
        if not isinstance(value, bytes):
            string_to_hash = f"{value}{self._seed if self._seed else ''}"
            return string_to_hash.encode('ascii')
        else:
            bytes_to_hash = value
            if self._seed:
                bytes_to_hash += str(self._seed).encode('ascii')
            return bytes_to_hash

    def _32bit_hash(self, value: ORIGINAL_ID_TYPE) -> int:
        hash_bytes = md5(self._bytes_to_hash(value)).digest()
        hash_ = int.from_bytes(hash_bytes, 'big')
        hash_ = ((hash_ & self.MAX_64BIT << 64) >> 64) ^ hash_ & self.MAX_64BIT
        hash_ = ((hash_ & self.MAX_32BIT << 32) >> 32) ^ hash_ & self.MAX_32BIT
        return hash_

    def generate_human_readable_id(self, original_id: ORIGINAL_ID_TYPE) -> str:
        if self.has_original_id(original_id):
            return self.get_human_readable_id(original_id)

        hash_ = self._32bit_hash(original_id)
        rest_hash, index1 = divmod(hash_, self.WORD_AMOUNT)
        number, index2 = divmod(rest_hash, self.WORD_AMOUNT)
        word1, word2 = self.WORDS[index1], self.WORDS[index2]
        words = f"{word1}-{word2}"

        self._hash_counter[words] = self._hash_counter.get(words, -1) + 1
        number += self._hash_counter[words]

        human_readable_id = f"{words}-{number}"
        self._original_to_human_readable[original_id] = human_readable_id
        self._human_readbale_to_original[human_readable_id] = original_id

        return human_readable_id

    def get_human_readable_id(
        self, original_id: ORIGINAL_ID_TYPE, default: str | None = None
    ) -> str | None:
        return self._original_to_human_readable.get(original_id, default)

    def get_original_id(
        self, human_readable_id: str, default: ORIGINAL_ID_TYPE | None = None
    ) -> ORIGINAL_ID_TYPE | None:
        return self._human_readbale_to_original.get(human_readable_id, default)

    def has_human_readable_id(self, human_readable_id: str) -> bool:
        return human_readable_id in self._human_readbale_to_original

    def has_original_id(self, original_id: ORIGINAL_ID_TYPE) -> bool:
        return original_id in self._original_to_human_readable

    def __len__(self) -> int:
        return len(self._original_to_human_readable)
