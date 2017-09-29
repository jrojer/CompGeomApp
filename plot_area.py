from imports import *

import re 

class PlotArea(QWidget):
    def __init__(self,parent):
        super().__init__(parent)

        self.points = []    
        self.scale = 100
        self.label_dict = {}

        self.dots = []
        self.blines = []
        self.polygons = []

    def MovePoints(self, dst):
        dst.append(self.points[::])
        self.points.clear()

    def MakeDotsSlot(self, dummy):
        if len(self.points) > 0:
            self.MovePoints(self.dots)
            self.update()
    def MakeBlineSlot(self, dummy):
        if len(self.points) > 1:
            self.MovePoints(self.blines)
            self.update()
    def MakePolygonSlot(self, dummy):
        if len(self.points) > 2:
            self.MovePoints(self.polygons)
            self.update()

    def DrawGrid(self,painter):
        for x in range(0,self.width(),self.scale):
            painter.drawLine(x,0,x,self.height())
        for y in range(0,self.height(),self.scale):
            painter.drawLine(0,y,self.width(),y)

    def FillBackground(self,painter):
        painter.fillRect(0,0,self.width(),self.height(),QtCore.Qt.white)

    def DrawBlines(self,painter):
        for bline in self.blines:
            for i in range(len(bline)-1):
                painter.drawLine(bline[i],bline[i+1])

    def DrawPolygons(self,painter):
        for polyg in self.polygons:
            for i in range(len(polyg)):
                painter.drawLine(polyg[i],polyg[(i+1)%len(polyg)])

    def DrawPoints(self,points,painter):
        painter.setBrush(QtCore.Qt.red)
        for point in points:
            w = self.scale/10
            x = point.x() - w/2
            y = point.y() - w/2
            painter.drawEllipse(x,y,w,w)
            self.PlaceLabel(point)

    def paintEvent(self,event):
        painter = QPainter(self)
        self.FillBackground(painter)
        self.DrawGrid(painter)

        self.DrawPoints(self.points,painter)

        for dots in self.dots:
            self.DrawPoints(dots,painter)
        for bline in self.blines:
            self.DrawPoints(bline,painter)
        for polyg in self.polygons:
            self.DrawPoints(polyg,painter)

        pen = QtGui.QPen()
        pen.setWidth(self.scale/50)
        pen.setColor(QtCore.Qt.blue)
        painter.setPen(pen)

        self.DrawBlines(painter)
        self.DrawPolygons(painter)
            
    def PlaceLabel(self,pos):
        if not (pos.x(),pos.y()) in self.label_dict:
            label= QtWidgets.QLabel(self)
            label.setText("({},{})".format(pos.x(),pos.y()))
            label.move(pos)
            label.setVisible(True)
            self.label_dict[(pos.x(),pos.y())] = label

    def ClearLabels(self):
        while len(self.label_dict) > 0:
            self.label_dict.popitem()[1].deleteLater()

    def mousePressEvent(self,event):
        '''Right click clears
           Left click places a dot'''
        pos = event.pos()
        if event.buttons() == QtCore.Qt.RightButton:
            self.points.clear() 
            self.dots.clear()
            self.blines.clear()
            self.polygons.clear()
            self.ClearLabels()
        else:
            self.points.append(pos)
            #self.PlaceLabel(pos)
        self.update()
    
    def ListsToText(self,lists,ch):
        text = ''
        if len(lists) > 0:
            for lst in lists:
                text += ch + ' ' + str(len(lst)) + '\n'
                for p in lst:
                    text += str(p.x()) + ' '+ str(p.y()) + '\n'
        return text
        
    def GetText(self):
        text = self.ListsToText(self.dots,'D') + self.ListsToText(self.blines,'L') + self.ListsToText(self.polygons,'P')
        
        return text

    def FromText(self,text):

        dots = []
        blines = []
        polygons = []

        point_dict={'D':dots,'L':blines,'P':polygons}

        text = text.strip()
        lines = text.split('\n')
        header_regex = re.compile(r'([DLP])\s+(\d+)')
        point_regex = re.compile(r'(\d+)\s+(\d+)')

        i = 0
        while (i < len(lines)):
            header_match = header_regex.fullmatch(lines[i])
            if not header_match: return False

            num = int(header_match.group(2))
            if i + num >= len(lines): return False 

            points = []

            for j in range(i+1,i+1+num):
                match = point_regex.fullmatch(lines[j])
                if not match: return False
                x = int(match.group(1))
                y = int(match.group(2))
                points.append(QPoint(x,y))
            point_dict[header_match.group(1)].append(points)
            i += num+1

        self.dots.clear() 
        self.blines.clear() 
        self.polygons.clear()
        self.ClearLabels()

        self.dots.extend(dots) 
        self.blines.extend(blines)
        self.polygons.extend(polygons)
        self.update()

        return True

