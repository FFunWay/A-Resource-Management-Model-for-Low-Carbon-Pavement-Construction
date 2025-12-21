import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog
import os
from datetime import datetime

# 1. 參數設定
N_SCENARIOS = 1000  # 模擬 1000 次 
TOTAL_AREA = 91.5 # 總面積 Q
BUDGET = 160400     # 預算上限 B

# 成本 (固定)
# C1: 高壓磚, C2: RC混凝土, C3: 透水混凝土
C = np.array([1325, 850, 1350]) 


# 1.1 結構強度係數 (高壓磚：中等，RC：最高，透水混凝土：較低)
a_1, a_2, a_3 = 0.7, 1.0, 0.5

# 正規化
a_max = max(a_1, a_2, a_3)
S = np.array([a_1 / a_max, a_2 / a_max, a_3 / a_max])
print(f"【結構強度係數 (正規化後)】S1={S[0]:.2f}, S2={S[1]:.2f}, S3={S[2]:.2f}")

S_MIN = 0.6  # 最低可接受的整體結構指標


# 1.2 排水性係數 (高壓磚：有限，RC：幾乎不透水，透水混凝土：最佳)
d_1, d_2, d_3 = 0.3, 0.1, 1.0

# 正規化
d_max = max(d_1, d_2, d_3)
D = np.array([d_1 / d_max, d_2 / d_max, d_3 / d_max])
print(f"【排水性係數 (正規化後)】D1={D[0]:.2f}, D2={D[1]:.2f}, D3={D[2]:.2f}")

D_MIN = 0.4  # 最低可接受的整體排水指標


# 1.3 高壓磚比例限制 (0.2Q ≤ x1 ≤ 0.6Q)
X1_MIN_RATIO = 0.2
X1_MAX_RATIO = 0.6

print(f"【高壓磚比例限制】{X1_MIN_RATIO*100:.0f}% ~ {X1_MAX_RATIO*100:.0f}% of Q")
print("-" * 50)


# 1.4 SAA 設定
N_LB = 50      # 計算 LB 的小樣本數
M_BATCHES = 20 # 重複計算 LB 的次數
N_UB = 5000    # 計算 UB 的大樣本數


# 1.5 建立輸出資料夾（固定路徑，不使用時間戳）
output_folder = r"C:\Users\USER\OneDrive\桌面\ORA\ORA期末專題\1222\F"
os.makedirs(output_folder, exist_ok=True)

# timestamp 仍保留（用於寫入 Result.txt 的執行時間，不影響資料夾命名）
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

print(f"【輸出資料夾】{output_folder}")
print("-" * 50)
output_lines = []
def log(text=""):
    """同時輸出到終端和收集到 output_lines"""
    print(text)
    output_lines.append(text)


# 2. 核心 function
def generate_scenarios(n_scenarios):
    """生成 n 個情境的碳排放係數樣本"""
    E1 = np.random.triangular(50.6, 75.6, 78.1, n_scenarios)   # 高壓磚
    E2 = np.random.triangular(81.0, 90.0, 99.0, n_scenarios)   # RC
    E3 = np.random.triangular(27.2, 27.8, 28.0, n_scenarios)   # 透水混凝土
    return np.vstack([E1, E2, E3])

def solve_optimization(E_mean_vector):
    """給定一組平均碳排係數，解出最佳配置 x"""
    c_obj = E_mean_vector
    
    # 限制式
    A_ub = [
        C,                              # 預算
        [-S[0], -S[1], -S[2]],          # 結構 >= S_MIN
        [-D[0], -D[1], -D[2]],          # 排水 >= D_MIN
        [0, 1, -1],                     # x3 >= x2
        [-0.5, 1, -0.5],                # x2 <= 0.5(x1+x3)
    ]
    b_ub = [
        BUDGET,
        -S_MIN * TOTAL_AREA,
        -D_MIN * TOTAL_AREA,
        0,
        0,
    ]
    A_eq = [[1, 1, 1]]
    b_eq = [TOTAL_AREA]
    bounds = [
        (X1_MIN_RATIO * TOTAL_AREA, X1_MAX_RATIO * TOTAL_AREA),
        (0, None),
        (0, None),
    ]
    
    res = linprog(c_obj, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')
    return res


# 3. 輸出模型參數並執行蒙地卡羅模擬
log("=" * 60)
log("【模型參數與限制式總覽】")
log("=" * 60)
log(f"\n[基本參數]")
log(f" 總面積 Q = {TOTAL_AREA} m²")
log(f" 預算上限 B = ${BUDGET:,}")
log(f" 模擬次數 N = {N_SCENARIOS}")
log(f"\n[材料成本 ($/m²)]")
log(f" C1 高壓磚 = ${C[0]}")
log(f" C2 RC混凝土 = ${C[1]}")
log(f" C3 透水混凝土 = ${C[2]}")
log(f"\n[結構強度係數 (正規化)]")
log(f" S1={S[0]:.2f}, S2={S[1]:.2f}, S3={S[2]:.2f}")
log(f" Smin = {S_MIN}")
log(f"\n[排水性係數 (正規化)]")
log(f" D1={D[0]:.2f}, D2={D[1]:.2f}, D3={D[2]:.2f}")
log(f" Dmin = {D_MIN}")
log(f"\n[SAA 設定]")
log(f" N_LB = {N_LB} (小樣本數)")
log(f" M_BATCHES = {M_BATCHES} (重複次數)")
log(f" N_UB = {N_UB} (大樣本驗證數)")

log("\n" + "=" * 60)
log("【限制式數學模型】")
log("=" * 60)
log("\n目標函數: Min Z = E1*x1 + E2*x2 + E3*x3  (最小化總碳排)")
log("\n限制式:")
log(f" 1. 面積限制:     x1 + x2 + x3 = {TOTAL_AREA}")
log(f" 2. 預算限制:     {C[0]}*x1 + {C[1]}*x2 + {C[2]}*x3 ≤ {BUDGET}")
log(f" 3. 高壓磚下限:   x1 ≥ {X1_MIN_RATIO}*Q = {X1_MIN_RATIO * TOTAL_AREA:.2f}")
log(f" 4. 高壓磚上限:   x1 ≤ {X1_MAX_RATIO}*Q = {X1_MAX_RATIO * TOTAL_AREA:.2f}")
log(f" 5. 結構強度:     {S[0]:.2f}*x1 + {S[1]:.2f}*x2 + {S[2]:.2f}*x3 ≥ {S_MIN}*Q = {S_MIN * TOTAL_AREA:.2f}")
log(f" 6. 排水性能:     {D[0]:.2f}*x1 + {D[1]:.2f}*x2 + {D[2]:.2f}*x3 ≥ {D_MIN}*Q = {D_MIN * TOTAL_AREA:.2f}")
log(f" 7. 透水≥RC:      x3 ≥ x2")
log(f" 8. RC比例限制:   x2 ≤ 0.5*(x1 + x3)")
log(f" 9. 非負限制:     x1, x2, x3 ≥ 0")
log("\n" + "=" * 60)

log("\n【蒙地卡羅模擬】")

E_samples = generate_scenarios(N_SCENARIOS)
E1_samples, E2_samples, E3_samples = E_samples[0], E_samples[1], E_samples[2]

E_mean = np.mean(E_samples, axis=1)

log(f"【碳排模擬結果 (N={N_SCENARIOS})】")
log(f"x1 高壓磚 (含工法變異): 平均 {E_mean[0]:.2f} (範圍 {E1_samples.min():.1f}-{E1_samples.max():.1f})")
log(f"x2 RC混凝土 (含施工變異): 平均 {E_mean[1]:.2f}")
log(f"x3 透水混凝土 (含厚度變異): 平均 {E_mean[2]:.2f}")
log("-" * 50)


# 4. 求解最佳化
res = solve_optimization(E_mean)

if res.success:
    x_opt = res.x
    
    log("【最佳化配置建議】")
    log(f" x1 高壓磚   : {x_opt[0]:7.2f} m² ({x_opt[0]/TOTAL_AREA*100:5.1f}%)")
    log(f" x2 RC混凝土 : {x_opt[1]:7.2f} m² ({x_opt[1]/TOTAL_AREA*100:5.1f}%)")
    log(f" x3 透水混凝土: {x_opt[2]:7.2f} m² ({x_opt[2]/TOTAL_AREA*100:5.1f}%)")
    log(f" 預估總成本 : ${np.dot(C, x_opt):,.0f}")
    log("-" * 50)
    

    # 驗證限制式
    log("【限制式驗證】")
    
    # 高壓磚比例
    x1_ratio = x_opt[0] / TOTAL_AREA
    log(f" 高壓磚比例: {x1_ratio*100:.1f}% (需介於 {X1_MIN_RATIO*100:.0f}%~{X1_MAX_RATIO*100:.0f}%) "
          f"{'✓' if X1_MIN_RATIO <= x1_ratio <= X1_MAX_RATIO else '✗'}")
    
    # 結構強度
    S_total = np.dot(S, x_opt) / TOTAL_AREA
    log(f" 整體結構強度: {S_total:.3f} (需 >= {S_MIN}) {'✓' if S_total >= S_MIN else '✗'}")
    
    # 排水性能
    D_total = np.dot(D, x_opt) / TOTAL_AREA
    log(f" 整體排水性能: {D_total:.3f} (需 >= {D_MIN}) {'✓' if D_total >= D_MIN else '✗'}")
    
    # 透水 >= RC
    log(f" x3 >= x2: {x_opt[2]:.2f} >= {x_opt[1]:.2f} {'✓' if x_opt[2] >= x_opt[1] else '✗'}")
    
    # RC 比例限制
    rc_limit = 0.5 * (x_opt[0] + x_opt[2])
    log(f" x2 <= 0.5*(x1+x3): {x_opt[1]:.2f} <= {rc_limit:.2f} {'✓' if x_opt[1] <= rc_limit else '✗'}")
    
    # 預算
    total_cost = np.dot(C, x_opt)
    log(f" 預算限制: ${total_cost:,.0f} <= ${BUDGET:,} {'✓' if total_cost <= BUDGET else '✗'}")
    
    log("-" * 50)
    


    # 5. 風險分析
    real_carbon_outcomes = np.dot(x_opt, E_samples)
    
    mean_carbon = np.mean(real_carbon_outcomes)
    risk_95 = np.percentile(real_carbon_outcomes, 95)
    risk_5 = np.percentile(real_carbon_outcomes, 5)
    
    log("【風險分析】")
    log(f" 預期總碳排 : {mean_carbon:,.2f} kgCO2e")
    log(f" 5% 分位數  : {risk_5:,.2f} kgCO2e (最佳情況)")
    log(f" 95% 風險值 : {risk_95:,.2f} kgCO2e (最糟情況)")
    log(f" 碳排變異範圍: {real_carbon_outcomes.min():,.2f} ~ {real_carbon_outcomes.max():,.2f}")
    log("-" * 50)


    # 6. SAA 上下界分析
    log("=" * 60)
    log("【SAA 上下界驗證分析】")
    log("=" * 60)
    
    # 計算下界
    lb_values = []
    solutions_pool = []

    log(f"\n1. 計算下界 (Lower Bound): 執行 {M_BATCHES} 次小規模最佳化 (N={N_LB})...")

    for i in range(M_BATCHES):
        scenarios = generate_scenarios(N_LB)
        e_mean = np.mean(scenarios, axis=1)
        res_lb = solve_optimization(e_mean)
        
        if res_lb.success:
            lb_values.append(res_lb.fun)
            solutions_pool.append(res_lb.x)
        else:
            log(f"   Batch {i+1} failed.")

    lower_bound = np.mean(lb_values)
    log(f"   -> 完成。Lower Bound (平均最佳值) = {lower_bound:.2f} kgCO2e")

    # 決定候選解
    best_idx = np.argmin(lb_values)
    candidate_x = solutions_pool[best_idx]

    log("-" * 60)
    log(f"2. 選定候選解 (Candidate Solution):")
    log(f"   挑選第 {best_idx+1} 次批次的解作為代表。")
    log(f"   配置: x1={candidate_x[0]:.1f}, x2={candidate_x[1]:.1f}, x3={candidate_x[2]:.1f}")

    # 計算上界
    log(f"3. 計算上界 (Upper Bound): 使用大樣本 (N={N_UB}) 驗證候選解...")

    validation_scenarios = generate_scenarios(N_UB)

    real_costs = np.dot(candidate_x, validation_scenarios)

    upper_bound = np.mean(real_costs)
    log(f"   -> 完成。Upper Bound (真實平均值) = {upper_bound:.2f} kgCO2e")

    # 結果分析
    log("=" * 60)
    log("【SAA 驗證結果總結】")

    gap = (upper_bound - lower_bound)
    gap_percent = (gap / upper_bound) * 100

    log(f"Lower Bound (LB) : {lower_bound:10.2f}")
    log(f"Upper Bound (UB) : {upper_bound:10.2f}")
    log(f"Optimality Gap   : {gap:10.2f} ({gap_percent:.4f}%)")

    if gap_percent < 5:
        log("\n[結論] Gap < 5%，模型收斂良好，解具備統計穩健性！")
    else:
        log("\n[結論] Gap 較大，建議增加 N_LB (小樣本數) 或檢查模型變異。")


    # 7. 視覺化
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    ax1 = axes[0, 0]
    ax1.hist(real_carbon_outcomes, bins=40, color='#69b3a2', edgecolor='black', alpha=0.7)
    ax1.axvline(mean_carbon, color='red', linestyle='dashed', linewidth=2, label=f'Expected: {mean_carbon:,.0f}')
    ax1.axvline(risk_95, color='orange', linestyle='dashed', linewidth=2, label=f'95% VaR: {risk_95:,.0f}')
    ax1.set_title('Carbon Footprint Distribution (Monte Carlo)')
    ax1.set_xlabel('Total Carbon Emission (kgCO2e)')
    ax1.set_ylabel('Frequency')
    ax1.legend()
    
    ax2 = axes[0, 1]
    labels = ['Interlocking\nPavers (x1)', 'RC Concrete\n(x2)', 'Pervious\nConcrete (x3)']
    sizes = x_opt
    colors = ['#ff9999', '#66b3ff', '#99ff99']
    explode = (0.02, 0.02, 0.02)
    ax2.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax2.set_title('Optimal Material Allocation')
    
    ax3 = axes[1, 0]
    ax3.hist(real_costs, bins=50, color='#69b3a2', edgecolor='black', alpha=0.7)
    ax3.axvline(upper_bound, color='red', linestyle='--', linewidth=2, label=f'UB (Mean): {upper_bound:.0f}')
    ax3.axvline(lower_bound, color='blue', linestyle='--', linewidth=2, label=f'LB: {lower_bound:.0f}')
    ax3.set_title(f'SAA Performance Verification (Gap: {gap_percent:.2f}%)')
    ax3.set_xlabel('Total Carbon Emission (kgCO2e)')
    ax3.set_ylabel('Frequency')
    ax3.legend()
    
    ax4 = axes[1, 1]
    ax4.hist(lb_values, bins=15, color='#66b3ff', edgecolor='black', alpha=0.7)
    ax4.axvline(lower_bound, color='blue', linestyle='--', linewidth=2, label=f'Mean LB: {lower_bound:.0f}')
    ax4.axvline(upper_bound, color='red', linestyle='--', linewidth=2, label=f'UB: {upper_bound:.0f}')
    ax4.set_title(f'Lower Bound Distribution ({M_BATCHES} batches)')
    ax4.set_xlabel('Objective Value (kgCO2e)')
    ax4.set_ylabel('Frequency')
    ax4.legend()
    
    plt.tight_layout()
    
    figure_path = os.path.join(output_folder, "Result_Figure.png")
    plt.savefig(figure_path, dpi=300, bbox_inches='tight')
    log(f"\n【圖片已儲存】{figure_path}")
    
    plt.show()
    

    # 8. 存檔
    result_path = os.path.join(output_folder, "Result.txt")
    with open(result_path, 'w', encoding='utf-8') as f:
        f.write(f"執行時間: {timestamp}\n")
        f.write("=" * 60 + "\n\n")
        f.write("\n".join(output_lines))
    
    print(f"\n【結果已儲存】{result_path}")
    print(f"\n所有輸出已存放於資料夾: {output_folder}")

else:
    log("=" * 50)
    log("【求解失敗】")
    log(f"錯誤訊息: {res.message}")
    log("=" * 50)
    log("\n可能原因：")
    log("1. 限制式互相衝突（如高壓磚比例與排水要求矛盾）")
    log("2. 預算不足以滿足所有限制")
    log("3. Smin 或 Dmin 設定過高")
    log("\n建議調整參數後重新執行。")
    
    result_path = os.path.join(output_folder, "Result.txt")
    with open(result_path, 'w', encoding='utf-8') as f:
        f.write(f"執行時間: {timestamp}\n")
        f.write("=" * 60 + "\n\n")
        f.write("\n".join(output_lines))
    
    print(f"\n【結果已儲存】{result_path}")
