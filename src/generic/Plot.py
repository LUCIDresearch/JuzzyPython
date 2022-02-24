"""
Plot.py
Created 21/12/2021
"""
import sys
from generalType2zSlices.sets.GenT2MF_Interface import GenT2MF_Interface


sys.path.append("..")
from generic.Tuple import Tuple

from type1.sets.T1MF_Interface import T1MF_Interface

from generalType2zSlices.sets.GenT2MF_Triangular import GenT2MF_Triangular
from intervalType2.sets.IntervalT2MF_Interface import IntervalT2MF_Interface

from generalType2zSlices.sets.GenT2MF_Trapezoidal import GenT2MF_Trapezoidal
import numpy as np
from mpl_toolkits.mplot3d import Axes3D  
import matplotlib.pyplot as plt
from typing import List

class Plot:
    """
    Class Plot:
    Uses the matplotlib to plot various graphs

    Parameters: None

    Funtions:
        plotControlSurface
        show
        figure
        title
        legend
        discretize
        plotMF
    """

    def __init__(self) -> None:
        pass
    
    def show(self):
        """Show all the figures created"""
        plt.show()
    
    def figure(self):
        """Create a new plot to draw upon"""
        self.fig = plt.figure()
    
    def figure3d(self):
        """Create a new 3d plot to draw upon"""
        self.fig, self.ax = plt.subplots(subplot_kw={"projection": "3d"})

    def title(self,title: str):
        """Set the title of the current figure"""
        plt.title(title)
    
    def legend(self):
        """Add legend to the current figure"""
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        plt.tight_layout()

    def plotControlSurface(self,x: List[float],y: List[float],z: List[List[float]],xLabel: str,yLabel: str,zLabel: str) -> None:
        """Plot a 3D surface showcasing the relationship between input (x,y) and output z"""
        fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
        
        x,y = np.meshgrid(x,y)
        ax.plot_surface(np.asarray(x), np.asarray(y),np.asarray(z))
        ax.set_xlabel(xLabel)
        ax.set_ylabel(yLabel)
        ax.set_zlabel(zLabel)
        plt.title("Control Surface")
    
    def plotMF2(self,xaxis: str,name: str,sets: IntervalT2MF_Interface,xDisc: int,addExtraEndPoints: bool) -> None:
        x = self.discretize(sets.getSupport(),xDisc)
        y1 = [0] * xDisc
        y2 = [0] * xDisc
        
        for i in range(xDisc):
            temp = sets.getFS(x[i])
            y1[i] = temp.getRight()
            y2[i] = temp.getLeft()
        
        if addExtraEndPoints:
            x2 = [0.0] * (len(x)+2)
            y1b = [0.0] * (len(y1)+2)
            y2b = [0.0] * (len(y2)+2)

            x2[0] = sets.getSupport().getLeft()
            x2[-1] = set.getSupport().getRight()

            y1b[0] = 0.0
            y1b[len(y1)-1] = 0.0
            y2b[0] = 0.0
            y2b[len(y2)-1] = 0.0

            for i in range(len(x)):
                x2[i+1] = x[i]
                y1b[i+1] = y1[i]
                y2b[i+1] = y2[i]
            x = x2
            y1 = y1b
            y2 = y2b
        ax = plt.gca()
        color = next(ax._get_lines.prop_cycler)['color']
        plt.plot(x,y1,label=name+"_upper", color = color)
        plt.plot(x,y2,label=name+"_lower", color = color, alpha=0.5)
        #plt.xlim(xAxisRange.getLeft(),xAxisRange.getRight())
        #plt.ylim(yAxisRange.getLeft(),yAxisRange.getRight())
        plt.ylabel("μ")
        plt.xlabel(xaxis)
        
    def plotMF(self,xaxis: str,name: str,sets: T1MF_Interface,xDisc: int,xAxisRange: Tuple,yAxisRange: Tuple,addExtraEndPoints: bool) -> None:
        """Plot a membership function on the current figure"""
        x = self.discretize(sets.getSupport(),xDisc)
        y = [0] * xDisc
        for i in range(xDisc):
            y[i] = sets.getFS(x[i])
        
        if addExtraEndPoints:
            x2 = [0.0] * (len(x)+2)
            y2 = [0.0] * (len(y)+2)
            x2[0] = sets.getSupport().getLeft()
            x2[-1] = sets.getSupport().getRight()
            for i in range(len(x)):
                x2[i+1] = x[i]
                y2[i+1] = y[i]
            x = x2
            y = y2
        plt.plot(x,y,label=name)
        plt.xlim(xAxisRange.getLeft(),xAxisRange.getRight())
        plt.ylim(yAxisRange.getLeft(),yAxisRange.getRight())
        plt.ylabel("μ")
        plt.xlabel(xaxis)
    
    def plotMFasLines(self,sets: GenT2MF_Interface,xDisc: int) -> None:
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        self.ax.set_zlabel("z")
        x = self.discretize(sets.getSupport(),xDisc)
        y1 = [[0 for c in range(xDisc)] for r in range(sets.getNumberOfSlices())]
        y2 = [[0 for c in range(xDisc)] for r in range(sets.getNumberOfSlices())]
        z1 = [[0 for c in range(xDisc)] for r in range(sets.getNumberOfSlices())]
        z2 = [[0 for c in range(xDisc)] for r in range(sets.getNumberOfSlices())]

        for zLevel in range(sets.getNumberOfSlices()):
            for i in range(xDisc):
                temp = sets.getZSlice(zLevel).getFS(x[i])
                y1[zLevel][i] = temp.getRight()
                y2[zLevel][i] = temp.getLeft()
                if zLevel==0:
                    z1[zLevel][i] = 0.0
                else:
                    z1[zLevel][i] = sets.getZValue(zLevel-1)
                z2[zLevel][i] = sets.getZValue(zLevel)

        for zLevel in range(sets.getNumberOfSlices()):
            self.ax.plot3D(x,y1[zLevel],z1[zLevel],label=sets.getName()+"_upper")
            self.ax.plot3D(x,y2[zLevel],z1[zLevel],label=sets.getName()+"_lower")
            self.ax.plot3D(x,y1[zLevel],z2[zLevel],label=sets.getName()+"_upper")
            self.ax.plot3D(x,y2[zLevel],z2[zLevel],label=sets.getName()+"_lower")

    def turnOnInteraction(self):
        plt.ion()

    def plotMFasSurface(self,plotName: str,sets: GenT2MF_Interface,xAxisRange: Tuple,xDisc: int,addExtraPoints: bool):
        self.ax.set_xlabel("X-Axis")
        self.ax.set_ylabel("Y-Axis")
        self.ax.set_zlabel("Z-Axis")
        if isinstance(sets,GenT2MF_Triangular):
            for zLevel in range(sets.getNumberOfSlices()):
                xUpper = [sets.getZSlice(zLevel).getUMF().getStart(), sets.getZSlice(zLevel).getUMF().getPeak(),sets.getZSlice(zLevel).getUMF().getEnd()]
                zUpper = None
                yUpper = [[0 for i in range(3)] for j in range(2)]

                if zLevel == 0:
                    zUpper = [0.0,sets.getZValue(zLevel)]
                else:
                    zUpper = [sets.getZValue(zLevel-1),sets.getZValue(zLevel)]
                for xD in range(3):
                    yUpper[0][xD] = sets.getZSlice(zLevel).getFS(xUpper[xD]).getRight()
                    yUpper[1][xD] = yUpper[0][xD]
                
                xLower = [sets.getZSlice(zLevel).getLMF().getStart(), sets.getZSlice(zLevel).getLMF().getPeak(),sets.getZSlice(zLevel).getLMF().getEnd()]
                zLower = None
                yLower = [[0 for i in range(3)] for j in range(2)]

                if zLevel == 0:
                    zLower = [0.0,sets.getZValue(zLevel)]
                else:
                    zLower = [sets.getZValue(zLevel-1),sets.getZValue(zLevel)]
                for xD in range(3):
                    yLower[0][xD] = sets.getZSlice(zLevel).getFS(xLower[xD]).getLeft()
                    yLower[1][xD] = yLower[0][xD]
                x,y = np.meshgrid(xUpper,zUpper)
                self.ax.plot_surface(np.asarray(x), np.asarray(y),np.asarray(yUpper),alpha = 0.5)
                x,y = np.meshgrid(xLower,zLower)
                self.ax.plot_surface(np.asarray(x), np.asarray(y),np.asarray(yLower),alpha = 0.5)
        elif isinstance(sets,GenT2MF_Trapezoidal):
            for zLevel in range(sets.getNumberOfSlices()):
                xUpper = [sets.getZSlice(zLevel).getUMF().getA(), sets.getZSlice(zLevel).getUMF().getB(),sets.getZSlice(zLevel).getUMF().getC(),sets.getZSlice(zLevel).getUMF().getD()]
                zUpper = None
                yUpper = [[0 for i in range(4)] for j in range(2)]

                if zLevel == 0:
                    zUpper = [0.0,sets.getZValue(zLevel)]
                else:
                    zUpper = [sets.getZValue(zLevel-1),sets.getZValue(zLevel)]
                for xD in range(4):
                    yUpper[0][xD] = sets.getZSlice(zLevel).getFS(xUpper[xD]).getRight()
                    yUpper[1][xD] = yUpper[0][xD]
                
                xLower = [sets.getZSlice(zLevel).getLMF().getA(), sets.getZSlice(zLevel).getLMF().getB(),sets.getZSlice(zLevel).getLMF().getC(),sets.getZSlice(zLevel).getLMF().getD()]
                zLower = None
                yLower = [[0 for i in range(4)] for j in range(2)]

                if zLevel == 0:
                    zLower = [0.0,sets.getZValue(zLevel)]
                else:
                    zLower = [sets.getZValue(zLevel-1),sets.getZValue(zLevel)]
                for xD in range(4):
                    yLower[0][xD] = sets.getZSlice(zLevel).getFS(xLower[xD]).getLeft()
                    yLower[1][xD] = yLower[0][xD]
                x,y = np.meshgrid(xUpper,zUpper)
                self.ax.plot_surface(np.asarray(x), np.asarray(y),np.asarray(yUpper),alpha = 0.5)
                x,y = np.meshgrid(xLower,zLower)
                self.ax.plot_surface(np.asarray(x), np.asarray(y),np.asarray(yLower),alpha = 0.5)
        else:
            for zLevel in range(sets.getNumberOfSlices()):
                xUpper = self.discretize(xAxisRange,xDisc)
                zUpper = None
                yUpper = [[0 for i in range(xDisc)] for j in range(2)]

                if zLevel == 0:
                    zUpper = [0.0,sets.getZValue(zLevel)]
                else:
                    zUpper = [sets.getZValue(zLevel-1),sets.getZValue(zLevel)]
                for xD in range(xDisc):
                    yUpper[0][xD] = sets.getZSlice(zLevel).getFS(xUpper[xD]).getRight()
                    yUpper[1][xD] = yUpper[0][xD]
                
                xLower = self.discretize(xAxisRange,xDisc)
                zLower = None
                yLower = [[0 for i in range(xDisc)] for j in range(2)]

                if zLevel == 0:
                    zLower = [0.0,sets.getZValue(zLevel)]
                else:
                    zLower = [sets.getZValue(zLevel-1),sets.getZValue(zLevel)]
                for xD in range(xDisc):
                    yLower[0][xD] = sets.getZSlice(zLevel).getFS(xLower[xD]).getLeft()
                    yLower[1][xD] = yLower[0][xD]
            

                if addExtraPoints:
                    x_upper2 = [0.0] * (xUpper.length + 2)
                    y_upper2 = [[0.0 for i in range(yUpper[0].length + 2)] for j in range(2)]
                    x_Lower2 = [0.0] * (xLower.length + 2)
                    y_Lower2 = [[0.0 for i in range(yLower[0].length + 2)] for j in range(2)]

                    x_upper2[0] = sets.getSupport().getLeft()
                    x_upper2[-1] = sets.getSupport().getRight()
                    x_Lower2[0] = x_upper2[0]
                    x_Lower2[-1] = x_upper2[-1]
            
                    for i in range(xUpper):
                        x_upper2[i + 1] = xUpper[i]
                        x_Lower2[i + 1] = xLower[i]
                        y_upper2[0][i + 1] = yUpper[0][i]
                        y_Lower2[0][i + 1] = yLower[0][i]
                        y_upper2[1][i + 1] = yUpper[1][i]
                        y_Lower2[1][i + 1] = yLower[1][i]
                    
                    xUpper = x_upper2
                    xLower = x_Lower2
                    yUpper = y_upper2
                    yLower = y_Lower2
                x,y = np.meshgrid(xUpper,zUpper)
                self.ax.plot_surface(np.asarray(x), np.asarray(y),np.asarray(yUpper),alpha = 0.5)
                x,y = np.meshgrid(xLower,zLower)
                self.ax.plot_surface(np.asarray(x), np.asarray(y),np.asarray(yLower),alpha = 0.5)

    def discretize(self,support: Tuple,discLevel: int) -> List[float]:
        """Discretize the support values"""
        d = [0] * discLevel
        stepSize = (support.getSize())/(discLevel-1.0)
        d[0] = support.getLeft()
        d[-1] = support.getRight()
        for i in range(1,discLevel-1):
            d[i] = support.getLeft()+i*stepSize
        return d
    