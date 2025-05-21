import uuid
from datetime import datetime
from abc import ABC, abstractmethod

# ------------------------------
# Osztályok: Járatok, Foglalások
# ------------------------------

class Jarat(ABC):
    def __init__(self, jaratszam, celallomas, jegyar):
        self.jaratszam = jaratszam
        self.celallomas = celallomas
        self.jegyar = jegyar

    def __str__(self):
        return f"{self.jaratszam} -> {self.celallomas} ({self.jegyar} Ft)"

    @abstractmethod
    def get_tipus(self):
        pass

class BelfoldiJarat(Jarat):
    def __init__(self, jaratszam, celallomas):
        super().__init__(jaratszam, celallomas, jegyar=15000)

    def get_tipus(self):
        return "Belföldi"

class NemzetkoziJarat(Jarat):
    def __init__(self, jaratszam, celallomas):
        super().__init__(jaratszam, celallomas, jegyar=45000)

    def get_tipus(self):
        return "Nemzetközi"

class LegiTarsasag:
    def __init__(self, nev):
        self.nev = nev
        self.jaratok = []

    def jarat_hozzaadas(self, jarat):
        self.jaratok.append(jarat)

class JegyFoglalas:
    def __init__(self, jarat, utas_nev, datum):
        self.azonosito = str(uuid.uuid4())[:8]
        self.jarat = jarat
        self.utas_nev = utas_nev
        self.datum = datum

    def __str__(self):
        return f"Azonosító: {self.azonosito} | Utas: {self.utas_nev} | Járat: {self.jarat} | Dátum: {self.datum.strftime('%Y-%m-%d')}"

# ------------------------------
# Foglalási rendszer motor
# ------------------------------

class FoglalasiRendszer:
    def __init__(self):
        self.legi_tarsasag = LegiTarsasag("ByAir")
        self.foglalasok = []
        self.adatok_betoltese()

    def adatok_betoltese(self):
        self.legi_tarsasag.jarat_hozzaadas(BelfoldiJarat("BY001", "Sármellék"))
        self.legi_tarsasag.jarat_hozzaadas(NemzetkoziJarat("BY201", "Berlin"))
        self.legi_tarsasag.jarat_hozzaadas(NemzetkoziJarat("BY202", "Bécs"))

        today = datetime.now()
        j = self.legi_tarsasag.jaratok
        self.foglalasok.append(JegyFoglalas(j[0], "Vicc Elek", today.replace(month=7, day=10)))
        self.foglalasok.append(JegyFoglalas(j[0], "Meg Győző", today.replace(month=7, day=11)))
        self.foglalasok.append(JegyFoglalas(j[1], "Nyúl Béla", today.replace(month=7, day=15)))
        self.foglalasok.append(JegyFoglalas(j[1], "Hát Izsák", today.replace(month=7, day=18)))
        self.foglalasok.append(JegyFoglalas(j[2], "Tóth András", today.replace(month=7, day=20)))
        self.foglalasok.append(JegyFoglalas(j[2], "Idét Lenke", today.replace(month=7, day=22)))
        self.foglalasok.append(JegyFoglalas(j[0], "Deb Ella", today.replace(month=7, day=25)))

    def foglalasok_listazasa(self):
        if not self.foglalasok:
            print("Nincs egyetlen foglalás sem.")
            return
        for f in self.foglalasok:
            print(f)

    def jegy_foglalasa(self):
        print("\nElérhető járatok:")
        for i, j in enumerate(self.legi_tarsasag.jaratok):
            print(f"{i+1}. {j}")

        try:
            idx = int(input("Válassz járatot (sorszám): ")) - 1
            if idx not in range(len(self.legi_tarsasag.jaratok)):
                print("Érvénytelen választás.")
                return
            kivalasztott = self.legi_tarsasag.jaratok[idx]
            nev = input("Add meg az utas nevét: ")
            datum_szoveg = input("Add meg az utazás dátumát (ÉÉÉÉ-HH-NN): ")
            datum = datetime.strptime(datum_szoveg, "%Y-%m-%d")

            if datum < datetime.now():
                print("A dátum csak jövőbeli lehet.")
                return

            for f in self.foglalasok:
                if f.jarat.jaratszam == kivalasztott.jaratszam and f.datum.date() == datum.date() and f.utas_nev == nev:
                    print("Ez a foglalás már létezik ezen a napon erre a járatra.")
                    return

            foglalas = JegyFoglalas(kivalasztott, nev, datum)
            self.foglalasok.append(foglalas)
            print(f"Foglalás sikeres! Azonosító: {foglalas.azonosito}. Ár: {kivalasztott.jegyar} Ft")
        except ValueError:
            print("Hibás dátumformátum.")

    def foglalas_lemondasa(self):
        azonosito = input("Add meg a lemondandó foglalás azonosítóját (vagy csak hidd el, hogy működik ez is:)")
        for f in self.foglalasok:
            if f.azonosito == azonosito:
                self.foglalasok.remove(f)
                print("Foglalás sikeresen törölve.")
                return
        print("Nem található ilyen foglalás.")

# ------------------------------
# Main
# ------------------------------

def main():
    rendszer = FoglalasiRendszer()

    while True:
        print("\n--- ByAir UltiMATE repülőjegy foglalási rendszer ---")
        print("1. Jegy foglalása")
        print("2. Foglalás lemondása")
        print("3. Foglalások listázása")
        print("4. Kilépés")

        valasztas = input("Válassz műveletet (1-4): ")

        if valasztas == "1":
            rendszer.jegy_foglalasa()
        elif valasztas == "2":
            rendszer.foglalas_lemondasa()
        elif valasztas == "3":
            rendszer.foglalasok_listazasa()
        elif valasztas == "4":
            print("Kilépés... Viszontlátásra!")
            break
        else:
            print("Érvénytelen választás.")

if __name__ == "__main__":
    main()
