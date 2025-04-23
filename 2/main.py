import serial
import fun
import odbior
import wysylanie

print("Implementacja protokołu xModem")

while 1:
    port = fun.wybierzPort()
    try:
        serialPort = serial.Serial(port, 9600, timeout=10)
        print("Poprawnie połączono z portem.")

        while True:
            menu = fun.wyborOperacji()

            if menu == 1:
                print("Wybrano odbieranie wiadomości.")
                odbior.odbierzWiadomosc(serialPort)
                break

            elif menu == 2:
                print("Wybrano wysyłanie wiadomości.")
                wiadomosc = input("Wprowadź wiadomość do wysłania: ")
                wysylanie.wyslijWiadomosc(serialPort, wiadomosc)
                break

            else:
                print("Wybrano niepoprawną opcję.")

        serialPort.close()

    except serial.SerialException as e:
        print(e)

    input("Aby kontynuować, naciśnij enter")