import subprocess
import re
import matplotlib.pyplot as plt
import numpy as np
import os
import statistics
from PIL import Image, ImageDraw, ImageFont

num_execucoes = int(input("Quantas execuções? "))

tempos_sequencial = []
tempos_openmp = []
tempos_tbb = []

tempos_sequencial_um_nucleo = []
tempos_openmp_um_nucleo = []
tempos_tbb_um_nucleo = []

media_sequencial = 0
desvio_sequencial = 0

media_openmp = 0
desvio_openmp = 0

media_tbb = 0
desvio_tbb = 0

media_sequencial_um_nucleo = 0
desvio_sequencial_um_nucleo = 0

media_openmp_um_nucleo = 0
desvio_openmp_um_nucleo = 0

media_tbb_um_nucleo = 0
desvio_tbb_um_nucleo = 0

script_dir = os.path.dirname(os.path.abspath(__file__))
exe_path = os.path.join(script_dir, '..', 'program_cpp', 'somar_vetor.exe')

for i in range(num_execucoes):
    print(f"({i + 1}/{num_execucoes}) Executando em múltiplos núcleos{'.' * ((i % 3) + 1)}{' ' * (3 - ((i % 3) + 1))}", end='\r')
    result = subprocess.run([exe_path], capture_output=True, text=True)
    output = result.stdout

    tempo_seq = float(re.search(r"Tempo sequencial: (\d+\.\d+)", output).group(1))
    tempo_tbb = float(re.search(r"Tempo TBB: (\d+\.\d+)", output).group(1))
    tempo_openmp = float(re.search(r"Tempo OpenMP: (\d+\.\d+)", output).group(1))

    tempos_sequencial.append(tempo_seq)
    tempos_openmp.append(tempo_openmp)
    tempos_tbb.append(tempo_tbb)

print('\n')

for i in range(num_execucoes):
    print(f"({i + 1}/{num_execucoes}) Executando em um núcleo{'.' * ((i % 3) + 1)}{' ' * (3 - ((i % 3) + 1))}", end='\r')
    result = subprocess.run(["taskset", "-c", "0", exe_path], capture_output=True, text=True)
    output = result.stdout

    tempo_seq = float(re.search(r"Tempo sequencial: (\d+\.\d+)", output).group(1))
    tempo_tbb = float(re.search(r"Tempo TBB: (\d+\.\d+)", output).group(1))
    tempo_openmp = float(re.search(r"Tempo OpenMP: (\d+\.\d+)", output).group(1))

    tempos_sequencial_um_nucleo.append(tempo_seq)
    tempos_openmp_um_nucleo.append(tempo_openmp)
    tempos_tbb_um_nucleo.append(tempo_tbb)

media_sequencial = statistics.mean(tempos_sequencial)
desvio_sequencial = statistics.stdev(tempos_sequencial)

media_openmp = statistics.mean(tempos_openmp)
desvio_openmp = statistics.stdev(tempos_openmp)

media_tbb = statistics.mean(tempos_tbb)
desvio_tbb = statistics.stdev(tempos_tbb)

media_sequencial_um_nucleo = statistics.mean(tempos_sequencial_um_nucleo)
desvio_sequencial_um_nucleo = statistics.stdev(tempos_sequencial_um_nucleo)

media_openmp_um_nucleo = statistics.mean(tempos_openmp_um_nucleo)
desvio_openmp_um_nucleo = statistics.stdev(tempos_openmp_um_nucleo)

media_tbb_um_nucleo = statistics.mean(tempos_tbb_um_nucleo)
desvio_tbb_um_nucleo = statistics.stdev(tempos_tbb_um_nucleo)

print(f"\n\nMédia sequencial: {media_sequencial}")
print(f"Desvio padrão sequencial: {desvio_sequencial}")

print(f"\nMédia openmp: {media_openmp}")
print(f"Desvio padrão openmp: {desvio_openmp}")

print(f"\nMédia tbb: {media_tbb}")
print(f"Desvio padrão tbb: {desvio_tbb}")

print(f"\nMédia sequencial (um núcleo): {media_sequencial_um_nucleo}")
print(f"Desvio padrão sequencial (um núcleo): {desvio_sequencial_um_nucleo}")

print(f"\nMédia openmp (um núcleo): {media_openmp_um_nucleo}")
print(f"Desvio padrão openmp (um núcleo): {desvio_openmp_um_nucleo}")

print(f"\nMédia tbb (um núcleo): {media_tbb_um_nucleo}")
print(f"Desvio padrão tbb (um núcleo): {desvio_tbb_um_nucleo}")

def adicionar_rotulos(x, y):
    for i, j in zip(x, y):
        plt.text(i, j, f"{j:.3f}", fontsize=8, ha='right')

execucoes = np.arange(1, num_execucoes + 1)

adicionar_rotulos(execucoes, tempos_sequencial)
adicionar_rotulos(execucoes, tempos_openmp)
adicionar_rotulos(execucoes, tempos_tbb)
adicionar_rotulos(execucoes, tempos_sequencial_um_nucleo)
adicionar_rotulos(execucoes, tempos_openmp_um_nucleo)
adicionar_rotulos(execucoes, tempos_tbb_um_nucleo)

plt.plot(execucoes, tempos_sequencial, marker='o', label='Sequencial')
plt.plot(execucoes, tempos_openmp, marker='s', label='OpenMP')
plt.plot(execucoes, tempos_tbb, marker='^', label='TBB')
plt.plot(execucoes, tempos_sequencial_um_nucleo, marker='o', linestyle='dashed', label='Sequencial (um núcleo)')
plt.plot(execucoes, tempos_openmp_um_nucleo, marker='s', linestyle='dashed', label='OpenMP (um núcleo)')
plt.plot(execucoes, tempos_tbb_um_nucleo, marker='^', linestyle='dashed', label='TBB (um núcleo)')
plt.xlabel("Execução")
plt.ylabel("Tempo (segundos)")
plt.title("Tempos de execução")
plt.legend()
plt.grid()
figure = plt.gcf()
figure.set_size_inches(32, 18)
plt.savefig("../grafico_tempos.png", bbox_inches='tight', dpi=150)

def gerar_tabela_imagem():
    largura, altura = 800, 30 * (num_execucoes + 2)
    imagem = Image.new("RGB", (largura, altura), "white")
    draw = ImageDraw.Draw(imagem)
    fonte = ImageFont.load_default()

    colunas = ["Execucao", "Seq.", "OpenMP", "TBB", "Seq. (1 Nuc.)", "OpenMP (1 Nuc.)", "TBB (1 Nuc.)"]
    espacamento = [80, 80, 80, 80, 100, 120, 100]
    x_inicial = 20
    y = 10
    
    for i, titulo in enumerate(colunas):
        draw.text((x_inicial + sum(espacamento[:i]), y), titulo, fill="black", font=fonte)
    y += 30
    
    for i in range(num_execucoes):
        valores = [
            str(i + 1),
            f"{tempos_sequencial[i]:.5f}",
            f"{tempos_openmp[i]:.5f}",
            f"{tempos_tbb[i]:.5f}",
            f"{tempos_sequencial_um_nucleo[i]:.5f}",
            f"{tempos_openmp_um_nucleo[i]:.5f}",
            f"{tempos_tbb_um_nucleo[i]:.5f}"
        ]
        for j, valor in enumerate(valores):
            draw.text((x_inicial + sum(espacamento[:j]), y), valor, fill="black", font=fonte)
        y += 30
    
    imagem.save("../tabela_tempos.png")

gerar_tabela_imagem()
