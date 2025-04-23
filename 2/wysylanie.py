import time
import fun


def wyslijWiadomosc(port, nazwa_pliku):
    try:
        with open(nazwa_pliku, 'rb') as plik:
            calaWiadomosc = plik.read()
    except FileNotFoundError:
        print(f"Błąd: Plik '{nazwa_pliku}' nie istnieje!")
        return
    except Exception as e:
        print(f"Błąd podczas otwierania pliku: {e}")
        return

    bloki = fun.podzielWiadomosc(calaWiadomosc)
    wybor = fun.wyborSumyKontrolnej()
    czas = time.time()
    otrzymanySygnal = None

    # Oczekiwanie na inicjalizację odbiornika
    while time.time() - czas < 60:
        if port.in_waiting > 0:
            zawartoscBufora = port.read(1)
            if zawartoscBufora in [fun.NAK, fun.C]:
                otrzymanySygnal = zawartoscBufora
                break
        time.sleep(1)

    if otrzymanySygnal is None:
        print("Błąd: Nie otrzymano sygnału inicjującego (NAK/C) w wymaganym czasie")
        return

    numerBloku = 1
    for blok in bloki:
        # Przygotowanie nagłówka bloku
        naglowek = fun.SOH + numerBloku.to_bytes(1, 'big') + (255 - numerBloku).to_bytes(1, 'big')

        # Obliczanie sumy kontrolnej
        if wybor:
            suma = fun.sumaKontrolna(blok).to_bytes(1, 'big')
        else:
            suma = fun.algorytmCRC(blok).to_bytes(2, 'big')

        # Budowanie pełnego pakietu
        pakiet = naglowek + blok + suma

        # Wysyłanie pakietu
        port.write(pakiet)
        print(f"Wysłano blok {numerBloku} ({len(blok)} bajtów)")

        # Oczekiwanie na potwierdzenie
        czas_ack = time.time()
        while time.time() - czas_ack < 5:
            if port.in_waiting > 0:
                odpowiedz = port.read(1)
                if odpowiedz == fun.ACK:
                    print(f"Potwierdzenie (ACK) dla bloku {numerBloku}")
                    numerBloku += 1
                    numerBloku %= 256
                    break
                elif odpowiedz == fun.NAK:
                    print(f"Błąd (NAK) dla bloku {numerBloku} - ponawiam")
                    port.write(pakiet)
                    czas_ack = time.time()
                elif odpowiedz == fun.CAN:
                    print("Odbiorca anulował transmisję (CAN)")
                    return
                else:
                    print(f"Nierozpoznana odpowiedź: {odpowiedz}")
            time.sleep(0.1)
        else:
            print("Timeout - brak odpowiedzi od odbiornika")
            return

    # Zakończenie transmisji
    port.write(fun.EOT)
    print("Wysłano sygnał zakończenia transmisji (EOT)")

    # Oczekiwanie na finalne ACK
    czas_eot = time.time()
    while time.time() - czas_eot < 5:
        if port.in_waiting > 0:
            if port.read(1) == fun.ACK:
                print("Transmisja zakończona pomyślnie")
                return
        time.sleep(0.1)

    print("Ostrzeżenie: Brak potwierdzenia zakończenia transmisji")