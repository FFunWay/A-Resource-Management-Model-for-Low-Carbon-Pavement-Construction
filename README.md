# Stochastic Programming for Low-Carbon Sidewalk Pavement Resource Allocation

## 1. Background and Motivation
### 1.1 Motivation
Sidewalks are essential urban infrastructure, yet their pavement structures, materials, and construction methods lead to an enormous number of feasible combinations. Each combination differs in cost, carbon emissions, structural strength, and drainage performance.
However, during the design stage, engineers often lack a systematic decision framework to compare these trade-offs quantitatively. As a result, low-carbon potential is rarely considered proactively.

International practice emphasizes carbon footprint assessment during the design stage, where reduction potential can reach up to 50 percent. In contrast, carbon audits in Taiwan are mostly conducted after project completion, when design decisions are already fixed and emission reduction opportunities are extremely limited.
### 1.2 Background
In practical sidewalk engineering, multiple paving and base combinations exist.
Their carbon and cost impacts are not systematically comparable, and there is no standardized resource framework to guide engineers during the design stage.
### 1.3 Problem Definition
This study develops a decision model to support sidewalk pavement design by systematically comparing material combinations under carbon emission and cost considerations.
## 2. Methodology
The problem is formulated as a resource allocation problem with uncertain carbon emission coefficients.
### 2.1 Assumptions and Limitations
Only the carbon emission factors are treated as stochastic parameters, while decision variables and project requirements are deterministic. Therefore, a full multi-stage stochastic programming formulation is not required.
Scenario-based expected value modeling is adopted to determine the optimal material allocation, while Monte Carlo simulation is used for parameter estimation and risk evaluation.
### 2.2 Model Formulation
**Decision Variables**<br>
| Item | Description |
|------|-----|
|$x_{1}$| Area of high-pressure bricks |
|$x_{2}$| Area of RC concrete |
|$x_{3}$| Area of permeable concrete |

**Deterministic Parameters**<br>
The following parameters are treated as deterministic and are specified by project requirements:
| Item | Description |
|------|-----|
| *Q* | total required sidewalk area |
| *B* | available budget |
|$C_{𝑗}$| unit construction cost of material 𝑗 |

**Stochastic Parameters**<br>
Carbon emission coefficients are modeled as stochastic parameters:
- $E_𝑗(s)$: unit carbon emission of material 𝑗 under scenario s $(\text{kgCO}_{2}\text{e/m}^{2})$

Three emission scenarios are considered for each material:
| Material  𝒋 / scen *s* | optimistic | normal | pessimistic |
|-----|---|---|---|
| high-pressure bricks | $E_1(O)$ | $E_1(N)$ | $E_1(P)$ |
| RC concrete | $E_2(O)$ | $E_2(N)$ | $E_2(P)$ |
| permeable concrete  | $E_3(O)$ | $E_3(N)$ | $E_3(P)$ |

Each scenario *s* occurs with probability $p_{s}$ , where: <br/>

<span style="font-size: 200%; display: block; text-align: center;">$$\quad \Large \sum_{s \in S} p_s = 1, \quad p_s \geq 0$$</span> <br>

**Objective Function**<br>
The objective is to minimize the expected total carbon emissions generated during sidewalk construction.<br>
- For a given scenario 𝑠, total carbon emissions are calculated as: <br>

<span style="font-size: 200%; display: block; text-align: center;">$$\quad \Large Z(s) = \sum_{j=1}^{3} E_{j}(s)x_{j}$$</span>

- The expected carbon emissions are then expressed as: <br>

<span style="font-size: 200%; display: block; text-align: center;">$$\quad \Large \mathbb{E}[Z] = \sum_{s \in S} p_s \sum_{j=1}^{3} E_{j}(s)x_{j}$$</span>

This formulation evaluates material allocation decisions based on the weighted average carbon emissions across all scenarios.

**Constraint**<br>
- Area and Budget Constraints:<br>
$x_{1}$ + $x_{2}$ + $x_{3}$ = *Q* , $\sum Cost_j x_j \le B$  <br>
- Interlocking Paver Proportion Constraint: <br>
0.2𝑄 ≤ 𝑥_{1} ≤ 0.6𝑄
Easy maintenance for areas with underground utilities.Avoid poor drainage if too many interlocking pavers are used
- Structural Strength Constraint
Let original structural coefficients be 𝑎1, 𝑎2,𝑎3 : <br>
Normalize them as: <br>
$$S_j = \frac{a_j}{\max(a_1, a_2, a_3)}, j = 1, 2, 3$$ <br>
Structural strength requirement: <br>
$S_{1}𝑥_{1}$ + $S_{2}𝑥_{2}$ + $S_{3}𝑥_{3}$ ≥ 𝑆𝑚𝑖𝑛𝑄 , where 𝑆𝑚𝑖𝑛 is the *minimum acceptable structural index*. Can be obtained from real projects or set as a baseline requirement
- Drainage Performance Constraint
$D_{1}𝑥_{1}$ + $D_{2}𝑥_{2}$ + $D_{3}𝑥_{3}$≥ 𝐷𝑚𝑖𝑛𝑄 , where 𝐷𝑗 = drainage performance index of each material, 𝐷𝑚𝑖𝑛= minimum required drainage capability.

| Constraint | Mathematical Form | Engineering Rationale |
|-----|-----|-----|
|Area| 𝑥1+𝑥2+𝑥3=𝑄 |Total area fixed|
|Budget| ∑𝐶𝑜𝑠𝑡𝑗𝑥𝑗≤B |Cost limit|
|Interlocking pavers| 0.2𝑄≤𝑥1≤0.6𝑄 |Maintainability & safety|
|Structure| 𝑆1𝑥1+𝑆2𝑥2+𝑆3𝑥3≥𝑆𝑚𝑖𝑛𝑄 | Minimum strength|
|Drainage| 𝐷1𝑥1+𝐷2𝑥2+𝐷3𝑥3≥𝐷𝑚𝑖𝑛𝑄 | Prevent flooding|
|Material relation 1| 𝑥3≥𝑥2 | Maintain drainage|
|Material relation 2| 𝑥2≤0.5(𝑥1+𝑥3) |Avoid impermeable dominance|

### 2.3 SAA 
Scheduling paper uses SAA to approximate expected waiting time:<br>
$$\min_{x} \frac{1}{N} \sum_{n} Z(x, \xi^{(n)})$$ <br>
Full SAA is unnecessary for this project because only the emission factor is random.

  Carbon emission coefficients are represented using discrete scenarios rather than continuous probability distributions.
For each pavement material 𝑗, three emission scenarios are considered:
- optimistic
- normal
- pessimistic <br>

Each scenario 𝑠 is associated with a probability $p_{s}$ , satisfying:
<span style="font-size: 200%; display: block; text-align: center;">$$\sum_{s \in S} p_s = 1$$</span>
These scenarios capture the uncertainty of emission factors while keeping the optimization model tractable.<br>

**Relation to Sample Average Approximation**<br>
Sample Average Approximation (SAA) is commonly applied in stochastic programming to approximate expected values by averaging outcomes across multiple sampled scenarios. However, in this study, uncertainty only affects the emission coefficients, while decision variables and engineering constraints remain deterministic.Therefore, full SAA-based scenario expansion is not applied to the optimization process. Instead, the expected carbon emissions are calculated using a scenario-weighted formulation in the objective function, and Monte Carlo simulation is employed separately for parameter estimation and risk analysis.

**Monte Carlo Risk Analysis**<br>

Monte Carlo simulation with a sample size of 1000 is conducted to evaluate the variability of total carbon emissions under emission uncertainty.
This analysis provides additional insights into the stability and risk behavior of the optimized solution without altering the optimization structure.

## 3. Data Collection and Analysis
### 3.1 Data Collection
**Carbon Footprint Data Sources**

Carbon footprint data in this study are obtained using a hybrid life cycle analysis approach with a cradle-to-gate system boundary.
This boundary includes material production and construction processes, which are the major contributors to carbon emissions in sidewalk pavement projects.<br>
The data compilation integrates multiple sources:<br>
- PCCES (Public Construction Cost Estimation System)
- Unit price analysis sheets
- Input–output tables

The analysis shows that pavement works account for more than 42% of the total project cost, making them the primary source of carbon emissions. Among them, high-pressure concrete tiles are the critical material, and their specifications and construction methods have a direct impact.

**Classification of Construction Methods** <br>
Types of Sidewalk Pavements: <br>
<img width="500" height="360" align="center" alt="types of sidewalk" src="https://github.com/user-attachments/assets/1aeb21a7-6034-4a3f-a15f-00402aa26815" /><br>
Bearing Capacity: If the on-site soil is weak, dry construction methods cannot be used; wet methods or concrete are required.<br>
Permeability requirement: If the site requires permeable pavement, only permeable systems can be used, or alternatives that meet the required regulatory strength.<br>

**Completed Engineering Cases**

<table style="width: 100%;">
  <tr>
    <td align="center" width="33.3%">
      <img alt="sidewalk cost table" src="https://github.com/user-attachments/assets/bc1d3809-e523-42eb-ba31-0416d393e4e7" />
    </td>
    <td align="center" width="33.3%">
      <img alt="sidewalk cost table_2" src="https://github.com/user-attachments/assets/3e187042-b802-4d47-b6c7-8680c2aa5152" />
    </td>
    <td align="center" width="33.3%">
      <img alt="sidewalk cost table_2" src="https://github.com/user-attachments/assets/b9c9c296-b2b0-40f4-bbfa-a3e0b1876fb2" />
    </td>
  </tr>
</table>
<br>
    
A total of seven completed sidewalk engineering cases are collected.
For each case, an optimization model is constructed based on its specific site conditions and required sidewalk area.
Since carbon emissions for these projects have already been audited, the optimized results can be directly compared with actual construction data.
This enables validation of the proposed model under real engineering conditions.

### 3.2 Analysis
🚩 **Part 1: Optimal Configuration & Cost Performance**

For each completed engineering case, an optimization model is constructed using site conditions, sidewalk area requirements, and budget constraints.
Infeasible construction methods are excluded based on bearing capacity and permeability requirements.
The model determines the optimal pavement material allocation by minimizing expected carbon emissions under engineering and cost constraints.

| Item | Area size(m²) | Present |
|------|---|---|
|$x_{1}$| 101.08 | 20% |
|$x_{2}$| 60.65 | 12% |
|$x_{3}$| 343.67 | 68% |

**Model tendency**

- Reduce RC → highest carbon emission
- Increase pervious → best drainage + lowest carbon
- Keep interlocking pavers at minimum ratio → required for maintainability

**Cost Evaluation**

💰Total cost = $649,439   💹Budget = $670,000 <br>
3.1% budget buffer → The optimal design is cost-efficient and feasible.

🚩**Part 2:Constraint Evaluation**

After optimization, all engineering constraints are checked to ensure feasibility.
The analysis shows that most constraints are satisfied with sufficient margins, while some constraints become binding in the optimal solution.

Engineering Constraints – All Satisfied:
| Constraints | Requirement | Result | Status | 
|--------|----|------|---|
| Structural strength | ≥ 0.6 | 0.60 | Binding |
| Drainage index | ≥0.4 | 0.75 | ✓ |
| x₃ ≥x₂ | - | 343.67 ≥ 60.65 | ✓ |
| RC ≤ 0.5(x₁ + x₃) | - | 60.65 ≤ 222.38 | ✓ |
| x₁ ratio | 20 ~ 60% | 20% | Binding |
| Budget | ≤670,000 | 649,439 | ✓ |

In particular: <br>
- The minimum interlocking paver proportion constraint reaches its lower bound.
- The minimum structural strength requirement reaches its threshold.

These binding constraints indicate the key engineering factors that influence carbon emission outcomes in the optimized design.

**Risk Behavior under Uncertainty**

To further evaluate the robustness of the optimized solution, **Monte Carlo** simulation with 1000 samples is conducted.The simulation analyzes the variability of total carbon emissions under uncertainty in emission coefficients.
| Metric | Value (kgCO₂e) |
|--------|----|
| Expected total emissions | 21,827 |
| 5th percentile (best case) | 20,644 |
| 95% VaR (worst 5%) | 22,838 |
| Range | 19,664 ~ 23,283 |

Variability mainly comes from construction method differences, thickness variations, and workmanship 
uncertainty.Even in worst-case simulations, emissions remain within a narrow band (+/– 6%).

### 3.3 Results and Managerial Implications

The optimization results indicate that the optimal pavement configuration consists of **68% permeable concrete, 12% RC concrete, and 20% interlocking pavers**.
This solution minimizes expected carbon emissions while satisfying all engineering constraints and remaining within the budget.

Note.
- The structural strength constraint (S=0.600) has just reached the lower limit, which is a binding constraint.
- The proportion of high-pressure bricks (20.0%) also reached the lower limit, which is a binding constraint.
- To increase structural strength, it may be necessary to increase the proportion of reinforced concrete (RC) or high-pressure bricks, but this will increase carbon emissions.

## 4. Conclusion

This study develops an optimization-based resource allocation model for low-carbon sidewalk pavement design under carbon emission uncertainty.
By integrating stochastic emission coefficients with deterministic engineering and budget constraints, the model identifies a feasible pavement configuration that minimizes expected construction-stage carbon emissions.

The results demonstrate that design-stage optimization provides clearer and more effective guidance for carbon reduction than post-construction carbon audits.In particular, material allocation decisions and binding engineering constraints play a decisive role in shaping achievable emission outcomes.

From a methodological perspective, combining a scenario-based expected value formulation with Monte Carlo analysis offers a practical way to address uncertainty while maintaining model simplicity and interpretability.
This approach is well suited for engineering decision-support problems where uncertainty affects parameters rather than decision feasibility.

<table style="width: 100%;">
  <tr>
    <td align="center" width="50%">
      <img alt="comparison of actual carbon emission" src="https://github.com/user-attachments/assets/9e0eb7cb-619f-40f6-81e8-18e6a3e6a25d" />
    </td>
    <td align="center" width="50%">
      <img alt="comparison of actual cost" src="https://github.com/user-attachments/assets/dfc77877-6ae9-45a9-b4e4-2cbd4ad355eb" />
    </td>
  </tr>
</table>
<br>
<table style="width: 100%">
  <tr>
    <img width="1414" height="326" alt="conclusion" src="https://github.com/user-attachments/assets/e41103d1-c1c1-4aa3-b2e6-baef5396f8d8" />
  </tr>
</table>
<br>

## 5. Reference
- Yao X, Shehadeh KS, Padman R. Multi-resource allocation and care sequence assignment in patient management: a stochastic programming approach. Health Care Manag Sci. 2024 Sep;27(3):352-369. doi: 10.1007/s10729-024-09675-6. Epub 2024 May 30. PMID: 38814509; PMCID: PMC11461687.
- Husemann, M., Kirste, A., & Stumpf, E. (2024). Analysis of cost-efficient urban air mobility systems: Optimization of operational and configurational fleet decisions. European Journal of Operational Research, 317(3), 678-695. https://www.sciencedirect.com/science/article/abs/pii/S0377221723003387
