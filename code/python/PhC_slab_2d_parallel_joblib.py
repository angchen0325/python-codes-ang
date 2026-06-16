# Import libraries
import time
import os

import numpy as np
import matplotlib.pyplot as plt
from joblib import Parallel, delayed  
import S4 

plt.rcParams["font.family"] = "Helvetica"


def R_PhC_slab(omega):
    """
    Define a function of S4 for calculating the reflectance of 2d PhC slabs.
    """
    period = [1, 1]
    S = S4.New(Lattice=((period[0], 0), (0, period[1])), NumBasis=70)
    S.SetMaterial(Name='Air', Epsilon=(1 + 0j) ** 2)
    S.SetMaterial(Name='Dielectric', Epsilon=12 + 0j)

    S.AddLayer(Name='Air_layer', Thickness=0.1, Material='Air')
    S.AddLayer(Name='Dielectric_layer', Thickness=0.5, Material='Dielectric')
    S.SetRegionCircle(
        Layer='Dielectric_layer',
        Material='Air',
        Center=(0, 0),
        Radius=0.1
    )
    S.AddLayer(Name='Bottom_layer', Thickness=0.1, Material='Air')

    S.SetExcitationPlanewave(
        IncidenceAngles=(0, 0), sAmplitude=1, pAmplitude=0, Order=0
    )
    S.SetOptions(PolarizationDecomposition=True)
    S.SetFrequency(omega)

    powr1 = S.GetPowerFluxByOrder(Layer='Air_layer', zOffset=0)
    powr2 = S.GetPowerFluxByOrder(Layer='Bottom_layer', zOffset=0)

    R = np.abs(np.real(powr2[0][0])) / np.real(powr1[0][0])
    return R


def main():
    start = time.time()
    omegaSpace = np.linspace(0.25, 0.6, num=351)

    n_jobs = os.cpu_count()  
    print(f"Running with {n_jobs} parallel workers...")

    # backend: "loky" is much faster than "threading"
    RSpace = Parallel(n_jobs=n_jobs, backend="loky")(
        delayed(R_PhC_slab)(omega) for omega in omegaSpace
    )

    end = time.time()
    print(f"Elapsed time is {(end - start):.4f} seconds.")

    RSpace = np.array(RSpace)
    fig, ax = plt.subplots()
    ax.plot(omegaSpace, RSpace, color="red", alpha=0.5)
    ax.set_xlim([omegaSpace.min(), omegaSpace.max()])
    ax.set_ylim([0, 1])
    ax.set_xlabel(r"Frequency (2$\pi c/a$)")
    ax.set_ylabel("Transmission")
    ax.grid(linestyle="--")
    fig.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()