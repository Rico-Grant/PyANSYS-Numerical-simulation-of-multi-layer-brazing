# geometry.py

def build_geometry(mapdl, params):
    L_half = params["L_half"]
    H_cc = params["H_cc"]
    H_agcuti = params["H_agcuti"]
    H_w = params["H_w"]
    H_ss = params["H_ss"]

    t_refine_cc = min(0.2, 0.3 * H_cc)
    t_refine_ss = min(0.2, 0.3 * H_ss)

    y0 = 0.0
    y1a = y0 + (H_cc - t_refine_cc)
    y1 = y0 + H_cc
    y2 = y1 + H_agcuti
    y3 = y2 + H_w
    y4 = y3 + H_agcuti
    y4b = y4 + t_refine_ss
    y5 = y4 + H_ss

    y_levels = [y0, y1a, y1, y2, y3, y4, y4b, y5]

    kp_left = []
    kp_right = []

    for yy in y_levels:
        kp_left.append(mapdl.k("", 0.0, yy, 0.0))
        kp_right.append(mapdl.k("", L_half, yy, 0.0))

    mapdl.allsel()

    left_lines = []
    right_lines = []
    for i in range(len(y_levels) - 1):
        left_lines.append(mapdl.l(kp_left[i], kp_left[i + 1]))
        right_lines.append(mapdl.l(kp_right[i], kp_right[i + 1]))

    h_lines = []
    for i in range(len(y_levels)):
        h_lines.append(mapdl.l(kp_left[i], kp_right[i]))

    mapdl.allsel()

    for i in range(len(y_levels) - 1):
        mapdl.al(left_lines[i], h_lines[i + 1], right_lines[i], h_lines[i])

    mapdl.allsel()
    mapdl.numcmp("ALL")
    mapdl.allsel()

    geo = {
        "y0": y0, "y1a": y1a, "y1": y1, "y2": y2, "y3": y3,
        "y4": y4, "y4b": y4b, "y5": y5,
        "y_levels": y_levels,
        "left_lines": left_lines,
        "right_lines": right_lines,
        "h_lines": h_lines,
    }
    return geo