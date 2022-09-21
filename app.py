from sre_parse import DIGITS
import tkinter as tk
import math 

LARGE_FONT_STYLE = ("Arial", 40, "bold")
SMALL_FONT_STYLE = ("Arial", 16)
DIGITS_FONT_STYLE = ("Arial", 24)
DEFAULT_FONT_STYLE = ("Arial", 20)

BRANCO = "#f3f3f7"
CINZA = "#333549"
CINZA_ESCURO = "#2b2d42"
LARANJA_ESCURO = "#eb5e28"
PRETO = "#11151c"
LARANJA = "#fe7f2d"
#BRANCO = "#25265E"

class Calculadora:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("320x600")
        self.window.resizable(0,0)
        self.window.title("Calculadora")

        self.total_expressao = ""
        self.atual_expressao = ""

        self.integrar = False
        self.limite_inferior = None
        self.limite_superior = None
        self.funcao = ""

        self.display_frame = self.criar_frame()
        
        self.total_label, self.label = self.create_display_labels()
        
        self.digits = {
            7:(2,1), 8:(2,2), 9:(2,3),
            4:(3,1), 5:(3,2), 6:(3,3),
            1:(4,1), 2:(4,2), 3:(4,3),
            0:(5,2), '.':(5,3)
        }

        self.operations = {"/": "\u00F7", "*": "\u00D7", "-":"-", "+":"+"}

        self.num_especiais = {math.pi:"π", math.e: "e"}
        
        self.buttons_frame = self.criar_painel_botoes()

        for x in range(1,5):
            self.buttons_frame.rowconfigure(x, weight=1)
            self.buttons_frame.columnconfigure(x, weight=1)
        
        self.create_digit_buttons()
        self.create_operator_buttons()
        self.create_special_buttons()
        self.bind_keys()

    def bind_keys(self):
        self.window.bind("<Return>", lambda event: self.evaluate())

        for key in self.digits:
            self.window.bind(str(key), lambda event, digit=key: self.add_to_expression(digit))
        
        for key in self.operations:
            self.window.bind(key, lambda event, operator=key: self.append_operator(operator))
    
    def create_special_buttons(self):
        self.create_clear_button()
        self.create_equals_button()
        self.criar_botao_integral()
        self.criar_botao_icognita()
        self.criar_botao_num_especiais()
        self.create_potencia_button()
        self.create_raiz_button()
        self.criar_botao_cos()
    
    def create_display_labels(self):
        total_label = tk.Label(self.display_frame, text=self.total_expressao, anchor=tk.E, bg=PRETO, fg=BRANCO, padx=24, font=SMALL_FONT_STYLE)
        total_label.pack(expand=True, fill="both")

        label = tk.Label(self.display_frame, text=self.atual_expressao, anchor=tk.E, bg=PRETO, fg=BRANCO, padx=24, font=LARGE_FONT_STYLE)
        label.pack(expand=True, fill="both")
        
        return total_label, label

    def criar_frame(self):
        frame = tk.Frame(self.window, height=221, bg=PRETO)
        frame.pack(expand=True, fill="both")
        return frame
    
    def add_to_expression(self, value):
        self.atual_expressao += str(value)
        self.update_label()

    def escreve_especiais_na_expressao(self, simbolo):
        self.atual_expressao += simbolo
        self.update_label()

    def criar_painel_botoes(self):
        frame = tk.Frame(self.window)
        frame.pack(expand=True,fill="both")
        return frame

    def create_digit_buttons(self):
        for digit, grid_value in self.digits.items():
            botao = tk.Button(self.buttons_frame, text=str(digit), bg=CINZA, fg=BRANCO, font=DIGITS_FONT_STYLE, 
                            borderwidth=0, command=lambda x = digit: self.add_to_expression(x))
            botao.grid(row=grid_value[0], column=grid_value[1], sticky=tk.NSEW)

    def append_operator(self, operator):
        self.atual_expressao += operator
        self.total_expressao += self.atual_expressao
        self.atual_expressao = ""
        self.update_total_label()
        self.update_label()
    
    def create_operator_buttons(self):
        i = 1
        for operator, symbol in self.operations.items():
            botao = tk.Button(self.buttons_frame, text=symbol, bg=CINZA_ESCURO, fg=BRANCO, font=DEFAULT_FONT_STYLE,
                                borderwidth=0, command=lambda x = operator: self.append_operator(x))
            botao.grid(row=i, column=4, sticky=tk.NSEW)
            i += 1

    def clear(self):
        self.atual_expressao = ""
        self.total_expressao = ""
        self.integrar = False
        self.limite_inferior = None
        self.limite_superior = None
        self.update_label()
        self.update_total_label()

    def create_clear_button(self):
        botao = tk.Button(self.buttons_frame, text="C", bg=LARANJA_ESCURO, fg=BRANCO, font=DIGITS_FONT_STYLE, 
                            borderwidth=0, command=self.clear)
        botao.grid(row=0, column=1, sticky=tk.NSEW)
    
    def criar_botao_icognita(self):
        botao = tk.Button(self.buttons_frame, text="x", bg=CINZA_ESCURO, fg=BRANCO, font=DIGITS_FONT_STYLE, 
                            borderwidth=0, command=lambda x = "x": self.escreve_especiais_na_expressao(x))
        botao.grid(row=5, column=1, sticky=tk.NSEW)

    def integral(self):
        self.clear()
        self.total_label.config(text = "\u222B[a,b] f(x)dx")
        self.label.config(text = "a = ")
        self.integrar = True
        #self.update_total_label()

    def criar_botao_integral(self):
        botao = tk.Button(self.buttons_frame, text="\u222B", bg=CINZA_ESCURO, fg=BRANCO, font=DEFAULT_FONT_STYLE, 
                            borderwidth=0, command=self.integral)
        botao.grid(row=1, column=1, sticky=tk.NSEW)

    def criar_botao_num_especiais(self):        
        i = 2
        for valor, simbolo in self.num_especiais.items():
            botao = tk.Button(self.buttons_frame, text=simbolo, bg=CINZA_ESCURO, fg=BRANCO, font=DIGITS_FONT_STYLE,
                                borderwidth=0, command=lambda x = simbolo: self.escreve_especiais_na_expressao(x))
            botao.grid(row=0, column=i, sticky=tk.NSEW)
            i += 1

    def potencia(self):
        self.atual_expressao += "**"
        self.total_expressao += self.atual_expressao
        self.atual_expressao = ""
        self.update_total_label()
        self.update_label()
        
    def create_potencia_button(self):
        botao = tk.Button(self.buttons_frame, text="x\u02B8", bg=CINZA_ESCURO, fg=BRANCO, font=DEFAULT_FONT_STYLE,
                            borderwidth=0, command=self.potencia)
        botao.grid(row=1, column=2, sticky=tk.NSEW)

    def raiz(self):
        self.atual_expressao = str(eval(f"{self.atual_expressao}**0.5"))
        self.update_label()

    def create_raiz_button(self):
        botao = tk.Button(self.buttons_frame, text="\u221Ax", bg=CINZA_ESCURO, fg=BRANCO, font=DEFAULT_FONT_STYLE, borderwidth=0, command=self.raiz)
        botao.grid(row=1, column=3, sticky=tk.NSEW)

    def cos(self):
        trig_valores = self.atual_expressao
        self.atual_expressao = "cos(" + trig_valores + ")"
        self.update_label()   

    def criar_botao_cos(self):
        botao = tk.Button(self.buttons_frame, text="cos(x)", bg=CINZA_ESCURO, fg=BRANCO, font=DEFAULT_FONT_STYLE,
                            borderwidth=0, command=self.cos)
        botao.grid(row=0, column=4, sticky=tk.NSEW)

    def evaluate(self):
        self.total_expressao += self.atual_expressao
        self.update_total_label()

        self.trata_num_especiais_na_expressao()
        
        try:
            if self.integrar and self.limite_inferior != None and self.limite_superior != None:
                self.atual_expressao = str(self.calcula_integral())
                self.total_expressao = ""
            else:
                self.atual_expressao = str(eval(self.total_expressao))
                self.total_expressao = ""
        except Exception as e:
            self.atual_expressao = "Error"
        finally:
            if self.integrar == True and "Error" not in self.atual_expressao:
                self.get_limites_integral()
            else: 
                self.update_total_label()
                self.update_label()

    def trata_num_especiais_na_expressao(self):
        for valor, simbolo in self.num_especiais.items():
            self.total_expressao = self.total_expressao.replace(simbolo, f' {valor} ')

        if "cos" in self.total_expressao:
            self.total_expressao = self.total_expressao.replace("cos", "math.cos")
        
    def get_limites_integral(self):
        if self.limite_inferior == None:
            self.limite_inferior = float(self.atual_expressao)
            self.atual_expressao = ""
            self.label.config(text = "b = ")
        
        elif self.limite_superior == None:
            self.limite_superior = float(self.atual_expressao)
            self.atual_expressao = ""
            self.label.config(text = "f(x) = ")

    def f(self, x):
        funcao = self.funcao.replace("x", str(x))
        return eval(funcao)
        
    def calcula_integral(self):
        self.funcao = self.total_expressao
        resultado = None
        a = int(self.limite_inferior)
        b = int(self.limite_superior)
        n = 1000
        delta_x = (b - a)/n
        
        resultado = 0.5*self.f(a) + sum([self.f(a + i*delta_x) for i in range(1,n)]) + 0.5*self.f(b)
        resultado *= delta_x 

        self.integrar = False

        return resultado
        
    def create_equals_button(self):
        botao = tk.Button(self.buttons_frame, text="=", bg=LARANJA, fg=BRANCO, font=DEFAULT_FONT_STYLE, borderwidth=0, command=self.evaluate)
        botao.grid(row=5, column=4, sticky=tk.NSEW)

    def update_total_label(self):
        expression = ""
        
        if self.integrar and self.limite_inferior == None:
            expression = "a = "
        elif self.integrar and self.limite_superior == None:
            expression = "b = "
        elif self.integrar and self.funcao == "":
            expression = "f(x) = "
        elif self.integrar == False and self.limite_inferior != None and self.limite_superior != None and self.funcao != "":
            expression = "\u222B[" + str(int(self.limite_inferior)) + "," + str(int(self.limite_superior)) + "] " + self.funcao + "dx"

        expression += self.total_expressao

        for operator, symbol in self.operations.items():
            if "**" in expression:
                expression = expression.replace("**", "^")
            if "math.cos" in expression:
                expression = expression.replace("math.cos", "cos")
            expression = expression.replace(operator, f' {symbol} ')
        
        
        self.total_label.config(text=expression)

    def update_label(self):
        
        self.label.config(text=self.atual_expressao[:10])
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = Calculadora()
    app.run()
