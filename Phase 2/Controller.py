from redis import *
from random import randint
from tkinter import *
import tkinter.messagebox as msg
from Model import *

class Regis_controller:
    user = User()
    def regis(self, jabatan, username, password):
        return self.user.set_user(jabatan, username, password)
    
class Adm_controller:
    user = User()
    def get_data(self, jabatan):
        return self.user.get_user(jabatan), self.user.get_user(jabatan, 1)
    
class Deleting_controller:
    user = User()
    def get_data(self, jabatan):
        return self.user.get_user(jabatan), self.user.get_user(jabatan, 1)
    def del_user(self, jabatan, value, idx = 1):
        return self.user.del_user(jabatan, idx, value)

class Login_controller:
    cli = Redis('localhost')
    admin = 'admin'
    client = 'client'
    jabatan = None
    nav_adm = None
    nav_cln = None

    def __init__(self,Navigation_admin,Client):
        self.nav_adm = Navigation_admin
        self.nav_cln = Client
    
    def check(self,username,password):
        for i in self.cli.lrange(self.admin,0,-1):
            b_user = str(i)[2:-1].split()[0]
            b_pass = str(i)[2:-1].split()[1]
            if b_user == username and b_pass == password:
                self.jabatan = self.admin
                self.w_client = None
        
        if self.jabatan == None:
            for j in self.cli.lrange(self.client,0,-1):
                b_user = str(j)[2:-1].split()[0]
                b_pass = str(j)[2:-1].split()[1]
                if b_user == username and b_pass == password:
                    self.jabatan = self.client
                    self.w_admin = None

        if self.jabatan == None:
            msg.showinfo("Announcement","Username atau password yang anda masukkan salah!")
        else:
            return True
            
    def navigation(self):
        if self.jabatan == self.admin:
            self.nav_cln = None
            self.nav_adm.set_window()
            self.nav_adm.show_window_admin()
        else:
            self.nav_adm = None
            self.nav_cln.set_window()
            self.nav_cln.show_window_client()
        return True
        

class Client_controller:
    cli = Redis('localhost')

    def cek_int(self,inp):
        try:
            int(inp)
            return False
        except:
            return True
    
    def get_packet(self): #UNTUK PELANGGAN MILIH ITU YANG OPTION MENU
        list_redis = self.cli.lrange('data paket',0,-1)
        name_packet = [str(i)[2:-1] for i in list_redis if 'stock' in str(self.cli.lrange(str(i)[2:-1],0,-1))]
        return name_packet

    def get_product(self,paket):
        return str(self.cli.lrange(paket,0,-1))[3:-2].split()

    def add_to_bucket(self,nama,jml,lb):
        if nama == 'Menu' or jml == '':
            msg.showinfo('Announcement!','Maaf pesanan anda belum lengkap\nSilahkan periksa menu atau jumlah pesanan!')
            return
        if self.cek_int(jml):
            msg.showinfo('Warning','Masukkan jumlah pesanan berupa angka!')
            return
        stock = self.get_product(nama)[-1]
        if int(jml) > int(stock) or int(stock) == 0:
            msg.showinfo('Announcement!','Maaf tolong periksa ketersediaan paketnya.\nCeknya dimenu "Show the packet"')
            return
        order = nama + ' ----> ' + jml
        lb.insert(END, order)
        return

    def get_rp(self,inp):
        mrg = ''
        for i in range(1,len(inp)+1,1):
            mrg += inp[-i]
            if (i % 3 == 0) and (i < len(inp)):
                mrg += '_'
        return mrg[::-1]
    
    def get_total(self,lb):
        g_lb1, g_lb2 = self.get_listbox(lb)
        unt = 0
        for i in range(len(g_lb1)):
            unt += self.get_total_harga(g_lb1[i],g_lb2[i])
        unt = self.get_rp(str(unt))
        return msg.showinfo("Total","Total harga: "+str(unt))

    def delete_from_bucket(self,lb):
        lb.delete(0,ANCHOR)
        return
    
    def delete_from_bucket_1(self,lb):
        lb.delete(END,ANCHOR)
        return

    def get_listbox(self,Lb1): #Harga bisa diambil dari sini
        ln = [0]*Lb1.size() #LIST_NAME
        lt = [0]*Lb1.size() #LIST_TOTAL
        
        for i in range(Lb1.size()):
            if len(Lb1.get(i).split()) > 3:
                nama1 = Lb1.get(i).split()[0:-2]
            else:
                nama1 = [Lb1.get(i).split()[0]]
            if len(nama1) != 1:
                nama = ''
                for n in range(len(nama1)):
                    nama += nama1[n] + ' '
                ln[i] = nama[:-1]
            else:
                ln[i] = nama1[0]
            lt[i] = Lb1.get(i).split()[-1]
            
        return ln,lt

    def get_total_harga(self,nama_paket,jml_pesan):
        data = self.get_product(nama_paket)
        unt = int(data[-3])*int(jml_pesan)
        return unt

    def cek_sama(self,inp1,inp2):
        mrg = ''
        for i in inp2:
            mrg = mrg + i + ' '
        mrg = mrg[:-1]
        return inp1 == mrg

    def get_untung(self,nama_paket,jml_pesan):
        data = self.get_product(nama_paket)
        modal = 0
        for i in self.cli.lrange('modal paket',0,-1):
            if self.cek_sama(nama_paket, str(i)[2:-1].split()[:-1]):
                modal = int(str(i)[2:-1].split()[-1])
        unt = (int(data[-3])-modal)*int(jml_pesan)
        return unt
    
    def set_unique(self,name_unik,total): #DIOPER PAS UDAH DIITUNG SEMUA BELANJAANNYA
        self.cli.rpush('kode unik',name_unik+' '+str(total))
        return

    def set_listing_day(self, nama, jumlah, today):
        data = self.cli.lrange('penjualan ' + nama,0,-1)
        bantu = None
        idx = 0
        ada = False
        for i in data:
            if today in str(i):
                bantu = str(i)[2:-1].split()[1]
                ada = True
                break
            else:
                idx += 1
        if ada:
            sets = today + ' ' + str(int(jumlah) + int(bantu))
            self.cli.lset('penjualan ' + nama, idx, sets)
        else:
            sets = today + ' ' + jumlah
            self.cli.rpush('penjualan ' + nama, sets)
        return

    def set_untung_today(self,jumlah,today):
        data_unt = self.cli.lrange('keuntungan',0,-1)
        bantu = None
        idx = 0
        ada = False
        for i in data_unt:
            if today in str(i):
                bantu = str(i)[2:-1].split()[1]
                ada = True
                break
            else:
                idx += 1
        if ada:
            sets = today + ' ' +str(jumlah+int(bantu))
            self.cli.lset('keuntungan',idx,sets)
        else:
            sets = today + ' ' + str(jumlah)
            self.cli.rpush('keuntungan',sets)
        return

    def get_something(self):
        data = '1234567890qwertyuiopasdfghjklzxcvbnm'
        thing = ''
        while len(thing)!= 5:
            thing += data[randint(0,len(data)-1)]

            if len(thing) == 5 and thing in str(self.cli.lrange('kode unik',0,-1)):
                thing = ''
        return thing

    def set_string(self,lists):
        mrg = ''
        for i in lists:
            mrg += i + ' '
        mrg = mrg[:-1]
        return mrg

    def set_buy_stock(self, nama, jml):
        paket = self.get_product(nama)
        paket[-1] = str(int(paket[-1]) - int(jml))
        self.cli.lset(nama, 0, self.set_string(paket))
        return

    def done(self,Lb1,tgl):
        list1,list2 = self.get_listbox(Lb1)

        if len(list1) == 0:
            msg.showinfo('Announcement','Silahkan memesan terlebih dahulu!')
            return
         
        total = 0
        unt = 0
        for i in range(len(list1)):
            self.set_listing_day(list1[i],list2[i],tgl)
            total += self.get_total_harga(list1[i],list2[i])
            unt += self.get_untung(list1[i],list2[i])
            self.set_buy_stock(list1[i], list2[i])
        self.set_untung_today(unt,tgl)
        code = self.get_something()
        unt = self.get_rp(str(unt))
        total = self.get_rp(str(total))
        self.set_unique(code, total)

        for i in range(len(list1)):
            self.delete_from_bucket(Lb1)
         
        msg.showinfo('Thankyou','Terima kasih telah memesan!\nPesanan anda seharga: '+ total +'\nKode unik anda: ' + code)
        return

class Kasir_controller:
    cli = Redis('localhost')

    def cek_int(self,inp):
        try:
            int(inp)
            return False
        except:
            return True
    
    def get_packet(self): #UNTUK PELANGGAN MILIH ITU YANG OPTION MENU
        list_redis = self.cli.lrange('data paket',0,-1)
        name_packet = [str(i)[2:-1] for i in list_redis if 'stock' in str(self.cli.lrange(str(i)[2:-1],0,-1))]
        return name_packet

    def get_unique(self):
        redis_unique = self.cli.lrange('kode unik',0,-1)
        data_unique = [0]*len(redis_unique)
        idx = 0
        for i in redis_unique:
            n = str(i)[2:-1].split()
            data_unique[idx] = n[0]
            idx += 1
            
        return data_unique

    def get_total_unique(self,kode):
        if kode == 'Pilih kode pembayaran':
            return None
        redis_unique = self.cli.lrange('kode unik',0,-1)
        hasil = None
        for i in redis_unique:
            if kode == str(i)[2:-1].split()[0]:
                hasil = str(i)[2:-1].split()[1]
        return hasil

    def get_rp(self,inp):
        mrg = ''
        for i in range(1,len(inp)+1,1):
            mrg += inp[-i]
            if (i % 3 == 0) and (i < len(inp)):
                mrg += '_'
        return mrg[::-1]

    def del_unique(self,kode,total):
        self.cli.lrem('kode unik',4,kode+' '+total)
        return
    
class Data_menu_controller:
    cli = Redis('localhost')
    
    def get_paket(self):
        return [str(i)[2:-1] for i in self.cli.lrange('data paket',0,-1)]

    def get_modal(self):
        return self.cli.lrange('modal paket',0,-1)

    def cek_sama(self,inp1,inp2):
        mrg = ''
        for i in inp2:
            mrg = mrg + i + ' '
        mrg = mrg[:-1]
        return inp1 == mrg
    
    def get_all_menu(self): #UNTUK MENU DI ADMIN, DIPRINT LEWAT LABELFRAME
        packet = self.get_paket()
        paket = {}
        modal = self.get_modal()
        for i in packet:
            data = str(self.cli.lrange(i,0,-1))[3:-2].split()
            cap = ''
            for n in range(0,len(data),2):
                cap = cap + data[n].replace('_',' ') + ' : ' + data[n+1] +', '
            for j in modal:
                if self.cek_sama(i, str(j)[2:-1].split()[:-1]):
                    cap = cap + 'modal : ' + str(j)[2:-1].split()[-1]
            paket[i] = cap
        return paket

class Data_tmenu_controller:
    cli = Redis('localhost')

    def cek_int(self, inp1, inp2 = 1):
        try:
            int(inp1)
            int(inp2)
            return False
        except:
            return True

    def cek_paket(self,nama):
        data_paket = [str(i)[2:-1] for i in self.cli.lrange('data paket',0,-1)]
        if nama in data_paket:
            return True
        return False
    
    def set_packet_to_redis(self, nama, daftar, harga):
        if len(daftar) % 2 == 1:
            msg.showinfo('WARNING','BAGIAN ITEMS TIDAK SESUAI')
            return 'err'
        
        self.cli.rpush('data paket',nama)
        gabung = ''
        
        for i in range(0,len(daftar),2):
            gabung += daftar[i] + ' ' + daftar[i+1] + ' '
        
        gabung = gabung + 'price ' + harga + ' stock 0'

        self.cli.rpush(nama, gabung) #Kurang Stock
        return 'scc'

    def set_modal_to_redis(self, nama, modal):
        self.cli.rpush('modal paket', nama + ' ' + modal)
        return

    def pop_up_success(self):
        msg.showinfo('Announcement','Success!')
        
    def pop_up(self, kondisi):
        if kondisi == 'kosong':
            msg.showinfo('WARNING','Masukkan data dengan benar!')
            return
        else:
            msg.showinfo('WARNING','Nama paket yang anda masukkan sudah terdaftar!')
            return

class Data_hrg_controller:
    cli = Redis('localhost')

    def cek_int(self,inp):
        try:
            int(inp)
            return False
        except:
            return True

    def get_packet(self):
        return [str(i)[2:-1] for i in self.cli.lrange('data paket',0,-1)]

    def pop_up(self):
        msg.showinfo('WARNING','Masukkan data dengan benar!')
    
    def set_change_price(self, nama, harga):
        if nama == '' or harga == '':
            self.pop_up()
            return
        if self.cek_int(harga):
            msg.showinfo('WARNING','Masukkan harga baru berupa angka!')
            return
        data = str(self.cli.lrange(nama,0,-1))[3:-2].split()
        if data[-2] != 'stock':
            data[-1] = harga
            self.set_to_redis(data)
            return
        data[-3] = harga
        self.set_to_redis(nama, data)
        return

    def set_to_redis(self, nama, data):
        mrg = ''
        for i in data:
            mrg += i + ' '
        self.cli.lset(nama,0,mrg[:-1])
        self.pop_up_success()
    
    def pop_up_success(self):
        msg.showinfo('Announcement','Success!')

class Data_stck_controller:
    cli = Redis('localhost')

    def cek_int(self,inp):
        try:
            int(inp)
            return False
        except:
            return True

    def get_packet(self):
        return [str(i)[2:-1] for i in self.cli.lrange('data paket',0,-1)]   

    def pop_up(self):
        msg.showinfo('WARNING','Masukkan data dengan benar!')
    
    def set_stock_to_redis(self, nama, stock):
        if nama == '' or stock == '':
            self.pop_up()
            return
        if self.cek_int(stock):
            msg.showinfo('WARNING','Masukkan stock berupa angka!')
            return
        data = str(self.cli.lrange(nama,0,-1))[3:-2].split()
        data[-1] = stock
        self.set_to_redis(nama, data)
        return

    def set_to_redis(self, nama, data):
        mrg = ''
        for i in data:
            mrg += i + ' '
        self.cli.lset(nama,0,mrg[:-1])
        self.pop_up_success()

    def pop_up_success(self):
        msg.showinfo('Announcement','Success!')
