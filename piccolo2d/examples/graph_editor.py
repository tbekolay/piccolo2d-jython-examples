from jip.embed import require
require('org.piccolo2d:piccolo2d-core:1.3.1')

import java.awt.Color
import java.awt.Dimension
from java.awt.event import InputEvent, MouseEvent
import java.util.ArrayList
import java.util.Random
import javax.swing.JFrame

from edu.umd.cs.piccolo import PCanvas, PLayer
from edu.umd.cs.piccolo.event import PDragEventHandler, PInputEventFilter
from edu.umd.cs.piccolo.nodes import PPath


class GraphEditor(PCanvas):
    def __init__(self, width, height):
        self.preferredSize = java.awt.Dimension(width, height)
        numNodes = 50
        numEdges = 50

        # Initialize, and create a layer for the edges
        # (always underneath the nodes)
        nodeLayer = self.layer
        edgeLayer = PLayer()
        self.root.addChild(edgeLayer)
        self.camera.addLayer(0, edgeLayer)
        random = java.util.Random()

        # Create some random nodes
        # Each node's attribute set has an
        # ArrayList to store associated edges
        for _ in xrange(numNodes):
            x = random.nextInt(width)
            y = random.nextInt(height)
            node = PPath.createEllipse(x, y, 20, 20)
            node.addAttribute("edges", java.util.ArrayList())
            nodeLayer.addChild(node)

        # Create some random edges
        # Each edge's attribute set has an
        # ArrayList to store associated nodes
        for _ in xrange(numEdges):
            n1 = random.nextInt(numNodes)
            n2 = random.nextInt(numNodes)

            # Make sure we have two distinct nodes.
            while n1 == n2:
                n2 = random.nextInt(numNodes)

            node1 = nodeLayer.getChild(n1)
            node2 = nodeLayer.getChild(n2)
            edge = PPath()
            node1.getAttribute("edges").add(edge)
            node2.getAttribute("edges").add(edge)
            edge.addAttribute("nodes", java.util.ArrayList())
            edge.getAttribute("nodes").add(node1)
            edge.getAttribute("nodes").add(node2)
            edgeLayer.addChild(edge)
            self.updateEdge(edge)

        # Create event handler to move nodes and update edges
        nodeLayer.addInputEventListener(NodeDragHandler(self))

    def updateEdge(self, edge):
        # Note that the node's "FullBounds" must be used
        # (instead of just the "Bounds") because the nodes
        # have non-identity transforms which must be included
        # when determining their position.
        node1 = edge.getAttribute("nodes").get(0)
        node2 = edge.getAttribute("nodes").get(1)
        start = node1.fullBoundsReference.center2D
        end = node2.fullBoundsReference.center2D
        edge.reset()
        edge.moveTo(start.x, start.y)
        edge.lineTo(end.x, end.y)


class NodeDragHandler(PDragEventHandler):
    def __init__(self, ge):
        PDragEventHandler.__init__(self)
        self.ge = ge
        filter_ = PInputEventFilter()
        filter_.orMask = InputEvent.BUTTON1_MASK | InputEvent.BUTTON3_MASK
        self.eventFilter = filter_

    def mouseEntered(self, e):
        PDragEventHandler.mouseEntered(self, e)
        if e.button == MouseEvent.NOBUTTON:
            e.pickedNode.paint = java.awt.Color.RED

    def mouseExited(self, e):
        PDragEventHandler.mouseExited(self, e)
        if e.button == MouseEvent.NOBUTTON:
            e.pickedNode.paint = java.awt.Color.WHITE

    def startDrag(self, e):
        self.super__startDrag(e)

        e.handled = True
        e.pickedNode.moveToFront()

    def drag(self, e):
        self.super__drag(e)

        edges = e.pickedNode.getAttribute("edges")
        for edge in edges:
            self.ge.updateEdge(edge)


class GraphEditorTester(javax.swing.JFrame):
    def __init__(self):
        self.title = "Piccolo2D Graph Editor"
        self.defaultCloseOperation = javax.swing.JFrame.EXIT_ON_CLOSE
        graphEditor = GraphEditor(500, 500)
        self.contentPane.add(graphEditor)
        self.pack()
        self.visible = True

if __name__ == '__main__':
    GraphEditorTester()
