"""
brasil_sfc.py — o modelo SFC Brasil (economia aberta) que vira o `.mky` Brasil.

É a adaptação do MinskyGovernmentNonlinear do Keen (ver MODELO-GOVERNO-REFERENCIA.md)
com quatro blocos novos. Este arquivo é a SPEC VALIDADA das equações — cada bloco aqui
vira um conjunto de peças no `.mky` (variáveis/operações/fios do Minsky).

Trilha (dossiê §8): valida a dinâmica em Python primeiro; depois transcreve ao .mky.
O objetivo é MECANISMO, não previsão calibrada (calibração fina = fase Lobo & Oreiro).

Os quatro blocos adaptados:
  [BC/Selic]    Selic como parâmetro de política (era Int_Rate=0.02 genérico).
  [Dívida púb.] estoque b=B_gov/PIB com a equação-padrão db/dt=(r_gov-g_nom)·b - pb.
                r_gov = θ·Selic + (1-θ)·r_pre  → o loop "juro infla o déficit" do ALR.
  [Fiscal/teto] arcabouço como CLAMP no gasto: G = min(G_desejado, teto·receita).
  [Externo]     câmbio e, reservas R que se FORMAM (superávit+carry+ouro/accum) e
                DEFENDEM o Real; pressão = f(carry = Selic-juro_ext-risco-infl).
                A tese do Laércio: R alto = corte de Selic viável sem disparar o dólar.

Núcleo real (inalterado do Keen): Goodwin não-linear com crescimento de tendência.
"""
import numpy as np


def genexp(X, x0, s, mn, y0):
    """Exponencial generalizada do Keen: passa por (x0,y0), inclinação s, piso mn."""
    return (y0 - mn) * np.exp((X - x0) * s / (y0 - mn)) + mn


# ---- parâmetros CALIBRADOS ao Brasil (fase Lobo & Oreiro, 13/11/2026) ----
# Fontes: Tesouro/RMD set/2025, BCB (DBGG/DLSP, setor externo), IBGE (PIB 2025),
# Copom nov/2025 (Selic 15%), IPEA (elasticidades comércio), Lobo & Oreiro (2012) SFC-LFT.
PARS = dict(
    v=3.0, delta=0.02, prod_gr=0.02, pop_gr=0.01,          # real core (g≈2,3% a.a., IBGE 2025)
    x_e=0.96, s_e=2.0, min_e=-0.04, y_e=0.0,               # Phillips (salário)
    x_i=0.05, s_i=1.5, min_i=-0.01, y_i=0.05,              # investimento
    x_g=0.95, s_g=-0.5, min_g=-0.05, y_g=0.0,              # gasto contracíclico
    # fiscal/dívida — composição RMD set/2025, 3 pernas (47% LFT/Selic, 26% pré+câmbio, 27% IPCA):
    tau=0.33, theta=0.47, theta_pre=0.26, theta_ipca=0.27,
    r_pre=0.13, cupom_real=0.06, g0=0.33, spread_priv=0.03,
    # externo — elast. IPEA: câmbio X 0,6 / M 0,3 (ML frágil); renda M 1,5 > X 1,0 (Thirlwall):
    r_world=0.04, risk=0.03, eps_x=0.6, eps_m=0.3, eta_m=1.5, eta_x=1.0, x0e=16.0, m0e=16.0,
    g_world=0.025, kappa=1.2, phi=0.5, intervene_frac=0.15, Yworld0=100.0,
    infl0=0.035, k_dem=0.15, pass_through=0.15,            # inflação (meta 3%, IPCA ~4,4%)
    # --- alavancas da MATRIZ (fase modelagem, 14/11/2026). Defaults NEUTROS: com tudo
    # desligado, simula() reproduz A/B/B±/C. Cada alavanca credita um autor (ver handoff §6). ---
    mult_pub=1.5,          # [inv_pub] multiplicador do investimento público (IPEA/Laércio)
    ret_reservas=0.04,     # [carrego] retorno das reservas (~juro externo); custo = Selic-ret-deprec
    b_dom=0.90,            # [phi-endóg] limiar de dominância fiscal (dívida/PIB onde o prêmio liga)
    risk_b=0.06,           # [phi-endóg] sensibilidade do prêmio de risco ao excesso de dívida
    phi_carry=0.40,        # [phi-endóg] canal UIP/carry (regime NORMAL): Selic alta aprecia o Real
    phi_sust=0.90,         # [phi-endóg] canal sustentabilidade (DOMINÂNCIA): db move o prêmio → câmbio
    b_alvo=0.78, pb_star=0.0, phi_pb=0.30, banda=0.05,     # [regra-dívida] âncora europeia 2024
    # [regime de gasto] distingue as DUAS peças do "pacote do mal":
    #   teto (EC 95/2016): gasto real congelado (teto cresce 0% real → G/PIB despenca).
    #   arcabouço (LC 200/2023): teto cresce 70% da alta real da receita, travado em 0,6–2,5%/ano.
    arc_frac=0.70, arc_min=0.006, arc_max=0.025,
    # [taylor] regra de Taylor opcional (Selic endógena) — alavanca DESLIGADA por padrão.
    # alvo = rn + meta + phi_pi·(infl−meta) + phi_y·(λ−0,95); params da ortodoxia (relatório 1).
    taylor_rn=0.06, taylor_pi_meta=0.03, taylor_phi_pi=2.0, taylor_phi_y=0.5, taylor_speed=1.5,
)


def _clamp_banda(gap, banda):
    """Dentro da banda (±banda) a regra não reage; fora, reage ao excesso. (reforma UE 2024)"""
    if abs(gap) <= banda:
        return 0.0
    return gap - (banda if gap > 0 else -banda)


def simula(Selic, R0=0.15, accum0=0.004, cap_arcabouco=1.00, T=40.0, dt=0.01, p=None,
           tax_rich=0.0, invest_pub=0.0, tau_fric=0.0,
           phi_endog=False, conta_carrego=False, regra_divida=False, b0=0.78,
           regime_gasto=None, every=5.0, taylor=False, ajuste=0.0, corte_G=0.0, ramp_anos=0.0):
    """Integra o sistema. Selic é o botão de política. R0=reservas/PIB iniciais;
    accum0=formação exógena de reservas/PIB (venda de ativos, ouro); cap_arcabouco=teto
    (1.00 = gasto não passa da receita). Retorna lista de snapshots.

    ALAVANCAS (default-off → reproduz A/B/B±/C):
      tax_rich      primário extra do topo, em fração do PIB (0.0035/0.008/0.013 = 3 níveis).
                    Credita Lindbergh/Melchionna/PSOL.                [Modelo 1]
      invest_pub    investimento público em fração do PIB; entra em G E forma capital com
                    multiplicador mult_pub (≈1,5) — canal mais forte que desoneração linear.
                    Credita Laércio (portos+know-how)/Humberto/IPEA.  [Modelo 4]
      tau_fric      fricção de fluxo 0..1 (IOF-derivativos/encaje) que reduz a mobilidade do
                    carry (kappa) e o repasse ao câmbio (phi). Credita Kobori/Chamon-Garcia. [M3/M4]
      phi_endog     prêmio de risco e câmbio ENDÓGENOS à dívida → teste de regime (normal:
                    corte deprecia; dominância: corte APRECIA). O coração do artigo.  [regime]
      conta_carrego soma o custo quase-fiscal do carry das reservas ao déficit →
                    cortar a Selic MELHORA o quase-fiscal (contraintuitivo).  [Modelo 2/3]
      regra_divida  troca o teto-clamp por regra de dívida com banda (pb = pb* + phi_pb·(b-alvo),
                    ≈0 dentro da banda) → o social vira endógeno à saúde da dívida.  [Modelo 4]
      regime_gasto  qual regra de gasto vige: 'teto' (EC 95, gasto real congelado), 'arcabouco'
                    (LC 200, cresce 70% da receita, travado 0,6–2,5%), 'livre' (revogado, sem
                    âncora), ou None (clamp legado G≤teto·receita → reproduz A/B/B±/C).  [bateria teto]
    """
    p = {**PARS, **(p or {})}
    g = p.__getitem__
    Sel = Selic                                         # taxa de política corrente (endógena se taylor=True)
    # estados: núcleo real + dívida(ratio) + externo
    K, a, N, w = 300.0, 1.0, 100.0, 1.0
    D_priv, b, R, D_ext, e = 0.0, b0, R0, 0.10, 1.0
    Yworld = g('Yworld0')                               # renda mundial (cresce → puxa X)
    prev_deprec = 0.0                                    # taxa de depreciação do passo anterior
    gc = None                                           # [regime_gasto] teto de gasto em %PIB (estado)
    g_real_lag = g('prod_gr') + g('pop_gr')             # crescimento real defasado (p/ o arcabouço)
    hist = []
    for i in range(int(T / dt)):
        Y = K / g('v'); L = Y / a; lam = L / N; Wages = w * L
        rm = min(1.0, (i * dt) / ramp_anos) if ramp_anos > 0 else 1.0  # [ramp] rampa o ajuste/corte em ramp_anos
        # --- fiscal + arcabouço/regra + alavancas tax_rich e invest_pub ---
        tax = (g('tau') + tax_rich) * Y                   # tax_rich = primário extra do topo (PSOL)
        G_Fn = genexp(lam, g('x_g'), g('s_g'), g('min_g'), g('y_g'))
        G_des = (g('g0') + G_Fn + invest_pub) * Y         # inv. público entra no gasto desejado
        if gc is None:
            gc = G_des / Y                                 # teto inicial = gasto desejado/PIB de t0
        if regra_divida:                                  # regra de dívida c/ banda (troca o teto)
            pb_target = g('pb_star') + g('phi_pb') * _clamp_banda(b - g('b_alvo'), g('banda'))
            G = tax - pb_target * Y                        # primário mira o alvo; social endógeno
        elif regime_gasto in ('teto', 'arcabouco'):       # as duas peças do "pacote do mal"
            G = min(G_des, gc * Y)                          # gasto limitado pelo teto (em %PIB)
        elif regime_gasto == 'livre':                     # teto E arcabouço revogados, sem âncora
            G = G_des
        else:
            G = min(G_des, cap_arcabouco * tax)           # clamp legado (reproduz A/B/B±/C)
        G = max(G - corte_G * rm * Y, 0.0)                 # [corte_G] corte de gasto (piso social): melhora o primário, drena demanda e gsy
        pb_ratio = (tax - G) / Y                           # superávit primário / PIB
        NetGovInj = G - tax                                # injeção primária no privado
        # --- privado (Keen) ---
        r_priv = Sel + g('spread_priv')
        Profit = Y - Wages - r_priv * D_priv + NetGovInj
        pi = Profit / K
        Inv = genexp(pi, g('x_i'), g('s_i'), g('min_i'), g('y_i')) * Y
        Inv += g('mult_pub') * invest_pub * Y             # formação de capital público (μ≈1,5)
        g_real = Inv / K - g('delta')
        # --- inflação e crescimento nominal ---
        ee = max(e, 0.05)
        infl = g('infl0') + g('k_dem') * (lam - 0.95) + g('pass_through') * max(e - 1.0, 0.0) * 0.1
        g_nom = g_real + infl
        # --- dívida pública: o loop juro→déficit do ALR (custo médio das 3 pernas) ---
        # 47% LFT segue a Selic; 26% pré; 27% NTN-B = IPCA + cupom real → 74% indexada.
        r_gov = (g('theta') * Sel + g('theta_pre') * g('r_pre')
                 + g('theta_ipca') * (infl + g('cupom_real')))
        # [carrego] custo quase-fiscal do carry das reservas = (Selic-ret-deprec)·R, soma ao déficit.
        # Reservas em dólar: a depreciação (ganho em R$) ABATE o custo → por isso entra com sinal −.
        carrego = max(Sel - g('ret_reservas') - prev_deprec, 0.0) * R if conta_carrego else 0.0
        pb_eff = pb_ratio - carrego + ajuste * rm          # carrego piora; [ajuste] = esforço primário exógeno (caso de teste)
        db = (r_gov - g_nom) * b - pb_eff
        # --- setor externo + reservas ---
        # [phi-endóg] prêmio de risco endógeno: liga acima do limiar de dominância b_dom.
        risk_eff = g('risk') + (g('risk_b') * max(b - g('b_dom'), 0.0) if phi_endog else 0.0)
        # [τ] fricção de fluxo reduz a mobilidade do carry (kappa) e o repasse ao câmbio (phi).
        kappa_eff = g('kappa') * (1.0 - tau_fric)
        phi_eff = g('phi') * (1.0 - 0.5 * tau_fric)
        # elast-câmbio: X sobe com depreciação (eps_x), M cai pouco (eps_m baixa → ML frágil).
        # elast-renda: X puxada pela renda mundial (eta_x), M pela doméstica (eta_m>eta_x).
        # eta_m>eta_x = restrição externa de Thirlwall: crescer importa mais que exportar.
        X = g('x0e') * ((Yworld / 100.0) ** g('eta_x')) * (ee ** g('eps_x'))
        M = g('m0e') * ((Y / 100.0) ** g('eta_m')) * (ee ** (-g('eps_m')))
        TB = X - M
        CA = TB - g('r_world') * D_ext
        carry = Sel - g('r_world') - risk_eff - infl     # carry REAL (com prêmio endógeno)
        KA = kappa_eff * carry * Y
        BP = CA + KA + accum0 * Y                           # balanço de pagamentos + formação
        if BP >= 0:                                         # entrada líquida → reservas formam
            dR, de = BP / Y, 0.0
        else:                                              # saída → BC defende com reservas
            defense = min(-BP, R * Y * g('intervene_frac'))
            dR = -defense / Y
            de = -phi_eff * (BP + defense) / max(Y, 1) * ee    # resíduo não-coberto deprecia
        # [phi-endóg] DOIS canais de sinal oposto, pesados pela dominância w_dom (logístico: ~0 em
        # regime normal, ~1 em dominância, vira em b_dom):
        #   NORMAL (1-w_dom): canal UIP/carry — Selic alta → carry alto → APRECIA; corte → deprecia.
        #   DOMINÂNCIA (w_dom): canal sustentabilidade — Selic alta infla db → DEPRECIA; corte → APRECIA.
        # A inversão de sinal entre os dois é o coração do artigo (a tese do ALR).
        if phi_endog:
            w_dom = 1.0 / (1.0 + np.exp(-12.0 * (b - g('b_dom'))))
            fric = 1.0 - 0.5 * tau_fric
            de += -g('phi_carry') * carry * ee * (1.0 - w_dom) * fric   # normal: carry aprecia
            de += g('phi_sust') * db * ee * w_dom * fric                # dominância: db deprecia
        dD_ext = (-CA if CA < 0 else -0.2 * D_ext)
        # --- integra (Euler) ---
        Wage_Fn = genexp(lam, g('x_e'), g('s_e'), g('min_e'), g('y_e'))
        K += (Inv - g('delta') * K) * dt; a += g('prod_gr') * a * dt
        N += g('pop_gr') * N * dt; w += Wage_Fn * w * dt
        D_priv += (Inv - Profit) * dt; b += db * dt
        R += dR * dt; D_ext += dD_ext * dt; e += de * dt
        Yworld += g('g_world') * Yworld * dt
        prev_deprec = de / ee                              # taxa de depreciação p/ o carrego do passo seguinte
        if taylor:                                          # [taylor] Selic endógena: o BC segue uma regra
            sel_alvo = (g('taylor_rn') + g('taylor_pi_meta')
                        + g('taylor_phi_pi') * (infl - g('taylor_pi_meta'))
                        + g('taylor_phi_y') * (lam - 0.95))
            Sel += g('taylor_speed') * (sel_alvo - Sel) * dt
            Sel = max(Sel, 0.0)                             # piso em zero
        # [regime_gasto] evolui o teto de gasto (em %PIB). O teto é um NÍVEL real; dividido por um
        # PIB que cresce a g_real, a razão G/PIB cai. Teto (EC95): nível real cresce 0% → cai rápido.
        # Arcabouço (LC200): nível cresce arc_frac·receita, travado na banda → cai devagar (austeridade
        # por atrito). É a crítica "ajuste por composição": sem cortar nominal, o social encolhe no PIB.
        if regime_gasto == 'teto':
            gc += (0.0 - g_real) * gc * dt
        elif regime_gasto == 'arcabouco':
            r_arc = min(g('arc_max'), max(g('arc_min'), g('arc_frac') * g_real_lag))
            gc += (r_arc - g_real) * gc * dt
        g_real_lag = g_real
        if i % max(1, int(every / dt)) == 0:
            hist.append(dict(t=i * dt, b=b, rg=r_gov - g_nom, cambio=e, R=R, selic=Sel,
                             infl=infl, g_nom=g_nom, lam=lam, pi=pi,
                             carrego=carrego, risk=risk_eff, pb=pb_ratio, gr=g_real,
                             gsy=G / Y, taxy=tax / Y, Y=Y, K=K, omega=Wages / Y))
    return hist


def _print(nome, rows):
    print(f"\nCenário {nome}")
    print(" t     b    r-g   câmbio  R/Y   infl  g_nom   λ")
    for r in rows:
        print("%4.0f %5.2f %+5.3f  %5.2f  %5.2f %+5.3f %+5.3f %5.3f" %
              (r['t'], r['b'], r['rg'], r['cambio'], r['R'], r['infl'], r['g_nom'], r['lam']))


if __name__ == "__main__":
    # Experimento central (dossiê §8.3): Selic atual (15%, Copom nov/25) vs corte do ALR.
    _print("A — Selic 15% (atual)", simula(0.15, T=25))
    _print("B — Selic 10% (corte gradual)", simula(0.10, T=25))
    # Teste da tese das reservas: corte COM muitas reservas vs POUCAS (base Brasil R/Y≈0.15).
    _print("B+ — Selic 10%, reservas altas (R0=0.25)", simula(0.10, R0=0.25, accum0=0.008, T=25))
    _print("B- — Selic 10%, reservas baixas (R0=0.08)", simula(0.10, R0=0.08, accum0=0.0, T=25))
