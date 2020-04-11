import tkinter.messagebox as msg

try:
    from redis import *
except:
    msg.showinfo("Warning","Install redis terlebih dahulu dengan pip")
    exit()

data_paket = ['Paket A','Paket B','Paket C']
isi_paket = {'Paket A':'Ayam_goreng 2 Nasi_putih 2 Es_teh_manis 2 harga 50_000 stock 20',
             'Paket B':'Ikan_goreng 2 Nasi_putih 2 Es_kelapa 2 harga 75_000 stock 20',
             'Paket C':'Belut_goreng 3 Nasi_putih 2 Es_jeruk 2 harga 85_000 stock 20',}
modal_paket = {'Paket A':'30_000','Paket B':'45_000','Paket C':'45_000'}
keuntungan = ['29/03/2020 500_000','30/03/2020 750_000']
penjualanA = ['29/03/2020 5','30/03/2020 10']
penjualanB = ['29/03/2020 0','30/03/2020 5']
penjualanC = ['29/03/2020 10','30/03/2020 10']
unique = ['wdy10 100_000','09sdj 125_000','29018 135_000','1jdp2 160_000']
cli = Redis('localhost')
cli.rpush('admin','admin admin')
cli.rpush('client','client client')
for i in data_paket:
    cli.rpush('data paket',i)
    cli.rpush(i,isi_paket[i])
    cli.rpush('modal paket',i + ' ' + modal_paket[i])
    if i == 'Paket A':
        cli.rpush('penjualan '+i,penjualanA[0])
        cli.rpush('penjualan '+i,penjualanA[1])
    elif i == 'Paket B':
        cli.rpush('penjualan '+i,penjualanB[0])
        cli.rpush('penjualan '+i,penjualanB[1])
    else:
        cli.rpush('penjualan '+i,penjualanC[0])
        cli.rpush('penjualan '+i,penjualanC[1])
        cli.rpush('keuntungan',keuntungan[0])
        cli.rpush('keuntungan',keuntungan[1])
        for n in unique:
            cli.rpush('kode unik',n)

msg.showinfo("Information","Sukses\nSekarang jalankan file 'Run to start (View)'\nUsername: admin, Password: admin\nUsername: client, Password: client")
