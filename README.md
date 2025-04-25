# Task distribution

- I have created a new table [here](https://docs.google.com/spreadsheets/d/1Upf4nPxh5kPqe4qOKV84EOifHWEVYadJx688urlQxb0/edit?gid=0#gid=0).
- Please let's keep track and update our progress. Following of this document is made according to this distribution.
- **Please feel free to discuss/make changes, both in the table and here.**
- **Plase let me know if you get any errors!**

# Notes

- Since last time:
    - Progress bars are enhanced.
    - Benchmark progress bar keeps track of the entire experiment, though not fully accurate.
    - Experiments should take significantly shorter (thanks to optimizations and config changes).
    - Now you can run multiple experiments on the same network, simultaneously, with the same folder and environment, as long as you provide **unique experiment IDs**. Please consider doing so.
    - For running experiments on the servers, though, we will need to use different `run.sh` and `cmd_container.sh` files, otherwise server throws stale file handling error. In other words, you can still work with a single `URB` folder, but work with different copies of `run.sh` (`run1.sh`, `run2.sh`...) and `cmd_container.sh` (`cmd_container1.sh`, `cmd_container2.sh`...). Don't forget to update `run.sh` with the filename of corresponding `cmd_container.sh`.

- Definition of **folds** and use of **seeds** changed!
    - Last time, `--seed` argument distinguished different **folds** of the same experiment. It was used both for `TrafficEnvironment` and `PyTorch`.
    - Now, we fix the environment seed to `42` (no need to specify, default value) and provide `--torch-seed` for different folds.
    - See `README.md` for details.
    - Consequently, we will have **1 experiment per each baseline experiment, and 3 runs for others**.

- After finishing an experiment, simply take the folder in `results`, named after the experiment ID, and push to the main direcotry of [here](https://github.com/COeXISTENCE-PROJECT/URB_data).

- There are major changes in the code, and also in `RouteRL/urb`. I strongly recommend running (hopefully, in your virtual environment):
```
pip3 install --force-reinstall --no-cache-dir -r requirements.txt
```

# Commands

I prepared commands for you, according to the task distribution. I made it for your convenience, they are anyway in parallel with what's described in this document and `README.md`.

> No worries, it wasn't manual work, I made it using a script.

### Anastasia
- `python3 scripts/ippo_torchrl.py --conf 1_ippo --torch-seed 0 --net provins --id pro_ipp_0`
- `python3 scripts/ippo_torchrl.py --conf 1_ippo --torch-seed 1 --net provins --id pro_ipp_1`
- `python3 scripts/ippo_torchrl.py --conf 1_ippo --torch-seed 2 --net provins --id pro_ipp_2`

- `python3 scripts/iql_torchrl.py --conf 1_iql --torch-seed 0 --net provins --id pro_iql_0`
- `python3 scripts/iql_torchrl.py --conf 1_iql --torch-seed 1 --net provins --id pro_iql_1`
- `python3 scripts/iql_torchrl.py --conf 1_iql --torch-seed 2 --net provins --id pro_iql_2`

---
### Łukasz
- ~~python3 scripts/baselines.py --conf 1_baseline --model random --net saint_arnoult --id sai_ran~~
- ~~python3 scripts/baselines.py --conf 1_baseline --model aon --net saint_arnoult --id sai_aon~~

- ~~python3 scripts/baselines.py --conf 1_baseline --model random --net provins --id pro_ran~~
- ~~python3 scripts/baselines.py --conf 1_baseline --model aon --net provins --id pro_aon~~

- ~~python3 scripts/mappo_torchrl.py --conf 1_mappo --torch-seed 0 --net saint_arnoult --id sai_map_0~~
- ~~python3 scripts/mappo_torchrl.py --conf 1_mappo --torch-seed 1 --net saint_arnoult --id sai_map_1~~
- ~~python3 scripts/mappo_torchrl.py --conf 1_mappo --torch-seed 2 --net saint_arnoult --id sai_map_2~~

---
### Michał
- ~~python3 scripts/baselines.py --conf 1_baseline --model random --net ingolstadt_custom --id ing_ran~~
- ~~python3 scripts/baselines.py --conf 1_baseline --model aon --net ingolstadt_custom --id ing_aon~~

- ~~python3 scripts/ippo_torchrl.py --conf 1_ippo --torch-seed 0 --net saint_arnoult --id sai_ipp_0~~
- ~~python3 scripts/ippo_torchrl.py --conf 1_ippo --torch-seed 1 --net saint_arnoult --id sai_ipp_1~~
- ~~Python3 scripts/ippo_torchrl.py --conf 1_ippo --torch-seed 2 --net saint_arnoult --id sai_ipp_2~~

- ~~python3 scripts/iql_torchrl.py --conf 1_iql --torch-seed 0 --net saint_arnoult --id sai_iql_0~~
- ~~python3 scripts/iql_torchrl.py --conf 1_iql --torch-seed 1 --net saint_arnoult --id sai_iql_1~~
- ~~python3 scripts/iql_torchrl.py --conf 1_iql --torch-seed 2 --net saint_arnoult --id sai_iql_2~~

- ~~python3 scripts/qmix_torchrl.py --conf 1_qmix --torch-seed 0 --net saint_arnoult --id sai_qmi_0~~
- ~~python3 scripts/qmix_torchrl.py --conf 1_qmix --torch-seed 1 --net saint_arnoult --id sai_qmi_1~~
- ~~python3 scripts/qmix_torchrl.py --conf 1_qmix --torch-seed 2 --net saint_arnoult --id sai_qmi_2~~

---
### Onur
-  ~~python3 scripts/mappo_torchrl.py --conf 1_mappo --torch-seed 0 --net provins --id pro_map_0~~
-  ~~python3 scripts/mappo_torchrl.py --conf 1_mappo --torch-seed 1 --net provins --id pro_map_1~~
-  ~~python3 scripts/mappo_torchrl.py --conf 1_mappo --torch-seed 2 --net provins --id pro_map_2~~

- `python3 scripts/qmix_torchrl.py --conf 1_qmix --torch-seed 0 --net provins --id pro_qmi_0`
- `python3 scripts/qmix_torchrl.py --conf 1_qmix --torch-seed 1 --net provins --id pro_qmi_1`
- `python3 scripts/qmix_torchrl.py --conf 1_qmix --torch-seed 2 --net provins --id pro_qmi_2`

- `python3 scripts/qmix_torchrl.py --conf 1_qmix --torch-seed 0 --net ingolstadt_custom --id ing_qmi_0`
- `python3 scripts/qmix_torchrl.py --conf 1_qmix --torch-seed 1 --net ingolstadt_custom --id ing_qmi_1`
- `python3 scripts/qmix_torchrl.py --conf 1_qmix --torch-seed 2 --net ingolstadt_custom --id ing_qmi_2`
  
---
### Zoltán
- ~~python3 scripts/ippo_torchrl.py --conf 1_ippo --torch-seed 0 --net ingolstadt_custom --id ing_ipp_0~~
- ~~python3 scripts/ippo_torchrl.py --conf 1_ippo --torch-seed 1 --net ingolstadt_custom --id ing_ipp_1~~
- ~~python3 scripts/ippo_torchrl.py --conf 1_ippo --torch-seed 2 --net ingolstadt_custom --id ing_ipp_2~~

- `python3 scripts/iql_torchrl.py --conf 1_iql --torch-seed 0 --net ingolstadt_custom --id ing_iql_0`
- `python3 scripts/iql_torchrl.py --conf 1_iql --torch-seed 1 --net ingolstadt_custom --id ing_iql_1`
- `python3 scripts/iql_torchrl.py --conf 1_iql --torch-seed 2 --net ingolstadt_custom --id ing_iql_2`

- `python3 scripts/mappo_torchrl.py --conf 1_mappo --torch-seed 0 --net ingolstadt_custom --id ing_map_0`
- `python3 scripts/mappo_torchrl.py --conf 1_mappo --torch-seed 1 --net ingolstadt_custom --id ing_map_1`
- `python3 scripts/mappo_torchrl.py --conf 1_mappo --torch-seed 2 --net ingolstadt_custom --id ing_map_2`

---

## Thank you and good luck!

<div style="text-align: center;">
  <img src="https://i.imgur.com/o3kImSM.png" style="width: 50%;" alt="image">
</div>
