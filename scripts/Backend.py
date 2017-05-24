import numpy as np
import pdb

def _read_csv(filename):
    with open(filename, "r") as f:
        content = f.read()
    data = []
    for line in content.splitlines():
        row = []
        for element in line.split(","):
            if element == "":
                element = 0
            row.append(float(element))
        data.append(row)
    return np.array(data)
        
def load_cie_data(filename):
    csvdata = _read_csv(filename)
    return csvdata

def interpolate_cie_data(ciedata, wavelengths):
    xdata = ciedata.T[0,:]
    XYZ = ciedata.T[1:]
    XYZ_interpol = np.ones([3,len(wavelengths)])
    for i,ydata in enumerate(XYZ):
        XYZ_interpol[i, :] = np.interp(wavelengths, xdata, ydata)
    return XYZ_interpol

def calculate_interference_color(Gamma, wavelengths, XYZ_interpol, gamma_factor=0.5):
    """ Calculate and correct the interference color for one path difference (Gamma).
    
    Parameters
    ----------
    Gamma : number
        path difference
    wavelengths : np.array
        array of wavelenghts
    XYZ_interpol : 
        Output of interpolate_cie_data for given wavelengths-array.

    gamma_factor : float
        factor for gamma correction 
        optional, default=0.5
    
    Returns
    -------
    RGB-value normalized to 1 as numpy-array
    """
    
    #--- calculate transmission

    L = np.array(wavelengths, ndmin=2).T
    L = (np.sin(np.pi*Gamma/L))**2

    #--- convert to XYZ and sum over wavelengths
    L_XYZ = np.dot(XYZ_interpol, L)

    #--- conversion to SRGB
    XYZ_to_RGB = np.array([[3.2406, -1.5372, -0.4986],
                            [-0.9689, 1.8758, 0.0415],
                            [0.0557, -0.2040, 1.0570]])
    RGB = np.dot(XYZ_to_RGB, L_XYZ)
    
    #--- clipping
    RGB[RGB>100]=100
    RGB[RGB<0]=0

    #--- normalize
    RGB/=100
    
    #---gamma correction
    RGB = RGB**gamma_factor
    
    return RGB.ravel()
