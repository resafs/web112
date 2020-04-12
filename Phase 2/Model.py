from redis import *
import tkinter.messagebox as msg

class User:
    cli = Redis('localhost')
    def get_user(self, jabatan, idx = 0):
        return [str(i)[2:-1].split()[idx] for i in self.cli.lrange(jabatan, 0, -1)]

    def set_user(self, jabatan, username, password):
        if jabatan == 'Pilih jabatan':
            msg.showinfo("Info","Pilih dulu jabatannya")
            return False
        if username == '' or password == '':
            msg.showinfo("Warning","Masukkan username dan password terlebih dahulu!")
            return False
        if len(username.split()) > 1 or len(password.split()) > 1:
            msg.showinfo("Warning","Username atau password tidak boleh memakai spasi!")
            return False
        if len(password) < 6:
            msg.showinfo("Warning","Panjang password tidak boleh kurang dari 6!")
            return False
        data = self.get_user(jabatan)
        if username in data:
            msg.showinfo("Info","Maaf username telah dipakai!")
            return False
        else:
            info = username + ' ' + password
            self.cli.rpush(jabatan, info)
            msg.showinfo("Info","Success!")
        return True

    def del_user(self, jabatan, idx, value):
        return self.cli.lrem(jabatan, idx, value)

class Transaksi:
    cli = Redis('localhost')
    paket = cli.lrange('data paket',0,-1)

    def get_rp(self,inp):
        mrg = ''
        for i in range(1,len(inp)+1,1):
            mrg += inp[-i]
            if (i % 3 == 0) and (i < len(inp)):
                mrg += '_'
        return mrg[::-1]

    def get_modal(self):
        return self.cli.lrange('modal paket',0,-1)
    
    def get_paket(self):
        return [str(i)[2:-1] for i in self.paket]
    
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
                if i in str(j):
                    cap = cap + 'modal : ' + str(j)[2:-1].split()[-1]
            paket[i] = cap
        return paket

    def get_day_keuntungan(self):
        data = self.cli.lrange('keuntungan',0,-1)
        day = ['']*len(data)
        idx = 0
        for i in data:
            day[idx] = str(i)[2:-1].split()[0]
            idx += 1
        return day

    def get_day_penjualan(self):
        paket = self.get_paket()
        tgl = []
        for i in paket:
            bantu = [str(i)[2:-1].split() for i in self.cli.lrange('penjualan ' + i, 0, -1)]
            for n in bantu:
                if n[0] not in tgl:
                    tgl.append(n[0])
        return tgl

    def daftar_penjualan(self,today):
        paket = self.get_paket()
        list_today = ['']*len(paket)
        idx = 0
        for i in paket:
            data_jual = self.cli.lrange('penjualan ' + i,0,-1)
            if not bool(data_jual):
                self.cli.rpush('penjualan ' + i, today + ' 0')
            idd = 1
            for j in data_jual:
                if today in str(j):
                    list_today[idx] = str(j)[2:-1].split()[1]
                    idx += 1
                elif idd == self.cli.llen('penjualan ' + i):
                    list_today[idx] = '0'
                    idx += 1
                else:
                    idd += 1
        return list_today
    
    
    def get_untung_today(self, today):
        data = self.cli.lrange('keuntungan',0,-1)
        for i in data:
            if today in str(i):
                return msg.showinfo('KEUNTUNGAN!','Keuntungan ' + str(today) + ': ' + str(i)[2:-1].split()[1])
                
        return msg.showinfo('KEUNTUNGAN!','Maaf belum ada yang membeli: ' + str(0))

    
