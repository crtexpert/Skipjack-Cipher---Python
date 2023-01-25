#############################################################################################
# İsim : Görkem
# Soyisim : Kahyaoğlu
# Numara  : B181210064
# Konu    : SkipJack şifreleme.
#############################################################################################
import base64
import tkinter as tk


def hexDegeri(metin):
    integerCevirme = int(metin, base=16)
    hexCevirme     = hex(integerCevirme)
    return hexCevirme

def convert_hex_to_ascii(h):
    chars_in_reverse = []
    while h != 0x0:
        chars_in_reverse.append(chr(h & 0xFF))
        h = h >> 8

    chars_in_reverse.reverse()
    return ''.join(chars_in_reverse)

def btnSifrele():
    anahtarmetin =[]
    for element in gizliAnahtar.get():
        b = element.encode('utf-8')
        anahtarmetin.append(int(b.hex(),base=16))

    sifrelenicekMetin = metinGirdi.get(1.0, tk.END).encode('utf-8')
    sifrelenmisMetin  = skipjack.sifrele(int(sifrelenicekMetin.hex(),base=16), anahtarmetin)

    yeniEkran = tk.Toplevel(ekran)
    yeniEkran.title("Şifrelenmiş Metin")
    yeniEkran.geometry("300x300")
    yeniEkran.configure(bg="gray")
    text = tk.Text(yeniEkran, font="Robote 10", bg="white", relief=tk.GROOVE, wrap=tk.WORD)
    text.place(x=10,y=40,width=280,height=150)
    text.insert(tk.END,hex(sifrelenmisMetin))

def btnDesifrele():
    anahtarmetin = []
    for element in gizliAnahtar.get():
        b = element.encode('utf-8')
        anahtarmetin.append(int(b.hex(), base=16))
    desifrelenicekMetin = metinGirdi.get(1.0, tk.END)
    desifrelenmisMetin = skipjack.desifrele(int(desifrelenicekMetin, base=16), anahtarmetin)
    yeniEkran = tk.Toplevel(ekran)
    yeniEkran.title("Şifrelenmiş Metin")
    yeniEkran.geometry("300x300")
    yeniEkran.configure(bg="gray")
    text = tk.Text(yeniEkran, font="Robote 10", bg="white", relief=tk.GROOVE, wrap=tk.WORD)
    text.place(x=10, y=40, width=280, height=150)
    text.insert(tk.END, convert_hex_to_ascii(desifrelenmisMetin))

def program():
    global metinGirdi
    global ekran
    global gizliAnahtar
    global skipjack

    ekran = tk.Tk()
    ekran.geometry("500x500")
    ekran.title("Skipjack Cipher")

    skipjack = SjCipher()

    def sifirla():
        gizliAnahtar.set("")
        metinGirdi.delete(1.0, tk.END)


    tk.Label(text="Şifrelenicek/Deşifrelenicek Metin", fg="black", font=("Times New Roman", 15)).place(relx=0.5, rely=0.05, anchor="center")

    metinGirdi = tk.Text(font=("Times New Roman", 15))
    metinGirdi.place(relx=0.5, rely=0.2, relheight=0.2, relwidth=0.8, anchor="center")
    tk.Label(text="Anahtar (10 karakter)", fg="black", font=("Times New Roman", 15)).place(relx=0.27, rely=0.35, anchor="center")

    gizliAnahtar = tk.StringVar()
    tk.Entry(textvariable=gizliAnahtar, font=("Times New Roman", 15)).place(relx=0.5, rely=0.42, relheight=0.07, relwidth=0.8, anchor="center")

    tk.Button(text="Şifrele", bg="gray", fg="white", bd=1, command=btnSifrele).place(relx=0.22, rely=0.55, relheight=0.07, relwidth=0.27, anchor="center")
    tk.Button(text="Deşifrele", bg="gray", fg="white", bd=1, command=btnDesifrele).place(relx=0.50, rely=0.55, relheight=0.07, relwidth=0.27, anchor="center")
    tk.Button(text="Sıfırla", bg="gray", fg="white", bd=1, command=sifirla).place(relx=0.78, rely=0.55, relheight=0.07, relwidth=0.27, anchor="center")


    ekran.mainloop()


#Skipjack algoritması için sınıf tanımı.
class SjCipher:
    def __init__(self):
        # Orjinal dökümanda belirtilen F tablosunun (S-Box) tanımı.
        self.fTablo = []
        self.fTabloTanimla()
        self.kelime1 = 0
        self.kelime2 = 0
        self.kelime3 = 0
        self.kelime4 = 0

    # Şifreleme işleminin gerçekleştiği ana fonksiyon bloğu.
    # 32 round  - 8 A kuralı - 8 B kuralı - 8 A kuralı - 8 B kuralı
    def sifrele(self, metin, anahtar):
        self.kelimeAyrıstır(metin)

        for tur in range(1, 33):
            if (1 <= tur <= 8) or (17 <= tur <= 24):
                self.aKurali(tur, anahtar)
                self.printstatus(tur)
            if (9 <= tur <= 16) or (25 <= tur <= 32):
                self.bKurali(tur, anahtar)
                self.printstatus(tur)

        return self.kelimeBirlestir()

    # Şifreleme algoritmasında bahsedilen toplamda 16 tur uygulanan A kuralı.
    def aKurali(self, tur, anahtar):
        # Degerleri kaybetmemek için geçici olarak değişkenlere atıyoruz.
        degisken1 = self.kelime1
        degisken2 = self.kelime2
        degisken3 = self.kelime3

        # A kuralının gerektirdiği işlemler.
        self.kelime1 = self.G(tur, anahtar, degisken1) ^ self.kelime4 ^ tur
        self.kelime2 = self.G(tur, anahtar, degisken1)
        self.kelime3 = degisken2
        self.kelime4 = degisken3

    # Şifreleme algoritmasında bahsedilen toplamda 16 tur uygulanan A kuralı.
    def bKurali(self, tur, anahtar):
        degisken1 = self.kelime1
        degisken2 = self.kelime2
        degisken3 = self.kelime3

        self.kelime1 = self.kelime4
        self.kelime2 = self.G(tur, anahtar, degisken1)
        self.kelime3 = degisken1 ^ degisken2 ^ tur
        self.kelime4 = degisken3

    def G(self, tur, anahtar, i):
        g = [0] * 6
        g[0] = (i >> 8) & 0xff
        g[1] = i & 0xff
        j = (4 * (tur - 1)) % 10

        for a in range(2, 6):
            g[a] = self.fTablo[g[a - 1] ^ anahtar[j]] ^ g[a - 2]
            j = (j + 1) % 10

        return (g[4] << 8) | g[5]

    # Algoritmada 16-bit 4 kelimeyi birleştirip 64-bit tek kelime oluşturan kod bloğu.
    def kelimeBirlestir(self):
        x1 = self.kelime1 << 3 * 16
        x2 = self.kelime2 << 2 * 16
        x3 = self.kelime3 << 1 * 16
        x4 = self.kelime4
        return x1 | x2 | x3 | x4

    # Algoritmada 64-bit kelimeyi 16-bit 4 parçaya bölen kod bloğu.
    def kelimeAyrıstır(self, kelime):
        self.kelime1 = (kelime >> (16 * 3)) & 0xFFFF
        self.kelime2 = (kelime >> (16 * 2)) & 0xFFFF
        self.kelime3 = (kelime >> (16 * 1)) & 0xFFFF
        self.kelime4 = kelime & 0XFFFF

    def fTabloTanimla(self):
        # S-box değerlerinin hexadecimal karşılığı.
        self.fTablo = [0xa3, 0xd7, 0x09, 0x83, 0xf8, 0x48, 0xf6, 0xf4, 0xb3, 0x21, 0x15, 0x78, 0x99, 0xb1, 0xaf, 0xf9,
                       0xe7, 0x2d, 0x4d, 0x8a, 0xce, 0x4c, 0xca, 0x2e, 0x52, 0x95, 0xd9, 0x1e, 0x4e, 0x38, 0x44, 0x28,
                       0x0a, 0xdf, 0x02, 0xa0, 0x17, 0xf1, 0x60, 0x68, 0x12, 0xb7, 0x7a, 0xc3, 0xc9, 0xfa, 0x3d, 0x53,
                       0x96, 0x84, 0x6b, 0xba, 0xf2, 0x63, 0x9a, 0x19, 0x7c, 0xae, 0xe5, 0xf5, 0xf7, 0x16, 0x6a, 0xa2,
                       0x39, 0xb6, 0x7b, 0x0f, 0xc1, 0x93, 0x81, 0x1b, 0xee, 0xb4, 0x1a, 0xea, 0xd0, 0x91, 0x2f, 0xb8,
                       0x55, 0xb9, 0xda, 0x85, 0x3f, 0x41, 0xbf, 0xe0, 0x5a, 0x58, 0x80, 0x5f, 0x66, 0x0b, 0xd8, 0x90,
                       0x35, 0xd5, 0xc0, 0xa7, 0x33, 0x06, 0x65, 0x69, 0x45, 0x00, 0x94, 0x56, 0x6d, 0x98, 0x9b, 0x76,
                       0x97, 0xfc, 0xb2, 0xc2, 0xb0, 0xfe, 0xdb, 0x20, 0xe1, 0xeb, 0xd6, 0xe4, 0xdd, 0x47, 0x4a, 0x1d,
                       0x42, 0xed, 0x9e, 0x6e, 0x49, 0x3c, 0xcd, 0x43, 0x27, 0xd2, 0x07, 0xd4, 0xde, 0xc7, 0x67, 0x18,
                       0x89, 0xcb, 0x30, 0x1f, 0x8d, 0xc6, 0x8f, 0xaa, 0xc8, 0x74, 0xdc, 0xc9, 0x5d, 0x5c, 0x31, 0xa4,
                       0x70, 0x88, 0x61, 0x2c, 0x9f, 0x0d, 0x2b, 0x87, 0x50, 0x82, 0x54, 0x64, 0x26, 0x7d, 0x03, 0x40,
                       0x34, 0x4b, 0x1c, 0x73, 0xd1, 0xc4, 0xfd, 0x3b, 0xcc, 0xfb, 0x7f, 0xab, 0xe6, 0x3e, 0x5b, 0xa5,
                       0xad, 0x04, 0x23, 0x9c, 0x14, 0x51, 0x22, 0xf0, 0x29, 0x79, 0x71, 0x7e, 0xff, 0x8c, 0x0e, 0xe2,
                       0x0c, 0xef, 0xbc, 0x72, 0x75, 0x6f, 0x37, 0xa1, 0xec, 0xd3, 0x8e, 0x62, 0x8b, 0x86, 0x10, 0xe8,
                       0x08, 0x77, 0x11, 0xbe, 0x92, 0x4f, 0x24, 0xc5, 0x32, 0x36, 0x9d, 0xcf, 0xf3, 0xa6, 0xbb, 0xac,
                       0x5e, 0x6c, 0xa9, 0x13, 0x57, 0x25, 0xb5, 0xe3, 0xbd, 0xa8, 0x3a, 0x01, 0x05, 0x59, 0x2a, 0x46]

    def printstatus(self, tur):
        w = self.kelimeBirlestir()
        print("round=" + str(tur) + " " + hex(w))


    def desifrele(self, sifreliMetin, anahtar):
        self.kelimeAyrıstır(sifreliMetin)

        for tur in reversed(range(1, 33)):
            if (25 <= tur <= 32) or (9 <= tur <= 16):
                self.tersBkurali(tur, anahtar)
            if (17 <= tur <= 24) or (1 <= tur <= 8):
                self.tersAkurali(tur, anahtar)

        return self.kelimeBirlestir()

    def tersAkurali(self, tur, anahtar):
        degisken1 = self.kelime1
        degisken2 = self.kelime2

        self.kelime1 = self.tersG(tur, anahtar, degisken2)
        self.kelime2 = self.kelime3
        self.kelime3 = self.kelime4
        self.kelime4 = degisken1 ^ degisken2 ^ tur

    def tersBkurali(self, tur, anahtar):
        degisken1 = self.kelime1

        self.kelime1 = self.tersG(tur, anahtar, self.kelime2)
        self.kelime2 = self.tersG(tur, anahtar, self.kelime2) ^ self.kelime3 ^ tur
        self.kelime3 = self.kelime4
        self.kelime4 = degisken1

    def tersG(self, tur, anahtar , i):
        g = [0] * 6
        g[4] = (i >> 8) & 0xff
        g[5] = i & 0xff
        j = (4 * (tur - 1) + 3) % 10

        for a in reversed(range(4)):
            g[a] = self.fTablo[g[a + 1] ^ anahtar[j]] ^ g[a + 2]
            j = (j - 1) % 10

        return (g[0] << 8) | g[1]


program()
