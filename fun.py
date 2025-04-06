import numpy as np

H = np.array([
    [1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
    [1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0],
    [1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1]
], dtype=int)

def kodowanie(dane):
    wynik = []
    for znak in dane:
        bity_danych = [int(bit) for bit in format(ord(znak), '08b')]
        bity_parzystosci = (np.dot(H[:, :8], bity_danych) % 2).tolist()
        wynik.append(bity_danych + bity_parzystosci)
    return wynik

def sprawdz_poprawnosc(dane_zakodowane):
    odkodowana = []
    for slowo in dane_zakodowane:
        syndrom = np.dot(H, slowo) % 2
        if np.any(syndrom):
            for i in range(16):
                if np.array_equal(H[:, i], syndrom):
                    slowo[i] = 1 - slowo[i]
                    break
        odkodowana.append(slowo[:8])
    return odkodowana

def dekodowanie(dane_odkodowane):
    return "".join(chr(int("".join(map(str, slowo)), 2)) for slowo in dane_odkodowane)