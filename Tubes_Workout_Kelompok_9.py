"""
APLIKASI MANAJEMEN WORKOUT HARIAN
Kelompok 9 | Algoritma Pemrograman    

Tipe Bentukan:
    DataWorkout  : record
        id       : integer
        jenis    : string
        durasi   : integer  { menit }
        kalori   : integer  { kalori terbakar }
        tanggal  : string   { format YYYY-MM-DD }

Array Global:
    data_workout : array [0..MAX_DATA-1] of DataWorkout
    n_workout    : integer { banyak data yang tersimpan }
"""

import json
import os
from dataclasses import dataclass
from datetime import datetime, timedelta
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox


# ==================================================
# TIPE BENTUKAN
# ==================================================
@dataclass
class DataWorkout:
    # satu record = satu sesi workout
    # id      : nomor urut
    # jenis   : nama olahraganya
    # durasi  : berapa menit
    # kalori  : kalori yang kebakar
    # tanggal : kapan workoutnya (YYYY-MM-DD)
    id: int
    jenis: str
    durasi: int
    kalori: int
    tanggal: str


# ==================================================
# KONSTANTA & ARRAY STATIS GLOBAL
# ==================================================
KALORI_PER_MENIT = {
    "Lari": 10,
    "Bersepeda": 8,
    "Renang": 9,
    "Yoga": 4,
    "Angkat Beban": 5,
    "Push Up": 6,
    "Sit Up": 5,
    "Pull Up": 7,
    "Skipping": 11,
    "Jalan Cepat": 5,
    "Zumba": 8,
    "Pilates": 4,
    "HIIT": 12,
    "Badminton": 7,
    "Basket": 8,
    "Sepak Bola": 9,
    "Tenis": 7,
    "Voli": 6,
    "Senam": 5,
    "Hiking": 6,
    "Karate": 8,
    "Tinju": 10,
    "Stretching": 3,
    "Plank": 4,
    "Burpees": 10,
}

KALORI_DEFAULT = 6   # kalau jenisnya tidak ada di daftar, pakai ini
MAX_DATA = 200       # kapasitas max array
DATA_FILE = "workout_data.json"

# array statis utama — ukurannya tetap MAX_DATA
data_workout = [None] * MAX_DATA
n_workout = 0   # banyak data yang aktif sekarang


# ==================================================
# SUBPROGRAM
# ==================================================

def hitung_kalori(jenis: str, durasi: int) -> int:
    # hitung_kalori(jenis, durasi) -> integer
    # mengitung berapa kalori yang terbakar berdasarkan jenis dan durasi
    # kalori/menit diambil dari tabel, kalau tidak ada pakai default
    kalori_per_menit = KALORI_PER_MENIT.get(jenis, KALORI_DEFAULT)
    kalori = kalori_per_menit * durasi
    return kalori


def load_data():
    # load_data() -> -
    # baca file JSON lalu masukin ke array statis global
    # kalau filenya tidak ada / rusak, n_workout tetap 0
    global data_workout, n_workout
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                raw = json.load(f)
            n_workout = 0
            i = 0
            while i < len(raw) and n_workout < MAX_DATA:
                item = raw[i]
                data_workout[n_workout] = DataWorkout(
                    id=item['id'],
                    jenis=item['jenis'],
                    durasi=item['durasi'],
                    kalori=item['kalori'],
                    tanggal=item['tanggal']
                )
                n_workout += 1
                i += 1
        except Exception:
            n_workout = 0


def save_data():
    # save_data() -> -
    # simpan isi array ke file JSON
    hasil = []
    i = 0
    while i < n_workout:
        w = data_workout[i]
        hasil.append({
            'id': w.id,
            'jenis': w.jenis,
            'durasi': w.durasi,
            'kalori': w.kalori,
            'tanggal': w.tanggal
        })
        i += 1
    with open(DATA_FILE, 'w') as f:
        json.dump(hasil, f, indent=4)


def tambah_data(jenis: str, durasi: int, kalori: int, tanggal: str) -> bool:
    # tambah_data(jenis, durasi, kalori, tanggal) -> boolean
    # masukkan satu data baru ke array di posisi n_workout
    # return False kalau array sudah penuh
    global n_workout
    if n_workout >= MAX_DATA:
        return False
    id_baru = n_workout + 1
    data_workout[n_workout] = DataWorkout(
        id=id_baru,
        jenis=jenis,
        durasi=durasi,
        kalori=kalori,
        tanggal=tanggal
    )
    n_workout += 1
    return True


def hapus_data_by_index(idx: int):
    # hapus_data_by_index(idx) -> -
    # hapus elemen di indeks idx, geser semua yang di belakangnya ke kiri
    # terus reset ulang ID agar tetap urut
    global n_workout
    i = idx
    while i < n_workout - 1:
        data_workout[i] = data_workout[i + 1]
        i += 1
    data_workout[n_workout - 1] = None
    n_workout -= 1
    # membenarkan ID supaya tidak loncat-loncat
    i = 0
    while i < n_workout:
        data_workout[i].id = i + 1
        i += 1


def cari_index_by_id(id_cari: int) -> int:
    # cari_index_by_id(id_cari) -> integer
    # sequential search untuk cari posisi data berdasarkan ID
    # return -1 kalau tiddak ketemu
    idx = -1
    i = 0
    while i < n_workout and idx == -1:
        if data_workout[i].id == id_cari:
            idx = i
        i += 1
    return idx


def sequential_search(jenis_cari: str) -> list:
    # sequential_search(jenis_cari) -> list of DataWorkout
    # cari semua data yang jenisnya cocok, scan dari awal sampai akhir
    hasil = []
    i = 0
    while i < n_workout:
        if data_workout[i].jenis.lower() == jenis_cari.lower():
            hasil.append(data_workout[i])
        i += 1
    return hasil


def _salin_array_ke_list() -> list:
    # _salin_array_ke_list() -> list of DataWorkout
    # membuat salinan data aktif ke list biasa
    # dipakai sebelum sorting supaya array asli tidak ikut berubah
    hasil = []
    i = 0
    while i < n_workout:
        w = data_workout[i]
        hasil.append(DataWorkout(
            id=w.id,
            jenis=w.jenis,
            durasi=w.durasi,
            kalori=w.kalori,
            tanggal=w.tanggal
        ))
        i += 1
    return hasil


def binary_search(jenis_cari: str) -> list:
    # binary_search(jenis_cari) -> list of DataWorkout
    # cari data berdasarkan jenis pakai binary search
    # karena data asli urutan ID, di sini di-sort dulu sementara berdasarkan jenis
    # setelah bertemu satu indeks, ekspansi ke kiri-kanan untuk ambil yang dobel

    # sort salinan dulu memakai insertion sort by jenis
    arr = _salin_array_ke_list()
    n = len(arr)
    i = 1
    while i < n:
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j].jenis.lower() > key.jenis.lower():
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
        i += 1

    # binary search — memakai flag idx_tengah 
    left = 0
    right = n - 1
    idx_tengah = -1
    while left <= right and idx_tengah == -1:
        mid = (left + right) // 2
        if arr[mid].jenis.lower() == jenis_cari.lower():
            idx_tengah = mid
        elif arr[mid].jenis.lower() < jenis_cari.lower():
            left = mid + 1
        else:
            right = mid - 1

    # jika ketemu, kumpulkan semua yang sama di sekitar posisi itu
    hasil = []
    if idx_tengah != -1:
        hasil.append(arr[idx_tengah])
        k = idx_tengah - 1
        while k >= 0 and arr[k].jenis.lower() == jenis_cari.lower():
            hasil.append(arr[k])
            k -= 1
        k = idx_tengah + 1
        while k < n and arr[k].jenis.lower() == jenis_cari.lower():
            hasil.append(arr[k])
            k += 1
    return hasil


def selection_sort(ascending: bool) -> list:
    # selection_sort(ascending) -> list of DataWorkout
    # urutkan data berdasarkan kalori memakaiselection sort
    # ascending=True -> dari kecil ke besar, False -> sebaliknya
    arr = _salin_array_ke_list()
    n = len(arr)
    i = 0
    while i < n - 1:
        idx_ekstrema = i
        j = i + 1
        while j < n:
            if ascending:
                if arr[j].kalori < arr[idx_ekstrema].kalori:
                    idx_ekstrema = j
            else:
                if arr[j].kalori > arr[idx_ekstrema].kalori:
                    idx_ekstrema = j
            j += 1
        arr[i], arr[idx_ekstrema] = arr[idx_ekstrema], arr[i]
        i += 1
    return arr


def insertion_sort(ascending: bool) -> list:
    # insertion_sort(ascending) -> list of DataWorkout
    # urutkan data berdasarkan durasi memakai insertion sort
    # ascending=True -> dari kecil ke besar, False -> sebaliknya
    arr = _salin_array_ke_list()
    i = 1
    while i < len(arr):
        key = arr[i]
        j = i - 1
        if ascending:
            while j >= 0 and arr[j].durasi > key.durasi:
                arr[j + 1] = arr[j]
                j -= 1
        else:
            while j >= 0 and arr[j].durasi < key.durasi:
                arr[j + 1] = arr[j]
                j -= 1
        arr[j + 1] = key
        i += 1
    return arr


# ==================================================
# GUI
# ==================================================

class WorkoutApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Workout Harian")
        self.root.geometry("950x650")
        self.root.minsize(800, 550)
        load_data()
        self._build_ui()

    def _build_ui(self):
        sidebar = ttk.Frame(self.root, bootstyle="dark", width=180)
        sidebar.pack(side=LEFT, fill=Y)
        sidebar.pack_propagate(False)

        ttk.Label(
            sidebar, text="WORKOUT\nHARIAN",
            font=("Helvetica", 14, "bold"),
            bootstyle="inverse-dark",
            justify=CENTER
        ).pack(pady=(20, 5))

        ttk.Separator(sidebar, bootstyle="secondary").pack(fill=X, padx=15, pady=10)

        ttk.Label(sidebar, text="Tema:", bootstyle="inverse-dark", font=("Helvetica", 9)).pack(anchor=W, padx=12)
        self.var_tema = ttk.StringVar(value="flatly")
        tema_list = ["flatly", "darkly", "cyborg", "journal", "litera", "lumen", "minty",
                     "pulse", "sandstone", "simplex", "sketchy", "solar", "superhero",
                     "united", "vapor", "yeti"]
        cb_tema = ttk.Combobox(sidebar, textvariable=self.var_tema, values=tema_list, state="readonly", width=15)
        cb_tema.pack(padx=10, pady=(2, 5))
        cb_tema.bind("<<ComboboxSelected>>", self._ganti_tema)

        menu_items = [
            ("  Tambah Workout", "success", self.show_tambah),
            ("  Semua Data",     "info",    self.show_semua),
            ("  Cari Workout",   "warning", self.show_cari),
            ("  Urutkan",        "primary", self.show_urutkan),
            ("  Rekomendasi",    "secondary", self.show_rekomendasi),
            ("  10 Terakhir",    "secondary", self.show_10_terakhir),
            ("  Per Periode",    "secondary", self.show_periode),
        ]

        for label, style, cmd in menu_items:
            ttk.Button(
                sidebar, text=label, bootstyle=f"{style}-outline",
                command=cmd, width=18
            ).pack(pady=3, padx=10)

        self.content_area = ttk.Frame(self.root)
        self.content_area.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)

        self.show_semua()

    def _ganti_tema(self, event=None):
        tema = self.var_tema.get()
        self.root.style.theme_use(tema)

    def _clear_content(self):
        for widget in self.content_area.winfo_children():
            widget.destroy()

    # ===== TAMBAH WORKOUT =====

    def show_tambah(self):
        self._clear_content()

        ttk.Label(self.content_area, text="Tambah Workout Baru",
                  font=("Helvetica", 16, "bold")).pack(anchor=W, pady=(0, 10))
        ttk.Separator(self.content_area).pack(fill=X, pady=(0, 15))

        form = ttk.Frame(self.content_area)
        form.pack(fill=X, padx=20)

        ttk.Label(form, text="Jenis Workout:").grid(row=0, column=0, sticky=W, pady=8)
        self.var_jenis = ttk.StringVar(value="Lari")
        cb_jenis = ttk.Combobox(form, textvariable=self.var_jenis,
                                values=list(KALORI_PER_MENIT.keys()), width=22)
        cb_jenis.grid(row=0, column=1, sticky=W, padx=10, pady=8)
        cb_jenis.bind("<<ComboboxSelected>>", self._update_kalori_preview)
        cb_jenis.bind("<KeyRelease>", self._update_kalori_preview)
        ttk.Label(form, text="(pilih atau ketik sendiri)",
                  font=("Helvetica", 8), bootstyle="secondary").grid(row=0, column=2, sticky=W)

        ttk.Label(form, text="Durasi (menit):").grid(row=1, column=0, sticky=W, pady=8)
        self.var_durasi = ttk.IntVar(value=30)
        spin_durasi = ttk.Spinbox(form, from_=1, to=300, textvariable=self.var_durasi,
                                  width=10, command=self._update_kalori_preview)
        spin_durasi.grid(row=1, column=1, sticky=W, padx=10, pady=8)
        spin_durasi.bind("<KeyRelease>", self._update_kalori_preview)

        ttk.Label(form, text="Kalori (otomatis):").grid(row=2, column=0, sticky=W, pady=8)
        self.var_kalori_preview = ttk.StringVar(value="300 kalori")
        ttk.Label(form, textvariable=self.var_kalori_preview,
                  font=("Helvetica", 12, "bold"), bootstyle="success").grid(
            row=2, column=1, sticky=W, padx=10, pady=8)

        ttk.Label(form, text="Tanggal (YYYY-MM-DD):").grid(row=3, column=0, sticky=W, pady=8)
        self.var_tanggal = ttk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        ttk.Entry(form, textvariable=self.var_tanggal, width=15).grid(
            row=3, column=1, sticky=W, padx=10, pady=8)

        self._update_kalori_preview()

        ttk.Button(
            self.content_area, text="SIMPAN WORKOUT",
            bootstyle="success", command=self._simpan_workout
        ).pack(pady=20, ipadx=10, ipady=5)

    def _update_kalori_preview(self, event=None):
        # update label preview kalori setiap kali jenis/durasi berubah
        try:
            jenis = self.var_jenis.get().strip()
            durasi = int(self.var_durasi.get())
            kalori = hitung_kalori(jenis, durasi)
            kpm = KALORI_PER_MENIT.get(jenis, KALORI_DEFAULT)
            custom = " (custom)" if jenis not in KALORI_PER_MENIT else ""
            self.var_kalori_preview.set(f"{kalori} kalori  [{kpm} kal/menit{custom}]")
        except Exception:
            self.var_kalori_preview.set("- kalori")

    def _simpan_workout(self):
        # validasi input dahulu sebelum disimpan
        try:
            jenis = self.var_jenis.get().strip()
            if not jenis:
                raise ValueError
            durasi = int(self.var_durasi.get())
            if durasi <= 0:
                raise ValueError
            tanggal = self.var_tanggal.get()
            datetime.strptime(tanggal, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error",
                "Jenis workout tidak boleh kosong, durasi harus angka positif, "
                "dan tanggal format YYYY-MM-DD!")
            return

        if n_workout >= MAX_DATA:
            messagebox.showerror("Error", f"Data penuh! Maksimum {MAX_DATA} entri.")
            return

        kalori = hitung_kalori(jenis, durasi)
        tambah_data(jenis, durasi, kalori, tanggal)
        save_data()
        messagebox.showinfo("Berhasil", f"Workout berhasil ditambahkan!\nKalori terbakar: {kalori}")
        self.show_semua()

    # ===== SEMUA DATA =====

    def show_semua(self):
        self._clear_content()

        ttk.Label(self.content_area, text="Semua Data Workout",
                  font=("Helvetica", 16, "bold")).pack(anchor=W, pady=(0, 10))
        ttk.Separator(self.content_area).pack(fill=X, pady=(0, 10))

        # menghitung total kalori manual dari array
        total_kalori = 0
        i = 0
        while i < n_workout:
            total_kalori += data_workout[i].kalori
            i += 1

        stats_frame = ttk.Frame(self.content_area)
        stats_frame.pack(fill=X, pady=(0, 10))

        card1 = ttk.Frame(stats_frame, bootstyle="primary")
        card1.pack(side=LEFT, padx=(0, 8))
        ttk.Label(card1, text="Total Workout", font=("Helvetica", 10)).pack(padx=15, pady=(8, 0))
        ttk.Label(card1, text=str(n_workout),
                  font=("Helvetica", 16, "bold"), bootstyle="primary").pack(padx=15, pady=(0, 8))

        card2 = ttk.Frame(stats_frame, bootstyle="danger")
        card2.pack(side=LEFT)
        ttk.Label(card2, text="Total Kalori", font=("Helvetica", 10)).pack(padx=15, pady=(8, 0))
        ttk.Label(card2, text=f"{total_kalori} kal",
                  font=("Helvetica", 16, "bold"), bootstyle="danger").pack(padx=15, pady=(0, 8))

        cols = ("ID", "Jenis", "Durasi (menit)", "Kalori", "Tanggal")
        tree_frame = ttk.Frame(self.content_area)
        tree_frame.pack(fill=BOTH, expand=True)

        tree = ttk.Treeview(tree_frame, columns=cols, show="headings", height=15, bootstyle="primary")
        for col in cols:
            tree.heading(col, text=col)
        tree.column("ID", width=40, anchor=CENTER)
        tree.column("Jenis", width=120)
        tree.column("Durasi (menit)", width=100, anchor=CENTER)
        tree.column("Kalori", width=80, anchor=CENTER)
        tree.column("Tanggal", width=100, anchor=CENTER)

        i = 0
        while i < n_workout:
            w = data_workout[i]
            tree.insert("", END, values=(w.id, w.jenis, w.durasi, w.kalori, w.tanggal))
            i += 1

        scrollbar = ttk.Scrollbar(tree_frame, orient=VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=LEFT, fill=Y)

        btn_frame = ttk.Frame(self.content_area)
        btn_frame.pack(fill=X, pady=8)
        ttk.Button(btn_frame, text="Ubah Data Terpilih", bootstyle="warning-outline",
                   command=lambda: self._ubah_terpilih(tree)).pack(side=LEFT, padx=4)
        ttk.Button(btn_frame, text="Hapus Data Terpilih", bootstyle="danger-outline",
                   command=lambda: self._hapus_terpilih(tree)).pack(side=LEFT, padx=4)

    def _ubah_terpilih(self, tree):
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Peringatan", "Pilih data yang ingin diubah!")
            return
        id_ubah = tree.item(selected[0])['values'][0]
        self._show_form_ubah(id_ubah)

    def _hapus_terpilih(self, tree):
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Peringatan", "Pilih data yang ingin dihapus!")
            return
        item = tree.item(selected[0])
        id_hapus = item['values'][0]
        jenis = item['values'][1]
        if messagebox.askyesno("Konfirmasi", f"Hapus workout '{jenis}' (ID {id_hapus})?"):
            idx = cari_index_by_id(id_hapus)
            if idx != -1:
                hapus_data_by_index(idx)
                save_data()
                messagebox.showinfo("Berhasil", "Data berhasil dihapus!")
                self.show_semua()

    def _show_form_ubah(self, id_ubah):
        # cari datanya dulu sebelum memunculkan form
        idx = cari_index_by_id(id_ubah)
        if idx == -1:
            return
        target = data_workout[idx]

        popup = ttk.Toplevel(self.root)
        popup.title(f"Ubah Workout ID {id_ubah}")
        popup.geometry("400x280")
        popup.grab_set()

        ttk.Label(popup, text=f"Ubah: {target.jenis}",
                  font=("Helvetica", 13, "bold")).pack(pady=15)

        form = ttk.Frame(popup)
        form.pack(padx=20)

        ttk.Label(form, text="Durasi baru (menit):").grid(row=0, column=0, sticky=W, pady=8)
        var_dur = ttk.IntVar(value=target.durasi)
        ttk.Spinbox(form, from_=1, to=300, textvariable=var_dur, width=10).grid(
            row=0, column=1, padx=10)

        ttk.Label(form, text="Tanggal:").grid(row=1, column=0, sticky=W, pady=8)
        var_tgl = ttk.StringVar(value=target.tanggal)
        ttk.Entry(form, textvariable=var_tgl, width=15).grid(row=1, column=1, padx=10)

        def simpan_ubah():
            try:
                durasi_baru = int(var_dur.get())
                tgl_baru = var_tgl.get()
                datetime.strptime(tgl_baru, "%Y-%m-%d")
            except Exception:
                messagebox.showerror("Error", "Input tidak valid!", parent=popup)
                return
            target.durasi = durasi_baru
            target.kalori = hitung_kalori(target.jenis, durasi_baru)
            target.tanggal = tgl_baru
            save_data()
            popup.destroy()
            messagebox.showinfo("Berhasil", f"Kalori otomatis update jadi {target.kalori}")
            self.show_semua()

        ttk.Button(popup, text="Simpan Perubahan", bootstyle="success",
                   command=simpan_ubah).pack(pady=15, ipadx=8, ipady=4)

    # ===== CARI WORKOUT =====

    def show_cari(self):
        self._clear_content()

        ttk.Label(self.content_area, text="Cari Workout",
                  font=("Helvetica", 16, "bold")).pack(anchor=W, pady=(0, 10))
        ttk.Separator(self.content_area).pack(fill=X, pady=(0, 15))

        ctrl = ttk.Frame(self.content_area)
        ctrl.pack(fill=X)

        ttk.Label(ctrl, text="Jenis Workout:").pack(side=LEFT)
        self.var_cari = ttk.StringVar(value="Lari")
        ttk.Combobox(ctrl, textvariable=self.var_cari,
                     values=list(KALORI_PER_MENIT.keys()), state="readonly",
                     width=18).pack(side=LEFT, padx=8)

        ttk.Label(ctrl, text="Metode:").pack(side=LEFT)
        self.var_metode = ttk.StringVar(value="Sequential")
        ttk.Radiobutton(ctrl, text="Sequential", variable=self.var_metode,
                        value="Sequential").pack(side=LEFT, padx=4)
        ttk.Radiobutton(ctrl, text="Binary", variable=self.var_metode,
                        value="Binary").pack(side=LEFT, padx=4)

        ttk.Button(ctrl, text="Cari", bootstyle="warning",
                   command=self._lakukan_cari).pack(side=LEFT, padx=10)

        self.frame_hasil_cari = ttk.Frame(self.content_area)
        self.frame_hasil_cari.pack(fill=BOTH, expand=True, pady=10)

    def _lakukan_cari(self):
        for w in self.frame_hasil_cari.winfo_children():
            w.destroy()

        jenis = self.var_cari.get()
        metode = self.var_metode.get()

        if metode == "Sequential":
            hasil = sequential_search(jenis)
        else:
            hasil = binary_search(jenis)

        ttk.Label(self.frame_hasil_cari,
                  text=f"Hasil {metode} Search untuk '{jenis}': {len(hasil)} data ditemukan",
                  bootstyle="info").pack(anchor=W, pady=5)

        if hasil:
            cols = ("ID", "Jenis", "Durasi", "Kalori", "Tanggal")
            tree = ttk.Treeview(self.frame_hasil_cari, columns=cols, show="headings",
                                height=8, bootstyle="warning")
            for col in cols:
                tree.heading(col, text=col)
            for w in hasil:
                tree.insert("", END, values=(w.id, w.jenis, w.durasi, w.kalori, w.tanggal))
            tree.pack(fill=X)
        else:
            ttk.Label(self.frame_hasil_cari, text="Tidak ditemukan!", bootstyle="danger").pack()

    # ===== URUTKAN =====

    def show_urutkan(self):
        self._clear_content()

        ttk.Label(self.content_area, text="Urutkan Workout",
                  font=("Helvetica", 16, "bold")).pack(anchor=W, pady=(0, 10))
        ttk.Separator(self.content_area).pack(fill=X, pady=(0, 15))

        ctrl = ttk.Frame(self.content_area)
        ctrl.pack(fill=X)

        ttk.Label(ctrl, text="Metode:").pack(side=LEFT)
        self.var_sort = ttk.StringVar(value="Selection")
        ttk.Radiobutton(ctrl, text="Selection Sort (Kalori)", variable=self.var_sort,
                        value="Selection").pack(side=LEFT, padx=8)
        ttk.Radiobutton(ctrl, text="Insertion Sort (Durasi)", variable=self.var_sort,
                        value="Insertion").pack(side=LEFT, padx=8)

        ttk.Label(ctrl, text="Urutan:").pack(side=LEFT, padx=(15, 0))
        self.var_urut = ttk.StringVar(value="Ascending")
        ttk.Radiobutton(ctrl, text="Ascending", variable=self.var_urut,
                        value="Ascending").pack(side=LEFT, padx=4)
        ttk.Radiobutton(ctrl, text="Descending", variable=self.var_urut,
                        value="Descending").pack(side=LEFT, padx=4)

        ttk.Button(ctrl, text="Urutkan", bootstyle="primary",
                   command=self._lakukan_sort).pack(side=LEFT, padx=15)

        self.frame_hasil_sort = ttk.Frame(self.content_area)
        self.frame_hasil_sort.pack(fill=BOTH, expand=True, pady=10)

    def _lakukan_sort(self):
        for w in self.frame_hasil_sort.winfo_children():
            w.destroy()

        ascending = self.var_urut.get() == "Ascending"
        metode = self.var_sort.get()

        if metode == "Selection":
            data = selection_sort(ascending)
            label_sort = "Selection Sort by Kalori"
        else:
            data = insertion_sort(ascending)
            label_sort = "Insertion Sort by Durasi"

        urutan = "Ascending" if ascending else "Descending"
        ttk.Label(self.frame_hasil_sort,
                  text=f"Hasil {label_sort} ({urutan})",
                  bootstyle="info").pack(anchor=W, pady=5)

        cols = ("ID", "Jenis", "Durasi (menit)", "Kalori", "Tanggal")
        tree = ttk.Treeview(self.frame_hasil_sort, columns=cols, show="headings",
                            height=12, bootstyle="primary")
        for col in cols:
            tree.heading(col, text=col)
        for w in data:
            tree.insert("", END, values=(w.id, w.jenis, w.durasi, w.kalori, w.tanggal))
        tree.pack(fill=X)

    # ===== REKOMENDASI =====

    def show_rekomendasi(self):
        self._clear_content()

        ttk.Label(self.content_area, text="Rekomendasi",
                  font=("Helvetica", 16, "bold")).pack(anchor=W, pady=(0, 10))
        ttk.Separator(self.content_area).pack(fill=X, pady=(0, 15))

        if n_workout == 0:
            ttk.Label(self.content_area, text="Belum ada data workout!",
                      bootstyle="danger").pack()
            return

        # hitung frekuensi tiap jenis
        frek = {}
        i = 0
        while i < n_workout:
            j = data_workout[i].jenis
            if j in frek:
                frek[j] += 1
            else:
                frek[j] = 1
            i += 1

        paling_sering = max(frek, key=frek.get)

        total_durasi = 0
        total_kalori = 0
        i = 0
        while i < n_workout:
            total_durasi += data_workout[i].durasi
            total_kalori += data_workout[i].kalori
            i += 1
        rata_durasi = total_durasi // n_workout
        rata_kalori = total_kalori // n_workout

        info_frame = ttk.Frame(self.content_area)
        info_frame.pack(fill=X, pady=5)

        infos = [
            ("Workout Favorit", paling_sering, "success"),
            ("Rata-rata Durasi", f"{rata_durasi} menit", "info"),
            ("Rata-rata Kalori", f"{rata_kalori} kalori", "danger"),
        ]
        for label, val, style in infos:
            row = ttk.Frame(info_frame)
            row.pack(fill=X, pady=4)
            ttk.Label(row, text=label + ":", width=20, anchor=W,
                      font=("Helvetica", 11)).pack(side=LEFT)
            ttk.Label(row, text=val, bootstyle=style,
                      font=("Helvetica", 11, "bold")).pack(side=LEFT)

        ttk.Separator(self.content_area).pack(fill=X, pady=10)

        rec_text = (f"Rekomendasi: Lakukan {paling_sering} selama {rata_durasi} menit "
                    f"untuk membakar ~{hitung_kalori(paling_sering, rata_durasi)} kalori!")
        ttk.Label(self.content_area, text=rec_text, font=("Helvetica", 12),
                  bootstyle="success", wraplength=600).pack(anchor=W, pady=5)

        ttk.Label(self.content_area, text="Frekuensi Per Jenis:",
                  font=("Helvetica", 12, "bold")).pack(anchor=W, pady=(15, 5))

        max_frek = max(frek.values())
        for jenis, count in sorted(frek.items(), key=lambda x: x[1], reverse=True):
            row = ttk.Frame(self.content_area)
            row.pack(fill=X, pady=3)
            ttk.Label(row, text=jenis, width=16, anchor=W).pack(side=LEFT)
            bar = ttk.Progressbar(row, value=count, maximum=max_frek,
                                  bootstyle="success-striped", length=250)
            bar.pack(side=LEFT, padx=8)
            ttk.Label(row, text=f"{count}x").pack(side=LEFT)

    # ===== 10 TERAKHIR =====

    def show_10_terakhir(self):
        self._clear_content()

        ttk.Label(self.content_area, text="10 Aktivitas Terakhir",
                  font=("Helvetica", 16, "bold")).pack(anchor=W, pady=(0, 10))
        ttk.Separator(self.content_area).pack(fill=X, pady=(0, 15))

        if n_workout == 0:
            ttk.Label(self.content_area, text="Belum ada data!", bootstyle="danger").pack()
            return

        # sort salinan berdasarkan tanggal descending memakai insertion sort
        arr = _salin_array_ke_list()
        n = len(arr)
        i = 1
        while i < n:
            key = arr[i]
            j = i - 1
            while j >= 0 and arr[j].tanggal < key.tanggal:
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = key
            i += 1

        # ambil 10 teratas
        terbaru = []
        i = 0
        while i < n and i < 10:
            terbaru.append(arr[i])
            i += 1

        cols = ("Tanggal", "Jenis", "Durasi (menit)", "Kalori")
        tree = ttk.Treeview(self.content_area, columns=cols, show="headings",
                            height=12, bootstyle="info")
        for col in cols:
            tree.heading(col, text=col)
        tree.column("Tanggal", width=110, anchor=CENTER)
        tree.column("Jenis", width=130)
        tree.column("Durasi (menit)", width=110, anchor=CENTER)
        tree.column("Kalori", width=90, anchor=CENTER)
        for w in terbaru:
            tree.insert("", END, values=(w.tanggal, w.jenis, w.durasi, w.kalori))
        tree.pack(fill=X)

    # ===== PER PERIODE =====

    def show_periode(self):
        self._clear_content()

        ttk.Label(self.content_area, text="Total Kalori per Periode",
                  font=("Helvetica", 16, "bold")).pack(anchor=W, pady=(0, 10))
        ttk.Separator(self.content_area).pack(fill=X, pady=(0, 15))

        ctrl = ttk.Frame(self.content_area)
        ctrl.pack(fill=X)

        ttk.Label(ctrl, text="Pilih Periode:").pack(side=LEFT)
        self.var_periode = ttk.StringVar(value="Hari ini")
        for opt in ["Hari ini", "Minggu ini", "Bulan ini"]:
            ttk.Radiobutton(ctrl, text=opt, variable=self.var_periode,
                            value=opt).pack(side=LEFT, padx=8)
        ttk.Button(ctrl, text="Hitung", bootstyle="primary",
                   command=self._hitung_periode).pack(side=LEFT, padx=15)

        self.frame_hasil_periode = ttk.Frame(self.content_area)
        self.frame_hasil_periode.pack(fill=BOTH, expand=True, pady=15)

    def _hitung_periode(self):
        for w in self.frame_hasil_periode.winfo_children():
            w.destroy()

        today = datetime.now().date()
        pilih = self.var_periode.get()

        if pilih == "Hari ini":
            start = today
            end = today
        elif pilih == "Minggu ini":
            start = today - timedelta(days=today.weekday())
            end = start + timedelta(days=6)
        else:
            start = today.replace(day=1)
            if today.month == 12:
                end = today.replace(year=today.year + 1, month=1, day=1) - timedelta(days=1)
            else:
                end = today.replace(month=today.month + 1, day=1) - timedelta(days=1)

        total = 0
        detail = []
        i = 0
        while i < n_workout:
            w = data_workout[i]
            tgl = datetime.strptime(w.tanggal, '%Y-%m-%d').date()
            if start <= tgl <= end:
                total += w.kalori
                detail.append(w)
            i += 1

        ttk.Label(self.frame_hasil_periode,
                  text=f"Periode: {start} s.d. {end}",
                  bootstyle="secondary").pack(anchor=W)
        ttk.Label(self.frame_hasil_periode,
                  text=f"Total Kalori: {total} kalori",
                  font=("Helvetica", 18, "bold"), bootstyle="danger").pack(anchor=W, pady=8)
        ttk.Label(self.frame_hasil_periode,
                  text=f"Jumlah Sesi: {len(detail)} workout").pack(anchor=W)

        if detail:
            ttk.Separator(self.frame_hasil_periode).pack(fill=X, pady=10)
            cols = ("Tanggal", "Jenis", "Durasi", "Kalori")
            tree = ttk.Treeview(self.frame_hasil_periode, columns=cols, show="headings",
                                height=8, bootstyle="danger")
            for col in cols:
                tree.heading(col, text=col)
            for w in detail:
                tree.insert("", END, values=(w.tanggal, w.jenis, w.durasi, w.kalori))
            tree.pack(fill=X)


# ==================================================
# MAIN
# ==================================================
if __name__ == "__main__":
    app = ttk.Window(themename="flatly")
    WorkoutApp(app)
    app.mainloop()
