from imports import *
from ui_comp_geom_app import Ui_CompGeomApp
#from plot_area import PlotArea

class MainWindow(QWidget):
    def __init__(self,parent = None):
        super().__init__(parent)
        self.ui = Ui_CompGeomApp()
        ui = self.ui
        ui.setupUi(self)
        ui.pushButton_bline.clicked.connect(ui.plot_widget.MakeBlineSlot)
        ui.pushButton_poly.clicked.connect(ui.plot_widget.MakePolygonSlot)
        ui.pushButton_dot.clicked.connect(ui.plot_widget.MakeDotsSlot)
        ui.pushButton_to_text.clicked.connect(self.ToTextSlot)
        ui.pushButton_to_plot.clicked.connect(self.ToPlotSlot)
        
    def ToTextSlot(self):
        self.ui.text_widget.setText(self.ui.plot_widget.GetText())

    def ToPlotSlot(self):
        self.ui.plot_widget.FromText(self.ui.text_widget.toPlainText())

        
