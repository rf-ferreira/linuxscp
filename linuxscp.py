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
            SCP()
            root.withdraw()
        except:
            tk.messagebox.showerror('Algo deu errado','Não foi possivel conectar ao servidor')
    
class SCP:
    def __init__(self):
        self.window = tk.Toplevel()
        self.window.resizable(False, False)
        self.window.title("Linux SCP")
        self.window.protocol("WM_DELETE_WINDOW", self.close)
        self.widgets()
        
    def widgets(self):
        self.lbl_server_directory = tk.Label(self.window, text="Diretorio do servidor")
        self.lbl_server_directory.grid(row=0, column=0)
        self.server_directory = tk.Entry(self.window)
        self.server_directory.grid(row=1, column=0)

        self.btn_browse_files = tk.Button(self.window, text="Procurar arquivo", command=self.browse_files)
        self.btn_browse_files.grid(row=2, column=0, sticky="EW")
        self.btn_send = tk.Button(self.window, text="Enviar para servidor", command=self.send_to_server)
        self.btn_send.grid(row=3, column=0, sticky="EW")
        self.btn_get = tk.Button(self.window, text="Transferir do servidor", command=self.get_from_server)
        self.btn_get.grid(row=4, column=0, sticky="EW")
        
        self.file_name = False

    def browse_files(self):
        self.file = tk.filedialog.askopenfile(parent=self.window,mode='rb',title='Procurar arquivo')
        if self.file:
            self.file_name = tk.Label(self.window, text=self.file.name)
            self.file_name.grid(row=5, column=0)

    def send_to_server(self):
        if self.file_name and self.server_directory.get().strip() != '':
            ftp_client = client.open_sftp()
            ftp_client.put(f'{self.file.name}', f'{self.server_directory.get()}{self.file.name.split("/")[-1]}')
            ftp_client.close()
            tk.messagebox.showinfo('Sucesso', 'Arquivo enviado', parent=self.window)
        else:
            tk.messagebox.showerror('Erro', 'Nao foi possivel enviar o arquivo', parent=self.window)
        
        if self.file_name:
            self.file_name.destroy()
            self.file_name = False
        self.server_directory.delete(0, 'end')

    def get_from_server(self):
        self.directory = tk.filedialog.askdirectory(parent=self.window, title="Escolher diretorio")
        stdin, stdout, stderr = client.exec_command(f'ls {"/".join(self.server_directory.get().split("/")[:-1])}')
        if self.server_directory.get().strip() != '' and f'{self.server_directory.get().split("/")[-1]}\n' in stdout.readlines():
            ftp_client = client.open_sftp()
            ftp_client.get(f'{self.server_directory.get()}', f'{self.directory}/{self.server_directory.get().split("/")[-1]}')
            ftp_client.close()
            tk.messagebox.showinfo('Sucesso', 'Arquivo transferido', parent=self.window)
        else:
            tk.messagebox.showerror('Erro', 'Nao foi possivel transferir o arquivo', parent=self.window)
        self.server_directory.delete(0, 'end')

    def close(self):
        root.quit()

root = tk.Tk()
root.title('Linux SCP')
root.resizable(False, False)
app = LinuxSCP(master=root)
app.mainloop()
