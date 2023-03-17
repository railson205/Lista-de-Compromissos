import tkinter as tk
from datetime import date, datetime, timedelta

class MyApplication:
    def __init__(self):
        self.organizar_compromissos()
        self.window = tk.Tk()
        self.window.title("Minha Aplicação")
        
        # Criar uma lista de compromissos
        self.compromissos = tk.Listbox(self.window, height=10, width=50)
        self.compromissos.pack(pady=10)

        # Carregar compromissos existentes do arquivo
        self.carregar_compromissos()

        # Adicionar campos de entrada de novo compromisso
        tk.Label(self.window, text="Novo Compromisso:").pack()
        self.nome_compromisso = tk.Entry(self.window, width=30)
        self.nome_compromisso.pack(pady=5)
        self.data_compromisso = tk.Entry(self.window, width=30)
        self.data_compromisso.pack(pady=5)

        # Adicionar botão para adicionar novo compromisso
        tk.Button(self.window, text="Adicionar Compromisso", command=self.adicionar_compromisso).pack(pady=5)

        self.window.mainloop()

    def carregar_compromissos(self):
        try:
            with open("compromissos.txt", "r") as f:
                for line in f:
                    compromisso, data_str = line.strip().split("-")
                    data = datetime.strptime(data_str, "%d/%m/%Y").date()
                    self.adicionar_compromisso_lista(compromisso, data)
        except FileNotFoundError:
            with open("compromissos.txt", "w") as f:
                pass

    def adicionar_compromisso(self):
        nome = self.nome_compromisso.get().strip()
        data_str = self.data_compromisso.get().strip()

        if nome and data_str:
            try:
                data = datetime.strptime(data_str, "%d/%m/%Y").date()
                self.adicionar_compromisso_lista(nome, data)
                self.salvar_compromisso(nome, data)
                self.nome_compromisso.delete(0, tk.END)
                self.data_compromisso.delete(0, tk.END)
            except ValueError:
                tk.messagebox.showerror("Erro", "Data inválida. Digite no formato dd/mm/aaaa")

    def adicionar_compromisso_lista(self, nome, data):
        hoje = date.today()
        delta = data - hoje
        dias_restantes = delta.days

        if dias_restantes == 0:
            dias_restantes_str = "Hoje"
        elif dias_restantes < 0:
            return
        else:
            dias_restantes_str = f"Faltam {dias_restantes} dias"

        self.compromissos.insert(tk.END, f"{nome} - {dias_restantes_str}")

    def salvar_compromisso(self, nome, data):
        with open("compromissos.txt", "a") as f:
            f.write(f"{nome}-{data.strftime('%d/%m/%Y')}\n")
        self.organizar_compromissos()
    
    def organizar_compromissos(self):
    # Abre o arquivo de texto com os compromissos
        # abre o arquivo e carrega os compromissos para uma lista
        with open('compromissos.txt', 'r') as f:
            compromissos = f.readlines()

        # converte cada compromisso para um dicionário com o nome e a data
        compromissos = [comp.strip().split('-') for comp in compromissos]
        compromissos = [{'nome': comp[0], 'data': datetime.strptime(comp[1], '%d/%m/%Y')} for comp in compromissos]

        # ordena os compromissos pela data mais próxima
        compromissos.sort(key=lambda x: x['data'])

        # reescreve o arquivo com os compromissos ordenados
        with open('compromissos.txt', 'w') as f:
            for comp in compromissos:
                f.write(f"{comp['nome']}-{comp['data'].strftime('%d/%m/%Y')}\n")

app = MyApplication()
