import sqlite3
from datetime import datetime, timedelta
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty
from kivy.clock import Clock    

# --- BANCO DE DADOS ---
def init_db():
    conn = sqlite3.connect("financas.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT,        -- 'Receita' ou 'Despesa'
            categoria TEXT,   -- 'Salário', 'Saúde', 'Restauração', etc.
            valor REAL,
            data TEXT         -- Formato YYYY-MM-DD
        )
    """)
    conn.commit()
    conn.close()

# --- TELAS DO APP ---
class TelaPrincipal(Screen):
    total_carteira = StringProperty("0.00 €")

    def on_enter(self):
        self.atualizar_saldo()
        
        Clock.schedule_interval(self.mover_mario, 1/60.0)
        
    def on_leave(self):
        Clock.unschedule(self.mover_mario)
        
    def mover_mario(self, dt):
        mario = self.ids.mario_sprite
        mario.x -= 2
        
        if mario.x < -mario.width:
            mario.x = self.width

    def atualizar_saldo(self):
        conn = sqlite3.connect("financas.db")
        cursor = conn.cursor()
        cursor.execute("SELECT tipo, valor FROM transacoes")
        linhas = cursor.fetchall()
        conn.close()

        saldo = 0.0
        for tipo, valor in linhas:
            if tipo == "Receita":
                saldo += valor
            else:
                saldo -= valor
        self.total_carteira = f"{saldo:.2f} €"

    def salvar_transacao(self, tipo, categoria, valor_texto):
        try:
            valor = float(valor_texto)
            if valor <= 0: return
        except ValueError:
            return # Ignora valores inválidos

        data_hoje = datetime.now().strftime("%Y-%m-%d")

        conn = sqlite3.connect("financas.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO transacoes (tipo, categoria, valor, data) VALUES (?, ?, ?, ?)",
            (tipo, categoria, valor, data_hoje)
        )
        conn.commit()
        conn.close()
        
        self.atualizar_saldo()


class TelaHistorico(Screen):
    texto_historico = StringProperty("Clique no filtro para carregar.")
    periodo_atual = "semanal"

    def exibir_historico(self, periodo=None):
        if periodo:
            self.periodo_atual = periodo
       
        conn = sqlite3.connect("financas.db")
        cursor = conn.cursor()
        
        hoje = datetime.now()
        if self.periodo_atual == "semanal":
            data_limite = (hoje - timedelta(days=7)).strftime("%Y-%m-%d")
            titulo = "--- HISTÓRICO SEMANAL ---\n"
        else:
            data_limite = (hoje - timedelta(days=30)).strftime("%Y-%m-%d")
            titulo = "--- HISTÓRICO MENSAL ---\n"

        cursor.execute(
            "SELECT id, tipo, categoria, valor, data FROM transacoes WHERE data >= ? ORDER BY data DESC", 
            (data_limite,)
        )
        linhas = cursor.fetchall()
        conn.close()

        if not linhas:
            self.texto_historico = titulo + "\nNenhum registro neste período."
            return

        resultado = titulo + "\n"
        for id_trans, tipo, cat, val, data in linhas:
            sinal = "+" if tipo == "Receita" else "-"
            resultado += f"ID: {id_trans}| [{data}] {sinal} {val:.2f} € ({cat})\n"
        	#id para deletar transaçoes erradas.
        self.texto_historico = resultado
    
    def deletar_transacao(self, id_texto):
        try:
            id_trans = int(id_texto)
        except ValueError:
            return
        conn = sqlite3.connect("financas.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM transacoes WHERE id = ?", (id_trans,))
        conn.commit()
        conn.close()

	#Atualizar a tela de historico
        self.exibir_historico() 


class GerenciadorTelas(ScreenManager):
    pass


class FinancasApp(App):
    def build(self):
        init_db()
        return GerenciadorTelas()

if __name__ == "__main__":
    FinancasApp().run()

