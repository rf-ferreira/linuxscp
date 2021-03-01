import os
import paramiko
import tkinter as tk
import tkinter.filedialog
from tkinter import messagebox

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

class LinuxSCP(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid()
        self.widgets()

    def widgets(self):
        self.user = tk.Label(text="User")
        self.user.grid(row=0, column=0)
        self.user_entry = tk.Entry()
        self.user_entry.grid(row=1, column=0)

        self.server_ip = tk.Label(text="Server IP")
        self.server_ip.grid(row=2, column=0)
        self.server_ip_entry = tk.Entry()
        self.server_ip_entry.grid(row=3, column=0)

        self.port = tk.Label(text="Port")
        self.port.grid(row=4, column=0)
        self.port_entry = tk.Entry()
        self.port_entry.grid(row=5, column=0)

        self.password = tk.Label(text="Password")
        self.password.grid(row=6, column=0)
        self.password_entry = tk.Entry(show="•")
        self.password_entry.grid(row=7, column=0)

        self.button = tk.Button(text="Conectar", command=self.connect)
        self.button.grid(row=8, column=0)


    def connect(self):
        try:
            client.connect(self.server_ip_entry.get(), port=self.port_entry.get(), username=self.user_entry.get(), password=self.password_entry.get())
            print('Conectado com sucesso')
            SCP()
        except Exception as e:
            print('Não foi possivel conectar ao servidor')
            print(e)
            tk.messagebox.showerror('Algo deu errado','Não foi possivel conectar ao servidor')
    
class SCP:
    def __init__(self):
       self.window = tk.Toplevel()
       self.window.resizable(False, False)
       self.window.title("Linux SCP")
       self.widgets()

    def widgets(self):
        print(server_ip)
        self.btn_browse_files = tk.Button(self.window, text="Procurar arquivo", command=self.browse_files)
        self.btn_browse_files.grid(row=0, column=0, sticky="EW")
        self.btn_send = tk.Button(self.window, text="Enviar para servidor", command=self.send_to_server)
        self.btn_send.grid(row=1, column=0)

    def browse_files(self):
        self.file = tk.filedialog.askopenfile(parent=root,mode='rb',title='Procurar arquivo')
        if self.file:
            self.file_name = tk.Label(self.window, text=self.file.name)
            self.file_name.grid(row=2, column=0)

    def send_to_server(self):
        try:
            ftp_client = client.open_sftp()
            ftp_client.put(f'{self.file.name}', f'/root/{self.file.name.split("/")[-1]}')
            ftp_client.close()
            print('Arquivo enviado com sucesso')
        except:
            print('Nao foi possivel enviar o arquivo')

root = tk.Tk()
root.title('Linux SCP')
app = LinuxSCP(master=root)
app.mainloop()
