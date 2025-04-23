#Julia Dobroszek Malwina Wodnicke
import sys
import fun


def wykonaj_kodowanie():
    nazwa_pliku_k = input("Podaj nazwę pliku z wiadomością: ")
    try:
        with open(f"{nazwa_pliku_k}.txt", "r", encoding="utf-8") as file:
            wiadomosc = file.read().strip()

        if not wiadomosc:
            print("Błąd: Plik jest pusty!")
            return

        dane_zakodowane = fun.kodowanie(wiadomosc)

        with open("dane_zakodowane.txt", "w", encoding="utf-8") as file:
            for linia in dane_zakodowane:
                file.write("".join(map(str, linia)) + "\n")

        print("Sukces: Wiadomość zakodowana i zapisana do 'dane_zakodowane.txt'")

    except FileNotFoundError:
        print("Błąd: Podany plik nie istnieje!")
    except Exception as e:
        print(f"Błąd podczas kodowania: {str(e)}")


def wykonaj_odkodowanie():
    nazwa_pliku_o = input("Podaj nazwę pliku z zakodowaną wiadomością: ")
    try:
        with open(f"{nazwa_pliku_o}.txt", "r", encoding="utf-8") as file:
            dane_zakodowane = [list(map(int, linia.strip())) for linia in file if linia.strip()]

        if not dane_zakodowane:
            print("Błąd: Plik jest pusty lub źle sformatowany!")
            return

        dane_odkodowane = fun.sprawdz_poprawnosc(dane_zakodowane)
        tekst = fun.dekodowanie(dane_odkodowane)

        if not tekst.strip():
            print("Ostrzeżenie: Odkodowana wiadomość jest pusta!")

        with open("dane_odkodowane.txt", "w", encoding="utf-8") as file:
            file.write(tekst)

        print("Sukces: Wiadomość odkodowana i zapisana do 'dane_odkodowane.txt'")

    except FileNotFoundError:
        print("Błąd: Podany plik nie istnieje!")
    except ValueError:
        print("Błąd: Plik zawiera niepoprawne dane (tylko 0 i 1 są dozwolone)!")
    except Exception as e:
        print(f"Błąd podczas odkodowywania: {str(e)}")


def main():
    while True:
        print("\n===== MENU =====\n"
              "1. Kodowanie wiadomości\n"
              "2. Odkodowanie i wykrywanie błędów\n"
              "3. Zakończ program")

        wybor = input("Twój wybór: ").strip()

        if wybor == "1":
            wykonaj_kodowanie()
        elif wybor == "2":
            wykonaj_odkodowanie()
        elif wybor == "3":
            print("Zamykanie programu...")
            sys.exit()
        else:
            print("Niepoprawny wybór. Spróbuj ponownie.")


if __name__ == "__main__":
    main()