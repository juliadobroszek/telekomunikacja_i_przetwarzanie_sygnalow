import heapq
import os
import socket
import pickle
from collections import defaultdict


class HuffmanEncoder:
    def __init__(self):
        self.heap = []
        self.codes = {}
        self.reverse_mapping = {}
        self.frequency = None

    class HeapNode:
        def __init__(self, char, freq):
            self.char = char
            self.freq = freq
            self.left = None
            self.right = None

        def __lt__(self, other):
            return self.freq < other.freq

        def __eq__(self, other):
            if not isinstance(other, HeapNode):
                return False
            return self.freq == other.freq

    def make_frequency_dict(self, text):
        self.frequency = defaultdict(int)
        for character in text:
            self.frequency[character] += 1
        return self.frequency

    def get_frequency_stats(self):
        return {char: (freq, self.codes.get(char, '')) for char, freq in self.frequency.items()}

    def make_heap(self, frequency):
        for key in frequency:
            node = self.HeapNode(key, frequency[key])
            heapq.heappush(self.heap, node)

    def merge_nodes(self):
        while len(self.heap) > 1:
            node1 = heapq.heappop(self.heap)
            node2 = heapq.heappop(self.heap)

            merged = self.HeapNode(None, node1.freq + node2.freq)
            merged.left = node1
            merged.right = node2

            heapq.heappush(self.heap, merged)

    def make_codes_helper(self, root, current_code):
        if root is None:
            return

        if root.char is not None:
            self.codes[root.char] = current_code
            self.reverse_mapping[current_code] = root.char
            return

        self.make_codes_helper(root.left, current_code + "0")
        self.make_codes_helper(root.right, current_code + "1")

    def make_codes(self):
        root = heapq.heappop(self.heap)
        current_code = ""
        self.make_codes_helper(root, current_code)

    def get_encoded_text(self, text):
        encoded_text = ""
        for character in text:
            encoded_text += self.codes[character]
        return encoded_text

    def pad_encoded_text(self, encoded_text):
        extra_padding = 8 - len(encoded_text) % 8
        for i in range(extra_padding):
            encoded_text += "0"

        padded_info = "{0:08b}".format(extra_padding)
        encoded_text = padded_info + encoded_text
        return encoded_text

    def get_byte_array(self, padded_encoded_text):
        if len(padded_encoded_text) % 8 != 0:
            print("Encoded text not padded properly")
            exit(0)

        b = bytearray()
        for i in range(0, len(padded_encoded_text), 8):
            byte = padded_encoded_text[i:i + 8]
            b.append(int(byte, 2))
        return b

    def compress(self, text):
        frequency = self.make_frequency_dict(text)
        self.make_heap(frequency)
        self.merge_nodes()
        self.make_codes()

        encoded_text = self.get_encoded_text(text)
        padded_encoded_text = self.pad_encoded_text(encoded_text)

        byte_array = self.get_byte_array(padded_encoded_text)
        return byte_array

    def get_encoding_map(self):
        return self.codes


def send_file(filename, host='localhost', port=12345):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            text = file.read()

        if not text:
            print("Błąd: Plik jest pusty!")
            return

        encoder = HuffmanEncoder()
        compressed_data = encoder.compress(text)
        encoding_map = encoder.get_encoding_map()
        frequency_stats = encoder.get_frequency_stats()

        data_to_send = {
            'compressed_data': compressed_data,
            'encoding_map': encoding_map,
            'original_filename': filename,
            'frequency_stats': frequency_stats
        }

        serialized_data = pickle.dumps(data_to_send)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.sendall(serialized_data)
            print(f"Plik {filename} został pomyślnie wysłany do {host}:{port}")

    except FileNotFoundError:
        print("Błąd: Plik nie istnieje!")
    except Exception as e:
        print(f"Wystąpił błąd: {e}")