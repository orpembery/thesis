#!/bin/bash

cd ..

git clone https://github.com/orpembery/helmholtz-firedrake.git

git clone https://github.com/orpembery/helmholtz-nearby-preconditioning.git

git clone https://github.com/orpembery/helmholtz-monte-carlo.git

git clone https://github.com/orpembery/running-helmholtz-monte-carlo.git

git clone https://github.com/orpembery/prob-gmres-examples.git

git clone https://github.com/orpembery/running-nbpc.git

curl -O https://zenodo.org/record/3665798/files/running-helmholtz-monte-carlo-data.zip

unzip running-helmholtz-monte-carlo-data.zip running-helmholtz-monte-carlo-data

