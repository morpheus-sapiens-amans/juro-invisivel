#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
O BLOCO QUE FALTAVA: o CÂMBIO. Até aqui o modelo era economia FECHADA — sem dólar,
sem fuga de capital. Este módulo responde "o que acontece com o câmbio" quando se
baixa a Selic — que é O ponto decisivo da proposta do Lara Resende.

Mecanismo (ilustrativo, não previsão):
- Juro doméstico alto atrai capital (carry) -> real forte.
- Baixar o juro -> valor de equilíbrio do dólar sobe (e*) -> real se deprecia.
- Um corte BRUSCO gera overshoot de expectativas (sentimento 's') muito maior que
  cortes graduais -> é por isso que o LR propõe FASES.
- O BC vende RESERVAS (US$ 350 bi) para amortecer -> mas reservas se esgotam.
- Depreciação -> inflação importada (pass-through).

Modelo do câmbio: correção de erro (e persegue e*) + sentimento (overshoot em cortes
rápidos) + intervenção com reservas. Cenários: status quo x fases (LR) x choque.

⚠️ RESSALVA (reconciliação 19/11 — ver ../REVISAO-RECONCILIACAO.md):
Aqui as reservas DEFENDEM o Real no curto prazo (o BC vende reserva sob ataque) — o que é
verdadeiro NESSE horizonte. MAS o modelo canônico do estudo (brasil_sfc.py / BrasilSFC)
mostra que ACUMULAR reserva/ouro NÃO "firma o Real": paga-se Selic sobre a reserva (o
"carrego", carry negativo), que pesa contra no longo prazo. NÃO afirmar publicamente que
"ouro firma o Real" — cairia no contraditório. Ouro e corte da Selic são COMPLEMENTARES:
cortar a Selic encolhe o carrego, tornando a reserva barata de carregar. O ouro é lastro
para o corte gradual; o corte é o que torna o lastro sustentável.
"""
import numpy as np, matplotlib, os
matplotlib.use("Agg"); import matplotlib.pyplot as plt
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),"saida")

RREF=0.0975; GAMMA=6.4; LAM=0.8      # e* = 1 + 6.4*(0.0975 - r): Selic 13,75%->dólar 1,0 ; 7,5%->~1,4
KJ=2.5; TAU=1.2                      # sentimento: overshoot a cortes rápidos, decai em ~1,2 ano
PHI=3.0; DRAIN=0.8                   # intervenção do BC e queima de reservas
PASS=0.10                           # pass-through câmbio -> inflação
estar=lambda r:1.0+GAMMA*max(0.0,RREF-r)

# juro real (Selic nominal - 4%): mesmos cenários do selic_fases.py
r_status=lambda t:0.0975                                              # Selic 13,75% (mídia)
r_fases =lambda t:0.0975 if t<4 else 0.07 if t<9 else 0.05 if t<14 else 0.035   # LR: 13,75->11->9->7,5
r_choque=lambda t:0.0975 if t<4 else 0.035                           # corte de 1x (LR evita)

def simular(rf,T=20,dt=0.01):
    n=int(T/dt); ts=np.linspace(0,T,n+1)
    e=np.ones(n+1); Res=np.ones(n+1); infl=np.full(n+1,0.04); s=0.0
    for i in range(n):
        t=ts[i]; r=rf(t)
        des=(estar(rf(t))-estar(rf(t-dt)))/dt if t>0 else 0.0
        s+=dt*(KJ*max(0.0,des)-s/TAU)
        gap=e[i]-estar(r); Iv=min(PHI*gap,Res[i]/(DRAIN*dt)) if (gap>0 and Res[i]>0) else 0.0
        edot=LAM*(estar(r)-e[i])+s-Iv
        e[i+1]=e[i]+dt*edot; Res[i+1]=max(0.0,Res[i]-Iv*DRAIN*dt)
        infl[i+1]=0.04+PASS*max(0.0,edot)/max(e[i],0.1)
    return ts,e,Res,infl

cen=[("Status quo (Selic 13,75%)",r_status,'tab:red','-'),
     ("Lara Resende (em fases)",r_fases,'tab:blue','-'),
     ("Choque (corte de 1x — LR evita)",r_choque,'gray','--')]
fig,ax=plt.subplots(1,3,figsize=(16,5))
for nome,rf,c,ls in cen:
    ts,e,Res,infl=simular(rf)
    ax[0].plot(ts,e,c,ls=ls,lw=2.3,label=nome)
    ax[1].plot(ts,Res*350,c,ls=ls,lw=2.3,label=nome)
    ax[2].plot(ts,infl*100,c,ls=ls,lw=2.3,label=nome)
ax[0].set_title('Dólar (índice: 1,0 = hoje)'); ax[0].set_ylabel('R$/US$ relativo')
ax[1].set_title('Reservas do BC (US$ bi)'); ax[1].axhline(0,color='k',lw=.8)
ax[2].set_title('Inflação (%)'); ax[2].axhline(4,color='k',lw=.6,alpha=.4)
for a in ax: a.set_xlabel('anos'); a.grid(alpha=.3); a.legend(fontsize=9)
fig.suptitle('O câmbio: por que o Lara Resende corta em FASES — gradual gera overshoot e inflação menores que o choque',fontweight='bold')
fig.tight_layout(); fig.savefig(f"{OUT}/fig6_cambio.png",dpi=110); plt.close(fig)
for nome,rf,_,_ in cen:
    ts,e,Res,infl=simular(rf)
    print(f"{nome:34} dólar: +{(e.max()-1)*100:.0f}%  reservas_min: US${Res.min()*350:.0f}bi  inflação_pico: {infl.max()*100:.1f}%")
