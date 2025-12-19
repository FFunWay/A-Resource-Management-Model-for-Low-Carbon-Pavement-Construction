import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog

# ==========================================
# 1. 參數設定 (Parameters)
# ==========================================
N_SCENARIOS = 1000  # 模擬 1000 次 
TOTAL_AREA = 505.4  # 總面積 Q
BUDGET = 670000     # 預算上限 B

# 成本 (固定值)
# C1: 高壓磚, C2: RC混凝土, C3: 透水混凝土
C = np.array([1325, 850, 1350]) 

# ==========================================
# 1.1 結構強度係數 (Structural Strength)
# ==========================================
# a_j: 各材料的結構強度係數 (可依文獻調整)
# 高壓磚：中等強度，RC：最高強度，透水混凝土：較低強度
a_1, a_2, a_3 = 0.7, 1.0, 0.5  # 原始結構係數

# 正規化: S_j = a_j / max(a_1, a_2, a_3)
a_max = max(a_1, a_2, a_3)
S = np.array([a_1 / a_max, a_2 / a_max, a_3 / a_max])
print(f"【結構強度係數 (正規化後)】S1={S[0]:.2f}, S2={S[1]:.2f}, S3={S[2]:.2f}")

# Smin: 最低可接受的整體結構指標 (可用實際資料計算或設定底標)
# 這裡設定為 0.6，表示整體加權結構強度至少要達到最大值的 60%
S_MIN = 0.6

# ==========================================
# 1.2 排水性係數 (Drainage Capacity)
# ==========================================
# d_j: 各材料的排水能力係數
# 高壓磚：有限排水，RC：幾乎不透水，透水混凝土：最佳排水
d_1, d_2, d_3 = 0.3, 0.1, 1.0  # 原始排水係數

# 正規化: D_j = d_j / max(d_1, d_2, d_3)
d_max = max(d_1, d_2, d_3)
D = np.array([d_1 / d_max, d_2 / d_max, d_3 / d_max])
print(f"【排水性係數 (正規化後)】D1={D[0]:.2f}, D2={D[1]:.2f}, D3={D[2]:.2f}")

# Dmin: 最低可接受的整體排水指標
# 這裡設定為 0.4，確保整體有足夠的排水滯洪能力
D_MIN = 0.4

# ==========================================
# 1.3 高壓磚比例限制
# ==========================================
# 高壓磚面積比例: 0.2Q ≤ x1 ≤ 0.6Q
X1_MIN_RATIO = 0.2  # 最低 20% (維護管線需求)
X1_MAX_RATIO = 0.6  # 最高 60% (確保排水能力)

print(f"【高壓磚比例限制】{X1_MIN_RATIO*100:.0f}% ~ {X1_MAX_RATIO*100:.0f}% of Q")
print("-" * 50)

# ==========================================
# 2. 蒙地卡羅模擬：生成 3 種材料的碳排樣本
# ==========================================
# 這裡就是我們把 "工法/厚度差異" 轉化為 "數學分佈" 的地方

# --- x1 高壓磚 (變異來源：工法差異) ---
# 依據 YSH 報告：級配工法(50.6) ~ 濕式工法(78.1)，最常用乾式(75.6)
E1_samples = np.random.triangular(50.6, 75.6, 78.1, N_SCENARIOS)

# --- x2 RC 混凝土 (變異來源：施工誤差) ---
# 依據 ORA_B 基準 90.0，假設會有 +/- 10% 的施工波動
E2_samples = np.random.triangular(81.0, 90.0, 99.0, N_SCENARIOS)

# --- x3 透水混凝土 (變異來源：碎石層厚度) ---
# 依據 YSH 報告：厚度從 10cm 到 30cm，碳排約在 27.2 ~ 28.0 之間
E3_samples = np.random.triangular(27.2, 27.8, 28.0, N_SCENARIOS)

# 合併樣本矩陣 (3 x 1000)
E_samples = np.vstack([E1_samples, E2_samples, E3_samples])

# 計算 SAA 需要的 "期望值" (平均碳排)
E_mean = np.mean(E_samples, axis=1)

print(f"【碳排模擬結果 (N={N_SCENARIOS})】")
print(f"x1 高壓磚 (含工法變異): 平均 {E_mean[0]:.2f} (範圍 {E1_samples.min():.1f}-{E1_samples.max():.1f})")
print(f"x2 RC混凝土 (含施工變異): 平均 {E_mean[1]:.2f}")
print(f"x3 透水混凝土 (含厚度變異): 平均 {E_mean[2]:.2f}")
print("-" * 50)

# ==========================================
# 3. 求解最佳化 (SAA Model with Extended Constraints)
# ==========================================
# 數學模型：Min E[Z] -> 最小化 "期望總碳排"
# 
# 限制式：
#   1. 預算限制: C1*x1 + C2*x2 + C3*x3 ≤ B
#   2. 面積限制: x1 + x2 + x3 = Q
#   3. 高壓磚比例: 0.2Q ≤ x1 ≤ 0.6Q
#   4. 結構強度: S1*x1 + S2*x2 + S3*x3 ≥ Smin*Q
#   5. 排水性能: D1*x1 + D2*x2 + D3*x3 ≥ Dmin*Q
#   6. 透水≥RC: x3 ≥ x2
#   7. RC比例: x2 ≤ 0.5*(x1 + x3)

# 定義線性規劃參數
c_obj = E_mean  # 目標函數係數 (用模擬出的平均值)

# --- 不等式限制 A_ub @ x <= b_ub ---
A_ub = [
    C,                              # 預算限制: C1*x1 + C2*x2 + C3*x3 <= B
    [-S[0], -S[1], -S[2]],          # 結構強度: -S1*x1 - S2*x2 - S3*x3 <= -Smin*Q (轉換自 >=)
    [-D[0], -D[1], -D[2]],          # 排水性能: -D1*x1 - D2*x2 - D3*x3 <= -Dmin*Q (轉換自 >=)
    [0, 1, -1],                     # 透水≥RC: x2 - x3 <= 0 (即 x3 >= x2)
    [-0.5, 1, -0.5],                # RC比例: -0.5*x1 + x2 - 0.5*x3 <= 0 (即 x2 <= 0.5*(x1+x3))
]
b_ub = [
    BUDGET,                         # 預算上限
    -S_MIN * TOTAL_AREA,            # 結構強度下限 (負號因為轉換)
    -D_MIN * TOTAL_AREA,            # 排水性能下限 (負號因為轉換)
    0,                              # x3 >= x2
    0,                              # x2 <= 0.5*(x1+x3)
]

# --- 等式限制 A_eq @ x = b_eq ---
A_eq = [[1, 1, 1]]      # 面積限制係數 (等式)
b_eq = [TOTAL_AREA]     # 總面積

# --- 變數邊界 (bounds) ---
# x1: 高壓磚比例限制 0.2Q ~ 0.6Q
# x2, x3: 非負
bounds = [
    (X1_MIN_RATIO * TOTAL_AREA, X1_MAX_RATIO * TOTAL_AREA),  # x1: 高壓磚
    (0, None),                                                 # x2: RC混凝土
    (0, None),                                                 # x3: 透水混凝土
]

# 執行求解
res = linprog(c_obj, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')

if res.success:
    x_opt = res.x
    
    print("【最佳化配置建議】")
    print(f" x1 高壓磚   : {x_opt[0]:7.2f} m² ({x_opt[0]/TOTAL_AREA*100:5.1f}%)")
    print(f" x2 RC混凝土 : {x_opt[1]:7.2f} m² ({x_opt[1]/TOTAL_AREA*100:5.1f}%)")
    print(f" x3 透水混凝土: {x_opt[2]:7.2f} m² ({x_opt[2]/TOTAL_AREA*100:5.1f}%)")
    print(f" 預估總成本 : ${np.dot(C, x_opt):,.0f}")
    print("-" * 50)
    
    # ==========================================
    # 3.1 驗證限制式是否滿足
    # ==========================================
    print("【限制式驗證】")
    
    # 高壓磚比例
    x1_ratio = x_opt[0] / TOTAL_AREA
    print(f" 高壓磚比例: {x1_ratio*100:.1f}% (需介於 {X1_MIN_RATIO*100:.0f}%~{X1_MAX_RATIO*100:.0f}%) "
          f"{'✓' if X1_MIN_RATIO <= x1_ratio <= X1_MAX_RATIO else '✗'}")
    
    # 結構強度
    S_total = np.dot(S, x_opt) / TOTAL_AREA
    print(f" 整體結構強度: {S_total:.3f} (需 >= {S_MIN}) {'✓' if S_total >= S_MIN else '✗'}")
    
    # 排水性能
    D_total = np.dot(D, x_opt) / TOTAL_AREA
    print(f" 整體排水性能: {D_total:.3f} (需 >= {D_MIN}) {'✓' if D_total >= D_MIN else '✗'}")
    
    # 透水 >= RC
    print(f" x3 >= x2: {x_opt[2]:.2f} >= {x_opt[1]:.2f} {'✓' if x_opt[2] >= x_opt[1] else '✗'}")
    
    # RC 比例限制
    rc_limit = 0.5 * (x_opt[0] + x_opt[2])
    print(f" x2 <= 0.5*(x1+x3): {x_opt[1]:.2f} <= {rc_limit:.2f} {'✓' if x_opt[1] <= rc_limit else '✗'}")
    
    # 預算
    total_cost = np.dot(C, x_opt)
    print(f" 預算限制: ${total_cost:,.0f} <= ${BUDGET:,} {'✓' if total_cost <= BUDGET else '✗'}")
    
    print("-" * 50)
    
    # ==========================================
    # 4. 風險分析 (Risk Analysis)
    # ==========================================
    # 看看這個配置在 1000 種不同情境下的表現
    real_carbon_outcomes = np.dot(x_opt, E_samples)
    
    mean_carbon = np.mean(real_carbon_outcomes)
    risk_95 = np.percentile(real_carbon_outcomes, 95)
    risk_5 = np.percentile(real_carbon_outcomes, 5)
    
    print("【風險分析】")
    print(f" 預期總碳排 : {mean_carbon:,.2f} kgCO2e")
    print(f" 5% 分位數  : {risk_5:,.2f} kgCO2e (最佳情況)")
    print(f" 95% 風險值 : {risk_95:,.2f} kgCO2e (最糟情況)")
    print(f" 碳排變異範圍: {real_carbon_outcomes.min():,.2f} ~ {real_carbon_outcomes.max():,.2f}")
    
    # 畫圖
    plt.figure(figsize=(12, 5))
    
    # 子圖1: 碳排分佈
    plt.subplot(1, 2, 1)
    plt.hist(real_carbon_outcomes, bins=40, color='#69b3a2', edgecolor='black', alpha=0.7)
    plt.axvline(mean_carbon, color='red', linestyle='dashed', linewidth=2, label=f'Expected: {mean_carbon:,.0f}')
    plt.axvline(risk_95, color='orange', linestyle='dashed', linewidth=2, label=f'95% VaR: {risk_95:,.0f}')
    plt.title('Carbon Footprint Distribution (Monte Carlo)')
    plt.xlabel('Total Carbon Emission (kgCO2e)')
    plt.ylabel('Frequency')
    plt.legend()
    
    # 子圖2: 材料配置比例
    plt.subplot(1, 2, 2)
    labels = ['Interlocking\nPavers (x1)', 'RC Concrete\n(x2)', 'Pervious\nConcrete (x3)']
    sizes = x_opt
    colors = ['#ff9999', '#66b3ff', '#99ff99']
    explode = (0.02, 0.02, 0.02)
    
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
            shadow=True, startangle=90)
    plt.title('Optimal Material Allocation')
    
    plt.tight_layout()
    plt.show()

else:
    print("=" * 50)
    print("【求解失敗】")
    print(f"錯誤訊息: {res.message}")
    print("=" * 50)
    print("\n可能原因：")
    print("1. 限制式互相衝突（如高壓磚比例與排水要求矛盾）")
    print("2. 預算不足以滿足所有限制")
    print("3. Smin 或 Dmin 設定過高")
    print("\n建議調整參數後重新執行。")
