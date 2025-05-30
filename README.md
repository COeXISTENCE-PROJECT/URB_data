<p align="center">
  <img src="images/urb.png" align="center" width="30%"/>
</p>

# Data for URB: Urban Routing Benchmark

Repository provides all results produced in the experiment from Urban Routing Benchmark paper. Each subdirectory of the `results` directory, classifies different experimental settings and includes the following scenarios and metrics.


| Directory name    | Experiment                  |
|-------------------|-----------------------------|
| scenario1         | 40% AVs                     |
| scenario1         | 40% AVs and longer training |
| scenario2         | 100% AVs                    |
| demonstrative     | Demonstrative               |
| hyperparam_search | Hyperparameter tuning       |
| res_scenario1     | Metrics for Scenario 1      |

Each experiment folder is named semantically (after the used network, algorithm, and random seed), and include an `exp_config.json` file (that documents all the parameterization used in that experiment).

## Scenario1 - 40% AVs

<p align="center">
  <img src="images/final_travel_times_one_replic_legend_out.png" align="center" width="75%"/>
</p>

## Scenario2 - 100% AVs in St. Arnoult

<p align="center">
  <img src="https://raw.githubusercontent.com/COeXISTENCE-PROJECT/URB/refs/heads/main/docs/100_per_avs.png" align="center" width="50%"/>
</p>

## Demonstrative

### Selfish AVs versus adapting humans in Nangis

<p align="center">
  <img src="results/demonstrative/nan_ipp_ada/plots/travel_times.png" align="center" width="40%"/>
</p>

### Malicious AVs in Nemours

<p align="center">
  <img src="results/demonstrative/nem_qmi_mal/plots/travel_times.png" align="center" width="40%"/>
</p>

### Altruistic AVs in Gretz-Armainvillers

<p align="center">
  <img src="results/demonstrative/gre_vdn_alt/plots/travel_times.png" align="center" width="40%"/>
</p>

## Metrics for Scenario 1

### ST. ARNOULT

| ALGORITHM     | $t^{PRE}$  | $t^{TEST}$ | $t_{CAV}$ | $t_{HDV}^{POST}$ | $c_{ALL}$ | $c_{HDV}$ | $c_{CAV}$ | $\Delta$ V  | $\Delta$ L  | WR |
|---------------|--------|-------------|------|-----|------|------|------|-----|-----|----|
| IPPO          | 3.15   | 3.28        | 3.34 | 3.24| 0.6  | 0.12 | 1.33 | -0.31 | 0.05 | 0% |
| IQL           | 3.15   | 3.34        | 3.49 | 3.24| 0.66 | 0.14 | 1.44 | -0.42 | 0.08 | 0% |
| MAPPO         | 3.15   | 3.32        | 3.43 | 3.25| 0.66 | 0.14 | 1.45 | -0.27 | 0.08 | 0% |
| QMIX          | 3.15   | 3.2         | 3.12 | 3.25| 0.65 | 0.13 | 1.43 | -0.2  | 0.01 | 66% |
| HUMAN         | 3.15   | 3.15        | 3.15 | 3.15| 0.0  | 0.0  | 0.0  | 0     | 0.0  | 100% |
| AON           | 3.15   | 3.15        | 3.01 | 3.25| 0.55 | 0.09 | 1.21 | -0.06 | -0.0 | 100% |
| RANDOM        | 3.15   | 3.38        | 3.58 | 3.25| 0.6  | 0.09 | 1.36 | -0.33 | 0.1  | 0% |

### PROVINS

| ALGORITHM     | $t^{PRE}$  | $t^{TEST}$ | $t_{CAV}$ | $t_{HDV}^{POST}$ | $c_{ALL}$ | $c_{HDV}$ | $c_{CAV}$ | $\Delta$ V  | $\Delta$ L  | WR |
|---------------|--------|-------------|------|-----|------|------|------|-----|-----|----|
| IPPO          | 2.8    | 2.88        | 2.92 | 2.85| 0.53 | 0.26 | 0.93 | -0.4  | 0.03 | 0% |
| IQL           | 2.8    | 2.92        | 3.03 | 2.84| 1.48 | 0.98 | 2.23 | -0.52 | 0.06 | 0% |
| MAPPO         | 2.8    | 2.92        | 3.03 | 2.85| 1.23 | 0.81 | 1.87 | -0.64 | 0.06 | 0% |
| QMIX          | 2.8    | 2.96        | 3.14 | 2.85| 0.88 | 0.54 | 1.41 | -0.8  | 0.07 | 0% |
| HUMAN         | 2.8    | 2.8         | 2.8  | 2.8 | 0.0  | 0.0  | 0.0  | 0.0   | 0.0  | 100% |
| AON           | 2.8    | 2.81        | 2.76 | 2.84| 0.47 | 0.19 | 0.99 | -0.14 | -0.0 | 100% |
| RANDOM        | 2.8    | 2.93        | 3.04 | 2.85| 0.51 | 0.22 | 0.95 | -0.62 | 0.06 | 0% |

### INGOLSTADT

| ALGORITHM     | $t^{PRE}$  | $t^{TEST}$ | $t_{CAV}$ | $t_{HDV}^{POST}$ | $c_{ALL}$ | $c_{HDV}$ | $c_{CAV}$ | $\Delta$ V  | $\Delta$ L  | WR |
|---------------|--------|-------------|------|-----|------|------|------|-----|-----|----|
| IPPO          | 4.21   | 4.4         | 4.72 | 4.18| 1.76 | 1.22 | 2.56 | -0.37 | 0.07 | 0% |
| IQL           | 4.21   | 4.45        | 4.8  | 4.22| 1.68 | 1.08 | 2.59 | -0.62 | 0.07 | 0% |
| MAPPO         | 4.21   | 4.44        | 4.81 | 4.2 | 1.82 | 1.21 | 2.75 | -0.62 | 0.07 | 0% |
| QMIX          | 4.21   | 4.36        | 4.55 | 4.23| 1.2  | 0.67 | 1.98 | -0.73 | 0.02 | 0% |
| HUMAN         | 4.21   | 4.21        | 4.21 | 4.21| 0.0  | 0.0  | 0.0  | 0.0   | 0.0  | 100% |
| AON           | 4.21   | 4.29        | 4.37 | 4.23| 0.87 | 0.55 | 0.24 | -0.45 | -0.01| 0% |
| RANDOM        | 4.21   | 4.45        | 4.81 | 4.22| 0.99 | 0.49 | 1.74 | -0.68 | 0.07 | 0% |

## Metrics for Scenario 2 

### ST. ARNOULT

| ALGORITHM     | $t^{PRE}$  | $t^{TEST}$ | $t_{CAV}$ | $t_{HDV}^{POST}$ | $c_{ALL}$ | $c_{HDV}$ | $c_{CAV}$ | $\Delta$ V  | $\Delta$ L  | WR |
|---------------|--------|-------------|------|-----|------|------|------|-----|-----|----|
| IPPO          | 3.15   | 3.51        | 3.51 | N/A | 1.65  | 0.0 | 1.65 | -0.76 | 0.15 | 0% |
| IQL           | 3.15   | 3.64        | 3.64 | N/A | 0.37 | 0.0 | 0.37 | -0.6 | 0.21 | 0% |
| MAPPO         | 3.15   | 3.65        | 3.65 | N/A | 0.65 | 0.0 | 0.65 | -0.7 | 0.21 | 0% |
| QMIX          | 3.15   | 3.58        | 3.58 | N/A | 0.42 | 0.0 | 0.42 | -0.63  | 0.18 | 0% |
| HUMAN         | 3.15   | 3.15        | N/A  | 3.15| 0.0  | 0.0  | 0.0  | 0     | 0.0  | 100% |
