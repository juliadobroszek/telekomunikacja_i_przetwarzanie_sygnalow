import time
import fun

def odbierzWiadomosc(port):
    czas = time.time()
    odebranySygnal = None
    wybor = fun.wyborSumyKontrolnej()

    def rozpocznijTransmisję():
        if wybor:
            port.write(fun.NAK)
        else:
            port.write(fun.C)

    def zweryfikujSumęKontrolną(rs):
        if wybor:
            suma = port.read(1)
            return suma == fun.sumaKontrolna(rs).to_bytes(1)

        else:
            suma = port.read(2)
            return suma == fun.algorytmCRC(rs).to_bytes(2)

    while time.time() - czas < 60:
        rozpocznijTransmisję()
        time.sleep(10)
        if port.in_waiting > 0:
            zawartoscBufora = port.read(1)
            if zawartoscBufora == fun.SOH:
                odebranySygnal = zawartoscBufora
                break

            elif zawartoscBufora == fun.CAN:
                print("Transmisja została anulowana przez nadawcę!")
                port.write(fun.CAN)
                port.write(fun.CAN)
                return

            else:
                print("Anuluję transmisję, otrzymano nieoczekiwany komunikat: ", fun.znakiSterujace.get(zawartoscBufora, str(zawartoscBufora)))
                port.write(fun.CAN)
                port.write(fun.CAN)
                return

    if odebranySygnal is None:
        print("Nie otrzymano oczekiwanej odpowiedzi SOH, zakończono oczekiwanie.")
        return

    else:
        print("Otrzymano komunikat: ", fun.znakiSterujace.get(odebranySygnal, str(odebranySygnal)))

    numerBloku = 1
    blad = [False, ""]

    while True:
        if port.in_waiting > 0:
            if odebranySygnal != fun.SOH:
                odebranySygnal = port.read(1)
                print("Otrzymano komunikat: ", fun.znakiSterujace.get(odebranySygnal, str(odebranySygnal)))
                if odebranySygnal == fun.EOT:
                    break

                elif odebranySygnal == fun.CAN:
                    blad = [True, "Nadawca anulował transmisję!"]
                    break

                elif odebranySygnal != fun.SOH:
                    blad[1] = "Nie otrzymano oczekiwanego komunikatu SOH."
                    break

                else:
                    blad[0] = False  # reset flagi błędu

            odebranySygnal = port.read(1)  # odczytujemy 1 bajt

            if odebranySygnal != numerBloku.to_bytes(1):  # weryfikujemy informacje o numerze bloku
                blad = [True, "Nieprawidłowy numer bloku!"]
                break

            odebranySygnal = port.read(1)  # odczytujemy numer dopełnienia

            if odebranySygnal != (255 - numerBloku).to_bytes(1):
                blad = [True, "Nieprawidłowa liczba dopełnienia"]
                break

            odebranySygnal = port.read(128)
            print(str(numerBloku) + " blok - otrzymane dane: " + odebranySygnal.decode('ascii', errors='ignore'))

            if zweryfikujSumęKontrolną(odebranySygnal) is False:
                blad = [True, "Nieprawdiłowa suma kontrolna/CRC"]

            if blad[0]:
                print(blad[1] + " - wysyłam komunikat NAK")
                port.write(fun.NAK)

            else:
                print("Suma kontrolna/CRC się zgadza - wysyłam komunikat ACK")
                port.write(fun.ACK)
                numerBloku += 1
                numerBloku %= 256  # bo numer bloku to liczba 8 bitowa - zakres 0-255

    if blad[0]:
        print("Anuluję transmisję: " + blad[1])
        port.write(fun.CAN)
        port.write(fun.CAN)

    else:  # jeśli wystąpi EOT
        print("Przesyłam komunikat ACK, by zakończyć transmisję")
        port.write(fun.ACK)