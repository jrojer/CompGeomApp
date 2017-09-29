from imports import *
from ui_comp_geom_app import Ui_CompGeomApp

from pathlib import Path
from pathlib import PurePath

from subprocess import Popen, PIPE, STDOUT

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
        ui.pushButton_to_plot_2.clicked.connect(self.ToPlotSlot2)
        ui.pushButton_run.clicked.connect(self.RunSlot)

        self.Scan()
        
    def ToTextSlot(self):
        self.ui.text_widget.setText(self.ui.plot_widget.GetText())

    def ToPlotSlot(self):
        self.ui.plot_widget.FromText(self.ui.text_widget.toPlainText())

    def ToPlotSlot2(self):
        self.ui.plot_widget.FromText(self.ui.text_widget_2.toPlainText())

    
    def Scan(self):
        path = Path(PurePath('.','algos'))
        if not path.is_dir():
            text_widget_2.setText("Error")
            return
        for item in path.iterdir():
            if item.suffix == '.exe':
                self.ui.algo_list_widget.addItem(item.name)

    def RunSlot(self):
        current_item = self.ui.algo_list_widget.currentItem()
        if current_item:
            input_stream = bytes(self.ui.text_widget.toPlainText(),'utf-8')
            filename = str(PurePath('.','algos',current_item.text()))
            p = Popen([filename], stdin=PIPE, stdout=PIPE, stderr=PIPE)
            output = p.communicate(input=input_stream)[0]
            self.ui.text_widget_2.setText(output.decode())
        
        
        

        
