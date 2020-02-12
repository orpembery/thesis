# Electronic Supplementary Information for the Thesis 'The Helmholtz Equation in Heterogeneous and Random Media: Analysis and Numerics'

This repository provides all the files needed to recompile and reproduce all the analysis of numerical results in Owen Pembery's PhD Thesis 'The Helmholtz Equation in Heterogeneous and Random Media: Analysis and Numerics', University of Bath, 2020.

In addition, the repositories described below provide the code necessary to run the numerical experiments described in the thesis.

## Explanation

* All the below explanations assume that one has downloaded a copy of this repository. It is useful to place this repository inside another directory, as doing anything more than recompiling the thesis will require downloading additional files, which will sit in the directory above this one.

* To only recompile the thesis one needs a LaTeX installation (preferably with the ability to download packages as-needed). To recompile the thesis, run
```
make
```

* To reproduce all of the analysis of the numerical results, reproduce all of the figures, and recompile the thesis one needs
1. A LaTeX installation as described above, along with
2. To follow these instructions:
..1. Install the complex branch of the Firedrake software. At the time of writing, instructions on downloading the complex branch of Firedrake are located [here](https://github.com/firedrakeproject/firedrake/projects/4#card-13363715).
..2. Activate the Firedrake venv (as described [here](https://www.firedrakeproject.org/download.html).
..3. Run
```
pip install pandas
```
..4. Run
```
./download_auxilliary_files.sh
```
..5. Ensure that the directories `../helmholtz-firedrake`, `../helmholtz-nearby-preconditioning`, `helmholtz-monte-carlo`, and `running-helmholtz-monte-carlo` are all on your `PYTHONPATH` when in the Firedrake venv.