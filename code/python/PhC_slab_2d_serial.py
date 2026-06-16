# Import libraries
import time
import numpy as np
import matplotlib.pyplot as plt
import S4
plt.rcParams["font.family"] = "Helvetica"


def R_PhC_slab(omega):
    '''
    Define a function of S4 for calculating the reflectance of 2d PhC slabs.
    args: 
        for the light: lda, wavelength;
        R: reflectance;
    '''
    period = [1, 1]
    S = S4.New(Lattice=((period[0], 0), (0, period[1])), NumBasis=70)
    S.SetMaterial(Name='Air', Epsilon=(1+0j)**2)
    S.SetMaterial(Name='Dielectric', Epsilon=12+0j)

    S.AddLayer(Name='Air_layer', Thickness=0.1, Material='Air')
    S.AddLayer(Name='Dielectric_layer', Thickness=0.5, Material='Dielectric')
    S.SetRegionCircle(
        Layer='Dielectric_layer',
        Material='Air',
        Center=(0, 0),
        Radius=0.1)

    S.AddLayer(Name='Bottom_layer', Thickness=0.1, Material='Air')

    S.SetExcitationPlanewave(
        IncidenceAngles=(0, 0), sAmplitude=1, pAmplitude=0, Order=0)
    S.SetOptions(PolarizationDecomposition=True)
    S.SetFrequency(omega)
    powr1 = S.GetPowerFluxByOrder(Layer='Air_layer', zOffset=0)
    powr2 = S.GetPowerFluxByOrder(Layer='Bottom_layer', zOffset=0)

    R = np.abs(np.real(powr2[0][0])) / np.real(powr1[0][0])

    return R


def main():
    start = time.time()
    omegaSpace = np.linspace(0.25, 0.6, 351)
    RSpace = np.array(list(map(R_PhC_slab, omegaSpace)))
    # data_result = 'Wavelength (um)\tT\n'
    # for omega, R in zip(omegaSpace, RSpace):
    #     data_result_append = f'{omega:.3f}\t{R:.6f}\n'
    #     data_result += data_result_append
    # with open('./data/PhC_T_py_serial.txt', 'w') as f:
    #     f.write(data_result)
    # f.close()

    end = time.time()
    print('Elapsed time is %.4f seconds.' % (end-start))

    fig, ax = plt.subplots()
    ax.plot(omegaSpace, RSpace, color='red', alpha=0.5)
    ax.set_xlim([omegaSpace.min(), omegaSpace.max()]), ax.set_ylim([0, 1])
    ax.set_xlabel(r'Frequency (2$\pi c/a$)'), ax.set_ylabel('Transmission')
    ax.grid(linestyle='--')
    fig.tight_layout()
    plt.show()


if __name__ == '__main__':
    main()
