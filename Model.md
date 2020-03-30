# Back-end process

## Login
Proses yang dilalui paling pertama adalah login, jika tidak berhasil maka tidak akan lanjut, jika berhasil akan lanjut sebagai user
tertentu sesuai dengan posisinya (dalam hal ini adalah: client atau admin).

## Admin
Pada bagian admin akan dibagi menjadi beberapa bentuk peran:
 1. Kasir.
 1. Pengatur menu (menambahkan menu baru).
 1. Pengatur harga baru terhadap menu yang telah ada.
 1. Pengatur stock.
---
Kasir bertugas sebagai pembantu client untuk membayarkan bill-nya untuk mendapatkan makanan dengan cara menyesuaikan kode unik dari
bill dengan data kode unik yang tersedia.

Pengatur menu bertugas apabila ada ide paket menu baru, maka ini bertugas untuk menambahkan menu ke dalam database.

Pengatur harga baru bertugas untuk memperbarui harga paket yang lama menjadi harga paket yang baru.

Pengatur stock bertugas menyesuaikan data asli dengan data yang ada di database, apabila stock baru saja ditambah atau terjadi suatu
kesalahan pada database yang membuatnya sedikit error.

## Client
Bertugas untuk memesan menu makanan yang diinginkan, membayarnya (untuk membayar harus ke sisi admin kasir terlebih dulu), saat client memesan menu, client dapat melihat isi dari suatu paket menu dan juga jika client tidak jadi untuk menambahkan suatu menu tersedia fungsi untuk menghapusnya dari daftar menu yang telah dipilih.

## Akhir
Jika sudah selesai memakai maka dapat dikeluarkan atau logout.
