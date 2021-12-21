"""
Plot.py
Created 21/12/2021
"""
import sys
sys.path.append("..")
import numpy as np
from mpl_toolkits.mplot3d import Axes3D  
import matplotlib.pyplot as plt

class Plot:
    """
    Class Plot:
    Uses the matplotlib to plot various graphs

    Parameters: None

    Funtions:
        plotControlSurface
    """

    def __init__(self) -> None:
        pass

    def plotControlSurface(self,x,y,z,xLabel,yLabel,zLabel) -> None:
        """Plot a 3D surface showcasing the relationship between input (x,y) and output z"""
        _, ax = plt.subplots(subplot_kw={"projection": "3d"})
        x,y = np.meshgrid(x,y)
        ax.plot_surface(np.asarray(x), np.asarray(y),np.asarray(z))
        ax.set_xlabel(xLabel)
        ax.set_ylabel(yLabel)
        ax.set_zlabel(zLabel)
        plt.show()