import time
import fun

def wyslijWiadomosc(port, calaWiadomosc):
    blok = fun.podzielWiadomosc(calaWiadomosc)
    wybor = fun.wyborSumyKontrolnej()
    czas = time.time()
    otrzymanySygnal = None

    while time.time() - czas < 60:
        if port.in_waiting > 0:
            zawartoscBufora = port.read(1)
            if zawartoscBufora in [fun.NAK, fun.C]: # NAK - suma kontrolna, C - suma kontrolna z algorytmem CRC
                otrzymanySygnal = zawartoscBufora
                break
        time.sleep(1)

    if otrzymanySygnal is None:
        print("Nie otrzymano oczekiwanej odpowiedzi NAK lub C.")
        return

    elif otrzymanySygnal == fun.C and wybor:
        print("Odbiorca oczekuje CRC, a wskazano sumę kontrolną.")
        port.write(fun.CAN)
        port.write(fun.CAN)
        return

    elif otrzymanySygnal == fun.NAK and not wybor:
        print("Odbiorca oczekuje sumy kontrolnej, a wskazano CRC.")
        port.write(fun.CAN)
        port.write(fun.CAN)
        return

    else:
        print("Otrzymano oczekiwany komunikat: ", fun.znakiSterujace.get(otrzymanySygnal, str(otrzymanySygnal)) + ", przechodzę do transmisji.")

    numerBloku = 1
    for Blok in blok:
        blokBajty = Blok.encode('ascii')
        nrBloku = numerBloku.to_bytes(1)
        dopelnienie = (255 - numerBloku).to_bytes(1)

        if wybor:
            suma = fun.sumaKontrolna(blokBajty).to_bytes(1)

        else:
            suma = fun.algorytmCRC(blokBajty).to_bytes(2)

        pakiet = fun.SOH + nrBloku + dopelnienie + blokBajty + suma
        print("Przesyłam blok: " + str(numerBloku) + " - " + Blok)
        port.write(pakiet)
        time.sleep(1)
        czas = time.time()

        while time.time() - czas < 5:
            if port.in_waiting > 0:
                otrzymanySygnal = port.read(1)
                if otrzymanySygnal == fun.ACK:
                    print("Odbiorca potwierdził poprawność (ACK), przechodzę do kolejnego bloku")
                    numerBloku += 1
                    numerBloku %= 256
                    break

                elif otrzymanySygnal == fun.NAK:
                    print("Odbiorca zgłosił błąd (NAK), ponawiam wysłanie bloku")
                    port.write(pakiet)

                elif otrzymanySygnal == fun.CAN:
                    print("Odbiorca anulował transmisję (CAN).")
                    port.write(fun.CAN)
                    port.write(fun.CAN)
                    return

                else:
                    print("Odbiorca odpowiedział nieoczekiwanie: " + fun.znakiSterujace.get(otrzymanySygnal, str(otrzymanySygnal)))

            time.sleep(0.2)
    print("Koniec transmisji, zgłaszam to odbiorcy")
    port.write(fun.EOT)
    time.sleep(1)
    czas = time.time()

    while time.time() - czas < 5:
        if port.in_waiting > 0:
            otrzymanySygnal = port.read(1)
            if otrzymanySygnal == fun.ACK:
                print("Odbiorca potwierdził poprawne zakończenie transmisji (ACK)")
                return

        time.sleep(0.1)
        print("Ponawiam przesłanie EOT.")
        port.write(fun.EOT)

    print("Ponowne wysyłanie komunikatu nie przyniosło oczekiwanego efektu, kończę transmisję bez reakcji z drugiej strony.")