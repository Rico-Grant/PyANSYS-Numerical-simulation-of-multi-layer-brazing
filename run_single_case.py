# run_single_case.py

import os
from copy import deepcopy

from config import DEFAULT_PARAMS
from materials import define_materials
from geometry import build_geometry
from meshing import assign_materials_to_areas, mesh_model
from boundary_conditions import apply_boundary_conditions
from Python.ThermalStress_iter.solver import setup_element_type, solve_model
from postprocess import extract_midline_stress, save_midline_outputs
from metrics import evaluate_metrics


def run_single_case(mapdl, user_params=None, outdir="results/single_case"):
    params = deepcopy(DEFAULT_PARAMS)
    if user_params is not None:
        params.update(user_params)

    os.makedirs(outdir, exist_ok=True)

    mapdl.clear()
    mapdl.prep7()

    setup_element_type(mapdl, params)
    define_materials(mapdl, params)

    geo = build_geometry(mapdl, params)
    assign_materials_to_areas(mapdl, params, geo)
    mesh_model(mapdl, params, geo)

    apply_boundary_conditions(mapdl)
    solve_model(mapdl, params)

    df_mid = extract_midline_stress(mapdl, params)
    x_mid = 0.5 * params["L_half"]
    save_midline_outputs(df_mid, outdir, x_mid)

    metrics = evaluate_metrics(df_mid, params)

    return {
        "params": params,
        "geo": geo,
        "df_mid": df_mid,
        "metrics": metrics,
    }