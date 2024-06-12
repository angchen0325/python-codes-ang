# Import libraries
import time
from mpi4py import MPI
import numpy as np
import matplotlib.pyplot as plt
import S4

plt.rcParams["font.family"] = "Helvetica"


def R_PhC_slab(omega):
    """
    Define a function of S4 for calculating the reflectance of 2d PhC slabs.
    args:
        for the light: lda, wavelength;
        R: reflectance;
    """
    period = [1, 1]
    S = S4.New(Lattice=((period[0], 0), (0, period[1])), NumBasis=70)
    S.SetMaterial(Name="Air", Epsilon=(1 + 0j) ** 2)
    S.SetMaterial(Name="Dielectric", Epsilon=12 + 0j)

    S.AddLayer(Name="Air_layer", Thickness=0.1, Material="Air")
    S.AddLayer(Name="Dielectric_layer", Thickness=0.5, Material="Dielectric")
    S.SetRegionCircle(
        Layer="Dielectric_layer", Material="Air", Center=(0, 0), Radius=0.1
    )

    S.AddLayer(Name="Bottom_layer", Thickness=0.1, Material="Air")

    S.SetExcitationPlanewave(
        IncidenceAngles=(0, 0), sAmplitude=1, pAmplitude=0, Order=0
    )
    S.SetOptions(PolarizationDecomposition=True)
    S.SetFrequency(omega)
    powr1 = S.GetPowerFluxByOrder(Layer="Air_layer", zOffset=0)
    powr2 = S.GetPowerFluxByOrder(Layer="Bottom_layer", zOffset=0)

    R = np.abs(np.real(powr2[0][0])) / np.real(powr1[0][0])

    return R


def main():
    start = time.time()

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    start_omega = 0.251
    end_omega = 0.600
    num = 350
    omegaSpace = np.linspace(start_omega, end_omega, num=num)

    chunk_size = len(omegaSpace) // size
    chunk_extra = len(omegaSpace) % size

    if rank < chunk_extra:
        start = rank * (chunk_size + 1)
        end = start + chunk_size + 1
    else:
        start = rank * chunk_size + chunk_extra
        end = start + chunk_size
    local_omegas = omegaSpace[start:end]

    local_Rs = np.array([R_PhC_slab(omega) for omega in local_omegas])

    all_Rs = ""
    if rank == 0:
        all_Rs = np.empty(num, dtype=float)
    comm.Gather(local_Rs, all_Rs, root=0)
    
    all_Rs = np.array(all_Rs)


    data_result = "Wavelength (um)\tT\n"
    for omega, R in zip(omegaSpace, all_Rs):
        data_result_append = f"{omega:.3f}\t{R:.6f}\n"
        data_result += data_result_append

    with open("./data/PhC_T_py_mpi.txt", "w") as f:
        f.write(data_result)
    f.close()

    end = time.time()
    print(f"Elapsed time is {(end-start):.4f} seconds.")

    fig, ax = plt.subplots()
    ax.plot(omegaSpace, all_Rs, color="red", alpha=0.5)
    ax.set_xlim([omegaSpace.min(), omegaSpace.max()]), ax.set_ylim([0, 1])
    ax.set_xlabel("Frequency (2$\pi c/a$)"), ax.set_ylabel("Transmission")
    ax.grid(linestyle="--")
    fig.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
