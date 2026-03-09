# metrics.py

import numpy as np

def evaluate_metrics(df_mid, params):
    H_cc = params["H_cc"]
    H_agcuti = params["H_agcuti"]
    H_w = params["H_w"]
    H_ss = params["H_ss"]

    if len(df_mid) == 0:
        return {
            "H_w_mm": H_w,
            "W_S1_max": np.nan,
            "W_SEQV_max": np.nan,
            "Global_SEQV_max": np.nan,
        }

    y = df_mid["y_mm"].values
    s1 = df_mid["S1_MPa"].values
    seqv = df_mid["SEQV_MPa"].values

    y1 = H_cc
    y2 = y1 + H_agcuti
    y3 = y2 + H_w
    y4 = y3 + H_agcuti
    y5 = y4 + H_ss

    mask_w = (y >= y2) & (y <= y3)

    return {
        "H_w_mm": H_w,
        "W_S1_max": np.nanmax(s1[mask_w]) if np.any(mask_w) else np.nan,
        "W_SEQV_max": np.nanmax(seqv[mask_w]) if np.any(mask_w) else np.nan,
        "Global_SEQV_max": np.nanmax(seqv),
    }