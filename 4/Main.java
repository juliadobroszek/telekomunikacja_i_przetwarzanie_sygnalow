import javax.sound.sampled.AudioFormat;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int option;
        do {
            System.out.println("=== Menu Konwertera A/C C/A ===");
            System.out.println("1. Nagrywaj");
            System.out.println("2. Odtwarzaj");
            System.out.println("3. Wyjdź");
            System.out.print("Wybierz opcję: ");
            option = scanner.nextInt();
            scanner.nextLine();

            switch (option) {
                case 1:
                    System.out.print("Podaj częstotliwość próbkowania (np. 22050, 44100, 48000): ");
                    float fs = scanner.nextFloat();
                    System.out.print("Podaj rozdzielczość bitową (8 lub 16): ");
                    int bits = scanner.nextInt();
                    scanner.nextLine();
                    System.out.print("Podaj nazwę pliku .wav: ");
                    String recordName = scanner.nextLine().trim();
                    if (!recordName.toLowerCase().endsWith(".wav")) {
                        recordName += ".wav";
                    }
                    AudioFormat format = KonwerterAudio.createFormat(fs, bits);
                    KonwerterAudio.nagrywaj(format, recordName);
                    break;
                case 2:
                    System.out.print("Podaj nazwę pliku .wav do odtworzenia: ");
                    String playName = scanner.nextLine();
                    KonwerterAudio.odtworz(playName);
                    break;
                case 3:
                    System.out.println("Koniec programu.");
                    break;
                default:
                    System.out.println("Nieprawidłowa opcja.");
            }
            System.out.println();
        } while (option != 3);
        scanner.close();
    }
}
