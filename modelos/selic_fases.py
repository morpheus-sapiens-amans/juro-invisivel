#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Redução da Selic EM FASES. ATRIBUIÇÃO (reconciliação 19/11 — ver ../REVISAO-RECONCILIACAO.md):
a lógica de ESCADA/degraus com checkpoints e "ancora primeiro, corta depois" é construção
do LAÉRCIO (a ponte Laércio/LR), NÃO "do LR" puro — o LR propõe ir a ~7,5% em ~12 meses;
o Jones diagnostica o juro mas não propõe corte operacional. Aqui: reduz gradualmente,
observa os dados, confirma o próximo corte. Comparamos 3 caminhos no mesmo modelo de Keen
(com governo contracíclico ligado, economia fechada):

  A) STATUS QUO  — Selic fica alta (o que mídia/mercado defendem)
  B) FASES (LR)  — corta por degraus, com checkpoints p/ observar
  C) CHOQUE      — corta tudo de uma vez (o que LR EVITA por risco cambial)

Juro do modelo = juro REAL ≈ Selic nominal − 4% de inflação.
  Selic 13,75% → 9,75% real | 11% → 7% | 9% → 5% | 7,5% → 3,5%
Calibração ilustrativa (mecanismo, não previsão).
"""
import numpy as np, matplotlib, os
matplotlib.use("Agg"); import matplotlib.pyplot as plt
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),"saida")
nu,alpha,beta,delta=3.0,0.02,0.01,0.01; phi0,phi1=0.04,9.6e-5
Ph=lambda l:(phi1/(1-min(l,0.999999))**2)-phi0
kap=lambda pi:0.02+0.10*np.exp(2.0*(pi-0.10))

def rhs(s,r,sig1=1.0,lamT=0.96):   # sig1 BAIXO = resposta fiscal limitada pelo arcabouço/teto
    o,l,d=s; sigma=np.clip(sig1*(lamT-l),0,0.08)
    pi=1-o-r*d+sigma; k=kap(pi); g=k/nu-delta
    return np.array([o*(Ph(l)-alpha), l*(g-alpha-beta), k-pi-g*d]), sigma

def run(r_of_t,s0=[0.85,0.93,0.55],T=120,dt=0.02):
    n=int(T/dt); ts=np.linspace(0,T,n+1); ys=np.zeros((n+1,3)); ys[0]=s0
    rs=np.zeros(n+1); sg=np.zeros(n+1); col=None
    for i in range(n):
        r=r_of_t(ts[i]); rs[i]=r
        k1,sg[i]=rhs(ys[i],r); k2,_=rhs(ys[i]+0.5*dt*k1,r)
        k3,_=rhs(ys[i]+0.5*dt*k2,r); k4,_=rhs(ys[i]+dt*k3,r)
        s2=ys[i]+dt/6*(k1+2*k2+2*k3+k4)
        if not np.all(np.isfinite(s2)) or s2[1]<=1e-4 or abs(s2[2])>50:
            col=ts[i]; ys=ys[:i+1];ts=ts[:i+1];rs=rs[:i+1];sg=sg[:i+1]; break
        ys[i+1]=s2
    rs[-1]=r_of_t(ts[-1]) if len(ts) else 0
    return ts,ys,rs,sg,col

# juro real como função do tempo (Selic nominal − 4%)
R_HI=0.0975   # Selic 13,75%
def r_status(t): return R_HI
def r_fases(t):
    if t<10: return R_HI          # 13,75%
    if t<22: return 0.07          # 11%   (1ª fase: observa)
    if t<34: return 0.05          # 9%    (2ª fase: confirma)
    return 0.035                  # 7,5%  (destino)
def r_choque(t): return R_HI if t<10 else 0.035

A=run(r_status); B=run(r_fases); C=run(r_choque)
fig,ax=plt.subplots(1,3,figsize=(16,5))
# painel do juro
ax[0].step(A[0],(A[2]+0.04)*100,where='post',color='tab:red',lw=2,label='Status quo (Selic alta)')
ax[0].step(B[0],(B[2]+0.04)*100,where='post',color='tab:blue',lw=2.5,label='Lara Resende (fases)')
ax[0].step(C[0],(C[2]+0.04)*100,where='post',color='gray',lw=1.5,ls='--',label='Choque (LR evita)')
ax[0].set_title('Selic nominal (%)'); ax[0].set_ylabel('% a.a.'); ax[0].legend(); ax[0].grid(alpha=.3)
for xc in [10,22,34]: ax[0].axvline(xc,color='k',alpha=.12)
# dívida
for S,c,lab in [(A,'tab:red','status quo'),(B,'tab:blue','fases (LR)'),(C,'gray','choque')]:
    ls='--' if lab=='choque' else '-'
    ax[1].plot(S[0],S[1][:,2],c,lw=2,ls=ls,label=lab+(f' → COLAPSO ~{int(S[4])}a' if S[4] else ''))
    ax[2].plot(S[0],S[1][:,1],c,lw=2,ls=ls,label=lab)
ax[1].set_title('Dívida / PIB'); ax[1].set_ylim(-1,6); ax[1].set_ylabel('d')
ax[2].set_title('Emprego λ')
for a in (ax[1],ax[2]): a.legend(); a.grid(alpha=.3)
for a in ax: a.set_xlabel('anos')
fig.suptitle('Reduzir a Selic EM FASES (Lara Resende): corta, observa, confirma — sem quebrar o país',fontweight='bold')
fig.tight_layout(); fig.savefig(f"{OUT}/fig5_selic_fases.png",dpi=110); plt.close(fig)
print("fig5 OK |",{'status_colapso':A[4],'fases_colapso':B[4],'choque_colapso':C[4]})
print("d_final: status=%.2f fases=%.2f choque=%.2f"%(A[1][-1,2],B[1][-1,2],C[1][-1,2]))
