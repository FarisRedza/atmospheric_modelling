from libradtran import *

# qrackling repod test
sim = Simulation(
    atmosphere_file=Atmosphere.MIDLATTITUDESUMMER,
    source=Source.SOLAR,
    wavelength_min=500,
    wavelength_max=1600,
    albedo=0.02,
    rte_solver=RTE_Solver.MYSTIC,
    mc_photons=(1000),
    mc_polarisation=MC_Polarisation.ZERO,
    mc_backward=None,
    mc_backward_output=(MC_Backward_Output.EDN, None),
    mc_basename=pathlib.Path(cwd + '/mystic'),
    mc_vroom=True,
    mc_rad_alpha=1,
    umu=-1, #OutputPolarAngles
    solar_zenith_angle=0,
    zout=1, #OutputAltitudes
    time='2025 3 14 13 29 49.58',
    latitude='N 56.405',
    longitude='W 3.183',
    output_user='edir edn eglo enet esum eup lambda uu zout',
    output_quantity=Output_Quantity.REFLECTIVITY,
    output_process=Output_Process.PER_NM,
    output_file=pathlib.Path('/home/faris/Downloads/output.txt'),
    output_format=Output_Format.ASCII,
    mol_abs_param_ck_scheme=Mol_Abs_Param_CK_Scheme.REPTRAN,
    mol_abs_param_ck_reptran_arg='coarse',
    crs_model_mol_id=CRS_Model_Mol_ID.RAYLEIGH,
    crs_model_crs_model=CRS_Model_CRS_Model.BODHAINE,
    mol_modify=[
        Moltype.O3, 200, 'DU',
        Moltype.H2O, 20, 'MM'
    ],
    aerosol_season=Aerosol_Season.SPRING_SUMMER,
    aerosol_default=True,
    aerosol_visibility=50,
    aerosol_species_file=Aerosol_Species_File.MARITIME_POLLUTED
)