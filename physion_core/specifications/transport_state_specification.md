Transport State Specification
Version: 1.0

Status: Stable

Purpose

Defines every transport-related variable owned by TransportState.

TransportState owns ONLY transport state variables.

Material properties belong to ChemistryState.

Heat transport belongs to ThermalState.

Electrical quantities belong to ElectricalState.

Only TransportSolver may modify these variables.

----------------------------------------------------------

Categories

Species Flux

Mass Flux

Diffusion Flux

Migration Flux

Convection Flux

Transport Rates

Transport Diagnostics

----------------------------------------------------------

Variable Template

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
TF001 lithium_flux

TF002 electrolyte_flux

TF003 solvent_flux

TF004 salt_flux
TM001 mass_flux

TM002 mass_flux_anode

TM003 mass_flux_cathode

TM004 mass_flux_separator

TD001 diffusion_flux

TD002 diffusion_flux_anode

TD003 diffusion_flux_cathode

TD004 effective_diffusion_flux

TG001 migration_flux

TG002 ionic_migration_flux

TG003 electronic_migration_flux

TC001 convection_flux

TC002 electrolyte_convection

TC003 solvent_convection

TR001 transport_rate

TR002 diffusion_rate

TR003 migration_rate

TR004 convection_rate

DG001 transport_limitation

DG002 diffusion_limitation

DG003 migration_limitation

DG004 convection_limitation

DG005 transport_balance

DG006 transport_warning

DG007 transport_fault

DG008 measurement_valid

DG009 convergence_flag

