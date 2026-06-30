# Electrical State Specification

Version: 1.0

Status: Stable

Purpose
-------

Defines every electrical variable owned by ElectricalState.

Only ElectricalSolver may modify these variables.

ElectricalState owns these variables exclusively.

---

# Categories

1. Voltage

2. Current

3. Charge

4. Capacity

5. Energy

6. Power

7. State Indicators

8. Resistance

9. Polarization

10. Efficiency

11. Electrical Losses

12. Diagnostics

---

# Variable Template

Variable ID:

Variable Name:

Description:

Unit:

Type:

Default:

Range:

Validation:

Solver:

Industrial Source:

Scientific Source:

Remarks:


# ==========================================================
# Voltage Variables
# ==========================================================

## EV001

Variable Name:
terminal_voltage

Description:
Measured terminal voltage of the cell.

Unit:
V

Type:
float

Default:
0.0

Range:
0.0 → 10.0

Validation:
Must be non-negative.

Solver:
ElectricalSolver

Industrial Source:
IEC 62660
SAE J1798
BMS

Scientific Source:
DFN
SPM
ECM

Status:
Stable

Remarks:
Output voltage seen by the external circuit.

---

## EV002

Variable Name:
ocv

Description:
Open-circuit voltage.

Unit:
V

Type:
float

Default:
0.0

Range:
0.0 → 10.0

Validation:
Must be non-negative.

Solver:
ElectricalSolver

Industrial Source:
IEC
OCV Characterization

Scientific Source:
DFN
SPM

Status:
Stable

Remarks:
Equilibrium voltage without external current.

---

## EV003

Variable Name:
equilibrium_voltage

Description:
Thermodynamic equilibrium voltage.

Unit:
V

Type:
float

Default:
0.0

Range:
0.0 → 10.0

Validation:
Must be non-negative.

Solver:
ElectricalSolver

Industrial Source:
Electrochemical Literature

Scientific Source:
DFN

Status:
Stable

Remarks:
Internal equilibrium potential.

---

## EV004

Variable Name:
overpotential

Description:
Total electrochemical overpotential.

Unit:
V

Type:
float

Default:
0.0

Range:
No fixed limit

Validation:
Finite number.

Solver:
ElectricalSolver

Industrial Source:
Electrochemical Impedance

Scientific Source:
Butler–Volmer
DFN

Status:
Stable

Remarks:
Sum of activation, ohmic and concentration contributions.


# ==========================================================
# Current Variables
# ==========================================================

## EI001

Variable Name:
current

Description:
Terminal current.

Unit:
A

Type:
float

Default:
0.0

Range:
No fixed limit

Validation:
Finite number.

Solver:
ElectricalSolver

Industrial Source:
IEC 62660
BMS

Scientific Source:
DFN
SPM
ECM

Status:
Stable

Remarks:
Positive and negative sign follow Physion sign convention.

---

## EI002

Variable Name:
current_density

Description:
Applied current density.

Unit:
A/m²

Type:
float

Default:
0.0

Range:
No fixed limit

Validation:
Finite number.

Solver:
ElectricalSolver

Industrial Source:
Cell Design

Scientific Source:
DFN
Butler-Volmer

Status:
Stable

Remarks:
Average current per active electrode area.


