# Aufgabe 4 - Modifizierte Caesar-Chiffre
# Hausübung 1, IT-Sicherheit
# Jan Niklas Benn

import random
import string
import os

# Konfig
SHIFT = 7        # Caesar Verschiebung
SEED = 42        # Seed für Permutation
DEMO_FILE = "demo/demo.txt"

ALPHABET = string.ascii_uppercase


# erzeugt aus dem Seed eine permutation des alphabets
def make_permutation(seed):
    rng = random.Random(seed)
    chars = list(ALPHABET)
    rng.shuffle(chars)
    perm = ""
    for c in chars:
        perm = perm + c
    return perm


# inverse der substitutionstabelle
# wenn perm[i] = c, dann inv[index(c)] = ALPHABET[i]
def inverse_permutation(perm):
    inv = [""] * 26
    for i in range(len(perm)):
        c = perm[i]
        pos = ALPHABET.index(c)
        inv[pos] = ALPHABET[i]

    result = ""
    for x in inv:
        result = result + x
    return result


def encrypt(plaintext, shift, seed):
    perm = make_permutation(seed)
    plaintext = plaintext.upper()
    result = ""
    for c in plaintext:
        if c in ALPHABET:
            # Schritt 1: Caesar Shift
            idx = ALPHABET.index(c)
            shifted = (idx + shift) % 26
            # Schritt 2: Substitution über perm
            result = result + perm[shifted]
        else:
            # Leerzeichen / Sonderzeichen bleiben
            result = result + c
    return result


def decrypt(ciphertext, shift, seed):
    perm = make_permutation(seed)
    inv = inverse_permutation(perm)
    ciphertext = ciphertext.upper()
    result = ""
    for c in ciphertext:
        if c in ALPHABET:
            # erst Substitution rückgängig
            unsub = inv[ALPHABET.index(c)]
            # dann Shift rückgängig
            unshifted = (ALPHABET.index(unsub) - shift) % 26
            result = result + ALPHABET[unshifted]
        else:
            result = result + c
    return result


# laedt den demo text aus der datei
def load_demo_text():
    if os.path.exists(DEMO_FILE) == False:
        print("Fehler: Demo Datei nicht gefunden unter " + DEMO_FILE)
        return None

    f = open(DEMO_FILE, "r", encoding="utf-8")
    text = f.read()
    f.close()
    return text.strip()


# CLI
def menu():
    while True:
        print("")
        print("=" * 50)
        print("Modifizierte Caesar-Chiffre")
        print("Aktiver Schluessel: SHIFT=" + str(SHIFT) + ", SEED=" + str(SEED))
        print("=" * 50)
        print("1. Encrypt")
        print("2. Decrypt")
        print("3. Demo")
        print("4. Exit")
        wahl = input("Auswahl: ").strip()

        if wahl == "1":
            text = input("Klartext: ")
            ct = encrypt(text, SHIFT, SEED)
            print("\nChiffretext:")
            print(ct)

        elif wahl == "2":
            text = input("Chiffretext: ")
            pt = decrypt(text, SHIFT, SEED)
            print("\nKlartext:")
            print(pt)

        elif wahl == "3":
            demo_text = load_demo_text()
            if demo_text == None:
                continue

            print("\nKlartext (" + str(len(demo_text)) + " Zeichen):")
            print(demo_text)

            ct = encrypt(demo_text, SHIFT, SEED)
            print("\nSchluessel: SHIFT=" + str(SHIFT) + ", SEED=" + str(SEED))
            print("\nChiffretext:")
            print(ct)

            pt = decrypt(ct, SHIFT, SEED)
            print("\nEntschluesselt:")
            print(pt)
            print("\nKlartext == Entschluesselt: " + str(demo_text == pt))

        elif wahl == "4":
            print("Programm beendet.")
            break

        else:
            print("Ungueltige Eingabe.")


if __name__ == "__main__":
    menu()
