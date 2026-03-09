# solver.py

def setup_element_type(mapdl, params):
    elem_type = params["elem_type"]
    mapdl.et(elem_type, "PLANE183")
    mapdl.keyopt(elem_type, 3, 2)   # plane strain


def solve_model(mapdl, params):
    T_zero_stress = params["T_zero_stress"]
    T_room = params["T_room"]

    mapdl.slashsolu()
    mapdl.antype("STATIC")
    mapdl.outres("ALL", "ALL")
    mapdl.tref(T_zero_stress)
    mapdl.tunif(T_room)
    mapdl.time(1)
    out = mapdl.solve()
    print(out)
    mapdl.finish()