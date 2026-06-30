Thermal State Specification

Version: 1.0

Status: Stable
Temperature

Temperature Gradient

Heat

Heat Capacity

Heat Generation

Heat Transfer

Thermal Resistance

Thermal Conductivity

Boundary Conditions

Cooling

Heating

Thermal Diagnostics

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

Status:

Remarks:


TV001

Variable Name:
temperature

Description:
Average cell temperature.

Unit:
K

Type:
float

Default:
298.15

Range:
200 → 600

Validation:
Must be positive.

Solver:
ThermalSolver

Industrial Source:
IEC 62660

Scientific Source:
DFN
P2D

Status:
Stable

Remarks:
Primary thermal state.

--------------------------------------------------

TV002

Variable Name:
surface_temperature

Description:
Outer surface temperature.

Unit:
K

Type:
float

Default:
298.15

Range:
200 → 600

Validation:
Must be positive.

Solver:
ThermalSolver

Status:
Stable

Remarks:
Used by cooling models.

--------------------------------------------------

TV003

Variable Name:
core_temperature

Description:
Internal core temperature.

Unit:
K

Type:
float

Default:
298.15

Range:
200 → 600

Validation:
Must be positive.

Solver:
ThermalSolver

Status:
Stable

Remarks:
Maximum internal temperature.

--------------------------------------------------

TV004

Variable Name:
ambient_temperature

Description:
Ambient environment temperature.

Unit:
K

Type:
float

Default:
298.15

Range:
150 → 500

Validation:
Must be positive.

Solver:
EnvironmentSolver

Status:
Stable

Remarks:
External temperature.

--------------------------------------------------

TV005

Variable Name:
reference_temperature

Description:
Reference temperature.

Unit:
K

Type:
float

Default:
298.15

Range:
Positive

Validation:
Positive.

Solver:
ThermalSolver

Status:
Stable

Remarks:
Reference operating temperature.

--------------------------------------------------

TV006

Variable Name:
delta_temperature

Description:
Characteristic temperature difference used by the thermal model.

Unit:
K

Type:
float

Default:
0.0

Range:
No fixed limit

Validation:
Finite number.

Solver:
ThermalSolver

Industrial Source:
Battery Thermal Management Systems

Scientific Source:
DFN
P2D
Thermal Modeling

Status:
Stable

Remarks:
Computed by the active thermal model.
Typical examples include:
• core_temperature - surface_temperature
• maximum_temperature - minimum_temperature
• temperature - ambient_temperature


TG001
temperature_gradient

TG002
gradient_x

TG003
gradient_y

TG004
gradient_z

TG005
maximum_gradient


TH001
heat

TH002
internal_heat

TH003
stored_heat

TH004
released_heat


TC001
heat_capacity

TC002
specific_heat

TC003
effective_heat_capacity

TC004
volumetric_heat_capacity

HG001
heat_generation

HG002
joule_heat

HG003
reaction_heat

HG004
entropic_heat

HG005
irreversible_heat

HG006
reversible_heat

HG007
side_reaction_heat

HG008
total_heat_generation


HT001
conduction_heat

HT002
convection_heat

HT003
radiation_heat

HT004
heat_flux

HT005
heat_transfer_rate


TR001
thermal_resistance

TR002
contact_thermal_resistance

TR003
interface_thermal_resistance

TR004
total_thermal_resistance


TK001
thermal_conductivity

TK002
effective_thermal_conductivity

TK003
conductivity_x

TK004
conductivity_y

TK005
conductivity_z


TB001
boundary_temperature

TB002
boundary_heat_flux

TB003
boundary_convection

TB004
boundary_radiation


CL001
cooling_power

CL002
cooling_rate

CL003
coolant_temperature

CL004
coolant_flow_rate

CL005
cooling_efficiency


HTR001
heater_power

HTR002
heater_efficiency

HTR003
heater_enabled


TD001
maximum_temperature

TD002
minimum_temperature

TD003
average_temperature

TD004
temperature_uniformity

TD005
thermal_runaway_detected

TD006
over_temperature

TD007
under_temperature

TD008
thermal_warning

TD009
thermal_fault

TD010
measurement_valid


