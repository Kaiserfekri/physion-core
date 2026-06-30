Chemistry State Specification
Version: 1.0
Status: Stable

Purpose

Defines every electrochemical variable owned by ChemistryState.

Only ChemistrySolver may modify these variables.

ChemistryState owns all chemistry variables exclusively.

----------------------------------------------------------

Categories

Species Concentration
Lithium Inventory
Stoichiometry
Electrolyte
Solid Phase
Diffusion
Reaction
Exchange Current
Charge Transfer
Thermodynamics
Kinetics
Transport
SEI
Lithium Plating
Side Reactions
Electrochemical Diagnostics

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


CS001 concentration_li
CS002 concentration_li_plus
CS003 concentration_electrolyte
CS004 concentration_anode
CS005 concentration_cathode
CS006 concentration_surface
CS007 concentration_bulk
CS008 concentration_average


LI001 lithium_inventory
LI002 lithium_inventory_loss
LI003 cyclable_lithium
LI004 trapped_lithium
LI005 active_lithium
LI006 inactive_lithium


ST001 stoichiometry_anode
ST002 stoichiometry_cathode
ST003 average_stoichiometry
ST004 stoichiometry_surface
ST005 stoichiometry_bulk


EL001 electrolyte_concentration
EL002 electrolyte_potential
EL003 electrolyte_activity
EL004 electrolyte_conductivity
EL005 electrolyte_diffusivity
EL006 electrolyte_porosity
EL007 electrolyte_tortuosity
EL008 electrolyte_temperature
EL009 electrolyte_viscosity
EL010 electrolyte_density
EL011 transference_number
EL012 activity_coefficient


SP001 solid_potential
SP002 solid_concentration
SP003 solid_diffusivity
SP004 solid_conductivity
SP005 particle_surface_concentration
SP006 particle_average_concentration
SP007 active_material_fraction
SP008 active_surface_area
SP009 particle_radius


DF001 diffusion_flux
DF002 lithium_flux
DF003 electrolyte_flux
DF004 solid_flux
DF005 diffusion_coefficient
DF006 effective_diffusion
DF007 diffusion_overpotential
DF008 diffusion_length
DF009 effective_diffusion_length


RC001 reaction_rate
RC002 reaction_current
RC003 reaction_area
RC004 reaction_extent
RC005 reaction_progress
RC006 faradaic_current


EX001 exchange_current_density
EX002 exchange_current
EX003 effective_exchange_current


CT001 charge_transfer_rate
CT002 charge_transfer_resistance
CT003 transfer_coefficient_anode
CT004 transfer_coefficient_cathode
CT005 charge_transfer_overpotential


TH001 gibbs_free_energy
TH002 entropy
TH003 enthalpy
TH004 chemical_potential
TH005 electrochemical_potential


KN001 butler_volmer_rate
KN002 tafel_slope
KN003 reaction_constant
KN004 activation_energy
KN005 kinetic_factor
KN006 reaction_order
KN007 symmetry_factor


TR001 ionic_conductivity
TR002 ionic_mobility
TR003 ionic_flux
TR004 transport_number
TR005 migration_flux
TR006 convection_flux


SEI001 sei_thickness
SEI002 sei_growth_rate
SEI003 sei_resistance
SEI004 sei_porosity
SEI005 sei_conductivity
SEI006 sei_lithium_consumption
SEI007 sei_volume
SEI008 sei_mass
SEI009 sei_growth_mode
SEI010 sei_effective_diffusivity


LP001 plating_rate
LP002 stripped_lithium
LP003 plated_lithium
LP004 plating_current
LP005 plating_thickness
LP006 plating_fraction
LP007 stripping_efficiency
LP008 dead_lithium


SR001 side_reaction_rate
SR002 side_reaction_current
SR003 gas_generation
SR004 gas_pressure
SR005 electrolyte_decomposition
SR006 solvent_consumption
SR007 salt_consumption
SR008 solvent_decomposition_rate
SR009 side_reaction_heat


DG001 reaction_uniformity
DG002 diffusion_limitation
DG003 concentration_limitation
DG004 lithium_balance
DG005 charge_balance
DG006 mass_balance
DG007 chemistry_warning
DG008 chemistry_fault
DG009 convergence_flag
DG010 measurement_valid
DG011 solver_iterations
DG012 residual_norm
DG013 convergence_residual


