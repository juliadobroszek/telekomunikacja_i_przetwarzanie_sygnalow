import time
import fun


def odbierzWiadomosc(port):
    nazwa_pliku = input("Podaj nazwę pliku do zapisu z rozszerzeniem: ")
    czas_start = time.time()
    wybor_sumy = fun.wyborSumyKontrolnej()
    odebrane_dane = bytearray()  # Przechowujemy dane binarne
    numer_bloku = 1
    blad = [False, ""]

    def zweryfikuj_sume(blok_danych):
        if wybor_sumy:
            suma_odebrana = port.read(1)
            return suma_odebrana == fun.sumaKontrolna(blok_danych).to_bytes(1, 'big')
        else:
            crc_odebrane = port.read(2)
            return crc_odebrane == fun.algorytmCRC(blok_danych).to_bytes(2, 'big')

    def rozpocznij_transmisje():
        port.write(fun.NAK if wybor_sumy else fun.C)

    rozpocznij_transmisje()

    while time.time() - czas_start < 60:  # 60s timeout
        if port.in_waiting > 0:
            sygnal = port.read(1)

            if sygnal == fun.SOH:  # Początek bloku
                # Odczytaj numer bloku i jego dopełnienie
                nr_bloku = int.from_bytes(port.read(1), 'big')
                dopelnienie = int.from_bytes(port.read(1), 'big')

                # Sprawdź poprawność numeru bloku
                if nr_bloku != numer_bloku % 256:
                    blad = [True, f"Błędny numer bloku: {nr_bloku} (oczekiwano {numer_bloku % 256})"]
                    port.write(fun.NAK)
                    continue

                # Odczytaj dane (128 bajtów)
                dane_bloku = port.read(128)
                odebrane_dane.extend(dane_bloku)

                # Weryfikacja sumy kontrolnej
                if zweryfikuj_sume(dane_bloku):
                    port.write(fun.ACK)
                    numer_bloku += 1
                else:
                    port.write(fun.NAK)

            elif sygnal == fun.EOT:  # Koniec transmisji
                port.write(fun.ACK)
                break

            elif sygnal == fun.CAN:  # Anulowanie
                blad = [True, "Nadawca anulował transmisję"]
                break

            else:
                blad = [True, f"Nieznany sygnał: {sygnal}"]
                continue

        time.sleep(0.1)

    # Zapis danych do pliku po transmisji
    if not blad[0] and odebrane_dane:
        try:
            with open(nazwa_pliku, 'wb') as plik:
                plik.write(odebrane_dane)
            print(f"Pomyślnie zapisano {len(odebrane_dane)} bajtów do pliku '{nazwa_pliku}'")
        except Exception as e:
            print(f"Błąd zapisu pliku: {str(e)}")
    elif blad[0]:
        print(f"Błąd transmisji: {blad[1]}")
    else:
        print("Nie odebrano żadnych danych")