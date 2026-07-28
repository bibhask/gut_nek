# Nek5000 Flow and Passive-Scalar Simulations

## Overview

This repository contains the mesh-generation scripts and Nek5000 files used for flow and passive-scalar simulations.

The repository includes three main components:

1. **Mesh-generation script**
2. **Flow-simulation files**
3. **Passive-scalar reaction files**

---

## 1. Mesh Generation

The Python script generates a Gmsh geometry file with the `.geo` extension.

The workflow is:

```text
Python script → .geo → .msh → gmsh2nek → .re2
```

Run the Python script:

```bash
python3 generate_geometry.py
```

Open the generated `.geo` file in [Gmsh](https://gmsh.info/), generate the mesh, and export it as a `.msh` file.

When exporting the mesh:

* Select **MSH Version 2 ASCII** or **Version 2 Binary**
* Keep **Save all elements** unchecked
* Keep **Save parametric coordinates** unchecked

Convert the mesh to Nek5000 format using:

```bash
gmsh2nek
```

Then run:

```bash
genmap
```

to generate the corresponding `.ma2` file.

---

## 2. Flow Simulation

The flow-simulation folder contains:

* `.usr` – initial conditions, boundary conditions, forcing, and other user-defined routines
* `.rea` – simulation parameters
* `.re2` – Nek5000 mesh
* `.ma2` – mesh-partitioning information
* `SIZE` – memory and discretization settings

For the provided nondimensional case, the Reynolds number can be changed using Parameter 2 in the `.rea` file.

For example:

```text
P002 = -100
```

corresponds to:

```text
Re = 100
```

The `.usr` file contains the specific initial and boundary conditions used in the simulation.

---

## 3. Passive-Scalar Simulation

The passive-scalar folder contains the Nek5000 files used for scalar advection, diffusion, and reaction.

The `.usr` file contains:

* Scalar initial conditions
* Scalar boundary conditions
* Reaction source and sink terms
* Other user-defined scalar routines

The `.rea` file contains the parameters used in the reaction equations, such as reaction-rate constants and scalar diffusivities.

Check the comments in the `.usr` and `.rea` files before changing any parameters.

---

## Running the Simulations

Download Nek5000 from:

https://github.com/Nek5000/Nek5000

Official documentation:

https://nek5000.github.io/NekDoc/



All Nek5000 files belonging to one case must have the same filename prefix.

---

## License

This repository is licensed under the Apache License 2.0. See the `LICENSE` file for details.

## Contact

For questions regarding the code or simulations, contact:

**Bibhas Kumar**
**Iowa State University**
**bibhas@iastate.edu**
