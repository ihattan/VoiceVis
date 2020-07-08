from PyQt5.QtCore import QRect

class Vis():

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.numSlices = 12
        self.spanAngle = int(360 / self.numSlices)

        # a list of size self.numSlices, equidistant points along a circle
        self.slicePoints = []
        self.calcSlicePoints()

        # frames will be used to draw the circles/slices
        # QRect() objects to be utilized by paintEvent()
        self.frstFrame = QRect()
        self.scndFrame = QRect()
        self.thrdFrame = QRect()
        self.calcFrames()


    def calcSlicePoints(self):
        offset = int(0.5 * self.spanAngle) # want slices centered on axes
        self.slicePoints = [(p * self.spanAngle) + offset for p in range(self.numSlices)]

    def calcFrames(self):
        spanAngle = int(360 / self.numSlices)
        offset = int(0.5 * spanAngle) # want slices centered on axes
        slicePoints = [(p * spanAngle) + offset for p in range(self.numSlices)]

        # first is largest, 1/3 the height of the given area
        # rest of the radii are 2/3 and 1/3 the size of the first
        frstRadius = int(self.height / 3)
        scndRadius = int(frstRadius * 2 / 3)
        thrdRadius = int(frstRadius * 1 / 3)

        # center of the visualization is offset to the left
        visCenterX = visCenterY = int(self.height / 2)

        self.frstFrame = QRect(visCenterX - frstRadius, visCenterY - frstRadius, frstRadius*2, frstRadius*2)
        self.scndFrame = QRect(visCenterX - scndRadius, visCenterY - scndRadius, scndRadius*2, scndRadius*2)
        self.thrdFrame = QRect(visCenterX - thrdRadius, visCenterY - thrdRadius, thrdRadius*2, thrdRadius*2)
