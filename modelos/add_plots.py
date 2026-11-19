#!/usr/bin/env python3
# Duplica o BrasilSFC.mky e adiciona PLOTS na faixa Brasil, fiados às variáveis-chave,
# pra o modelo "ganhar vida" no play. Trabalha numa CÓPIA — não toca o original.
import sys, re, shutil
sys.path.append('/home/morpheus/src/minsky')
from pyminsky import minsky
import xml.etree.ElementTree as ET

SRC = '/home/morpheus/Documentos/tessera-talk/roteiros/ajuste fiscal/keen-ravel/models/BrasilSFC.mky'
OUT = '/home/morpheus/Documentos/tessera-talk/roteiros/ajuste fiscal/keen-ravel/models/BrasilSFC-com-plots.mky'
TMP = '/tmp/brasil_plots_tmp.mky'

# plots a criar: (titulo, x, y, [variaveis a fiar nos pens 6,7,8...])
PLOTS = [
    ('Divida_e_Cambio', 500, 3000, ['b_divida', 'e_cambio']),
    ('Reservas_e_Juro', 1150, 3000, ['R_reservas', 'r_gov', 'carry']),
]
PEN0 = 6   # índice da 1ª porta de entrada (pen) num PlotWidget novo (6 bounds + pens)

minsky.load(SRC)
plot_focus = []
for titulo, x, y, _vars in PLOTS:
    minsky.canvas.addPlot()
    h = minsky.canvas.itemFocus
    h.moveTo(x, y)
    try:
        h.title(titulo)
    except Exception:
        pass
    plot_focus.append((x, y))
minsky.save(TMP)
print('plots adicionados; itens:', len(minsky.model.items()))

# ---- cirurgia de XML: fiar variavel.saida -> plot.pen ----
xml = open(TMP).read()
root = ET.fromstring(re.sub(r'xmlns="[^"]+"', '', xml, count=1))


def ports(it):
    return [p.text for p in it.find('ports').iter('int')] if it.find('ports') is not None else []


by_name = {}
plot_by_pos = {}
for it in root.find('items'):
    nm = it.findtext('name'); typ = it.findtext('type')
    x = it.findtext('x'); y = it.findtext('y')
    if nm:
        by_name[nm] = it
    if typ == 'PlotWidget' and x and y:
        plot_by_pos[(round(float(x)), round(float(y)))] = it

wires = []
wid = 95000
for (titulo, px, py, vs) in PLOTS:
    plot_it = plot_by_pos[(px, py)]
    pp = ports(plot_it)
    for j, vname in enumerate(vs):
        var_it = by_name.get(vname)
        if var_it is None:
            print('  !! variável não encontrada:', vname); continue
        src = ports(var_it)[0]          # porta de saída da variável
        dst = pp[PEN0 + j]              # pen do plot
        wid += 1
        wires.append('  <Wire><id>%d</id><from>%s</from><to>%s</to></Wire>' % (wid, src, dst))
        print('  fio: %s -> plot "%s" pen %d' % (vname, titulo, j))

newxml = xml.replace('</wires>', '\n'.join(wires) + '\n </wires>', 1)
open(OUT, 'w').write(newxml)
print('salvo:', OUT)

# ---- validar: carrega, roda, renderiza os plots pra conferir que receberam dados ----
minsky.load(OUT)
minsky.reset()
while minsky.t() < 20:
    minsky.step()
print('rodou ate t=%.2f sem erro' % minsky.t())
try:
    minsky.renderAllPlotsAsSVG('/tmp/brasil_plots_render.svg')
    svg = open('/tmp/brasil_plots_render.svg').read()
    print('SVG dos plots: %d bytes (dados presentes se > ~2000)' % len(svg))
except Exception as e:
    print('render falhou:', type(e).__name__, e)
