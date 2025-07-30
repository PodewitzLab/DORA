Note: README will be updated soon

# DORA: Transition State Explorer (v1.a)

**DORA** is a Python class for analyzing molecular dissociation pathways. It identifies the transition state by fitting energy and entropy data along a reaction coordinate using physical models. The characterization of the transition state is done using a quantum chemical descriptor of choice.

## Features

- Fits a descriptor of dissociation scan using an exponential decay.
- Determines the cleaving point using said descriptor unless manually specified.
- Fits electronic energy scan (`dE`) using a Morse potential.
- Approximates entropy contributions (`TdS`) with a sigmoid function, using entropic contributions of both equilibrium structures (`TdS_AB` and `TdS_A` + `TdS_B`).
- Calculates Gibbs free energy (`dG = dE + TdS`) and localizes the transition state.

## Requirements

- Python 3
- NumPy
- SciPy


## Usage


```
from dora import DORA

# Example data (replace with your actual values)
descriptor_data = [...]
distance_data = [...]
dE_data = [...]
dE_A = ...
dE_B = ...
TdS_AB = ...
TdS_A = ...
TdS_B = ...

model = DORA(descriptor_data, distance_data, dE_data,
             dE_A, dE_B, TdS_AB, TdS_A, TdS_B)

input_data, output_data = model.run()
```
