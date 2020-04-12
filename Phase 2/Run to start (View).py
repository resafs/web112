import tkinter.messagebox as msg
from tkinter import *
from redis import *
from datetime import date
from Controller import *
from Model import *
from PIL import ImageTk, Image


class Navigation_admin:
    window = None
    def __init__(self, window = None):
        self.window = window
        if self.window != None:
            self.window.withdraw()

    def set_window(self):
        self.window = Tk()

    def show_window_admin(self):
        global window_kasir
        global window_data
        global window_unt
        global window_jual
        global window_regis
        global window_adm
        global window_deleting
        global quiz
        
        window_kasir = None
        window_data = None
        window_unt = None
        window_jual = None
        window_regis = None
        window_adm = None
        window_deleting = None
        quiz = None
        
        self.window.deiconify()
        self.window.protocol("WM_DELETE_WINDOW", lambda: self.dstry_all(window_kasir,window_data,window_unt,window_jual,quiz,window_adm,window_regis,window_deleting))
        self.window.geometry('200x460')
        self.window.title('Admin')
        self.window.configure(background='sky blue')
        frame = LabelFrame(self.window,text="Navigate",background='white')
        frame.pack(padx=10,pady=10)
        btn_kasir = Button(frame,text='Kasir', width=15, height=2,bg='#8fffff',fg='#000',command= lambda: self.quiz('kasir', window_kasir))
        btn_kasir.pack(padx=4,pady=5)
        btn_kelola = Button(frame,text='Tentang Menu', width=15, height=2,bg='#8fffff',fg='#000',command= lambda: self.quiz('menu', window_data))
        btn_kelola.pack(padx=4,pady=5)
        btn_keuntungan = Button(frame,text='Keuntungan', width=15, height=2,bg='#8fffff',fg='#000',command= lambda: self.quiz('keuntungan', window_unt))
        btn_keuntungan.pack(padx=4,pady=5)
        btn_terjual = Button(frame,text='Terjual', width=15, height=2,bg='#8fffff',fg='#000',command= lambda: self.quiz('penjualan', window_jual))
        btn_terjual.pack(padx=4,pady=5)
        
        btn_kelola = Button(frame,text='Melihat user', width=15, height=2,bg='#8fffff',fg='#000',command= lambda: self.quiz('lihat user', window_adm))
        btn_kelola.pack(padx=4,pady=5)
        btn_keuntungan = Button(frame,text='Mendaftarkan user', width=15, height=2,bg='#8fffff',fg='#000',command= lambda: self.quiz('daftar user', window_regis))
        btn_keuntungan.pack(padx=4,pady=5)
        btn_terjual = Button(frame,text='Menghapus', width=15, height=2,bg='#8fffff',fg='#000',command= lambda: self.quiz('hapus user', window_deleting))
        btn_terjual.pack(padx=4,pady=5)
        
        btn_keluar = Button(frame,text='Logout', width=15, height=2,bg='#8fffff',fg='#000',command= lambda: self.dstry_all(window_kasir,window_data,window_unt,window_jual,quiz,window_adm,window_regis,window_deleting))
        btn_keluar.pack(padx=4,pady=5)
        self.window.mainloop()

    def quiz(self, nav, window_data):
        global quiz
        if not quiz and not window_data:
            quiz = True
            self.root = Tk()
            self.root.title("Password " + nav)
            self.root.protocol("WM_DELETE_WINDOW", lambda: self.dst_quiz(self.root))
            self.root.geometry('300x150')

            s_pass = StringVar(self.root)

            Label(self.root, text="Password", font=('arial',17,'bold')).place(x=105, y=10)

            e_user = Entry(self.root, text=s_pass, font=('arial',15,'bold'), width=15, show='*')
            e_user.place(x=80,y=45)

            btn_btl = Button(self.root, text='Kembali', font=('arial',13,'bold'), command = lambda: self.dst_quiz(self.root), width = 8)
            btn_btl.place(x=40, y = 85)

            btn_oke = Button(self.root, text='Masuk', font=('arial',13,'bold'), command = lambda: self.get_in(s_pass.get(), nav, self.root, window_data) , width = 8)
            btn_oke.place(x=175, y = 85)
            
            self.root.mainloop()
            return
        else:
            self.pop_up_window()
        
    def dst_quiz(self, window):
        global quiz
        window.destroy()
        quiz = None

    def get_in(self, s_pass, nav, window, window_data):
        global quiz
        if s_pass == 'navkas' and nav == 'kasir':
            quiz = False
            window.destroy()
            self.show_kasir()
        elif s_pass == 'navmenu'  and nav == 'menu':
            quiz = False
            window.destroy()
            self.show_data()
        elif s_pass == 'navunt' and nav == 'keuntungan':
            quiz = False
            window.destroy()
            self.show_unt()
        elif s_pass == 'navjual' and nav == 'penjualan':
            quiz = False
            window.destroy()
            self.show_jual()
        elif s_pass == 'navlihat' and nav == 'lihat user':
            quiz = False
            window.destroy()
            self.show_adm()
        elif s_pass == 'navdaftar' and nav == 'daftar user':
            quiz = False
            window.destroy()
            self.show_regis()
        elif s_pass == 'navhapus' and nav == 'hapus user':
            quiz = False
            window.destroy()
            self.show_deleting()
        else:
            msg.showinfo("Warning","Password yang anda masukkan salah!")
            
    def dstry_all(self,window_kasir,window_data,window_unt,window_jual,quiz,window_adm,window_regis,window_deleting):
        if window_kasir:
            window_kasir.dstry()
        if window_data:
            window_data.dstry()
        if window_unt:
            window_unt.dstry()
        if window_jual:
            window_jual.dstry()
        if window_adm:
            window_adm.dstry()
        if window_regis:
            window_regis.dstry()
        if window_deleting:
            window_deleting.dstry()
        if quiz:
            self.root.destroy()
        if self.window:
            msg.showinfo('Thankyou','Semoga hari anda menyenangkan admin!')
            self.window.destroy()
            self.window = None
            login = Login(Tk(),Login_controller(Navigation_admin(),Client(ctrl_c = Client_controller(), tgl = tgl)))
            login.show_window_login()

    def pop_up_window(self):
        msg.showinfo("Info","Jendela yang anda inginkan sedang terbuka!")
        return

    def show_kasir(self):
        global window_kasir
        if not window_kasir:
            window_kasir = Kasir(Tk(),Kasir_controller())
            window_kasir.show_window_kasir()

    def destroy_window_kasir(self,window):
        global window_kasir
        window.destroy()
        window_kasir = None

    def show_data(self):
        global window_data
        if not window_data:
            window_data = Data(Tk())
            window_data.show_window_data()

    def destroy_window_data(self,window):
        global window_data
        window.destroy()
        window_data = None

    def show_unt(self):
        global window_unt
        if not window_unt:
            window_unt = Untung(Tk(),Transaksi())
            window_unt.show_window_untung()

    def destroy_window_unt(self,window):
        global window_unt
        window.destroy()
        window_unt = None

    def show_jual(self):
        global window_jual
        if not window_jual:
            window_jual = Jual(Tk(), Transaksi())
            window_jual.show_window_jual()

    def destroy_window_jual(self,window):
        global window_jual
        window.destroy()
        window_jual = None

    def show_regis(self):
        global window_regis
        if not window_regis:
            window_regis = Regis(Tk(), Regis_controller())
            window_regis.show_window_regis()

    def destroy_window_regis(self,window):
        global window_regis
        window.destroy()
        window_regis = None
        
    def show_adm(self):
        global window_adm
        if not window_adm:
            window_adm = Adm(Tk(), Adm_controller())
            window_adm.show_window_adm()

    def destroy_window_adm(self,window):
        global window_adm
        window.destroy()
        window_adm = None

    def show_deleting(self):
        global window_deleting
        if not window_deleting:
            window_deleting = Deleting(Tk(), Deleting_controller())
            window_deleting.show_window_deleting()

    def destroy_window_deleting(self,window):
        global window_deleting
        window.destroy()
        window_deleting = None

class Regis:
    window = None
    ctrl = None
    
    def __init__(self, window = None, ctrl = None):
        self.window = window
        if self.window != None:
            self.window.withdraw()
        self.ctrl = ctrl

    def show_window_regis(self):
        self.window.deiconify()
        self.window.protocol("WM_DELETE_WINDOW", lambda: self.dstry())
        self.window.title("Admin form")
        self.window.geometry('485x250')

        self.s_user = StringVar(self.window)
        self.s_user.set('')
        self.s_pass = StringVar(self.window)
        self.s_pass.set('')
        self.s_jabatan = StringVar(self.window)
        self.s_jabatan.set('Pilih jabatan')


        Label(self.window, text="Registration Form", font=('arial',17,'bold')).place(x=155, y=10)

        jabatan = Label(self.window, text="Pilih bagian jabatan:", font=('arial',15,'bold'),anchor=E)
        jabatan.place(x=21,y=55)
        username = Label(self.window, text="Masukkan username:", font=('arial',15,'bold'),anchor=E)
        username.place(x=10,y=105)
        password = Label(self.window, text="Masukkan password:", font=('arial',15,'bold'),anchor=E)
        password.place(x=10,y=155)

        droplist_menu = ['admin','client']
        entry_kode = OptionMenu(self.window, self.s_jabatan, *droplist_menu)
        entry_kode.config(highlightbackground = "#b3b3b3", highlightthickness=1,width=34)
        entry_kode.place(x=225, y=55)
        e_user = Entry(self.window, text= self.s_user, font=('arial',15,'bold'), width=22)
        e_user.place(x=225,y=105)
        e_pass = Entry(self.window, text= self.s_pass, font=('arial',15,'bold'), width=22)
        e_pass.place(x=225,y=155)
        e_pass.config(show='*')


        btn_oke = Button(self.window, text='Daftarkan', font=('arial',13,'bold'), command = lambda: self.regis( self.s_jabatan.get(), self.s_user.get(), self.s_pass.get()), width = 21)
        btn_oke.place(x=250, y = 200)

        btn_oke = Button(self.window, text='Kembali', font=('arial',13,'bold'), command = lambda: self.dstry(), width = 20)
        btn_oke.place(x=14, y = 200)
        self.window.mainloop()

    def regis(self, jab, user, s_pass):
        if self.ctrl.regis(jab, user, s_pass):
            self.s_user.set('')
            self.s_pass.set('')
            self.s_jabatan.set('Pilih jabatan')
        else:
            self.s_user.set('')
            self.s_pass.set('')
        return

    def dstry(self):
        regis = Navigation_admin(self.window)
        regis.destroy_window_regis(self.window)
        regis = None
        self.window = None

class Adm:
    window = None
    ctrl = None
    
    def __init__(self, window = None, ctrl = None):
        self.window = window
        if self.window != None:
            self.window.withdraw()
        self.ctrl = ctrl

    def show_window_adm(self):
        self.window.deiconify()
        self.window.protocol("WM_DELETE_WINDOW", lambda: self.dstry())
        self.window.title("Show account")
        self.window.geometry('485x145')

        self.s_jabatan = StringVar(self.window)
        self.s_jabatan.set('Pilih jabatan')


        Label(self.window, text="Showing account", font=('arial',17,'bold')).place(x=155, y=10)

        jabatan = Label(self.window, text="Pilih bagian jabatan:", font=('arial',15,'bold'),anchor=E)
        jabatan.place(x=21,y=55)

        droplist_menu = ['admin','client', 'semuanya']
        entry_kode = OptionMenu(self.window, self.s_jabatan, *droplist_menu)
        entry_kode.config(highlightbackground = "#b3b3b3", highlightthickness=1,width=34)
        entry_kode.place(x=225, y=55)


        btn_oke = Button(self.window, text='Lihat', font=('arial',13,'bold'), command = lambda: self.showing(self.s_jabatan.get(), droplist_menu[:-1]), width = 21)
        btn_oke.place(x=250, y = 105)

        btn_oke = Button(self.window, text='Kembali', font=('arial',13,'bold'), command = lambda: self.dstry(), width = 20)
        btn_oke.place(x=14, y = 105)
        self.window.mainloop()

    def show_all(self, droplist):
        self.s_jabatan.set('Pilih jabatan')
        root = Tk()
        root.title('Daftar user')

        f = Frame(root,bg='black')
        f.pack()

        Label(f, text='Jabatan', font=('arial',11,'bold'), anchor=N).grid(row=0, column=0, sticky='nsew',padx=1,pady=1)
        Label(f, text='Username', font=('arial',11,'bold'), anchor=N).grid(row=0, column=1, sticky='nsew',padx=1,pady=1)
        Label(f, text='Password', font=('arial',11,'bold'), anchor=N).grid(row=0, column=2, sticky='nsew',padx=1,pady=1)
        row = 1
        for i in droplist:
            data_user, data_pass = self.ctrl.get_data(i)
            for s in range(len(data_user)):
                Label(f, text=i, font=('arial',11), anchor=N).grid(row=row, column=0, sticky='nsew',padx=1,pady=1)
                Label(f, text=data_user[s], font=('arial',11), anchor=N).grid(row=row, column=1, sticky='nsew',padx=1,pady=1)
                Label(f, text=data_pass[s], font=('arial',11), anchor=N).grid(row=row, column=2, sticky='nsew',padx=1,pady=1)
                row += 1
        root.mainloop()
        return

    def showing(self, jabatan, droplist):
        if jabatan == 'Pilih jabatan':
            msg.showinfo("Info","Pilih dulu jabatannya")
            return
        if jabatan == 'semuanya':
            self.show_all(droplist)
            return
        self.s_jabatan.set('Pilih jabatan')
        data_user, data_pass = self.ctrl.get_data(jabatan)
        root = Tk()
        root.title('Daftar user')

        f = Frame(root,bg='black')
        f.pack()

        Label(f, text='Jabatan', font=('arial',11,'bold'), anchor=N).grid(row=0, column=0, sticky='nsew',padx=1,pady=1)
        Label(f, text='Username', font=('arial',11,'bold'), anchor=N).grid(row=0, column=1, sticky='nsew',padx=1,pady=1)
        Label(f, text='Password', font=('arial',11,'bold'), anchor=N).grid(row=0, column=2, sticky='nsew',padx=1,pady=1)
        row = 1
        for i in range(len(data_user)):
            Label(f, text=jabatan, font=('arial',11), anchor=N).grid(row=row, column=0, sticky='nsew',padx=1,pady=1)
            Label(f, text=data_user[i], font=('arial',11), anchor=N).grid(row=row, column=1, sticky='nsew',padx=1,pady=1)
            Label(f, text=data_pass[i], font=('arial',11), anchor=N).grid(row=row, column=2, sticky='nsew',padx=1,pady=1)
            row += 1
        root.mainloop()
        return

    def dstry(self):
        adm = Navigation_admin(self.window)
        adm.destroy_window_adm(self.window)
        adm = None
        self.window = None

class Deleting:
    window = None
    ctrl = None
    
    def __init__(self, window = None, ctrl = None):
        self.window = window
        if self.window != None:
            self.window.withdraw()
        self.ctrl = ctrl

    def show_window_deleting(self):
        self.window.deiconify()
        self.window.protocol("WM_DELETE_WINDOW", lambda: self.dstry())
        
        self.window.title("Deleting form")
        self.window.geometry('485x208')

        s_user = StringVar(self.window)
        s_user.set('')
        s_jabatan = StringVar(self.window)
        s_jabatan.set('Pilih jabatan')


        Label(self.window, text="Deleting Account", font=('arial',17,'bold')).place(x=155, y=10)

        jabatan = Label(self.window, text="Pilih bagian jabatan:", font=('arial',15,'bold'),anchor=E)
        jabatan.place(x=21,y=55)
        username = Label(self.window, text="Masukkan username:", font=('arial',15,'bold'),anchor=E)
        username.place(x=10,y=105)

        droplist_menu = ['admin','client']
        entry_kode = OptionMenu(self.window, s_jabatan, *droplist_menu)
        entry_kode.config(highlightbackground = "#b3b3b3", highlightthickness=1,width=34)
        entry_kode.place(x=225, y=55)

        e_user = Entry(self.window, text=s_user, font=('arial',15,'bold'), width=22)
        e_user.place(x=225,y=105)


        btn_oke = Button(self.window, text='Hapus', font=('arial',13,'bold'), command = lambda: self.delete(s_jabatan.get(), s_user.get()), width = 21)
        btn_oke.place(x=250, y = 155)

        btn_oke = Button(self.window, text='Kembali', font=('arial',13,'bold'), command = lambda: self.dstry(), width = 20)
        btn_oke.place(x=14, y = 155)
        self.window.mainloop()

    def delete(self, jabatan, username):
        if jabatan == 'Pilih jabatan':
            msg.showinfo("Info","Pilih dulu jabatannya")
            return
        if username == '':
            msg.showinfo("Info","Masukkan lebih dulu usernamenya!")
            return
        data_user, data_pass = self.ctrl.get_data(jabatan)
        if username in data_user:
            idx = data_user.index(username)
            info = data_user[idx] + ' ' + data_pass[idx]
            self.ctrl.del_user(jabatan, info)
            msg.showinfo("Info","Berhasil menghapus user!")
            return
        else:
            msg.showinfo("Info","Maaf username yang ingin dihapus tidak ada!")
            return
        return

    def dstry(self):
        deleting = Navigation_admin(self.window)
        deleting.destroy_window_deleting(self.window)
        deleting = None
        self.window = None

class Kasir:
    window = None
    ctrl = None
    kode = None
    bayar = None
    droplist_menu = None
    entry_kode = None
    
    def __init__(self,window = None, ctrl = None):
        self.window = window
        if self.window != None:
            self.window.withdraw()
        self.ctrl = ctrl

    def show_window_kasir(self):
        self.window.deiconify()
        self.window.protocol("WM_DELETE_WINDOW", lambda: self.dstry())
        self.window.title('Pembayaran')
        self.window.geometry("224x96")
        lf = LabelFrame(self.window)
        lf.pack(pady=3)
        
        self.kode = StringVar(self.window)
        self.kode.set('Pilih kode pembayaran')
        self.bayar = StringVar(self.window)
        self.bayar.set('')

        label_kode = Label(lf,text='KODE:',font=('arial',10,'bold'))
        label_kode.grid(row=0,column=0)
        self.droplist_menu = self.ctrl.get_unique()
        self.entry_kode = OptionMenu(lf,self.kode,*self.droplist_menu)
        self.entry_kode.config(highlightbackground = "#b3b3b3", highlightthickness=1,width=20)
        self.entry_kode.grid(row=0,column=1,sticky='ew')


        #### harga_redis = nanti dimunculin harganya berdasarkan kode diatas
        ####masg.showinfo("Harga yang harus dibayar: " + str(redis))

        

        label_bayar = Label(lf,text='Bayar:',font=('arial',10,'bold'))
        label_bayar.grid(row=1,column=0)
        entry_bayar = Entry(lf, textvar=self.bayar, highlightbackground = "#b3b3b3", highlightthickness=1)
        entry_bayar.grid(row=1,column=1,padx=0,pady=3,sticky='nsew')


        btn_total = Button(lf,text='Total',command = lambda: self.show_hrg(self.ctrl.get_total_unique(self.kode.get())),width=6)
        btn_total.grid(row=2,column=0,sticky='ew')
        
        btn_bayar = Button(lf,text='Bayar',command = lambda: self.membayar(self.bayar.get(),self.kode.get(), lf),width=17)
        btn_bayar.grid(row=2,column=1,padx=0,pady=3,sticky='nsew')
        self.window.mainloop()

    def membayar(self, bayar, kode, lf): ## NANTI DIKAITIN SAMA DATABASE
        total = self.ctrl.get_total_unique(kode)
        if total == None or bayar == '':
            if total == None:
                msg.showinfo("Info", "Pilih kode pembayaran terlebih dahulu!")
                return
            else:
                msg.showinfo("Info", "Masukkan jumlah yang konsumen bayarkan!")
                return
            
        if self.ctrl.cek_int(bayar):
            msg.showinfo('Warning','Masukkan jumlah pembayaran konsumen berupa angka!')
            return
        
        if int(bayar) == int(total):
            msg.showinfo("Hasil", "Tidak ada kembalian. \nTerimakasih sudah berbelanja")
            self.ctrl.del_unique(kode, str(total))
            self.kode.set('Pilih kode pembayaran')
            self.bayar.set('')
            self.droplist_menu = self.ctrl.get_unique()
            self.entry_kode = OptionMenu(lf,self.kode,*self.droplist_menu)
            self.entry_kode.config(highlightbackground = "#b3b3b3", highlightthickness=1,width=20)
            self.entry_kode.grid(row=0,column=1,sticky='ew')
        elif int(bayar) > int(total):
            msg.showinfo("Hasil", "Kembaliannya: " + str(self.ctrl.get_rp(str(int(bayar)-int(total)))) +'\nTerimakasih sudah berbelanja!')
            self.ctrl.del_unique(kode, str(total))
            self.kode.set('Pilih kode pembayaran')
            self.bayar.set('')
            self.droplist_menu = self.ctrl.get_unique()
            self.entry_kode = OptionMenu(lf,self.kode,*self.droplist_menu)
            self.entry_kode.config(highlightbackground = "#b3b3b3", highlightthickness=1,width=20)
            self.entry_kode.grid(row=0,column=1,sticky='ew')
        else:
            msg.showinfo("Hasil", "Maaf uangnya kurang")
        return

    def show_hrg(self,total):
        if total == None:
            return
        msg.showinfo("HARGA","Harga yang harus dibayar: " + total)

    def dstry(self):
        kasir = Navigation_admin(self.window)
        kasir.destroy_window_kasir(self.window)
        kasir = None
        self.window = None

class Untung:
    window = None
    transac = None
    tanggal = None
    
    def __init__(self,window = None, transac = None):
        self.window = window
        if self.window != None:
            self.window.withdraw()
        self.transac = transac
        
    def show_window_untung(self):
        self.window.deiconify()
        self.window.protocol("WM_DELETE_WINDOW", lambda: self.dstry())
        self.window.geometry('230x115')
        self.window.title('Keuntungan')

        self.tanggal = StringVar(self.window)
        self.tanggal.set("Pilih tanggal")

        hari = Label(self.window,text='Tanggal:',font=('arial',15,'bold'))
        hari.place(x=6,y=20)
        
        droplist_day = self.transac.get_day_keuntungan()
        entry_kode = OptionMenu(self.window,self.tanggal,*droplist_day)
        entry_kode.config(highlightbackground = "#b3b3b3", highlightthickness=1,width=14)
        entry_kode.place(x=95,y=24)

        btn_cek = Button(self.window,text='Cek',command= lambda: self.get_untung_today(self.tanggal.get()),width=18)
        btn_cek.place(x=86,y=75)
        
        btn_dstry = Button(self.window,text='Tutup',command= lambda: self.dstry(),width=10)
        btn_dstry.place(x=6,y=75)
        self.window.mainloop()

    def get_untung_today(self, tanggal):
        if tanggal == 'Pilih tanggal':
            msg.showinfo("Announcement","Pilih dulu tanggalnya!")
            return
        self.tanggal.set("Pilih tanggal")
        self.transac.get_untung_today(tanggal)
        

    def dstry(self):
        untung = Navigation_admin(self.window)
        untung.destroy_window_unt(self.window)
        untung = None
        self.window = None

class Jual:
    cli = Redis('localhost')
    window = None
    transac = None
    roos = None
    tanggal = None
    
    def __init__(self,window = None, transac = None):
        self.window = window
        if self.window != None:
            self.window.withdraw()
        self.transac = transac

    def show_window_jual(self):
        self.window.deiconify()
        self.window.protocol("WM_DELETE_WINDOW", lambda: self.dstry())
        self.window.geometry('230x115')
        self.window.title('Penjualan')

        self.tanggal = StringVar(self.window)
        self.tanggal.set('Pilih tanggal')

        hari = Label(self.window,text='Tanggal:',font=('arial',15,'bold'))
        hari.place(x=6,y=20)
        droplist_day = self.transac.get_day_penjualan()
        entry_kode = OptionMenu(self.window,self.tanggal,*droplist_day)
        entry_kode.config(highlightbackground = "#b3b3b3", highlightthickness=1,width=14)
        entry_kode.place(x=95,y=24)

        btn_cek = Button(self.window,text='Cek',command= lambda: self.show_penjualan(self.tanggal.get()),width=18)
        btn_cek.place(x=86,y=75)
        
        btn_dstry = Button(self.window,text='Tutup',command= lambda: self.dstry(),width=10)
        btn_dstry.place(x=6,y=75)
        self.window.mainloop()

    def show_penjualan(self,today):
        if today == 'Pilih tanggal':
            msg.showinfo("Announcement","Pilih dulu tanggalnya!")
            return
        self.roos = Tk()
        self.roos.title('Penjualan')
        self.roos.protocol("WM_DELETE_WINDOW", lambda: self.dstr())
        paket = self.transac.get_paket()
        list_today = self.transac.daftar_penjualan(today)
        row = 0
        l = LabelFrame(self.roos,background='black')
        l.pack()
        Label(l,text='PENJUALAN ' + today,font=('arial',15,'bold')).grid(row=row,columnspan=2,sticky='nsew',padx=1,pady=1)
        row += 1
        idx = 0
        Label(l,text='Nama Paket',font=('arial',15,'bold')).grid(row=row, column=0,sticky='ew',padx=1,pady=1)
        Label(l,text='Total',font=('arial',15,'bold')).grid(row=row, column=1,sticky='ew',padx=1,pady=1)
        for i in paket:
            Label(l,text=i,font=('arial',10,'bold'),anchor='w').grid(row=row+1,column=0,pady=1,sticky='nsew',padx=1)
            Label(l,text=': '+list_today[idx],font=('arial',10,'bold'),anchor='w').grid(row=row+1,column=1,pady=1,sticky='nsew',padx=1)
            row += 1
            idx += 1
        self.roos.mainloop()
        return

    def dstr(self):
        self.tanggal.set('Pilih tanggal')
        self.roos.destroy()
        self.roos = None

    def dstry(self):
        if self.roos != None:
            self.dstr()
        jual = Navigation_admin(self.window)
        jual.destroy_window_jual(self.window)
        jual = None
        self.window = None


class Data:
    window = None
    def __init__(self,window = None):
        self.window = window
        if self.window != None:
            self.window.withdraw()

    def show_window_data(self):
        global window_data_menu
        global window_data_tmenu
        global window_data_hrg
        global window_data_stck
        window_data_menu = None
        window_data_tmenu = None
        window_data_hrg = None
        window_data_stck = None

        self.window.deiconify()
        self.window.protocol("WM_DELETE_WINDOW", lambda: self.dstry())
        self.window.geometry('250x200')
        self.window.title('Update Data')
        self.window.configure(background='brown')


        lf = LabelFrame(self.window)
        lf.pack(padx=10,pady=10)

        btn_menu = Button(lf,text='Menu',command= lambda: self.show_window_data_menu(), width=15, height=2)
        btn_menu.grid(padx=2)
        
        btn_tmenu = Button(lf,text='Tambah Menu',command= lambda: self.show_window_data_tmenu(), width=15, height=2)
        btn_tmenu.grid(padx=2,pady=2)

        btn_hrg = Button(lf,text='Ganti Harga',command= lambda: self.show_window_data_hrg(), width=15, height=2)
        btn_hrg.grid(padx=2,pady=2)

        btn_updt = Button(lf,text='Update Stock',command= lambda: self.show_window_data_stck(), width=15, height=2)
        btn_updt.grid(padx=2,pady=2)
    
        
        btn_dstry = Button(lf,text='Tutup',command= lambda : self.dstry(window_data_menu,window_data_tmenu,window_data_hrg,window_data_stck), width=15, height=2)
        btn_dstry.grid(padx=2,pady=2)
        
        self.window.mainloop()
        
    def dstry(self, window_data_men = None, window_data_tmen = None, window_data_hr = None, window_data_stc = None):
        global window_data_menu
        if window_data_men or window_data_menu:
            window_data_menu.dstry()
        global window_data_tmenu
        if window_data_tmen or window_data_tmenu:
            window_data_tmenu.dstry()
        global window_data_hrg
        if window_data_hr or window_data_hrg:
            window_data_hrg.dstry()
        global window_data_stck
        if window_data_stc or window_data_stck:
            window_data_stck.dstry()
        if self.window:
            self.dstr()

    def dstr(self):
        untung = Navigation_admin(self.window)
        untung.destroy_window_data(self.window)
        untung = None
        self.window = None

    def show_window_data_menu(self):
        global window_data_menu
        if not window_data_menu:
            window_data_menu = Data_menu(Tk(), Data_menu_controller())
            window_data_menu.show_window_data_menu()

    def destroy_window_menu(self,window):
        global window_data_menu
        window.destroy()
        window_data_menu = None

    def show_window_data_tmenu(self):
        global window_data_tmenu
        if not window_data_tmenu:
            window_data_tmenu = Data_tmenu(Tk(),Data_tmenu_controller())
            window_data_tmenu.show_window_data_tmenu()

    def destroy_window_tmenu(self,window):
        global window_data_tmenu
        window.destroy()
        window_data_tmenu = None

    def show_window_data_hrg(self):
        global window_data_hrg
        if not window_data_hrg:
            window_data_hrg = Data_hrg(Tk(),Data_hrg_controller())
            window_data_hrg.show_window_data_hrg()

    def destroy_window_hrg(self,window):
        global window_data_hrg
        window.destroy()
        window_data_hrg = None

    def show_window_data_stck(self):
        global window_data_stck
        if not window_data_menu:
            window_data_stck = Data_stck(Tk(),Data_stck_controller())
            window_data_stck.show_window_data_stck()

    def destroy_window_stck(self,window):
        global window_data_stck
        window.destroy()
        window_data_stck = None


class Data_menu:
    window = None
    ctrl = None
    def __init__(self, window = None, ctrl = None):
        self.window = window
        if self.window != None:
            self.window.withdraw()
        self.ctrl = ctrl

    def show_window_data_menu(self):
        self.window.deiconify()
        self.window.title("MENU")
        self.window.protocol("WM_DELETE_WINDOW", lambda: self.dstry())
            
        fr = LabelFrame(self.window,background='black')
        fr.pack()

        nmr = Label(fr,text='Nomor',font=('arial',15,'bold'))
        nmr.grid(row=0,column=0,sticky='nsew',padx=1,pady=1)
            
        menu = Label(fr,text='Menu',font=('arial',15,'bold'))
        menu.grid(row=0,column=2,sticky='nsew',padx=1,pady=1)
            
        pkt = Label(fr,text='Nama Paket',font=('arial',15,'bold'))
        pkt.grid(row=0,column=1,sticky='nsew',padx=1,pady=1)

        row = self.show_menu(fr)
            
        btn_dstry = Button(fr,text='Tutup',command= lambda : self.dstry(), width=15, height=2)
        btn_dstry.grid(row=row, columnspan=3, sticky='sew')
        self.window.mainloop()

    def show_menu(self, frame):
        paket = self.ctrl.get_all_menu()
        idx_row = 1
        for i in paket.keys():
            teks = paket[i].replace(':','=')
            Label(frame,text=str(idx_row),font=('arial',12,'bold')).grid(row=idx_row,column=0,padx=1,pady=1,sticky='ew')
            Label(frame,text=i,font=('arial',12,'bold'),anchor=W).grid(row=idx_row,column=1,padx=1,pady=1,sticky='ew')
            Label(frame,text=': '+teks,font=('arial',12,'bold'),anchor=W).grid(row=idx_row,column=2,padx=1,pady=1,sticky='we')
            idx_row += 1            
        return idx_row

    def dstry(self):
        menu = Data(self.window)
        menu.destroy_window_menu(self.window)
        menu = None
        self.window = None

class Data_tmenu:
    window = None
    ctrl = None
    s_nama = None
    s_itm = None
    s_hrg = None
    s_mdl = None

    en_nama = None
    en_itm = None
    en_hrg = None
    en_mdl = None
    
    def __init__(self,window = None, ctrl = None):
        self.window = window
        if self.window != None:
            self.window.withdraw()
        self.ctrl = ctrl

    def show_window_data_tmenu(self):
        self.window.deiconify()
        self.window.protocol("WM_DELETE_WINDOW", lambda: self.dstry())
        self.window.title("Adding Menu")

        fr = LabelFrame(self.window)
        fr.pack()
            
        nama = Label(fr,text='Nama paket:',font=('arial',15,'bold'))
        nama.grid(row=0,column=0,sticky=E)
        item = Label(fr,text='Items:',font=('arial',15,'bold'))
        item.grid(row=1,column=0,sticky=E)
        mdl = Label(fr,text='Harga modal:',font=('arial',15,'bold'))
        mdl.grid(row=4,column=0,sticky=E)
        harga = Label(fr,text='Harga paket:',font=('arial',15,'bold'))
        harga.grid(row=5,column=0,sticky=E)
        ann1 = Label(fr,text='Format items: nama_item1 banyak_item1 nama_item2 banyak_item2 ....',font=('arial',10))
        ann1.grid(row=2,columnspan=2,sticky=W)
        ann2 = Label(fr,text='contoh: ikan_bakar 2 tahu_goreng 10 pisang_goreng 5',font=('arial',10))
        ann2.grid(row=3,columnspan=2,sticky=W)

        #String variable
        self.s_nama = StringVar(self.window)
        self.s_nama.set('')
        self.s_itm = StringVar(self.window)
        self.s_itm.set('')
        self.s_hrg = StringVar(self.window)
        self.s_hrg.set('')
        self.s_mdl = StringVar(self.window)
        self.s_mdl.set('')

        self.en_nama = Entry(fr, textvar = self.s_nama, highlightbackground = "#b3b3b3", highlightthickness=1, width = 60)
        self.en_nama.grid(row=0,column=1,sticky=W)
        self.en_itm = Entry(fr, textvar = self.s_itm, highlightbackground = "#b3b3b3", highlightthickness = 1, width = 60)
        self.en_itm.grid(row=1,column=1,sticky=W)
        self.en_hrg = Entry(fr, textvar = self.s_hrg, highlightbackground = "#b3b3b3", highlightthickness=1, width = 60)
        self.en_hrg.grid(row=5,column=1,sticky=W)
        self.en_mdl = Entry(fr, textvar = self.s_mdl, highlightbackground = "#b3b3b3", highlightthickness=1, width = 60)
        self.en_mdl.grid(row=4,column=1,sticky=W)
            
            
        btn_tmbh = Button(fr,text='Tambah', command= lambda: self.tmbh(self.s_nama.get(),self.s_itm.get(),self.s_hrg.get(),self.s_mdl.get()), width=51, height=2)
        btn_tmbh.grid(row=6,column=1,sticky='ew')
        btn_dstry = Button(fr,text='Tutup', command= lambda : self.dstry(), width=18, height=2)
        btn_dstry.grid(row=6,column=0,sticky='we')
        self.window.mainloop()

    def tmbh(self, nama, items, harga, modal):
        if nama == '' or items == '' or harga == '' or modal == '':
            self.ctrl.pop_up('kosong')
            return
        if self.ctrl.cek_paket(nama):
            self.ctrl.pop_up('nama paket terdaftar')
            return
        if self.ctrl.cek_int(harga, modal):
            msg.showinfo('Warning','Masukkan harga berupa angka!')
            return

        for i in range(1,len(items.split()),2):
            if self.ctrl.cek_int(items.split()[i]):
                msg.showinfo('Warning','Masukkan jumlah items paket berupa angka!')
                return
        
        hasil = self.ctrl.set_packet_to_redis(nama, items.split(), harga)
        if hasil == 'err':
            return
        self.ctrl.set_modal_to_redis(nama, modal)
        self.ctrl.pop_up_success()
        self.s_nama.set('')
        self.s_itm.set('')
        self.s_hrg.set('')
        self.s_mdl.set('')
        
        self.en_nama.grid(row=0,column=1,sticky=W)
        self.en_itm.grid(row=1,column=1,sticky=W)
        self.en_hrg.grid(row=5,column=1,sticky=W)
        self.en_mdl.grid(row=4,column=1,sticky=W)
        return
        
    def dstry(self):
        tmenu = Data(self.window)
        tmenu.destroy_window_tmenu(self.window)
        tmenu = None
        self.window = None
    

class Data_hrg:
    window = None
    ctrl = None
    s_nama = None
    s_hrgb = None
    
    def __init__(self,window = None, ctrl = None):
        self.window = window
        if self.window != None:
            self.window.withdraw()
        self.ctrl = ctrl

    def show_window_data_hrg(self):
        self.window.deiconify()
        self.window.protocol("WM_DELETE_WINDOW", lambda: self.dstry())
        self.window.title("Ganti Harga Menu")

        fr = LabelFrame(self.window)
        fr.pack()
            
        nama = Label(fr,text='Nama paket:',font=('arial',15,'bold'))
        nama.grid(row=0,column=0,sticky=E,padx=3,pady=2)
        harga_b = Label(fr,text='Harga terbaru:',font=('arial',15,'bold'))
        harga_b.grid(row=1,column=0,sticky=E,padx=3,pady=2)

        self.s_nama = StringVar(self.window)
        self.s_nama.set('Pilih paket')
        self.s_hrgb = StringVar(self.window)
        self.s_hrgb.set('')
    
        
        paket = self.ctrl.get_packet()
        entry_kode = OptionMenu(fr,self.s_nama,*paket)
        entry_kode.config(highlightbackground = "#b3b3b3", highlightthickness=1)
        entry_kode.grid(row=0,column=1,sticky='nsew',padx=3,pady=2)
        en_hrgb = Entry(fr, textvar = self.s_hrgb, highlightbackground = "#b3b3b3", highlightthickness = 1,width=35)
        en_hrgb.grid(row=1,column=1,sticky=W,padx=3,pady=2)
            
        btn_ubh = Button(fr,text='Ubah',command= lambda: self.set_change_price(self.s_nama.get(), self.s_hrgb.get()), width=30, height=2)
        btn_ubh.grid(row=2,column=1,sticky = 'we')
        btn_dstry = Button(fr,text='Tutup',command= lambda : self.dstry(), width=19, height=2)
        btn_dstry.grid(row=2,column=0,sticky = 'ew')
        self.window.mainloop()

    def set_change_price(self, nama, harga):
        self.ctrl.set_change_price(nama, harga)
        self.s_nama.set('Pilih paket')
        self.s_hrgb.set('')
        
    def dstry(self):
        hrg = Data(self.window)
        hrg.destroy_window_hrg(self.window)
        hrg = None
        self.window = None

class Data_stck:
    window = None
    ctrl = None
    s_nama = None
    s_updt = None
    
    def __init__(self,window = None, ctrl = None):
        self.window = window
        if self.window != None:
            self.window.withdraw()
        self.ctrl = ctrl

    def show_window_data_stck(self):
        self.window.deiconify()
        self.window.protocol("WM_DELETE_WINDOW", lambda: self.dstry())
        self.window.title("Update Stock")

        fr = LabelFrame(self.window)
        fr.pack()
            
        nama = Label(fr,text='Nama paket:',font=('arial',15,'bold'))
        nama.grid(row=0,column=0,sticky=E,padx=3,pady=2)
        stock = Label(fr,text='Stock paket:',font=('arial',15,'bold'))
        stock.grid(row=1,column=0,sticky=E,padx=3,pady=2)

        self.s_nama = StringVar(self.window)
        self.s_nama.set('Pilih paket')
        self.s_updt = StringVar(self.window)
        self.s_updt.set('')


        paket = self.ctrl.get_packet()
        entry_kode = OptionMenu(fr, self.s_nama,*paket)
        entry_kode.config(highlightbackground = "#b3b3b3", highlightthickness=1)
        entry_kode.grid(row=0,column=1,sticky='nsew',padx=3,pady=2)
        en_updt = Entry(fr, textvar = self.s_updt, highlightbackground = "#b3b3b3", highlightthickness = 1,width=35)
        en_updt.grid(row=1,column=1,sticky=W,padx=3,pady=2)
            
        btn_ubh = Button(fr,text='Update',command= lambda: self.set_stock_to_redis(self.s_nama.get(), self.s_updt.get()), width=30, height=2)
        btn_ubh.grid(row=2,column=1,sticky = 'ew')
        btn_dstry = Button(fr,text='Tutup',command= lambda : self.dstry(), width=16, height=2)
        btn_dstry.grid(row=2,column=0,sticky = 'we')
        self.window.mainloop()

    def set_stock_to_redis(self, nama, stock):
        self.ctrl.set_stock_to_redis(nama, stock)
        self.s_nama.set('Pilih paket')
        self.s_updt.set('')
        
    def dstry(self):
        stck = Data(self.window)
        stck.destroy_window_stck(self.window)
        stck = None
        self.window = None


class Client:
    window = None
    ctrl_c = None
    tgl = None
    s_nama = None
    s_bnyk = None
    
    def __init__(self,window = None, ctrl_c = None,tgl = None):
        self.window = window
        if self.window != None:
            self.window.withdraw()
        self.ctrl_c = ctrl_c
        self.tgl = tgl

    def set_window(self):
        self.window = Tk()

    def show_window_client(self):
        self.window.deiconify()
        self.window.protocol("WM_DELETE_WINDOW", lambda: self.cancel())
        self.window.title('Order')
        self.window.configure(background='white')
        
        lf = LabelFrame(self.window)
        lf.pack()
        lf.configure(background='white')

        head = Label(lf,text='ORDER',bg='white',width=10,font=('arial',19,'bold'),borderwidth=1,relief='solid')
        head.grid(row=0,columnspan=2,padx=2,pady=3,sticky=NSEW)
        nama = Label(lf,text='Nama paket:',bg='white',font=('calibri',15,'bold'))
        nama.grid(row=1,column=0,sticky=E,padx=2,pady=3)
        banyak = Label(lf,text='Jumlah pesanan:',bg='white',font=('calibri',15,'bold'))
        banyak.grid(row=2,column=0,sticky=E,padx=2,pady=3)
        bucket = Label(lf,text='Daftar pesanan:',bg='white',font=('calibri',15,'bold'))
        bucket.grid(row=3,columnspan=2,sticky=N,padx=2,pady=3)

        #String Variabel
        self.s_nama = StringVar(self.window)
        self.s_nama.set('Menu')
        self.s_bnyk = StringVar(self.window)
        self.s_bnyk.set('')

        paket = self.ctrl_c.get_packet()
        en_nama = OptionMenu(lf, self.s_nama,*paket)
        en_nama.config(highlightbackground = "#b3b3b3", highlightthickness=1)
        en_nama.grid(row=1,column=1,sticky='nsew',padx=2,pady=3)

        en_bnyk = Entry(lf, bg='white', textvar=self.s_bnyk, width=20, highlightbackground="#bebebe", highlightthickness=1)
        en_bnyk.grid(row=2,column=1,sticky='nsew',padx=2,pady=3)

        lb = Listbox(lf,width=47)
        lb.grid(row=4,columnspan=2,sticky=NSEW,padx=2,pady=3)

        btn_shw = Button(lf,text='Show the packet', width=19, height=2,bg='#8fffff',fg='#000',command= lambda: self.show_packet(self.s_nama.get()))
        btn_shw.grid(row=5,column=0,padx=2,pady=3)

        btn_add = Button(lf,text='Add to bucket', width=18, height=2,bg='#8fffff',fg='#000',command= lambda: self.ctrl_c.add_to_bucket(self.s_nama.get(),self.s_bnyk.get(),lb))
        btn_add.grid(row=5,column=1,padx=2,pady=3)

        btn_lht_hrg = Button(lf,text='Lihat harga pembelian', width=39, height=2,bg='#8fffff',fg='#000',command= lambda: self.ctrl_c.get_total(lb))
        btn_lht_hrg.grid(row=6,columnspan=2,padx=2,pady=3,sticky=NSEW)

        btn_del = Button(lf,text='Remove from bucket', width=39, height=2,bg='#8fffff',fg='#000',command= lambda: self.ctrl_c.delete_from_bucket_1(lb))
        btn_del.grid(row=7,columnspan=2,padx=2,pady=3,sticky=NSEW)

        btn_done = Button(lf,text='Done', width=19, height=2,bg='#8fffff',fg='#000',command= lambda: self.do_done(lb,self.tgl))
        btn_done.grid(row=8,column=0,padx=2,pady=3)

        btn_btl = Button(lf, text='Exit', width=18, height=2,bg='#8fffff',fg='#000',command= lambda: self.cancel())
        btn_btl.grid(row=8,column=1,padx=2,pady=3)

        self.window.mainloop()

    def do_done(self, Lb1, tgl):
        self.ctrl_c.done(Lb1, tgl)
        self.s_nama.set('Menu')
        self.s_bnyk.set('')

    def cancel(self):
        msg.showinfo('Thankyou','Semoga hari anda menyenangkan.')
        self.window.destroy()
        self.window = None
        login = Login(Tk(),Login_controller(Navigation_admin(),Client(ctrl_c = Client_controller(), tgl = tgl)))
        login.show_window_login()

    def show_packet(self,paket):
         if paket == 'Menu':
              msg.showinfo('Announcement!','Silahkan pilih menu terlebih dahulu!')
              return
         root = Tk()
         root.configure(background='black')
         root.title('In Packet')
         
         lr = LabelFrame(root,background='black')
         lr.pack()
         
         isi_paket_a = self.ctrl_c.get_product(paket)
         nama = Label(lr, text=paket, bg='white', height=2, borderwidth=0, font=('calibri',10,'bold'))
         nama.grid(columnspan=2,sticky='nsew')
         rows = 1
         for i in range(0,len(isi_paket_a),2):
              jenis = isi_paket_a[i].replace('_',' ')
              jumlah = isi_paket_a[i+1]
              Label(lr, text=jenis, bg='white', width=50, borderwidth=0, font=('calibri',10,'bold')).grid(row=i+1,column=0,sticky='nsew', padx=1, pady=1)
              Label(lr, text=jumlah, bg='white', borderwidth=0, font=('calibri',10,'bold')).grid(row=i+1,column=1,sticky='nsew', pady=1)
              rows += 1
         root.mainloop()        

class Placeholder_State(object):
     __slots__ = 'normal_color', 'normal_font', 'placeholder_text', 'placeholder_color', 'placeholder_font', 'with_placeholder'


class Login:
    window = None
    ctrl = None
    
    def __init__(self,window = None, ctrl = None):
        self.window = window
        if self.window != None:
            self.window.withdraw()
        self.ctrl = ctrl
        
    def add_placeholder_to(entry, placeholder, color="grey", font=None):
        normal_color = entry.cget("fg")
        normal_font = entry.cget("font")
        
        if font is None:
            font = normal_font

        state = Placeholder_State()
        state.normal_color=normal_color
        state.normal_font=normal_font
        state.placeholder_color=color
        state.placeholder_font=font
        state.placeholder_text = placeholder
        state.with_placeholder=True

        
        def on_focusin(event, entry=entry, state=state):
            if state.with_placeholder:
                entry.delete(0, "end")
                entry.config(fg = state.normal_color, font=state.normal_font)
            
                state.with_placeholder = False

        def on_focusout(event, entry=entry, state=state):
            if entry.get() == '':
                entry.insert(0, state.placeholder_text)
                entry.config(fg = state.placeholder_color, font=state.placeholder_font)
                
                state.with_placeholder = True

        entry.insert(0, placeholder)
        entry.config(fg = color, font=font)

        entry.bind('<FocusIn>', on_focusin, add="+")
        entry.bind('<FocusOut>', on_focusout, add="+")
        
        entry.placeholder_state = state

        return state

    def show_window_login(self):
        self.window.deiconify()
        self.window.geometry('300x380')
        self.window.protocol("WM_DELETE_WINDOW", lambda: self.dstry())
        self.window.title('Login')
        self.window.configure(background='sky blue')

        frame = LabelFrame(self.window,text="login")
        frame.pack()

        #String Variabel
        username = StringVar(self.window)
        password = StringVar(self.window)
        
        logo = Image.open("Hepibidi.png")
        photo = ImageTk.PhotoImage(logo)
        Label(image=photo).pack()

        a = Label(self.window,text='Sign-in',relief='solid',width=10,font=('arial',19,'bold')).place(x=75,y=140)
        b = Label(self.window,text='Username:',bg='sky blue',width=10,font=('calibri',15,'bold')).place(x=30,y=210)
        c = Label(self.window,text='Password:',bg='sky blue',width=10,font=('calibri',15,'bold')).place(x=30,y=260)

        username = Entry(self.window, bg='white', textvar=username, width=20, highlightbackground="#bebebe", highlightthickness=1)
        username.place(x=130,y=215)
        Login.add_placeholder_to(username, ' Username')

        password = Entry(self.window, bg='white', textvar=password, width=20, highlightbackground="#bebebe", highlightthickness=1)
        password.place(x=130,y=265)
        password.config(show='*')
        Login.add_placeholder_to(password, ' Password')

        btn_login = Button(self.window,text='Login', width=15, height=2,bg='#8fffff',fg='#000',command= lambda: self.check(username.get(),password.get()))
        btn_login.place(x=95,y=309)
        self.window.mainloop()

    def dstry(self):
        msg.showinfo("Announcement","Terima kasih telah memakai aplikasi ini!")
        self.window.destroy()
        self.window = None

    def check(self,user,passw):
        if self.ctrl.check(user,passw):
            self.window.destroy()
            self.ctrl.navigation()

if __name__ == '__main__':
    tgl = date.today().strftime('%d/%m/%Y')
    adm = Navigation_admin()
    cln = Client(ctrl_c = Client_controller(), tgl = tgl)
    log_ctrl = Login_controller(adm, cln)
    login = Login(Tk(),log_ctrl)
    login.show_window_login()

