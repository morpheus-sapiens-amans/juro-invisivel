#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modelo de Steve Keen (Goodwin -> dívida privada -> governo) em Python puro.
Reproduz o que o Keen faz no vídeo: montar parâmetros, "apertar play", e ver os
gráficos convergirem ou irem pro beleléu (debt-deflation). Usado aqui para a tese
do Lara Resende: mexer no JURO (r) e no DÉFICIT do governo e ver o que estabiliza.

Estados: omega (fatia dos salários), lambda (emprego), d (dívida privada / PIB).
Integrador RK4 próprio. numpy + matplotlib (backend Agg).

NOTA: calibração ILUSTRATIVA — a ESTRUTURA das equações é fiel ao Keen; os
decimais foram escolhidos para mostrar nitidamente os regimes qualitativos.
"""
import numpy as np, matplotlib, os
matplotlib.use("Agg")
import matplotlib.pyplot as plt
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),"saida")

# ---------- parâmetros estruturais ----------
nu, alpha, beta, delta = 3.0, 0.02, 0.01, 0.01
phi0, phi1 = 0.04, 9.6e-5
def Phillips(lam):                       # Phillips ORIGINAL: emprego -> variação do salário
    lam = min(lam, 0.999999)
    return phi1/(1.0-lam)**2 - phi0
def kappa(pi):                           # investimento NÃO-LINEAR da taxa de lucro
    return 0.02 + 0.10*np.exp(2.0*(pi-0.10))

# ---------- modelos ----------
def goodwin(s):
    o, l = s
    g = (1.0-o)/nu - delta
    return np.array([o*(Phillips(l)-alpha), l*(g-alpha-beta)])

def keen(s, r, sig1=0.0, lamT=0.96, sigcap=0.08):
    """Keen com dívida + governo. sig1>0 = déficit público CONTRACÍCLICO."""
    o, l, d = s
    sigma = np.clip(sig1*(lamT-l), 0.0, sigcap)      # déficit sobe quando emprego cai
    pi = 1.0 - o - r*d + sigma                        # lucro = 1 - salários - juros + injeção fiscal
    k = kappa(pi); g = k/nu - delta
    return np.array([o*(Phillips(l)-alpha), l*(g-alpha-beta), k-pi-g*d]), sigma, g

def integ(fn, s0, T=400, dt=0.05, keenargs=None):
    n=int(T/dt); ts=np.linspace(0,T,n+1); ys=np.zeros((n+1,len(s0))); ys[0]=s0
    sig=np.zeros(n+1); gg=np.zeros(n+1); collapse=None
    for i in range(n):
        def d(s):
            if keenargs is None: return goodwin(s)
            return keen(s,*keenargs)[0]
        k1=d(ys[i]); k2=d(ys[i]+0.5*dt*k1); k3=d(ys[i]+0.5*dt*k2); k4=d(ys[i]+dt*k3)
        s2=ys[i]+dt/6*(k1+2*k2+2*k3+k4)
        if keenargs is not None:
            _,sig[i],gg[i]=keen(ys[i],*keenargs)
        if not np.all(np.isfinite(s2)) or s2[1]<=1e-4 or (len(s2)>2 and abs(s2[2])>50):
            collapse=ts[i]; ys=ys[:i+1]; ts=ts[:i+1]; sig=sig[:i+1]; gg=gg[:i+1]; break
        ys[i+1]=s2
    return ts,ys,sig,gg,collapse

# ===== FIG 1: Goodwin — ciclo perpétuo =====
ts,ys,_,_,_=integ(goodwin,[0.85,0.90],T=200)
fig,ax=plt.subplots(1,2,figsize=(13,5))
ax[0].plot(ts,ys[:,0],lw=2,label=r'$\omega$ salários'); ax[0].plot(ts,ys[:,1],lw=2,label=r'$\lambda$ emprego')
ax[0].set_title('1) Goodwin: o capitalismo é intrinsecamente cíclico'); ax[0].set_xlabel('anos'); ax[0].legend(); ax[0].grid(alpha=.3)
ax[1].plot(ys[:,1],ys[:,0],color='crimson',lw=1.3); ax[1].set_xlabel(r'emprego $\lambda$'); ax[1].set_ylabel(r'salários $\omega$')
ax[1].set_title('Órbita fechada: nunca "chega" ao equilíbrio'); ax[1].grid(alpha=.3)
fig.tight_layout(); fig.savefig(f"{OUT}/fig1_goodwin.png",dpi=110); plt.close(fig)

# ===== FIG 2: o JURO decide a velocidade do colapso =====
fig,ax=plt.subplots(1,2,figsize=(13,5.2)); cores={0.03:'tab:green',0.06:'tab:orange',0.09:'tab:red'}
for r,c in cores.items():
    ts,ys,_,_,col=integ(keen,[0.85,0.90,0.50],T=500,keenargs=(r,))
    ax[0].plot(ts,ys[:,2],c,lw=2,label=f'r={int(r*100)}%'+(f' → colapso ~{int(col)}a' if col else ''))
    ax[1].plot(ts,ys[:,1],c,lw=2,label=f'r={int(r*100)}%')
ax[0].set_title('2) Dívida privada / PIB — sem governo'); ax[0].set_ylabel('d'); ax[0].set_ylim(-1,6)
ax[1].set_title('Emprego λ — juro alto = colapso mais rápido e fundo')
for a in ax: a.set_xlabel('anos'); a.grid(alpha=.3); a.legend()
fig.suptitle('O JURO não muda SE quebra — muda QUÃO RÁPIDO quebra',fontweight='bold')
fig.tight_layout(); fig.savefig(f"{OUT}/fig2_juro_colapso.png",dpi=110); plt.close(fig)

# ===== FIG 3: varredura do juro — tempo até o colapso =====
rs=np.arange(0.02,0.121,0.004); tcol=[]
for r in rs:
    _,_,_,_,col=integ(keen,[0.85,0.90,0.50],T=800,keenargs=(r,))
    tcol.append(col if col else np.nan)
fig,ax=plt.subplots(figsize=(10,5.5))
ax.plot(rs*100,tcol,'o-',color='darkred',lw=2)
ax.set_xlabel('juro real r (% a.a.)'); ax.set_ylabel('anos até o colapso')
ax.set_title('3) A alavanca do juro: cada ponto a mais de juro antecipa a crise')
ax.grid(alpha=.3)
fig.tight_layout(); fig.savefig(f"{OUT}/fig3_alavanca_juro.png",dpi=110); plt.close(fig)

# ===== FIG 4: o DÉFICIT do governo estabiliza (anti-austeridade) =====
r=0.08
ts0,ys0,_,_,c0=integ(keen,[0.85,0.90,0.50],T=500,keenargs=(r,0.0))        # sem governo
ts1,ys1,sig1,_,c1=integ(keen,[0.85,0.90,0.50],T=500,keenargs=(r,3.0))     # déficit contracíclico
fig,ax=plt.subplots(1,3,figsize=(16,5))
ax[0].plot(ts0,ys0[:,2],'tab:red',lw=2,label='SEM governo → colapso')
ax[0].plot(ts1,ys1[:,2],'tab:blue',lw=2,label='COM déficit contracíclico → estável')
ax[0].set_title(f'Dívida/PIB  (r={int(r*100)}%)'); ax[0].set_ylabel('d'); ax[0].set_ylim(-1,6)
ax[1].plot(ts0,ys0[:,1],'tab:red',lw=2); ax[1].plot(ts1,ys1[:,1],'tab:blue',lw=2)
ax[1].set_title('Emprego λ')
ax[2].plot(ts1,sig1*100,'tab:purple',lw=2); ax[2].set_title('Déficit público σ (% PIB)\nsobe na crise, recua na calmaria')
for a in ax: a.set_xlabel('anos'); a.grid(alpha=.3)
ax[0].legend()
fig.suptitle('4) O gasto público não é o vilão — é o que impede o colapso (até certo juro)',fontweight='bold')
fig.tight_layout(); fig.savefig(f"{OUT}/fig4_governo_estabiliza.png",dpi=110); plt.close(fig)

print("Figuras geradas:",[f for f in os.listdir(OUT) if f.endswith('.png')])
print(f"Fig2 colapsos | fig4 sem-gov colapso~{c0} | com-gov colapso={c1}")
