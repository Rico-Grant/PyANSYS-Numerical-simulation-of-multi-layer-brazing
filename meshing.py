# meshing.py

def assign_materials_to_areas(mapdl, params, geo):
    mat_cc = params["mat_cc"]
    mat_agcuti = params["mat_agcuti"]
    mat_w = params["mat_w"]
    mat_ss = params["mat_ss"]
    real_const = params["real_const"]
    elem_type = params["elem_type"]

    y0 = geo["y0"]
    y1 = geo["y1"]
    y2 = geo["y2"]
    y3 = geo["y3"]
    y4 = geo["y4"]
    y5 = geo["y5"]

    mapdl.asel("S", "LOC", "Y", y0, y1)
    mapdl.aatt(mat_cc, real_const, elem_type, 0)

    mapdl.asel("S", "LOC", "Y", y1, y2)
    mapdl.aatt(mat_agcuti, real_const, elem_type, 0)

    mapdl.asel("S", "LOC", "Y", y2, y3)
    mapdl.aatt(mat_w, real_const, elem_type, 0)

    mapdl.asel("S", "LOC", "Y", y3, y4)
    mapdl.aatt(mat_agcuti, real_const, elem_type, 0)

    mapdl.asel("S", "LOC", "Y", y4, y5)
    mapdl.aatt(mat_ss, real_const, elem_type, 0)

    mapdl.allsel()


def mesh_model(mapdl, params, geo):
    nx = params["nx"]
    ny_cc_bulk = params["ny_cc_bulk"]
    ny_cc_near = params["ny_cc_near"]
    ny_ag1 = params["ny_ag1"]
    ny_w = params["ny_w"]
    ny_ag2 = params["ny_ag2"]
    ny_ss_near = params["ny_ss_near"]
    ny_ss_bulk = params["ny_ss_bulk"]

    h_lines = geo["h_lines"]
    left_lines = geo["left_lines"]
    right_lines = geo["right_lines"]

    mapdl.allsel()
    for ln in h_lines:
        mapdl.lsel("S", "LINE", "", ln)
        mapdl.lesize("ALL", "", "", nx)

    ndiv_y = [
        ny_cc_bulk,
        ny_cc_near,
        ny_ag1,
        ny_w,
        ny_ag2,
        ny_ss_near,
        ny_ss_bulk
    ]

    for i, nd in enumerate(ndiv_y):
        mapdl.lsel("S", "LINE", "", left_lines[i])
        mapdl.lsel("A", "LINE", "", right_lines[i])
        mapdl.lesize("ALL", "", "", nd)

    mapdl.allsel()
    mapdl.mshape(0, "2D")
    mapdl.mshkey(1)
    mapdl.amesh("ALL")
    mapdl.nummrg("NODE")
    mapdl.allsel()