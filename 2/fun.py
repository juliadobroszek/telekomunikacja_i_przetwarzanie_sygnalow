SOH = b'\x01'
EOT = b'\x04'
ACK = b'\x06'
NAK = b'\x15'
CAN = b'\x18'
C = b'C'

znakiSterujace = {
    b'\x01': "SOH",
    b'\x04': "EOT",
    b'\x06': "ACK",
    b'\x15': "NAK",
    b'\x18': "CAN",
    b'C': "C"
}

def wybierzPort():
    wyborPortu = 0

    while wyborPortu not in (1, 2):
        print("Wybierz port: ")
        print("1) Port COM1")
        print("2) Port COM2")
        try:
            wyborPortu = int(input("Wybór: "))
        except ValueError:
            print("Podano niepoprawną wartość.")
            continue

        if wyborPortu == 1:
            port = "COM1"

        elif wyborPortu == 2:
            port = "COM2"

        else:
            print("Podaj 1 lub 2.")

    return port

def wyborSumyKontrolnej():
    while True:
        print("Wybierz sumę kontrolną lub algorytm CRC: ")
        print("1) suma kontrolna")
        print("2) algorytm CRC")
        wybor = int(input("Wybór: "))
        if wybor == 1:
            print("Wybrano sumę kontrolną.")
            return True

        elif wybor == 2:
            print("Wybrano algorytm CRC.")
            return False

        else:
            print("Wybrano niepoprawną opcję.")

def wyborOperacji():
    print("Wybierz co chcesz zrobić: ")
    print("1) Odbierz wiadomość")
    print("2) Wyślij wiadomość")
    menu = int(input("Wybierz opcję: "))
    return menu

def sumaKontrolna(blok):
    suma = sum(blok)

    while suma > 256: #tworzenie sumy kontrolnej, jeśli suma znaków > 256 to odejmujemy 256
        suma -= 256

    return suma

def algorytmCRC(blok):
    crc = 0
    # dzielnik dla wersji CRC16 (dla protokołu xModem)
    dzielnik = 0x1021

    for bajt in blok:
        crc ^= (bajt << 8)

        for i in range(8):
            if crc & 0x8000:  # sprawdzamy czy bit najbardziej po lewo jest ustawiony na 1
                crc = (crc << 1) ^ dzielnik  # jesli jest on rowny 1 to przesuwamy w lewo o 1 i robimy xor z dzielnikiem

            else:
                crc = crc << 1  # jesli bit nie wynosi 1 to przesuwamy w lewo o 1

            crc &= 0xFFFF  # maska 16 bit aby zapewnić że crc bedzie mialo wlasnie tyle bitow

    return crc

def padding(dane_binarne):
    blok_size = 128
    dlugosc = len(dane_binarne)
    dopelnienie = (blok_size - (dlugosc % blok_size)) % blok_size
    return dane_binarne + bytes([0] * dopelnienie)

# funkcja podziału wiadomości na bloki o rozmiarze 128 bajtow
def podzielWiadomosc(wiadomosc):
    wiadomosc = padding(wiadomosc)
    blokiWiadomosci = []

    for i in range(0, len(wiadomosc), 128):
        blok = wiadomosc[i:i + 128]
        blokiWiadomosci.append(blok)

    return blokiWiadomosci