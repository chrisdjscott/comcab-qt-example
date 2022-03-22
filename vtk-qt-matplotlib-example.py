
import sys

from PySide6 import QtWidgets
import vtk
import vtkmodules.qt
vtkmodules.qt.PyQtImpl = "PySide6"
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from matplotlib.backends.backend_qtagg import (
    FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
import numpy as np


class PlotWidget(QtWidgets.QWidget):
    def __init__(self, title, x, y, parent=None):
        super(PlotWidget, self).__init__(parent)

        vbox = QtWidgets.QVBoxLayout()
        self.setLayout(vbox)

        canvas = FigureCanvas(Figure(figsize=(5, 3)))
#        vbox.addWidget(NavigationToolbar(canvas, self))
        vbox.addWidget(canvas)

        self._ax = canvas.figure.subplots()
        self._ax.plot(x, y, ".")
        self._ax.set_title(title)


class VTKWidget(QVTKRenderWindowInteractor):
    def __init__(self, parent=None, **kw):
        super(VTKWidget, self).__init__(parent=parent, **kw)

        # cone example demo
        ren = vtk.vtkRenderer()
        self.GetRenderWindow().AddRenderer(ren)

        cone = vtk.vtkConeSource()
        cone.SetResolution(8)

        coneMapper = vtk.vtkPolyDataMapper()
        coneMapper.SetInputConnection(cone.GetOutputPort())

        coneActor = vtk.vtkActor()
        coneActor.SetMapper(coneMapper)

        ren.AddActor(coneActor)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setWindowTitle("VTK + Matplotlib example")

        # main widget
        main_widget = QtWidgets.QWidget()
        main_layout = QtWidgets.QHBoxLayout()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # create widget and layout for holding plots
        plot_widget = QtWidgets.QWidget()
        self._plot_layout = QtWidgets.QVBoxLayout()
        plot_widget.setLayout(self._plot_layout)
        main_layout.addWidget(plot_widget)

        # add some demo plots
        t = np.linspace(0, 10, 501)
        self._plot_layout.addWidget(PlotWidget("Plot 1", t, np.tan(t)))
        self._plot_layout.addWidget(PlotWidget("Plot 2", t, np.sin(t)))
        self._plot_layout.addWidget(PlotWidget("Plot 3", t, np.cos(t)))

        # create and add VTK widget
        self._vtk_widget = VTKWidget()
        main_layout.addWidget(self._vtk_widget)

        # show the main window and initialise the VTK widget
        self.show()
        self._vtk_widget.Initialize()
        self._vtk_widget.Start()


def main():
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
