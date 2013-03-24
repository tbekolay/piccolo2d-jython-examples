from jip.embed import require
require('org.piccolo2d:piccolo2d-core:1.3.1')
require('org.piccolo2d:piccolo2d-extras:1.3.1')

import java.awt.Color

from edu.umd.cs.piccolo import PNode
from edu.umd.cs.piccolo.event import PBasicInputEventHandler, PDragEventHandler
from edu.umd.cs.piccolo.event import PInputEvent
from edu.umd.cs.piccolo.nodes import PImage, PPath, PText
from edu.umd.cs.piccolox import PFrame


class InterfaceFrame(PFrame):
    def initialize(self):
        # Remove the Default pan event handler and add a drag event handler
        # so that we can drag the nodes around individually.
        self.canvas.panEventHandler = None
        self.canvas.addInputEventListener(PDragEventHandler())

        # Create a node.
        aNode = PNode()

        # A node will not be visible until its bounds and paint are set.
        aNode.setBounds(0, 0, 100, 80)
        aNode.paint = java.awt.Color.RED

        # A node needs to be a descendant of the root to be displayed.
        layer = self.canvas.layer
        layer.addChild(aNode)

        # A node can have child nodes added to it.
        anotherNode = PNode()
        anotherNode.setBounds(0, 0, 100, 80)
        anotherNode.paint = java.awt.Color.YELLOW
        aNode.addChild(anotherNode)

        # The base bounds of a node are easy to change. Changing the bounds
        # of a node will not affect its children.
        aNode.setBounds(-10, -10, 200, 110)

        # Each node has a transform that can be used to modify the position,
        # scale or rotation of a node.  Changing a node's transform, will
        # transform all of its children as well.
        aNode.translate(100, 100)
        aNode.scale(1.5)
        aNode.rotate(45)

        # Add a couple of PPath nodes and a PText node.
        layer.addChild(PPath.createEllipse(0, 0, 100, 100))
        layer.addChild(PPath.createRectangle(0, 100, 100, 100))
        layer.addChild(PText("Hello World"))

        # Here we create a PImage node that displays a thumbnail image
        # of the root node. Then we add the new PImage to the main layer.
        image = PImage(layer.toImage(300, 300, None))
        layer.addChild(image)

        myCompositeFace = PPath.createRectangle(0, 0, 100, 80)

        # Create parts for the face.
        eye1 = PPath.createEllipse(0, 0, 20, 20)
        eye1.paint = java.awt.Color.YELLOW
        eye2 = eye1.clone()
        mouth = PPath.createRectangle(0, 0, 40, 20)
        mouth.paint = java.awt.Color.BLACK

        # Add the face parts.
        myCompositeFace.addChild(eye1)
        myCompositeFace.addChild(eye2)
        myCompositeFace.addChild(mouth)

        # Don't want anyone grabbing out our eye's.
        myCompositeFace.childrenPickable = False

        # Position the face parts.
        eye2.translate(25, 0)
        mouth.translate(0, 30)

        # Set the face bounds so that it neatly contains the face parts.
        b = myCompositeFace.getUnionOfChildrenBounds(None)
        b.inset(-5, -5)
        myCompositeFace.setBounds(b)

        # Oops it's too small, so scale it up.
        myCompositeFace.scale(1.5)

        layer.addChild(myCompositeFace)

        ts = ToggleShape()
        ts.paint = java.awt.Color.ORANGE
        layer.addChild(ts)


class ToggleShape(PPath):
    def __init__(self):
        self.pressed = False
        self.pathToEllipse = (0, 0, 100, 80)
        self.addInputEventListener(ToggleShapeHandler(self))

    def paint(self, paintContext):
        if self.pressed:
            g2 = paintContext.graphics
            g2.paint = self.paint
            g2.fill(self.boundsReference)
        else:
            PPath.paint(paintContext)


class ToggleShapeHandler(PBasicInputEventHandler):
    def __init__(self, ts):
        self.ts = ts

    def mousePressed(self, e):
        PBasicInputEventHandler.mousePressed(self, e)
        self.ts.pressed = True
        self.ts.repaint()

    def mouseReleased(self, e):
        PBasicInputEventHandler.mouseReleased(self, e)
        self.ts.pressed = False
        self.ts.repaint()

if __name__ == '__main__':
    InterfaceFrame()
