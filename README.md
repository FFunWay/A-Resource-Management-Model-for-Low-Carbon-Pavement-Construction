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
- optimistic
- normal
- pessimistic
Each scenario *s* occurs with probability $p_{s}$, where:

### 2.3 Uncertainty and SAA

## 3. Data Collection and Analysis
### 3.1 Data Collection
### 3.2 Analysis
### 3.3 Results and Managerial Implications

## 4. Conclusion

## 5. Reference
