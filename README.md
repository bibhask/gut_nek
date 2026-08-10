# Kumar_Mukherjee_PRE_simulation_files

## Nek5000 Flow and Passive-Scalar Simulations

This repository contains the mesh-generation scripts and Nek5000 files used for the flow and passive-scalar simulations reported by Kumar and Mukherjee.

The repository is organized into three main components:

1. **Mesh-generation files**
2. **Flow-simulation files**
3. **Passive-scalar simulation files**

The model parameters controlling the Reynolds number, scalar diffusivities, reaction rates, and nutrient absorption can be changed directly in the corresponding Nek5000 `.rea` files, as described below.

---

# 1. Mesh Generation

The Python script generates a Gmsh geometry file with the `.geo` extension.

The mesh-generation workflow is

```text
Python script → .geo → .msh → gmsh2nek → .re2 → genmap → .ma2
```

Run the Python script using

```bash
python3 generate_geometry.py
```

The generated `.geo` file can then be opened in [Gmsh](https://gmsh.info/). Generate the mesh and export it as a `.msh` file.

When exporting the mesh, use:

* **MSH Version 2 ASCII** or **MSH Version 2 Binary**
* **Save all elements:** unchecked
* **Save parametric coordinates:** unchecked

Convert the Gmsh mesh to Nek5000 format using

```bash
gmsh2nek
```

This generates the Nek5000 `.re2` mesh file.

Next, run

```bash
genmap
```

to generate the corresponding `.ma2` mesh-partitioning file.

---

# 2. Flow Simulation

The flow-simulation directory contains the Nek5000 files required for solving the incompressible flow problem.

Typical files include:

* `.usr` — user-defined routines, including initial conditions, boundary conditions, forcing, and other case-specific operations
* `.rea` — simulation parameters
* `.re2` — Nek5000 mesh
* `.ma2` — mesh-partitioning information
* `SIZE` — memory allocation and spectral-element discretization settings

## Governing equation

The nondimensional momentum equation solved in the flow simulations is

$$
\mathrm{Re}
\left(
\frac{\partial \mathbf{u}}{\partial t}
+
\mathbf{u}\cdot\nabla\mathbf{u}
\right)
=======

-\nabla P
+
\nabla^2\mathbf{u},
$$

where

* $\mathbf{u}$ is the velocity field,
* $P$ is the nondimensional pressure, and
* $\mathrm{Re}$ is the Reynolds number.

The incompressibility condition is

$$
\nabla\cdot\mathbf{u}=0.
$$

## Changing the Reynolds number

For the nondimensional formulation used here, the Reynolds number is specified using **Parameter 2 (`P002`)** in the `.rea` file.

Nek5000 interprets a negative value of `P002` as the Reynolds number.

For example,

```text
-100.000     p002
```

corresponds to

$$
\mathrm{Re}=100.
$$

Similarly,

```text
-10.000      p002
```

gives

$$
\mathrm{Re}=10,
$$

and

```text
-1000.000    p002
```

gives

$$
\mathrm{Re}=1000.
$$

Therefore, to run the flow simulation at a different Reynolds number, modify `P002` in the corresponding `.rea` file.

The velocity initial conditions and boundary conditions used for the simulations are defined in the `.usr` file.

---

# 3. Passive-Scalar Simulation

The passive-scalar simulations solve for two scalar fields:

* **Passive scalar 1 (`PS1`)**: nutrient concentration, $N$
* **Passive scalar 2 (`PS2`)**: bacterial concentration, $B$

The scalar fields undergo advection, diffusion, and reaction.

## Governing equations

### Nutrient concentration — PS1

The nutrient field satisfies

$$
\frac{\partial N}{\partial t}
+
\mathbf{u}\cdot\nabla N
=======================

## D_N^* \nabla^2 N

\mathrm{PARAM}(50),
B\frac{N}{\bar{N}+N},
$$

where

$$
D_N^*=\frac{1}{\mathrm{Pe}_N}.
$$

For the present model,

$$
\mathrm{PARAM}(50)
==================

# \mathrm{Da}_N

\kappa,\mathrm{Da}_B.
$$

Thus, the equation can equivalently be written as

$$
\frac{\partial N}{\partial t}
+
\mathbf{u}\cdot\nabla N
=======================

## \frac{1}{\mathrm{Pe}_N}\nabla^2N

\mathrm{Da}_N
B\frac{N}{\bar{N}+N}.
$$

---

### Bacterial concentration — PS2

The bacterial field satisfies

$$
\frac{\partial B}{\partial t}
+
\mathbf{u}\cdot\nabla B
=======================

D_B^* \nabla^2 B
+
\mathrm{PARAM}(51),
B\frac{N}{\bar{N}+N},
$$

where

$$
D_B^*=\frac{1}{\mathrm{Pe}_B}.
$$

For the present model,

$$
\mathrm{PARAM}(51)=\mathrm{Da}_B.
$$

Therefore,

$$
\frac{\partial B}{\partial t}
+
\mathbf{u}\cdot\nabla B
=======================

\frac{1}{\mathrm{Pe}_B}\nabla^2B
+
\mathrm{Da}_B
B\frac{N}{\bar{N}+N}.
$$

Here, $\bar{N}$ is the nutrient concentration scale appearing in the Monod-type reaction term.

---

# 4. Changing the Passive-Scalar Diffusivities

Nek5000 uses the thermal-equation terminology `CONDUCT` and `RHOCP` for passive-scalar transport coefficients.

For a passive scalar $\phi_i$,

$$
D_i^*
=====

\frac{\mathrm{CONDUCT}_i}{\mathrm{RHOCP}_i}.
$$

In the provided simulations,

$$
\mathrm{RHOCP}_i=1,
$$

so that

$$
D_i^*=\mathrm{CONDUCT}_i.
$$

Therefore,

$$
\boxed{
\mathrm{CONDUCT}_{PS1}
======================

\frac{1}{\mathrm{Pe}_N}
}
$$

and

$$
\boxed{
\mathrm{CONDUCT}_{PS2}
======================

\frac{1}{\mathrm{Pe}_B}
}
$$

The relevant portion of the `.rea` file is

```text
1.00000     p102
0.00000     p103 weight of stabilizing filter (.01)

4  Lines of passive scalar data follows 2 CONDUCT; 2RHOCP

0.00013       0.00013       1.00000       1.00000       1.00000
1.00000       1.00000       1.00000       1.00000
1.00000       1.00000       1.00000       1.00000       1.00000
1.00000       1.00000       1.00000       1.00000

13   LOGICAL SWITCHES FOLLOW
T      IFFLOW
```

For the two passive scalars used in this repository, the first two entries of the `CONDUCT` data are

```text
0.00013       0.00013
   ↑             ↑
   PS1           PS2
```

Therefore,

```text
First CONDUCT value  = 1/Pe_N
Second CONDUCT value = 1/Pe_B
```

For example, the provided values

```text
0.00013       0.00013
```

correspond to approximately

$$
\mathrm{Pe}_N
=============

\mathrm{Pe}_B
\approx
7692.
$$

To use different Péclet numbers, replace these two values with

```text
1/Pe_N       1/Pe_B
```

respectively.

For example, for

$$
\mathrm{Pe}_N=1000,
\qquad
\mathrm{Pe}_B=500,
$$

use

```text
0.00100       0.00200       1.00000       1.00000       1.00000
```

while keeping the corresponding `RHOCP` values equal to `1.00000`.

---

# 5. Changing the Reaction Parameters

The reaction parameters are specified directly in the `.rea` file.

The relevant entries are

```text
0.00000     p049
0.030000    p050 DA NUTRIENTS
0.030000    p051 DA BACTERIA
0.00100     p053 BETA ABSORPTION
```

Their meanings are:

| Nek5000 parameter | Model parameter                     | Description                           |
| ----------------- | ----------------------------------- | ------------------------------------- |
| `P050`            | $\mathrm{Da}_N=\kappa\mathrm{Da}_B$ | Nutrient-consumption Damköhler number |
| `P051`            | $\mathrm{Da}_B$                     | Bacterial-growth Damköhler number     |
| `P053`            | $\beta$                             | Nutrient absorption parameter         |

Thus, the default values in the provided case are

$$
\mathrm{Da}_N=0.03,
$$

$$
\mathrm{Da}_B=0.03,
$$

and

$$
\beta=0.001.
$$

These values can be changed directly in the `.rea` file to explore different reaction regimes.

For example, changing

```text
0.030000     p051 DA BACTERIA
```

to

```text
0.100000     p051 DA BACTERIA
```

changes the bacterial Damköhler number from

$$
\mathrm{Da}_B=0.03
$$

to

$$
\mathrm{Da}_B=0.10.
$$

---

# 6. Nutrient Absorption Boundary Condition

The nutrient field (`PS1`) includes an absorption boundary condition of the form

$$
\mathrm{flux}
=============

-\beta N,
$$

where

$$
\beta=\mathrm{PARAM}(53).
$$

Thus, in the Nek5000 user routines the condition is implemented in the form

```fortran
flux = -param(53)*N
```

for the nutrient scalar.

Equivalently,

$$
\mathrm{flux}
=============

-\mathrm{PARAM}(53),PS1.
$$

The value of `PARAM(53)` is specified through `P053` in the `.rea` file:

```text
0.00100     p053 BETA ABSORPTION
```

Therefore, changing `P053` changes the nutrient absorption strength without changing the governing equations.

The corresponding nutrient boundary must use the Nek5000 user-defined scalar flux boundary condition (`f`) where this flux is imposed.

---

# 7. Main Parameters to Vary

The principal nondimensional parameters can therefore be varied as follows:

| Physical/model parameter            | Nek5000 input                        | Where to change |
| ----------------------------------- | ------------------------------------ | --------------- |
| Reynolds number $\mathrm{Re}$       | `-P002`                              | `.rea`          |
| $1/\mathrm{Pe}_N$                   | First `CONDUCT` value                | `.rea`          |
| $1/\mathrm{Pe}_B$                   | Second `CONDUCT` value               | `.rea`          |
| $\mathrm{Da}_N=\kappa\mathrm{Da}_B$ | `P050`                               | `.rea`          |
| $\mathrm{Da}_B$                     | `P051`                               | `.rea`          |
| Absorption coefficient $\beta$      | `P053`                               | `.rea`          |
| Initial conditions                  | user routines                        | `.usr`          |
| Boundary conditions                 | user routines / boundary identifiers | `.usr` / mesh   |
| Polynomial order                    | `lx1`                                | `SIZE`          |

For most parameter sweeps, the quantities of primary interest can therefore be changed directly in the `.rea` file.

---

# 8. Example Parameter Modification

As an example, suppose a simulation is required with

$$
\mathrm{Re}=100,
$$

$$
\mathrm{Pe}_N=5000,
$$

$$
\mathrm{Pe}_B=10000,
$$

$$
\mathrm{Da}_N=0.02,
$$

$$
\mathrm{Da}_B=0.05,
$$

and

$$
\beta=0.002.
$$

The corresponding `.rea` parameters would include

```text
-100.000     p002

0.020000     p050 DA NUTRIENTS
0.050000     p051 DA BACTERIA
0.002000     p053 BETA ABSORPTION
```

and the first two passive-scalar `CONDUCT` entries would be

```text
0.000200       0.000100       1.00000       1.00000       1.00000
```

because

$$
\frac{1}{\mathrm{Pe}_N}
=======================

# \frac{1}{5000}

2\times10^{-4},
$$

and

$$
\frac{1}{\mathrm{Pe}_B}
=======================

# \frac{1}{10000}

10^{-4}.
$$

---

# 9. Running the Simulations

Nek5000 can be obtained from the official repository:

https://github.com/Nek5000/Nek5000

Official Nek5000 documentation:

https://nek5000.github.io/NekDoc/

Compile a case using

```bash
makenek <case_name>
```

and run the compiled case using the appropriate Nek5000 execution command for the local or HPC environment.

For MPI execution, a typical Nek5000 command is

```bash
nekmpi <case_name> <number_of_MPI_ranks>
```

or the corresponding cluster-specific `mpirun`/`srun` command.

---

## Important File-Naming Requirement

All Nek5000 files belonging to the same simulation case must use the same case-name prefix.

For example,

```text
case1.usr
case1.rea
case1.re2
case1.ma2
```

should all use the prefix

```text
case1
```

before running the simulation.

---

# 10. Repository Structure

A typical directory structure is

```text
Kumar_Mukherjee_PRE_simulation_files/
│
├── Mesh_generation/
│   └── generate_geometry.py
│
├── Flow_simulation/
│   ├── case.usr
│   ├── case.rea
│   ├── case.re2
│   ├── case.ma2
│   └── SIZE
│
├── Passive_scalar_simulation/
│   ├── case.usr
│   ├── case.rea
│   ├── case.re2
│   ├── case.ma2
│   └── SIZE
│
├── LICENSE
└── README.md
```

Users interested in reproducing or extending the simulations should first identify the desired nondimensional parameters and modify the corresponding `.rea` entries according to the tables above.

---

# License

This repository is licensed under the Apache License 2.0. See the `LICENSE` file for details.

---

# Contact

For questions regarding the code or simulations, contact:

**Bibhas Kumar**
**Iowa State University**
**[bibhas@iastate.edu](mailto:bibhas@iastate.edu)**
