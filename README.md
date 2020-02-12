# Electronic Supplementary Information for the Thesis 'The Helmholtz Equation in Heterogeneous and Random Media: Analysis and Numerics'

This repository provides all the files needed to recompile and reproduce all the analysis of numerical results in Owen Pembery's PhD Thesis 'The Helmholtz Equation in Heterogeneous and Random Media: Analysis and Numerics', University of Bath, 2020.

In addition, the repositories described below provide the code necessary to run the numerical experiments described in the thesis.

## Reproducing the thesis

* All the below explanations assume that one has downloaded a copy of this repository. It is useful to place this repository inside another directory, as doing anything more than recompiling the thesis will require downloading additional files, which will sit in the directory above this one.

* To only recompile the thesis one needs a LaTeX installation (preferably with the ability to download packages as-needed). To recompile the thesis, run
```
make
```

* To reproduce all of the analysis of the numerical results, reproduce all of the figures, and recompile the thesis:
1. Install LaTeX as described above
2. Install the complex branch of the Firedrake software. At the time of writing, instructions on downloading the complex branch of Firedrake are located [here](https://github.com/firedrakeproject/firedrake/projects/4#card-13363715).
3. Activate the Firedrake venv (as described [here](https://www.firedrakeproject.org/download.html).
4. Run
```
pip install pandas
```
5. Run
```
./download_auxilliary_files.sh
```
6. Ensure that the directories `../helmholtz-firedrake`, `../helmholtz-nearby-preconditioning`, `helmholtz-monte-carlo`, and `running-helmholtz-monte-carlo` are all on your `PYTHONPATH` when in the Firedrake venv.

* To re-run the numerical experiments in the thesis, one must run the code manually. The code to run the numerical experiments is located in the repositories [running-helmholtz-monte-carlo](https://github.com/orpembery/running-helmholtz-monte-carlo), [running-nbpc](https://github.com/orpembery/running-nbpc), and [prob-gmres-examples](https://github.com/orpembery/prob-gmres-examples) (although the code in these repositories requires the code in [helmholtz-firedrake](https://github.com/orpembery/helmholtz-firedrake), [helmholtz-nearby-preconditioning](https://github.com/orpembery/helmholtz-nearby-preconditioning), and [helmholtz-monte-carlo](https://github.com/orpembery/helmholtz-monte-carlo)). (All of these repositories are downloaded to the directory `..` by running `./download_auxilliary_files.sh`.

In order to make the relationship between the code and the thesis more transparent, the following table shows which scripts, in which repositories, are used to create which figures and tables in the thesis.

| Figures/Tables | Scripts used to run the numerical experiment | Repository containing scripts |Scripts used to produce the Figures/Tables (in this repository)|
|----------------|----------------------------------------------|-------------------------------|---------------------------------------------------------------|
|Figures 4.1-4.6|running-nbpc-scaling-linfinity-balena.sh|running-nbpc/nbpc-scaling-linfinity|nbpc-linfinity-plots.py|
|Figures 4.7-4.9, Table 4.1|running-nbpc-scaling-l1-balena.sh|running-nbpc/nbpc-scaling-l1|l1-plot-and-table.py|
|Figures 4.10-4.13, Table 4.2, Figures E1-E24|qmc_error_computations.sh|running-helmholtz-monte-carlo|calculate-qmc-error|
|Figure 4.14, Table 4.4|running-qmc-nbpc-adaptive.sh and running-qmc-mean-based-pc.sh|running-nbpc/qmc-nbpc-adaptive and running-nbpc/qmc-mean-based-pc|nbpc-qmc-sequential-table.py|
|Figure 4.15|run_pc_examples.py|prob-gmres-examples|plot-probabilistic-runs.py|
|Table 4.3|N/A|N/A|n_actual.py|
|Table 4.5|running_variable_M.sh|running-helmholtz-monte-carlo|Nbpc-qmc-parallel-table.py|

Note that the data  created by the scripts `qmc_error_computations` and `running_variable_m` is located in `../running-helmholtz-monte-carlo-data/data-for-num-qmc-points` and `../running-helmholtz-monte-carlo-data/data-for-nbpc-qmc` respectively. If you are running these numerical experiments again, you will need to move the data to the correct locations manually, so that the thesis correctly compiles.

* Some of the scripts are for running code on Bath's HPC system [Balena](https://www.bath.ac.uk/corporate-information/balena-hpc-cluster/), and would need to be adapted. You may find the scripts in the repository [balena-complex-hacks](https://github.com/orpembery/balena-complex-hacks) useful for this.



---

For any queries, contact Owen Pembery on opembery 'at' gmail 'dot' com.











