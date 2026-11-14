"""Python re-implementation of the nc_tfet_n / nc_tfet_p DC equations.

Reproduces the output characteristics (Id-Vds) without needing Cadence,
as a quick sanity check of the Verilog-A models.

Usage:  python scripts/plot_iv.py
Output: results/python_iv_check.png
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

Q = 1.602176634e-19
EPS0 = 8.8541878128e-12


def tfet_current(vgs, vds, A_BTBT, W=1e-6, TSI=10e-9, TOX=1e-9, LTUN=3e-9,
                 LCH=10e-9, EPS_SI=11.7, EPS_OX=3.9, CFE0=-0.01,
                 FE_NONLIN=1e-3, B_BTBT=2e7, P=2.0, VFB=0.0,
                 A_SDT=1e-9, B_SDT=1e9):
    """Magnitude of drain current for n-type conventions (vgs, vds >= 0)."""
    cox = EPS_OX * EPS0 / TOX
    csi = EPS_SI * EPS0 / TSI
    cbase = cox * csi / (cox + csi)
    cfe = CFE0 / (1.0 + FE_NONLIN * np.abs(vgs))
    vg_int = vgs / (1.0 + cbase / cfe)
    phi_s = np.maximum(vg_int - VFB, 0.0)
    e_tun = np.maximum(phi_s / LTUN, 1.0)
    r_btbt = A_BTBT * e_tun ** P * np.exp(-B_BTBT / e_tun)
    i_btbt = Q * W * LTUN * TSI * r_btbt
    i_sdt = A_SDT * W * np.exp(-B_SDT * LCH) * np.abs(vds)
    return i_btbt * np.tanh(vds / 0.1) + i_sdt


def main():
    vds = np.linspace(0, 1, 201)
    vgs_list = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))

    for vgs in vgs_list:
        axes[0].plot(vds, tfet_current(vgs, vds, 1.0e19) * 1e6,
                     label=f"Vgs={vgs:.1f} V")
        axes[1].plot(vds, -tfet_current(vgs, vds, 1.8e19) * 1e6,
                     label=f"|Vgs|={vgs:.1f} V")

    axes[0].set_title("nc_tfet_n  (A_BTBT = 1.0e19)")
    axes[1].set_title("nc_tfet_p  (A_BTBT = 1.8e19)")
    for ax in axes:
        ax.set_xlabel("|Vds| (V)")
        ax.set_ylabel("Id (uA)")
        ax.grid(True, alpha=0.3)
        ax.legend()

    os.makedirs("results", exist_ok=True)
    fig.tight_layout()
    fig.savefig("results/python_iv_check.png", dpi=150)
    print("n-type Id @ Vgs=1V, Vds=1V : %.1f uA" %
          (tfet_current(1.0, 1.0, 1.0e19) * 1e6))
    print("p-type |Id| @ |Vgs|=1V, |Vds|=1V : %.1f uA" %
          (tfet_current(1.0, 1.0, 1.8e19) * 1e6))
    print("saved results/python_iv_check.png")


if __name__ == "__main__":
    main()
