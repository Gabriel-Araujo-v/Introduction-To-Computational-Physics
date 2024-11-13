
import matplotlib.pyplot as plt
import numpy as np

class IterateMapApp:
    def __init__(self, r=0.2, x=0.6, iterations=50):
        self.r = r  # Valor inicial de r
        self.x = x  # Valor inicial de x
        self.iterations = iterations  # Número de iterações

    # Getters e setters para r, x e iterations
    def set_r(self, r):
        self.r = r

    def get_r(self):
        return self.r

    def set_x(self, x):
        self.x = x

    def get_x(self):
        return self.x

    def set_iterations(self, iterations):
        self.iterations = iterations

    def get_iterations(self):
        return self.iterations

    def calculate(self):
        x_values = []
        iteration_values = []

        x = self.x
        for i in range(self.iterations + 1):
            x_values.append(x)
            iteration_values.append(i)
            x = self.map(self.r, x)

        self.plot_results(iteration_values, x_values)

    def map(self, r, x):
        return 4 * r * x * (1 - x)  # Iteração do mapa logístico

    def plot_results(self, iteration_values, x_values):
        plt.figure(figsize=(10, 6))
        plt.plot(iteration_values, x_values, marker='o', linestyle='-', markersize=4)
        plt.xlabel('Iterações')
        plt.ylabel('x')
        plt.title(f'Trajetória para r = {self.r}, x0 = {self.x}')
        plt.grid(True)
        plt.show()

class BifurcateApp:
    def __init__(self, initial_r=0.2, dr=0.005, ntransient=200, nplot=50):
        self.r = initial_r  # Parâmetro de controle
        self.dr = dr  # Incremento do parâmetro r, sugerido dr <= 0.01
        self.ntransient = ntransient  # Número de iterações não plotadas
        self.nplot = nplot  # Número de iterações plotadas
        self.x = 0.5  # Valor inicial de x
        self.results = []  # Lista para armazenar os resultados

    def map(self, x, r):
        # Mapa logístico: calcula o próximo valor de x
        return 4 * r * x * (1 - x)

    def do_step(self):
        # Realiza um passo de iteração para r < 1.0
        if self.r < 1.0:
            x = self.x

            # Iterações transitórias (não plotadas)
            for i in range(self.ntransient):
                x = self.map(x, self.r)

            # Iterações plotadas (metade na primeira cor, metade na segunda)
            for i in range(self.nplot):
                x = self.map(x, self.r)
                self.results.append((self.r, x))  # Armazena os valores de r e x

            # Incrementa r para a próxima iteração
            self.r += self.dr

    def plot_results(self):
        # Cria o gráfico de bifurcação
        r_values, x_values = zip(*self.results)
        plt.figure(figsize=(10, 6))
        plt.scatter(r_values, x_values, s=1)  # Plotagem com pontos pequenos
        plt.xlabel('r')
        plt.ylabel('x')
        plt.xlim([0.7,1])
        plt.title('Diagrama de Bifurcação')
        plt.grid(True)
        plt.show()

    def reset(self):
        # Redefine os parâmetros e limpa os resultados
        self.r = 0.2
        self.dr = 0.005
        self.ntransient = 200
        self.nplot = 50
        self.results.clear()

class GraphicalSolutionApp:
    def __init__(self, r=0.7, x=0.1, iterate=1):
        self.r = r  # Parâmetro de controle
        self.x0 = x  # Valor inicial de x
        self.iterate = iterate  # Número de iterações de f(x)

    def f(self, x):
        """
        Função do mapa logístico: f(x) = 4 * r * x * (1 - x), com múltiplas iterações.
        """
        for _ in range(self.iterate):
            x = 4 * self.r * x * (1 - x)
        return x

    def plot_function_and_diagonal(self):
        """
        Plota a curva do mapa logístico f(x) e a linha diagonal y = x.
        """
        x_values = np.linspace(0, 1, 500)
        y_values = [self.f(x) for x in x_values]

        # Curva do mapa logístico
        plt.plot(x_values, y_values, label='f(x)')

        # Linha diagonal y = x
        plt.plot(x_values, x_values, linestyle='--', label='y = x')

    def draw_trajectory(self, steps=10):
        """
        Desenha a trajetória da solução gráfica do mapa logístico.
        """
        x, y = self.x0, 0

        for _ in range(steps):
            # Desenha a linha vertical até a curva f(x)
            y_next = self.f(x)
            plt.plot([x, x], [y, y_next], color='r', linewidth=0.8)

            # Desenha a linha horizontal até a diagonal y = x
            plt.plot([x, y_next], [y_next, y_next], color='r', linewidth=0.8)

            # Atualiza x e y para o próximo passo
            x, y = y_next, y_next

        # Adiciona a legenda com o último valor de x
        plt.text(0.05, 0.95, f'Último x = {x:.4f}', fontsize=12,
                 transform=plt.gca().transAxes, ha='left', va='top',
                 bbox=dict(facecolor='white', alpha=0.8))

    def start_running(self, steps=10):
        """
        Inicia a simulação gráfica, incluindo f(x), y = x e a trajetória.
        """
        plt.figure(figsize=(6, 6))
        self.plot_function_and_diagonal()  # Plota f(x) e y = x
        self.draw_trajectory(steps)  # Desenha a trajetória iterativa

        # Configuração do gráfico
        plt.xlim(0, 1)
        plt.ylim(0, 1)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title(f'Solução Gráfica para r={self.r}, x0={self.x0}, iter={self.iterate}')
        plt.grid(True)
        plt.show()
