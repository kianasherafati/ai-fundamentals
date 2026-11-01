# MDP and Reinforcement Learning

A notebook exploring iterative policy evaluation and policy iteration on a small finite MDP, followed by tabular Q-learning on LunarLander with discretized observations and an epsilon-greedy policy.

## Explore

From this directory:

```sh
python -m pip install -r requirements.txt
python -m jupyterlab
```

Open [lunar_lander.ipynb](lunar_lander.ipynb) and use this directory as the notebook working directory. The notebook requests `LunarLander-v3`; Gymnasium's Box2D extra is required. Installing Box2D may require native build tools on some platforms.

The notebook contains training runs of thousands of episodes. Review the training settings before running all cells. The saved GIFs are examples from the submitted experiment; their filenames do not establish general policy performance.

| Random-policy example | Trained-policy example |
| --- | --- |
| ![Random LunarLander policy](random_policy_lander.gif) | ![Saved LunarLander policy](videos/trained_policy.gif) |

[Course report](report.pdf)
