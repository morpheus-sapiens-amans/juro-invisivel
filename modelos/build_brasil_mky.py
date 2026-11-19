#!/usr/bin/env python3
# Constrói o .mky Brasil estendendo MinskyGovernmentNonlinear.mky.
# Transcreve python-modelo/brasil_sfc.py: BC/Selic + dívida pública + arcabouço + externo/reservas.
import sys, re
sys.path.append('/home/morpheus/src/minsky')
from pyminsky import minsky
import xml.etree.ElementTree as ET

BASE = '/home/morpheus/src/minsky/examples/MinskyGovernmentNonlinear.mky'
OUT  = '/home/morpheus/Documentos/tessera-talk/roteiros/ajuste fiscal/keen-ravel/models/BrasilSFC.mky'
TMP  = '/tmp/brasil_tmp.mky'   # arquivo intermediário (recriado a cada build)

minsky.load(BASE)

# ---------- layout ----------
BANDS = {'mon': 1250, 'fis': 1600, 'debt': 1950, 'ext': 2300, 'fx': 2650}
_col = {k: 0 for k in BANDS}
def pos(band):
    x = 260 + _col[band]*150
    _col[band] += 1
    return x, BANDS[band]

# ---------- registries ----------
params = []   # (name, value, x, y)
readers = []  # (name, x, y)
ops = []      # (key, optype, x, y)
flows = []    # (name, x, y)  named intermediates
integs = []   # (name, init, x, y)
wires = []    # (src_key, dst_key, dst_in)  dst_in in {1,2,'rate'}

def P(name, val, band):
    x,y = pos(band); params.append((name, str(val), x, y)); return name
def R(name, band):
    x,y = pos(band); readers.append((name, x, y)); return name
def O(key, op, band):
    x,y = pos(band); ops.append((key, op, x, y)); return key
def F(name, band):
    x,y = pos(band); flows.append((name, x, y)); return name
def I(name, init, band):
    x,y = pos(band); integs.append((name, str(init), x, y)); return name
def W(src, dst, din): wires.append((src, dst, din))

# ---------- readers (leem as variáveis do modelo base por nome) ----------
Y   = R('Output', 'mon')
Inv = R('Investment', 'mon')
lam = R('E_\\mathrm{Rate}', 'mon')
gFn = R('G_{Fn}', 'fis')

# ---------- parâmetros (CALIBRADOS Brasil: RMD set/25, BCB, IBGE, IPEA, Lobo&Oreiro 2012) ----------
Selic=P('Selic',0.15,'mon'); r_pre=P('r_pre',0.13,'mon'); theta=P('theta',0.47,'mon')
theta_pre=P('theta_pre',0.26,'mon'); theta_ipca=P('theta_ipca',0.27,'mon'); cupom=P('cupom_real',0.06,'mon')
tau=P('tau',0.33,'fis'); g0=P('g0',0.33,'fis')
tax_rich=P('tax_rich',0.0,'fis')   # [alavanca] primário extra do topo (PSOL/Sherazade); 0 = reproduz base
teto=P('teto',1.00,'fis'); infl0=P('infl0',0.035,'mon'); k_dem=P('k_dem',0.15,'mon')
lam0=P('lam0',0.95,'mon'); deltaK=P('deltaK',0.02,'mon'); vB=P('vB',3,'mon')
r_world=P('r_world',0.04,'ext'); risk=P('risk',0.03,'ext'); accum=P('accum',0.004,'ext')
kappa=P('kappa',1.2,'ext'); phi=P('phi',0.5,'fx')
interv=P('interv',0.15,'fx'); one=P('one',1.0,'ext'); negOne=P('negOne',-1.0,'fx')
# setor externo com elasticidades (IPEA) + renda mundial crescente (Thirlwall)
eps_x=P('eps_x',0.6,'ext'); eps_m=P('eps_m',0.3,'ext'); eta_x=P('eta_x',1.0,'ext'); eta_m=P('eta_m',1.5,'ext')
x0e=P('x0e',16.0,'ext'); m0e=P('m0e',16.0,'ext'); g_world=P('g_world',0.025,'ext'); hundred=P('hundred',100.0,'ext')

# ---------- BLOCO monetário: r_gov = θ·Selic + θpre·r_pre + θipca·(infl+cupom) [3 pernas RMD set/25] ----------
O('rgA','multiply','mon'); W(theta,'rgA',1); W(Selic,'rgA',2)          # 47% LFT segue Selic
O('rgB','multiply','mon'); W(theta_pre,'rgB',1); W(r_pre,'rgB',2)      # 26% pré+câmbio
O('ipca','add','mon');     W('infl','ipca',1); W(cupom,'ipca',2)       # NTN-B: IPCA + cupom real
O('rgC','multiply','mon'); W(theta_ipca,'rgC',1); W('ipca','rgC',2)    # 27% indexado ao IPCA
O('rgAB','add','mon');     W('rgA','rgAB',1); W('rgB','rgAB',2)
O('rgABC','add','mon');    W('rgAB','rgABC',1); W('rgC','rgABC',2)
F('r_gov','mon');          W('rgABC','r_gov',1)

# g_real = Inv/(vB*Y) - deltaK
O('kest','multiply','mon'); W(vB,'kest',1); W(Y,'kest',2)
O('invk','divide','mon');   W(Inv,'invk',1); W('kest','invk',2)
O('greal','subtract','mon');W('invk','greal',1); W(deltaK,'greal',2)
F('g_real','mon');          W('greal','g_real',1)

# infl = infl0 + k_dem*(lam - lam0)
O('gap','subtract','mon');  W(lam,'gap',1); W(lam0,'gap',2)
O('deminfl','multiply','mon'); W(k_dem,'deminfl',1); W('gap','deminfl',2)
O('inflOp','add','mon');    W(infl0,'inflOp',1); W('deminfl','inflOp',2)
F('infl','mon');            W('inflOp','infl',1)  # nf 'infl' lê op 'inflOp'

# g_nom = g_real + infl
O('gnom','add','mon');      W('g_real','gnom',1); W('infl','gnom',2)
F('g_nom','mon');           W('gnom','g_nom',1)

# ---------- BLOCO fiscal + arcabouço ----------
# tax = (tau + tax_rich)·Y  — a alavanca tax_rich soma o primário do topo à carga linear
O('tausum','add','fis');    W(tau,'tausum',1); W(tax_rich,'tausum',2)
O('taxOp','multiply','fis'); W('tausum','taxOp',1); W(Y,'taxOp',2)
F('tax','fis');            W('taxOp','tax',1)
O('gshare','add','fis');   W(g0,'gshare',1); W(gFn,'gshare',2)
O('gdes','multiply','fis');W('gshare','gdes',1); W(Y,'gdes',2)
O('gcap','multiply','fis');W(teto,'gcap',1); W('tax','gcap',2)
O('G','min','fis');        W('gdes','G',1); W('gcap','G',2)
F('G_gov','fis');          W('G','G_gov',1)
O('primbal','subtract','fis'); W('tax','primbal',1); W('G_gov','primbal',2)
O('pb','divide','fis');    W('primbal','pb',1); W(Y,'pb',2)
F('pb_ratio','fis');       W('pb','pb_ratio',1)

# ---------- BLOCO dívida: db = (r_gov - g_nom)*b - pb ----------
I('b_divida',0.78,'debt')
O('rg','subtract','debt');  W('r_gov','rg',1); W('g_nom','rg',2)
O('rgb','multiply','debt'); W('rg','rgb',1); W('b_divida','rgb',2)
O('db','subtract','debt');  W('rgb','db',1); W('pb_ratio','db',2)
W('db','b_divida','rate')

# ---------- BLOCO externo: carry trade + comércio com elasticidades (Thirlwall) ----------
O('c1','subtract','ext'); W(Selic,'c1',1); W(r_world,'c1',2)
O('c2','subtract','ext'); W('c1','c2',1); W(risk,'c2',2)
O('carryOp','subtract','ext'); W('c2','carryOp',1); W('infl','carryOp',2)
F('carry','ext');         W('carryOp','carry',1)
O('k1','multiply','ext'); W(kappa,'k1',1); W('carry','k1',2)
O('KA','multiply','ext'); W('k1','KA',1); W(Y,'KA',2)

I('e_cambio',1.0,'fx')
I('Yworld',100.0,'ext')
# X = x0e·(Yworld/100)^eta_x·e^eps_x  (exportações: renda mundial + câmbio)
O('ywr','divide','ext');  W('Yworld','ywr',1); W(hundred,'ywr',2)
O('ywp','pow','ext');     W('ywr','ywp',1); W(eta_x,'ywp',2)
O('expc','pow','ext');    W('e_cambio','expc',1); W(eps_x,'expc',2)
O('xq','multiply','ext'); W(x0e,'xq',1); W('ywp','xq',2)
O('Xop','multiply','ext');W('xq','Xop',1); W('expc','Xop',2)
F('X_exp','ext');         W('Xop','X_exp',1)
# M = m0e·(Y/100)^eta_m·e^(-eps_m)  (importações: renda doméstica + câmbio, ML frágil)
O('yr','divide','ext');   W(Y,'yr',1); W(hundred,'yr',2)
O('yp','pow','ext');      W('yr','yp',1); W(eta_m,'yp',2)
O('nem','multiply','ext');W(negOne,'nem',1); W(eps_m,'nem',2)
O('impc','pow','ext');    W('e_cambio','impc',1); W('nem','impc',2)
O('mq','multiply','ext'); W(m0e,'mq',1); W('yp','mq',2)
O('Mop','multiply','ext');W('mq','Mop',1); W('impc','Mop',2)
F('M_imp','ext');         W('Mop','M_imp',1)
# TB = X - M
O('TBop','subtract','ext');W('X_exp','TBop',1); W('M_imp','TBop',2)
F('TB','ext');            W('TBop','TB',1)
# Yworld cresce: dYworld = g_world·Yworld  (puxa as exportações na tendência)
O('ywg','multiply','ext');W(g_world,'ywg',1); W('Yworld','ywg',2)
W('ywg','Yworld','rate')

O('accumY','multiply','ext'); W(accum,'accumY',1); W(Y,'accumY',2)
O('bp1','add','ext');     W('TB','bp1',1); W('KA','bp1',2)
O('bpOp','add','ext');    W('bp1','bpOp',1); W('accumY','bpOp',2)
F('BP','ext');            W('bpOp','BP',1)

# ---------- BLOCO reservas + câmbio ----------
# R em NÍVEL (≈15% do PIB inicial Y≈100 = US$358bi/PIB, BCB dez/25); BP acumula em nível.
I('R_reservas',15,'fx')
O('intR','multiply','fx'); W(interv,'intR',1); W('R_reservas','intR',2)
O('negintR','multiply','fx'); W(negOne,'negintR',1); W('intR','negintR',2)
O('dR','max','fx');       W('BP','dR',1); W('negintR','dR',2)
W('dR','R_reservas','rate')
O('uncov','subtract','fx'); W('BP','uncov',1); W('dR','uncov',2)
O('u1','multiply','fx');  W(phi,'u1',1); W('uncov','u1',2)
O('u2','multiply','fx');  W('u1','u2',1); W('e_cambio','u2',2)
O('u3','divide','fx');    W('u2','u3',1); W(Y,'u3',2)
O('de','multiply','fx');  W(negOne,'de',1); W('u3','de',2)
W('de','e_cambio','rate')

# ================= CRIAR OS ITENS =================
for name,val,x,y in params:
    minsky.canvas.addVariable(name,'parameter'); h=minsky.canvas.itemFocus; h.moveTo(x,y); h.init(val)
for name,x,y in readers:
    minsky.canvas.addVariable(name,'flow'); h=minsky.canvas.itemFocus; h.moveTo(x,y)
for name,x,y in flows:
    minsky.canvas.addVariable(name,'flow'); h=minsky.canvas.itemFocus; h.moveTo(x,y)
for key,op,x,y in ops:
    minsky.canvas.addOperation(op); h=minsky.canvas.itemFocus; h.moveTo(x,y)
for name,init,x,y in integs:
    minsky.canvas.addOperation('integrate'); h=minsky.canvas.itemFocus
    h.description(name); h.moveTo(x,y); h.intVar.init(init)

minsky.save(TMP)
print('itens apos add:', len(minsky.model.items()))

# ================= RESOLVER PORTAS E FIAR =================
xml = open(TMP).read()
root = ET.fromstring(re.sub(r'xmlns="[^"]+"','',xml,count=1))
def ports(it): return [p.text for p in it.find('ports').iter('int')] if it.find('ports') is not None else []

by_name = {}          # nome -> item (ultima ocorrencia = a que adicionamos; readers/flows)
by_pos  = {}          # (x,y) -> item (operacoes)
intvar_by_name = {}   # nome integral -> intvar item
intop_by_ivid = {}    # intVar id -> IntOp item
for it in root.find('items'):
    nm = it.findtext('name'); typ = it.findtext('type'); x=it.findtext('x'); y=it.findtext('y')
    if nm: by_name[nm] = it
    if typ and typ.startswith('Operation') and x and y:
        by_pos[(round(float(x)),round(float(y)))] = it
    if typ in ('IntOp','integrate'):
        iv = it.findtext('intVar');
        if iv: intop_by_ivid[iv] = it
    if typ=='Variable:integral' and nm:
        intvar_by_name[nm] = it

op_pos = {key:(x,y) for key,op,x,y in ops}
integ_names = {n for n,_,_,_ in integs}
flow_names = {n for n,_,_ in flows} | {n for n,_,_ in readers}

def out_port(key):
    if key in integ_names:
        return ports(intvar_by_name[key])[0]
    if key in op_pos:
        x,y = op_pos[key]; return ports(by_pos[(round(float(x)),round(float(y)))])[0]
    # param/reader/flow by name
    return ports(by_name[key])[0]

def in_port(key, din):
    if din=='rate':
        iv = intvar_by_name[key].findtext('id'); return ports(intop_by_ivid[iv])[1]
    if key in op_pos:
        x,y=op_pos[key]; return ports(by_pos[(round(float(x)),round(float(y)))])[din]
    # named flow input
    return ports(by_name[key])[1]

wire_xml = []
wid = 90000
for src,dst,din in wires:
    fp = out_port(src); tp = in_port(dst,din); wid += 1
    wire_xml.append('  <Wire><id>%d</id><from>%s</from><to>%s</to></Wire>'%(wid,fp,tp))
newxml = xml.replace('</wires>', '\n'.join(wire_xml)+'\n </wires>', 1)
open(OUT,'w').write(newxml)
print('fios injetados:', len(wire_xml))

# ================= VALIDAR =================
minsky.load(OUT); minsky.reset()
while minsky.t()<20: minsky.step()
handles={}
for i in range(len(minsky.model.items())):
    it=minsky.model.items[i]
    try: handles.setdefault(it.name(), it)
    except Exception: pass
def val(n):
    h=handles.get(n)
    try: return round(h.value(),4)
    except Exception: return None
print('VALIDADO t=%.2f'%minsky.t())
for n in ['b_divida','R_reservas','e_cambio','carry','BP','r_gov','infl','g_nom','pb_ratio','G_gov','tax']:
    print('  %-12s = %s'%(n, val(n)))
