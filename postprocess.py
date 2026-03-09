# postprocess.py

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def extract_midline_stress(mapdl, params):
    L_half = params["L_half"]

    mapdl.post1()
    mapdl.set("LAST")

    x_mid = 0.5 * L_half
    tol = max(L_half, 1.0) * 1e-6

    nodes = np.array(mapdl.mesh.nodes)
    nnum = np.array(mapdl.mesh.nnum)

    mask = np.isclose(nodes[:, 0], x_mid, atol=tol)
    mid_nodes = nnum[mask]
    mid_coords = nodes[mask]

    if len(mid_nodes) == 0:
        print(f"WARNING: 没有找到位于 x = {x_mid:.6f} 附近的节点。")
        return pd.DataFrame(columns=["node", "x_mm", "y_mm", "S1_MPa", "SEQV_MPa"])

    order = np.argsort(mid_coords[:, 1])
    mid_nodes = mid_nodes[order]
    mid_coords = mid_coords[order]
    y_path = mid_coords[:, 1]

    s1_vals = np.full(len(mid_nodes), np.nan)
    seqv_vals = np.full(len(mid_nodes), np.nan)

    try:
        result = mapdl.result
        p_nnum, p_data = result.principal_nodal_stress(0)
        p_dict = {int(nd): vals for nd, vals in zip(np.asarray(p_nnum).ravel(), np.asarray(p_data))}

        for i, nd in enumerate(mid_nodes):
            if int(nd) in p_dict:
                vals = np.asarray(p_dict[int(nd)]).ravel()
                if len(vals) >= 1:
                    s1_vals[i] = vals[0]
                if len(vals) >= 5:
                    seqv_vals[i] = vals[-1]
    except Exception as e:
        print("result.principal_nodal_stress failed:", e)

    if np.all(np.isnan(seqv_vals)):
        try:
            all_seqv = np.asarray(mapdl.post_processing.nodal_eqv_stress()).ravel()
            if len(all_seqv) == len(nnum):
                seqv_dict = {int(nd): val for nd, val in zip(nnum, all_seqv)}
                for i, nd in enumerate(mid_nodes):
                    if int(nd) in seqv_dict:
                        seqv_vals[i] = seqv_dict[int(nd)]
        except Exception as e:
            print("post_processing.nodal_eqv_stress failed:", e)

    if np.all(np.isnan(s1_vals)):
        try:
            all_s1 = np.asarray(mapdl.post_processing.nodal_principal_stress("1")).ravel()
            if len(all_s1) == len(nnum):
                s1_dict = {int(nd): val for nd, val in zip(nnum, all_s1)}
                for i, nd in enumerate(mid_nodes):
                    if int(nd) in s1_dict:
                        s1_vals[i] = s1_dict[int(nd)]
        except Exception as e:
            print("post_processing.nodal_principal_stress failed:", e)

    valid_mask = ~(np.isnan(s1_vals) & np.isnan(seqv_vals))

    df_mid = pd.DataFrame({
        "node": mid_nodes[valid_mask],
        "x_mm": mid_coords[:, 0][valid_mask],
        "y_mm": y_path[valid_mask],
        "S1_MPa": s1_vals[valid_mask],
        "SEQV_MPa": seqv_vals[valid_mask],
    })

    return df_mid


def save_midline_outputs(df_mid, outdir, x_mid):
    os.makedirs(outdir, exist_ok=True)

    csv_path = os.path.join(outdir, "midline_stress.csv")
    df_mid.to_csv(csv_path, index=False, encoding="utf-8-sig")

    if len(df_mid) == 0:
        print("WARNING: 中线路径没有可用应力数据，未生成图。")
        return

    plt.figure(figsize=(7, 5))
    plt.plot(df_mid["y_mm"], df_mid["S1_MPa"], "r-o", ms=3, lw=1.8, label="S1")
    plt.xlabel("Distance along Y (mm)")
    plt.ylabel("Stress (MPa)")
    plt.title(f"Maximum principal stress along x = {x_mid:.4f} mm")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(outdir, "midline_S1.png"), dpi=300)
    plt.close()

    plt.figure(figsize=(7, 5))
    plt.plot(df_mid["y_mm"], df_mid["SEQV_MPa"], "b-s", ms=3, lw=1.8, label="SEQV")
    plt.xlabel("Distance along Y (mm)")
    plt.ylabel("Stress (MPa)")
    plt.title(f"von Mises stress along x = {x_mid:.4f} mm")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(outdir, "midline_SEQV.png"), dpi=300)
    plt.close()

    plt.figure(figsize=(7, 5))
    plt.plot(df_mid["y_mm"], df_mid["S1_MPa"], "r-o", ms=3, lw=1.8, label="S1")
    plt.plot(df_mid["y_mm"], df_mid["SEQV_MPa"], "b--s", ms=3, lw=1.8, label="SEQV")
    plt.xlabel("Distance along Y (mm)")
    plt.ylabel("Stress (MPa)")
    plt.title(f"Stress variation along x = {x_mid:.4f} mm")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(outdir, "midline_stress_compare.png"), dpi=300)
    plt.close()