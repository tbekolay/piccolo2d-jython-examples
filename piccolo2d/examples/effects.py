from jip.embed import require
require('org.piccolo2d:piccolo2d-core:1.3.1')
require('org.piccolo2d:piccolo2d-extras:1.3.1')

import math

import java.awt.Color
import java.lang.System

from edu.umd.cs.piccolo.activities import PActivity
from edu.umd.cs.piccolo.nodes import PPath
from edu.umd.cs.piccolox import PFrame


class EffectsFrame(PFrame):
    def initialize(self):
        # Create a new node that we will apply different activities to, and
        # place that node at location 200, 200.
        aNode = PPath.createRectangle(0, 0, 100, 80)
        layer = self.canvas.layer
        layer.addChild(aNode)
        aNode.setOffset(200, 200)

        # Store the current time in milliseconds for use below.
        currentTime = java.lang.System.currentTimeMillis()

        # Create a new custom "flash" activity. This activity will start running in
        # five seconds, and while it runs it will flash aNode's paint between
        # red and green every half second.
        flash = FlashActivity(aNode, -1, 500, currentTime + 5000)

        # Schedule the activity.
        self.canvas.root.addActivity(flash)

        # Create three activities that animate the node's position. Since our node
        # already descends from the root node the animate methods will automatically
        # schedule these activities for us.
        a1 = aNode.animateToPositionScaleRotation(0, 0, 0.5, 0, 5000)
        a2 = aNode.animateToPositionScaleRotation(100, 0, 1.5,
                                                  math.radians(110), 5000)
        a3 = aNode.animateToPositionScaleRotation(200, 100, 1, 0, 5000)

        # The animate activities will start immediately (in the next call to
        # PRoot.processInputs) by default. Here we set their start times (in PRoot
        # global time) so that they start when the previous one has finished.
        a1.startTime = currentTime
        a2.startAfter(a1)
        a3.startAfter(a2)

        a1.delegate = FlashActivityDelegate()


class FlashActivityDelegate(PActivity.PActivityDelegate):
    def activityStarted(self, t):
        print "a1 started"

    def activityStepped(self, t):
        pass

    def activityFinished(self, t):
        print "a1 finished"


class FlashActivity(PActivity):
    def __init__(self, node, *args, **kwargs):
        PActivity.__init__(self, *args, **kwargs)
        self.fRed = True
        self.aNode = node

    def activityStep(self, elapsedTime):
        if self.fRed:
            self.aNode.paint = java.awt.Color.RED
        else:
            self.aNode.paint = java.awt.Color.GREEN
        self.fRed = not self.fRed

if __name__ == "__main__":
    EffectsFrame()
