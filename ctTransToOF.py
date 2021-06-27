def sutherland(x, As, Ts):
    return As*x**(3/2)/(Ts+x)

def header():
    head = '/*--------------------------------*- C++ -*----------------------------------*\\ \n  =========                 |\n  \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox\n   \\\\    /   O peration     | Website:  https://openfoam.org\n    \\\\  /    A nd           | Version:  6\n     \\\\/     M anipulation  |\n\\*---------------------------------------------------------------------------*/\nFoamFile\n{\n    version     2.0;\n    format      ascii;\n    class       dictionary;\n    location    "chemkin";\n    object      transportProperties;\n}\n// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //\n'
    return head

def get_transport_texts(mech):
    Data = []
    texts = []

    gas = ct.Solution('./mechanism/' + mech)

    list_species = gas.species_names

    Temp = np.arange(200,2501,1)
    texts.append([header()])
    for species in list_species:
        print('Species = ',species)
        print('Species_Index = ',gas.species_index(species))
        gas.X = '{}:1'.format(species)
        muy = [] ## dynamic viscosity (Pa-s)

        for temp in Temp:
            gas.TP = temp, ct.one_atm
            muy.append(gas.viscosity)

        popt, pcov = curve_fit(sutherland, Temp, muy)
        string = '\"{0}\"\n{1}\n    transport\n    {2}\n        As {3};\n        Ts {4};\n    {5}\n{6}\n'.format(species,'{', '{', popt[0], popt[1], '}', '}')
        print('As = ', popt[0],'\n', 'Ts = ', popt[1])
        print('#######################################')
        Data.append([popt[0], popt[1]])
        texts.append([string])
    texts.append(['// ************************************************************************* //'])
    return texts

if __name__ == '__main__':

    import cantera as ct
    import numpy as np
    from scipy.optimize import curve_fit

    mech = 'jws-kin_therm.cti'

    texts = get_transport_texts(mech)
    np.savetxt('./mechanism/' + mech.split('.')[0] + '.dat', texts, fmt="%s")

