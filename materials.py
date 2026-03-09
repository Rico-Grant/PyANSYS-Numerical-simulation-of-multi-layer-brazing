# materials.py

def clear_mptemp(mapdl):
    mapdl.run("MPTEMP,,,,,,,,")
    mapdl.run("MPTEMP,1,0")


def define_materials(mapdl, params):
    mat_cc = params["mat_cc"]
    mat_agcuti = params["mat_agcuti"]
    mat_w = params["mat_w"]
    mat_ss = params["mat_ss"]

    # =========================
    # C/C
    # =========================
    clear_mptemp(mapdl)

    temps_cc = [293.0, 493.0, 693.0, 893.0, 1123.0]
    alpha_cc = [0.45e-6, 0.55e-6, 0.82e-6, 1.05e-6, 1.20e-6]
    E_cc = 64.5e3
    nu_cc = 0.25

    mapdl.mp("EX", mat_cc, E_cc)
    mapdl.mp("EY", mat_cc, E_cc)
    mapdl.mp("PRXY", mat_cc, nu_cc)

    mapdl.mptemp(1, *temps_cc)
    mapdl.mpdata("ALPX", mat_cc, 1, *alpha_cc)
    mapdl.mpdata("ALPY", mat_cc, 1, *alpha_cc)

    # =========================
    # AgCuTi
    # =========================
    clear_mptemp(mapdl)

    temps_agcuti = [293.0, 493.0, 693.0, 893.0, 1073.0]
    alpha_agcuti = [19.00e-6, 19.70e-6, 20.20e-6, 20.50e-6, 21.00e-6]
    ex_agcuti = [100e3, 90e3, 80e3, 67e3, 58e3]
    sigy_agcuti = [230.0, 170.0, 98.0, 25.0, 20.0]
    et_agcuti = [0.01 * e for e in ex_agcuti]

    mapdl.mp("PRXY", mat_agcuti, 0.36)
    mapdl.mptemp(1, *temps_agcuti)
    mapdl.mpdata("EX", mat_agcuti, 1, *ex_agcuti)
    mapdl.mpdata("EY", mat_agcuti, 1, *ex_agcuti)
    mapdl.mpdata("ALPX", mat_agcuti, 1, *alpha_agcuti)
    mapdl.mpdata("ALPY", mat_agcuti, 1, *alpha_agcuti)

    mapdl.run(f"TB,BISO,{mat_agcuti},,,TEMP")
    for T, sy, et in zip(temps_agcuti, sigy_agcuti, et_agcuti):
        mapdl.run(f"TBTEMP,{T}")
        mapdl.run(f"TBDATA,1,{sy},{et}")

    # =========================
    # W
    # =========================
    clear_mptemp(mapdl)

    temps_w = [293.0, 773.0, 1273.0, 1773.0]
    ex_w = [411e3, 390e3, 365e3, 335e3]
    alpha_w = [4.5e-6, 4.8e-6, 5.1e-6, 5.3e-6]
    sigy_w = [550.0, 450.0, 320.0, 220.0]
    et_w = [3000.0, 2600.0, 2200.0, 1800.0]

    mapdl.mp("PRXY", mat_w, 0.28)
    mapdl.mptemp(1, *temps_w)
    mapdl.mpdata("EX", mat_w, 1, *ex_w)
    mapdl.mpdata("EY", mat_w, 1, *ex_w)
    mapdl.mpdata("ALPX", mat_w, 1, *alpha_w)
    mapdl.mpdata("ALPY", mat_w, 1, *alpha_w)

    mapdl.run(f"TB,BISO,{mat_w},,,TEMP")
    for T, sy, et in zip(temps_w, sigy_w, et_w):
        mapdl.run(f"TBTEMP,{T}")
        mapdl.run(f"TBDATA,1,{sy},{et}")

    # =========================
    # 304SS
    # =========================
    clear_mptemp(mapdl)

    temps_ss = [293.15, 473.15, 673.15, 873.15, 1073.15, 1273.15]
    alpha_ss = [17.00e-6, 18.00e-6, 19.10e-6, 19.60e-6, 20.20e-6, 20.50e-6]
    ex_ss = [198e3, 185e3, 167e3, 159e3, 151e3, 101e3]
    sigy_ss = [206.0, 186.0, 155.0, 149.0, 91.0, 54.0]
    et_ss = [0.01 * e for e in ex_ss]

    mapdl.mp("PRXY", mat_ss, 0.31)
    mapdl.mptemp(1, *temps_ss)
    mapdl.mpdata("EX", mat_ss, 1, *ex_ss)
    mapdl.mpdata("EY", mat_ss, 1, *ex_ss)
    mapdl.mpdata("ALPX", mat_ss, 1, *alpha_ss)
    mapdl.mpdata("ALPY", mat_ss, 1, *alpha_ss)

    mapdl.run(f"TB,BISO,{mat_ss},,,TEMP")
    for T, sy, et in zip(temps_ss, sigy_ss, et_ss):
        mapdl.run(f"TBTEMP,{T}")
        mapdl.run(f"TBDATA,1,{sy},{et}")