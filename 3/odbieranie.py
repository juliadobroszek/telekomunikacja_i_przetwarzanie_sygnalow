import socket
import pickle
import os
import sys
from collections import defaultdict


class HuffmanDecoder:
    def __init__(self, reverse_mapping):
        self.reverse_mapping = reverse_mapping

    def remove_padding(self, padded_encoded_text):
        padded_info = padded_encoded_text[:8]
        extra_padding = int(padded_info, 2)
        return padded_encoded_text[8:-extra_padding] if extra_padding > 0 else padded_encoded_text[8:]

    def decode_text(self, encoded_text):
        current_code = ""
        decoded_text = ""
        for bit in encoded_text:
            current_code += bit
            if current_code in self.reverse_mapping:
                decoded_text += self.reverse_mapping[current_code]
                current_code = ""
        return decoded_text

    def decompress(self, compressed_data):
        bit_string = "".join(f"{byte:08b}" for byte in compressed_data)
        encoded_text = self.remove_padding(bit_string)
        return self.decode_text(encoded_text)


def get_program_directory():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


def receive_file(host='localhost', port=12345):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((host, port))
            s.listen(1)
            print(f"\nNasłuchiwanie na {host}:{port}... (Naciśnij Ctrl+C aby przerwać)")

            conn, addr = s.accept()
            with conn:
                print(f"Połączenie zaakceptowane od {addr}")

                data = b""
                while True:
                    chunk = conn.recv(4096)
                    if not chunk:
                        break
                    data += chunk

                if not data:
                    print("Błąd: Nie otrzymano żadnych danych!")
                    return

                try:
                    received_data = pickle.loads(data)
                except pickle.UnpicklingError:
                    print("Błąd: Nieprawidłowy format danych!")
                    return

                required_keys = {'compressed_data', 'encoding_map', 'original_filename', 'frequency_stats'}
                if not all(key in received_data for key in required_keys):
                    print("Błąd: Brak wymaganych danych w pakiecie!")
                    return

                compressed_data = received_data['compressed_data']
                encoding_map = received_data['encoding_map']
                original_filename = received_data['original_filename']
                frequency_stats = received_data['frequency_stats']

                safe_filename = "".join(c for c in original_filename if c.isalnum() or c in (' ', '.', '_', '-'))
                base, ext = os.path.splitext(safe_filename)
                output_filename = f"{base}_decompressed{ext}"

                output_path = os.path.join(get_program_directory(), output_filename)

                counter = 1
                while os.path.exists(output_path):
                    output_path = os.path.join(
                        get_program_directory(),
                        f"{base}_decompressed_{counter}{ext}"
                    )
                    counter += 1

                decoder = HuffmanDecoder({v: k for k, v in encoding_map.items()})
                decompressed_text = decoder.decompress(compressed_data)

                try:
                    with open(output_path, 'w', encoding='utf-8') as file:
                        file.write(decompressed_text)
                    # print(f"\nPlik został pomyślnie zapisany jako:\n{output_path}")

                    original_size = len(compressed_data)
                    decompressed_size = len(decompressed_text.encode('utf-8'))
                    ratio = (original_size / decompressed_size) * 100

                    print("{:<10} {:<15} {}".format("Znak", "Częstotliwość", "Kod Huffmana"))
                    print("-" * 35)

                    for char, (freq, code) in sorted(frequency_stats.items(), key=lambda x: x[1][0], reverse=True):
                        char_display = f"'{char}'" if char.isprintable() and char != ' ' else repr(char)
                        print("{:<10} {:<15} {}".format(
                            char_display,
                            freq,
                            code
                        ))

                    # print("\nSłownik kodowy Huffmana:")
                    # for char, code in sorted(encoding_map.items(), key=lambda x: len(x[1])):
                    #     char_repr = repr(char)[1:-1] if not char.isprintable() else char
                    #     print(f"'{char_repr}': {code}")

                except PermissionError:
                    print(f"Błąd: Brak uprawnień do zapisu w folderze programu!")
                    print(f"Folder programu: {get_program_directory()}")
                except Exception as e:
                    print(f"Błąd podczas zapisywania pliku: {e}")

    except KeyboardInterrupt:
        print("\nPrzerwano nasłuchiwanie.")
    except socket.error as e:
        print(f"Błąd gniazda: {e}")
    except Exception as e:
        print(f"Krytyczny błąd: {e}")


if __name__ == "__main__":
    print("=== Odbiornik plików Huffmana ===")
    print(f"Pliki będą zapisywane w: {get_program_directory()}\n")

    host = input("Podaj adres IP do nasłuchiwania (domyślnie localhost): ") or "localhost"
    port = input("Podaj port (domyślnie 12345): ") or 12345

    try:
        port = int(port)
        receive_file(host, port)
    except ValueError:
        print("Błąd: Port musi być liczbą!")
    except Exception as e:
        print(f"Błąd inicjalizacji: {e}")

    input("\nNaciśnij Enter aby zakończyć...")