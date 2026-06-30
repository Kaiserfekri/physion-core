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

## ECG001

Variable Name:
charge

Description:
Instantaneous stored electrical charge.

Unit:
C

Type:
float

Default:
0.0

Range:
0.0 → ∞

Validation:
Must be non-negative.

Solver:
ElectricalSolver

Industrial Source:
IEC 62660

Scientific Source:
DFN
SPM

Status:
Stable

Remarks:
Represents total stored charge.

---

## ECG002

Variable Name:
charge_transferred

Description:
Total transferred charge.

Unit:
C

Type:
float

Default:
0.0

Range:
0.0 → ∞

Validation:
Must be non-negative.

Solver:
ElectricalSolver

Industrial Source:
Coulomb Counting

Scientific Source:
Battery Management

Status:
Stable

Remarks:
Integrated charge during simulation.

---

## ECG003

Variable Name:
charge_rate

Description:
Charge transfer rate.

Unit:
C/s

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
BMS

Scientific Source:
Electrochemistry

Status:
Stable

Remarks:
Normally identical to electrical current.


## ECP001

Variable Name:
capacity_nominal

Description:
Rated cell capacity.

Unit:
Ah

Type:
float

Default:
0.0

Range:
0.0 → ∞

Validation:
Positive.

Solver:
ElectricalSolver

Industrial Source:
IEC 61960

Scientific Source:
Battery Datasheet

Status:
Stable

Remarks:
Manufacturer nominal capacity.

---

## ECP002

Variable Name:
capacity_available

Description:
Available usable capacity.

Unit:
Ah

Type:
float

Default:
0.0

Range:
0.0 → ∞

Validation:
Positive.

Solver:
ElectricalSolver

Status:
Stable

Remarks:
Temperature and aging dependent.

---

## ECP003

Variable Name:
capacity_remaining

Description:
Remaining usable capacity.

Unit:
Ah

Type:
float

Default:
0.0

Range:
0.0 → capacity_available

Validation:
Cannot exceed available capacity.

Solver:
ElectricalSolver

Status:
Stable

Remarks:
Current remaining charge.

---

## ECP004

Variable Name:
capacity_lost

Description:
Lost capacity.

Unit:
Ah

Type:
float

Default:
0.0

Range:
0.0 → ∞

Validation:
Positive.

Solver:
AgingSolver

Status:
Stable

Remarks:
Permanent degradation.

---

## ECP005

Variable Name:
usable_capacity

Description:
Effective usable capacity.

Unit:
Ah

Type:
float

Default:
0.0

Range:
Positive.

Validation:
Finite.

Solver:
ElectricalSolver

Status:
Stable

Remarks:
Capacity available considering operating limits.


## EEN001

Variable Name:
energy

Description:
Stored electrical energy.

Unit:
Wh

Type:
float

Default:
0.0

Range:
0.0 → ∞

Validation:
Must be non-negative.

Solver:
ElectricalSolver

Status:
Stable

Remarks:
Total stored usable energy.

---

## EEN002

Variable Name:
energy_available

Description:
Available usable energy.

Unit:
Wh

Type:
float

Default:
0.0

Range:
0.0 → ∞

Validation:
Must be non-negative.

Solver:
ElectricalSolver

Status:
Stable

Remarks:
Temperature and aging dependent.

---

## EEN003

Variable Name:
energy_remaining

Description:
Remaining usable energy.

Unit:
Wh

Type:
float

Default:
0.0

Range:
0.0 → energy_available

Validation:
Cannot exceed available energy.

Solver:
ElectricalSolver

Status:
Stable

Remarks:
Remaining electrical energy.

---

## EEN004

Variable Name:
energy_delivered

Description:
Total discharged energy.

Unit:
Wh

Type:
float

Default:
0.0

Range:
0.0 → ∞

Validation:
Must be non-negative.

Solver:
ElectricalSolver

Status:
Stable

Remarks:
Integrated output energy.

---

## EEN005

Variable Name:
energy_charged

Description:
Total charged energy.

Unit:
Wh

Type:
float

Default:
0.0

Range:
0.0 → ∞

Validation:
Must be non-negative.

Solver:
ElectricalSolver

Status:
Stable

Remarks:
Integrated input energy.


## EPW001

Variable Name:
power

Description:
Instantaneous electrical power.

Unit:
W

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

Status:
Stable

Remarks:
Positive during discharge.

---

## EPW002

Variable Name:
power_charge

Description:
Charging power.

Unit:
W

Type:
float

Default:
0.0

Range:
0.0 → ∞

Validation:
Must be non-negative.

Solver:
ElectricalSolver

Status:
Stable

Remarks:
Power entering the cell.

---

## EPW003

Variable Name:
power_discharge

Description:
Discharging power.

Unit:
W

Type:
float

Default:
0.0

Range:
0.0 → ∞

Validation:
Must be non-negative.

Solver:
ElectricalSolver

Status:
Stable

Remarks:
Power leaving the cell.

---

## EPW004

Variable Name:
peak_power

Description:
Maximum observed power.

Unit:
W

Type:
float

Default:
0.0

Range:
0.0 → ∞

Validation:
Must be non-negative.

Solver:
ElectricalSolver

Status:
Stable

Remarks:
Simulation maximum.

---

## EPW005

Variable Name:
average_power

Description:
Average electrical power.

Unit:
W

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

Status:
Stable

Remarks:
Time averaged power.


## ESI001

Variable Name:
soc

Description:
State of Charge.

Unit:
-

Type:
float

Default:
0.0

Range:
0.0 → 1.0

Validation:
Must remain inside limits.

Solver:
ElectricalSolver

Status:
Stable

Remarks:
Normalized charge level.

---

## ESI002

Variable Name:
dod

Description:
Depth of Discharge.

Unit:
-

Type:
float

Default:
0.0

Range:
0.0 → 1.0

Validation:
Must remain inside limits.

Solver:
ElectricalSolver

Status:
Stable

Remarks:
Normalized discharged fraction.

---

## ESI003

Variable Name:
soe

Description:
State of Energy.

Unit:
-

Type:
float

Default:
0.0

Range:
0.0 → 1.0

Validation:
Must remain inside limits.

Solver:
ElectricalSolver

Status:
Stable

Remarks:
Normalized available energy.

---

## ESI004

Variable Name:
soh

Description:
State of Health.

Unit:
-

Type:
float

Default:
1.0

Range:
0.0 → 1.0

Validation:
Must remain inside limits.

Solver:
AgingSolver

Status:
Stable

Remarks:
Remaining health indicator.

---

## ESI005

Variable Name:
sop

Description:
State of Power.

Unit:
-

Type:
float

Default:
1.0

Range:
0.0 → 1.0

Validation:
Must remain inside limits.

Solver:
ElectricalSolver

Status:
Stable

Remarks:
Available power capability.


ERR001
ohmic_resistance

ERR002
contact_resistance

ERR003
electrolyte_resistance

ERR004
electrode_resistance

ERR005
separator_resistance

ERR006
interfacial_resistance

ERR007
film_resistance

ERR008
charge_transfer_resistance

ERR009
diffusion_resistance

ERR010
total_resistance


EPL001
activation_polarization

EPL002
ohmic_polarization

EPL003
concentration_polarization

EPL004
diffusion_polarization

EPL005
reaction_polarization

EPL006
electrolyte_polarization

EPL007
anode_polarization

EPL008
cathode_polarization

EPL009
interfacial_polarization

EPL010
total_polarization


EEF001
coulombic_efficiency

EEF002
energy_efficiency

EEF003
voltage_efficiency

EEF004
power_efficiency

EEF005
charge_efficiency

EEF006
discharge_efficiency

EEF007
round_trip_efficiency

EEF008
conversion_efficiency



ELS001
power_loss

ELS002
energy_loss

ELS003
ohmic_loss

ELS004
activation_loss

ELS005
concentration_loss

ELS006
joule_heating_loss

ELS007
side_reaction_loss

ELS008
leakage_loss

ELS009
parasitic_loss

ELS010
total_loss



EDG001
voltage_drop

EDG002
voltage_ripple

EDG003
current_ripple

EDG004
peak_voltage

EDG005
minimum_voltage

EDG006
maximum_current

EDG007
minimum_current

EDG008
peak_power

EDG009
minimum_power

EDG010
average_power

EDG011
average_voltage

EDG012
average_current

EDG013
electrical_fault

EDG014
short_circuit_detected

EDG015
over_voltage

EDG016
under_voltage

EDG017
over_current

EDG018
reverse_current

EDG019
open_circuit_detected

EDG020
measurement_valid




