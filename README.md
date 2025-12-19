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
$S_{1}$$𝑥_{1}$ + S_{2}𝑥_{2} + S_{3}𝑥_{3} ≥ 𝑆𝑚𝑖𝑛𝑄

- 

### 2.3 Uncertainty and SAA
In this study, uncertainty arises from the carbon emission coefficients associated with different pavement materials.
Construction-related factors such as material specifications, construction methods, and implementation conditions lead to variability in carbon emissions.<br>
**Uncertainty**<br>

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

This hybrid approach enables the identification of emission hotspots associated with different pavement materials and construction methods.

**Classification of Construction Methods** <br>
Sidewalk pavement construction methods are classified based on pavement type and base structure.Different construction methods exhibit distinct bearing capacities and drainage characteristics.

Site conditions are considered when selecting feasible construction methods: <br>
- If on-site soil conditions are weak, dry construction methods are excluded.
- If permeability is required, only permeable pavement systems or alternatives meeting regulatory strength requirements are considered.

This classification process is used to remove infeasible options before optimization.

**Completed Engineering Cases**

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

## 5. Reference
