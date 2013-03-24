from jip.embed import require
require('org.piccolo2d:piccolo2d-core:1.3.1')

import java.awt.Color
import java.awt.Font
from java.awt.event import ComponentAdapter
import javax.swing.JFrame

from edu.umd.cs.piccolo import PCanvas, PNode
from edu.umd.cs.piccolo.event import PBasicInputEventHandler


class TabularFisheye(PCanvas):
    def __init__(self):
        self.calendarNode = CalendarNode()
        self.layer.addChild(self.calendarNode)

        self.zoomEventHandler = None
        self.panEventHandler = None

        self.addComponentListener(TabularFisheyeResizeHandler(self))


class TabularFisheyeResizeHandler(ComponentAdapter):
    def __init__(self, tf):
        self.tf = tf

    def componentResized(self, e):
        self.tf.calendarNode.setBounds(self.tf.x, self.tf.y, self.tf.width - 1,
                                       self.tf.height - 1)
        self.tf.calendarNode.layoutChildren(False)


class CalendarNode(PNode):
    DEFAULT_NUM_DAYS = 7
    DEFAULT_NUM_WEEKS = 12
    TEXT_X_OFFSET = 1
    TEXT_Y_OFFSET = 10
    DEFAULT_ANIMATION_MILLIS = 250
    FOCUS_SIZE_PERCENT = 0.65
    DEFAULT_FONT = java.awt.Font("Arial", java.awt.Font.PLAIN, 10)

    def __init__(self):
        self.numDays = CalendarNode.DEFAULT_NUM_DAYS
        self.numWeeks = CalendarNode.DEFAULT_NUM_WEEKS
        self.daysExpanded = 0
        self.weeksExpanded = 0

        for week in xrange(self.numWeeks):
            for day in xrange(self.numDays):
                self.addChild(DayNode(week, day))

        self.addInputEventListener(PickDayHandler(self))

    def getDay(self, week, day):
        return self.getChild(week * self.numDays + day)

    def layoutChildren(self, *args):
        if len(args) == 0:
            self.super__layoutChildren()
            return

        animate, = args
        focusWidth = 0
        focusHeight = 0

        if self.daysExpanded != 0 and self.weeksExpanded != 0:
            focusWidth = (self.width * CalendarNode.FOCUS_SIZE_PERCENT
                          / self.daysExpanded)
            focusHeight = (self.height * CalendarNode.FOCUS_SIZE_PERCENT
                           / self.weeksExpanded)

        collapsedWidth = (self.width - (focusWidth * self.daysExpanded)
                          ) / (self.numDays - self.daysExpanded)
        collapsedHeight = (self.height - (focusHeight * self.weeksExpanded)
                           ) / (self.numWeeks - self.weeksExpanded)

        yOffset = 0

        for week in xrange(self.numWeeks):
            xOffset = 0

            for day in xrange(self.numDays):
                each = self.getDay(week, day)
                width = collapsedWidth
                height = collapsedHeight

                if each.hasWidthFocus:
                    width = focusWidth
                if each.hasHeightFocus:
                    height = focusHeight

                if animate:
                    anim = each.animateToBounds(xOffset, yOffset, width,
                        height, CalendarNode.DEFAULT_ANIMATION_MILLIS)
                    anim.stepRate = 0
                else:
                    each.setBounds(xOffset, yOffset, width, height)

                xOffset += width
                rowHeight = height

            yOffset += rowHeight

    def setFocusDay(self, focusDay, animate):
        for i in xrange(self.childrenCount):
            each = self.getChild(i)
            each.hasWidthFocus = False
            each.hasHeightFocus = False

        if focusDay is None:
            self.daysExpanded = 0
            self.weeksExpanded = 0
        else:
            focusDay.hasWidthFocus = True
            self.daysExpanded = 1
            self.weeksExpanded = 1

            for day in xrange(self.numDays):
                self.getDay(focusDay.week, day).hasHeightFocus = True

            for week in xrange(self.numWeeks):
                self.getDay(week, focusDay.day).hasWidthFocus = True

        self.layoutChildren(animate)


class PickDayHandler(PBasicInputEventHandler):
    def __init__(self, cn):
        PBasicInputEventHandler.__init__(self)
        self.cn = cn

    def mouseReleased(self, e):
        pickedDay = e.pickedNode
        if pickedDay.hasWidthFocus and pickedDay.hasHeightFocus:
            self.cn.setFocusDay(None, True)
        else:
            self.cn.setFocusDay(pickedDay, True)


class DayNode(PNode):
    def __init__(self, week, day):
        self.hasWidthFocus = False
        self.hasHeightFocus = False
        self.lines = [
            "7:00 AM Walk the dog.",
            "9:30 AM Meet John for Breakfast.",
            "12:00 PM Lunch with Peter.",
            "3:00 PM Research Demo.",
            "6:00 PM Pickup Sarah from gymnastics.",
            "7:00 PM Pickup Tommy from karate.",
        ]
        self.week = week
        self.day = day
        self.dayOfMonthString = str((week * 7) + day)
        self.setPaint(java.awt.Color.BLACK)

    def paint(self, paintContext):
        g2 = paintContext.graphics

        g2.setPaint(self.getPaint())
        g2.draw(self.boundsReference)
        g2.font = CalendarNode.DEFAULT_FONT

        y = self.y + CalendarNode.TEXT_Y_OFFSET
        paintContext.graphics.drawString(self.dayOfMonthString,
                                         self.x + CalendarNode.TEXT_X_OFFSET, y)

        if self.hasWidthFocus and self.hasHeightFocus:
            paintContext.pushClip(self.boundsReference)
            for line in self.lines:
                y += 10
                g2.drawString(line, self.x + CalendarNode.TEXT_X_OFFSET, y)
            paintContext.popClip(self.boundsReference)


class TabularFisheyeTester(javax.swing.JFrame):
    def __init__(self):
        self.title = "Piccolo2D Tabular Fisheye"
        self.defaultCloseOperation = javax.swing.JFrame.EXIT_ON_CLOSE
        self.contentPane.add(TabularFisheye())
        self.pack()
        self.visible = True

if __name__ == '__main__':
    TabularFisheyeTester()
