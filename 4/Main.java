import javax.sound.sampled.AudioFormat;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int opcja;
        do {
            System.out.println("1 - Nagrywanie");
            System.out.println("2 - Odtwarzanie");
            System.out.println("3 - Wyjście z programu");
            System.out.print("Wybierz opcję: ");
            opcja = scanner.nextInt();
            scanner.nextLine();

            switch (opcja) {
                case 1:
                    System.out.print("Podaj częstotliwość próbkowania (np. 22050, 44100, 48000): ");
                    float czestotliwosc = scanner.nextFloat();
                    System.out.print("Podaj rozdzielczość bitową (8 lub 16): ");
                    int rozdzielczoscBitowa = scanner.nextInt();
                    scanner.nextLine();
                    System.out.print("Podaj nazwę pliku .wav: ");
                    String nazwaPliku = scanner.nextLine().trim();
                    if (!nazwaPliku.toLowerCase().endsWith(".wav")) {
                        nazwaPliku += ".wav";
                    }
                    AudioFormat format = KonwersjaDzwieku.createFormat(czestotliwosc, rozdzielczoscBitowa);
                    KonwersjaDzwieku.nagrywaj(format, nazwaPliku);
                    break;
                case 2:
                    System.out.print("Podaj nazwę pliku .wav do odtworzenia: ");
                    String playName = scanner.nextLine();
                    KonwersjaDzwieku.odtworz(playName);
                    break;
                case 3:
                    System.out.println("Koniec programu.");
                    break;
                default:
                    System.out.println("Nieprawidłowa opcja.");
            }
            System.out.println();
        } while (opcja != 3);
        scanner.close();
    }
}
