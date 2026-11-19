"""
Port fiel do modelo reduzido da Seção 5 de
Dejanir H. Silva, "Neo-Fisherian Adventures in the Tropics" (2026).

Fonte: função JavaScript solvePath()/solve() embutida no explorer
https://dejanirsilva.github.io/neofisherian_adventures/ (index.html).

É um modelo New Keynesian de economia aberta linearizado, com teoria fiscal
do nível de preços (FTPL), prêmio de risco cambial (UIP com wedge), composição
da dívida (pós-fixada/prefixada/indexada) e intervenção cambial (venda de
reservas). Sistema linear empilhado no tempo (6 estados × T trimestres),
resolvido por eliminação direta.

Estado por trimestre (índices 0..5):
  0 c    - consumo
  1 c_T  - consumo de tradables
  2 pi   - IPC relativo ao IPC terminal (em log)
  3 a    - posição externa líquida (NFA)
  4 q_lag- câmbio real defasado
  5 piN_lag - inflação de não-tradables defasada
"""
import math
import numpy as np

# Calibração default (do objeto `defaults` do explorer).
DEFAULTS = dict(
    inertia=0.0591101286411708,  # peso da inflação defasada na Phillips
    slope=1.0,                    # multiplicador da inclinação da Phillips
    sale=0.0,                     # venda de reservas (% do PIB)
    duration=4,                   # trimestres até recompra das reservas
    cuts=4,                       # nº de cortes trimestrais da Selic
    short=0.3342,                 # dívida pós-fixada (LFT/Selic)
    nominal=0.3801,               # dívida prefixada nominal
    reserves=0.4038,              # reservas iniciais (/dívida)
    risk=0.0,                     # prob. trimestral de reversão do plano
    spend=0.0,                    # fração da economia de juros que é gasta
    swap=0.0,                     # prefixado -> pós (pp)
)


def solve_path(p, T=180, announced=None, terminal=None):
    short, nominal = p["short"], p["nominal"]
    if short < 0 or nominal < 0 or short + nominal > 1 + 1e-10:
        raise ValueError("Shares da dívida devem somar <= 100%.")

    Rf = 1.01 ** 0.25
    R = Rf * math.exp(0.06 / 4)       # bruto doméstico c/ wedge UIP de 6% a.a.
    b = 1.0 / R
    h = Rf / R
    g = 0.04641
    H = 1.325
    alpha = 0.25
    L = alpha / (1 - alpha)
    zeta = 0.02                        # Uzawa / desconto endógeno
    nr = 0.4398
    tr = 0.041
    k = 0.0172874121512447 / (1 - 0.3087) * p["slope"]   # inclinação Phillips
    n = 1 - 1 / 7.81                   # decaimento da dívida prefixada (dur 7.81)
    j = 1 - 1 / 29.57                  # decaimento da dívida indexada (dur 29.57)
    indexed = 1 - short - nominal
    plan_cut = math.log(1.075 / 1.1375) / 4   # corte Selic 13,75% -> 7,5%
    cut = plan_cut if terminal is None else terminal
    if announced is None:
        rate = [plan_cut * min((t + 1) / p["cuts"], 1) for t in range(T)]
    else:
        rate = list(announced)
    f = [(-p["sale"] / (100 * tr)) if t < p["duration"] else 0.0 for t in range(len(rate))]

    size = 6 * T
    M = np.zeros((size, size))
    rhs = np.zeros(size)
    rows = []  # cada linha: (coef_array[size], valor)

    def push(coef, value):
        rows.append((coef, value))

    # Condições de contorno dos estados 4 e 5 em t=0
    for i in (4, 5):
        c = np.zeros(size); c[i] = 1
        push(c, -cut if i == 5 else 0.0)
    # Linha inicial NFA/tradable
    r0 = np.zeros(size); r0[3] = 1; r0[1] += 1
    for i, v in [(0, 1), (1, -1), (2, 1), (4, -1)]:
        r0[i] -= R * H * v
    push(r0, R * H * cut)

    inertia = p["inertia"]
    pc = [(-L - k) * (1 - alpha) / (1 - inertia),
          L * (1 - alpha) / (1 - inertia),
          (1 - alpha) / (1 - inertia),
          alpha * g,
          L * (1 - alpha) / (1 - inertia),
          -inertia * (1 - alpha) / (1 - inertia)]
    A = [[1 - zeta - pc[0], -pc[1], -pc[2], -pc[3], -pc[4], -pc[5]],
         [-zeta, 1, 0, -g, 0, 0],
         pc,
         [zeta, -1, 0, R * (1 + H * g) + g, 0, 0],
         [1, -1, 0, 0, 0, 0],
         [-L, L, 1, 0, L, 0]]
    B = [1 - alpha, 0, alpha, 0, 0, 0]
    F = [alpha * g, g, -alpha * g, Rf - R - (1 + R * H) * g, 0, 0]

    for t in range(T - 1):
        for i in range(6):
            c = np.zeros(size); c[6 * (t + 1) + i] = 1
            for q in range(6):
                c[6 * t + q] = -A[i][q]
            push(c, B[i] * (rate[t] - cut) + F[i] * f[t])

    for i in (0, 2):
        c = np.zeros(size); c[6 * (T - 1) + i] = 1
        push(c, 0.0)

    # Linha fiscal (restrição orçamentária intertemporal linearizada)
    fiscal = np.zeros(size)
    constant = -R * (1 + p["reserves"]) * (short + nominal) * cut
    fiscal[2] = -R * (1 + p["reserves"]) * (short + nominal)
    fiscal[0] = -Rf * p["reserves"]
    fiscal[1] = Rf * p["reserves"]
    full_weight = 1 + (1 - h) * p["reserves"]
    real_weight = (1 - p["spend"]) * full_weight
    reserve_carry = (h - 1) * tr / nr - h * p["reserves"] * g
    for t in range(T):
        nominal_price = -R * (1 + p["reserves"]) * nominal * n * n ** t
        real_coeff = -R * (1 + p["reserves"]) * indexed * j * j ** t + b ** t * real_weight
        constant += nominal_price * rate[t] + real_coeff * (rate[t] - cut) - b ** t * reserve_carry * f[t]
        if t + 1 < T:
            fiscal[6 * (t + 1) + 2] -= real_coeff
        fiscal[6 * t + 3] -= b ** t * h * p["reserves"] * g
        fiscal[6 * t] -= b ** t * (h - 1) * p["reserves"]
        fiscal[6 * t + 1] += b ** t * (h - 1) * p["reserves"]
    constant -= R * (1 + p["reserves"]) * nominal * n * n ** T * cut / (1 - n)
    push(fiscal, -constant)

    # Monta e resolve o sistema (JS faz eliminação gaussiana; numpy é equivalente)
    for idx, (coef, value) in enumerate(rows):
        M[idx] = coef
        rhs[idx] = value
    v = np.linalg.solve(M, rhs)

    result = [None] * T
    debt = 0.0
    for t in range(T - 1, -1, -1):
        q = v[6 * t] - v[6 * t + 1]
        a = v[6 * t + 3]
        real = rate[t] - cut - (v[6 * (t + 1) + 2] if t + 1 < T else 0.0)
        debt = (b * debt - real_weight * real + h * p["reserves"] * g * a
                + (h - 1) * p["reserves"] * q + reserve_carry * f[t])
        result[t] = dict(
            inflation=100 * math.expm1(math.log(1.1375) - 4 * math.log(R) + 4 * (v[6 * t + 2] + cut)),
            real=100 * math.expm1(4 * (math.log(R) + real)),
            fx=100 * q,
            debt=100 * (debt - p["spend"] * full_weight * real),
            selic=100 * math.expm1(math.log(1.1375) + 4 * rate[t]),
            reserve=100 * (nr * p["reserves"] + tr * f[t]),
        )
    return result[:25]


def debt_mix(settings):
    return dict(short=settings["short"] + settings["swap"] / 100,
                nominal=settings["nominal"] - settings["swap"] / 100)


def solve(settings):
    p = {**settings, **debt_mix(settings)}
    if not p.get("risk"):
        return solve_path(p)
    # Caso com risco de reversão: linearidade permite somar as "notícias"
    T = 180
    low = math.log(1.075 / 1.1375) / 4
    high = math.log(1.175 / 1.1375) / 4
    survival = 1 - p["risk"]
    start = p["cuts"]
    expected = [low * (t + 1) / start if t < start
                else high + (low - high) * survival ** (t - start + 1) for t in range(T)]
    path = solve_path(p, T, expected, high)
    revision = [p["risk"] * (low - high) * survival ** t for t in range(T)]
    news = solve_path({**p, "sale": 0}, T, revision, 0)
    initial_inflation = 1.1375 / (1.01 * math.exp(0.06))
    initial_real = 1.01 * math.exp(0.06)
    for t in range(len(path)):
        r = path[t]
        for key, base in (("inflation", initial_inflation), ("real", initial_real)):
            change = 0.0
            for jj in range(start, t + 1):
                change += math.log((1 + news[t - jj][key] / 100) / base)
            r[key] = 100 * math.expm1(math.log1p(r[key] / 100) + change)
        for key in ("fx", "debt"):
            for jj in range(start, t + 1):
                r[key] += news[t - jj][key]
    return path


PRESETS = {
    "benchmark": {**DEFAULTS},
    "sale": {**DEFAULTS, "sale": 1},
    "risk": {**DEFAULTS, "risk": 0.5},
    "spending": {**DEFAULTS, "spend": 1},
    "both": {**DEFAULTS, "risk": 0.5, "spend": 1},
    # portfólios históricos (set/2014 prefixado-longo; set/2026 LFT-pesado)
    "early_2014": {**DEFAULTS, "short": 0.19133689583783411,
                   "nominal": 0.44090174235982654, "reserves": 0.504936404861777},
    "late_2026": {**DEFAULTS, "short": 0.5363555768127152,
                  "nominal": 0.21930436887766616, "reserves": 0.2004256524300443},
}


def _fmt(path, key):
    return "  ".join(f"{path[t][key]:6.2f}" for t in (0, 1, 2, 3, 4, 8, 12, 24))


if __name__ == "__main__":
    print("=" * 72)
    print("VERIFICAÇÃO — reproduzindo números-âncora do paper (Seção 5)")
    print("=" * 72)
    pre_plan = 100 * (1.1375 / (1.01 * math.exp(0.06)) - 1)   # inflação de regime pré-plano (~6,1%)
    bench = solve(PRESETS["benchmark"])
    sale = solve(PRESETS["sale"])
    i0_b = bench[0]["inflation"]
    i0_s = sale[0]["inflation"]
    print(f"\nInflação de regime (pré-plano) = {pre_plan:.2f}%  (paper ~6,1%)")
    print(f"\nPlano base SEM intervenção cambial:")
    print(f"  inflação de impacto (trim 0) = {i0_b:.2f}%   surto = +{i0_b-pre_plan:.2f}pp")
    print(f"  (paper: sobe de ~6,1% para ~9,4%  =>  surto ~+3,3pp)")
    print(f"\nPlano base COM venda de reservas de 1% do PIB:")
    print(f"  inflação de impacto (trim 0) = {i0_s:.2f}%   surto = +{i0_s-pre_plan:.2f}pp")
    print(f"  (paper: impacto ~6,4%  =>  surto ~+0,3pp)")

    print("\n" + "-" * 72)
    print("Trimestres amostrados:        0       1       2       3       4       8      12      24")
    for name in ("benchmark", "sale"):
        path = solve(PRESETS[name])
        print(f"\n[{name}]")
        for key, lab in [("selic", "Selic nom."), ("inflation", "IPC infl."),
                         ("real", "Selic real"), ("fx", "câmbio real"), ("debt", "dívida real")]:
            print(f"  {lab:12s} {_fmt(path, key)}")

    print("\n" + "-" * 72)
    print("Composição da dívida (inflação de impacto, trim 0):")
    for name in ("early_2014", "late_2026", "benchmark"):
        p0 = solve(PRESETS[name])[0]["inflation"]
        print(f"  {name:12s} short={PRESETS[name]['short']:.3f}  ->  inflação trim0 = {p0:.2f}%")

    print("\n" + "-" * 72)
    print("Credibilidade (gastar economia de juros / risco de reversão):")
    for name in ("benchmark", "spending", "risk", "both"):
        path = solve(PRESETS[name])
        print(f"  {name:10s}  impacto trim0 = {path[0]['inflation']:6.2f}%   "
              f"pico = {max(r['inflation'] for r in path):6.2f}%   "
              f"infl. trim8 = {path[8]['inflation']:6.2f}%")
