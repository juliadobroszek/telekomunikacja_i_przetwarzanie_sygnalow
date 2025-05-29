import javax.sound.sampled.*;
import java.io.File;
import java.io.IOException;

public class KonwersjaDzwieku {

    public static AudioFormat createFormat(float sampleRate, int sampleSizeInBits) {
        int channels = 1; //jeden kanał
        boolean signed = true; //sygnał ze znakiem
        boolean bigEndian = false; //kolejność bajtów
        return new AudioFormat(AudioFormat.Encoding.PCM_SIGNED,
                sampleRate,
                sampleSizeInBits,
                channels,
                (sampleSizeInBits / 8) * channels,
                sampleRate,
                bigEndian);
    }

    public static void nagrywaj(AudioFormat format, String fileName) {
        try {
            TargetDataLine line = AudioSystem.getTargetDataLine(format);
            line.open(format);
            line.start();

            System.out.println("Nagrywanie... Naciśnij Enter, aby zakończyć.");
            AudioInputStream ais = new AudioInputStream(line);
            // strumień audio z linii wejściowej
            Thread writer = new Thread(() -> {
                try {
                    AudioSystem.write(ais, AudioFileFormat.Type.WAVE, new File(fileName));
                } catch (IOException e) {
                    e.printStackTrace();
                }
            });
            writer.start();

            System.in.read();
            line.stop();
            line.close();
            writer.join();
            ais.close();

            System.out.println("Nagrywanie zakończone. Plik zapisany: " + fileName);
        } catch (LineUnavailableException | IOException | InterruptedException e) {
            e.printStackTrace();
        }
    }

    public static void odtworz(String fileName) {
        try {
            File file = new File(fileName);
            if (!file.exists()) {
                System.err.println("Plik nie istnieje: " + fileName);
                return;
            }

            AudioInputStream ais = AudioSystem.getAudioInputStream(file);
            Clip clip = AudioSystem.getClip();
            clip.open(ais);
            clip.start();
            System.out.println("Odtwarzanie...");
            Thread.sleep(clip.getMicrosecondLength() / 1000);
            clip.stop();
            clip.close();
            ais.close();
        } catch (UnsupportedAudioFileException | IOException | LineUnavailableException | InterruptedException e) {
            e.printStackTrace();
        }
    }
}
