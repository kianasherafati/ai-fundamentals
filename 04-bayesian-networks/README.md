# Bayesian Networks and Inference

A notebook with discrete Bayesian-network representations, conditional probability tables, and exact and approximate inference. Examples include an alarm/temperature system and match outcomes conditioned on team skills.

- **Exact inference:** joint probabilities, enumeration, and variable elimination.
- **Approximate inference:** rejection sampling, likelihood weighting, and Gibbs sampling.
- **Visualization:** network structure and conditional probability tables.

## Explore

From this directory:

```sh
python -m pip install -r requirements.txt
python -m jupyterlab
```

Open [bayesian_inference.ipynb](bayesian_inference.ipynb) from this working directory so imports from `utils/` resolve. The notebook contains repeated helper definitions from successive course exercises; execute cells in their intended order.

[Network utilities](utils/bayes_net.py) · [Course report](report.pdf)
