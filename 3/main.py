import os
import socket
import pickle
from wysylanie import HuffmanEncoder, send_file
from odbieranie import HuffmanDecoder, receive_file


def display_menu():
    print("\n=== Program Kodowania Huffmana ===")
    print("1. Wyślij plik (kodowanie i wysyłka)")
    print("2. Odbierz plik (odbiór i dekodowanie)")
    print("3. Wyjście")
    choice = input("Wybierz opcję (1-3): ")
    return choice


def sender_menu():
    print("\n=== Tryb wysyłania ===")
    filename = input("Podaj nazwę pliku do wysłania: ")
    if not os.path.exists(filename):
        print("Błąd: Plik nie istnieje!")
        return

    host = input("Podaj adres IP odbiorcy (domyślnie localhost): ") or "localhost"
    port = input("Podaj port (domyślnie 12345): ") or 12345

    try:
        port = int(port)
        send_file(filename, host, port)
    except ValueError:
        print("Błąd: Port musi być liczbą!")
    except Exception as e:
        print(f"Błąd podczas wysyłania: {e}")


def receiver_menu():
    print("\n=== Tryb odbioru ===")
    host = input("Podaj adres IP do nasłuchiwania (domyślnie localhost): ") or "localhost"
    port = input("Podaj port (domyślnie 12345): ") or 12345

    try:
        port = int(port)
        receive_file(host, port)
    except ValueError:
        print("Błąd: Port musi być liczbą!")
    except Exception as e:
        print(f"Błąd podczas odbioru: {e}")


def main():
    while True:
        choice = display_menu()

        if choice == "1":
            sender_menu()
        elif choice == "2":
            receiver_menu()
        elif choice == "3":
            print("Zamykanie programu...")
            break
        else:
            print("Nieprawidłowy wybór, spróbuj ponownie.")


if __name__ == "__main__":
    main()