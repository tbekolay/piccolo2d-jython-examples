from jip.embed import require
require('org.piccolo2d:piccolo2d-core:1.3.1')
require('org.piccolo2d:piccolo2d-extras:1.3.1')

import java.awt.BasicStroke
import java.awt.Color
from java.awt.event import KeyEvent, InputEvent

from edu.umd.cs.piccolo import PCanvas
from edu.umd.cs.piccolo.event import PBasicInputEventHandler
from edu.umd.cs.piccolo.event import PInputEvent, PInputEventFilter
from edu.umd.cs.piccolo.nodes import PPath
from edu.umd.cs.piccolox import PFrame


class InteractionFrame(PFrame):
    def initialize(self):
        # Remove the pan event handler that is installed by default so that it
        # does not conflict with our new squiggle handler.
        self.canvas.panEventHandler = None

        # Create a squiggle handler and register it with the Canvas.
        squiggleHandler = SquiggleHandler(self.canvas)
        self.canvas.addInputEventListener(squiggleHandler)

        # Create a green rectangle node.
        nodeGreen = PPath.createRectangle(0, 0, 100, 100)
        nodeGreen.paint = java.awt.Color.GREEN
        self.canvas.layer.addChild(nodeGreen)

        # Attach event handler directly to the node.
        nodeGreen.addInputEventListener(NodeGreenHandler())


class NodeGreenHandler(PBasicInputEventHandler):
    def mousePressed(self, e):
        e.pickedNode.paint = java.awt.Color.ORANGE
        e.inputManager.keyboardFocus = e.path
        e.handled = True

    def mouseDragged(self, e):
        aNode = e.pickedNode
        delta = e.getDeltaRelativeTo(aNode)
        aNode.translate(delta.width, delta.height)
        e.handled = True

    def mouseReleased(self, e):
        e.pickedNode.paint = java.awt.Color.GREEN
        e.handled = True

    def keyPressed(self, e):
        node = e.pickedNode
        if e.keyCode == KeyEvent.VK_UP:
            node.translate(0, -10.)
        elif e.keyCode == KeyEvent.VK_DOWN:
            node.translate(0, 10.)
        elif e.keyCode == KeyEvent.VK_LEFT:
            node.translate(-10., 0)
        elif e.keyCode == KeyEvent.VK_RIGHT:
            node.translate(10., 0)


class SquiggleHandler(PBasicInputEventHandler):
    def __init__(self, canvas):
        self.canvas = canvas
        self.eventFilter = PInputEventFilter(InputEvent.BUTTON1_MASK)

        # The squiggle that is currently getting created.
        self.squiggle = None

    def mousePressed(self, e):
        PBasicInputEventHandler.mousePressed(self, e)

        p = e.position

        # Create a new squiggle and add it to the canvas.
        self.squiggle = PPath()
        self.squiggle.moveTo(p.x, p.y)
        self.squiggle.stroke = java.awt.BasicStroke(1 / e.camera.viewScale)
        self.canvas.layer.addChild(0, self.squiggle)

        # Reset the keyboard focus.
        e.inputManager.keyboardFocus = None

    def mouseDragged(self, e):
        PBasicInputEventHandler.mouseDragged(self, e)

        # Update the squiggle while dragging.
        self.updateSquiggle(e)

    def mouseReleased(self, e):
        PBasicInputEventHandler.mouseReleased(self, e)

        # Update the squiggle one last time.
        self.updateSquiggle(e)
        self.squiggle = None

    def updateSquiggle(self, e):
        # Add a new segment to the squiggle
        # from the last mouse position to
        # the current mouse position.
        p = e.position
        self.squiggle.lineTo(p.x, p.y)

if __name__ == '__main__':
    InteractionFrame()
