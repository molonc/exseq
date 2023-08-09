import time
import mvp
import gsioc

# MVP3: 1-7 hybridization
# MVP1:
#   - 1 MVP3
#   - 2 Wash
#   - 3 Wash SSC
#   - 4 Imaging
#   - 5 Cleavage


def cleavage(mvp1, pump):
    """[summary]

    Args:
        mvp1 ([MVPObject]): Which MVP we should be moving
        pump ([GSIOC object]): The pump
    """
    # Set mvp 1 to 5, rotating clockwise
    print("Start cleavage buffer")
    mvp.change_valve_pos(mvp1, 0, 5)
    time.sleep(5)
    pump.push(500)
    time.sleep(1200)
    # time.sleep(10)
    pump.stop()
    print("Cleavage buffer: Done")
    time.sleep(2)


def wash(mvp1, pump):
    """[summary]

    Args:
        mvp1 ([MVPObject]): Which MVP we should be moving
        pump ([pump object]): The pump
    """
    print("Start wash buffer")
    mvp.change_valve_pos(mvp1, 0, 2)
    time.sleep(5)
    pump.push(500)
    time.sleep(1200)
    pump.stop()
    print("Wash buffer: Done")
    time.sleep(2)


def washssc(mvp1, pump):
    """[summary]

    Args:
        mvp1 ([MVPObject]): Which MVP we should be moving
        pump ([GSIOC object]): The pump
    """
    print("Start wash(SSC) buffer")
    mvp.change_valve_pos(mvp1, 0, 3)
    time.sleep(5)
    pump.push(500)
    time.sleep(900)
    pump.stop()
    print("Wash(SSC) buffer: Done")
    time.sleep(2)


def hybridization(pos, mvp1, mvp2, pump):
    """
    Args:
        pos ([int]): position of the valve
        mvp1 ([MVPObject]): MVP1
        mvp2 ([type]): MVP3
        pump ([GSIOC object]): The pump
    """
    print("Start wash(SSC) buffer")
    mvp.change_valve_pos(mvp1, 0, 1)
    time.sleep(2)
    mvp.change_valve_pos(mvp2, 0, pos)
    time.sleep(5)
    pump.push(500)
    time.sleep(1800)
    pump.stop()
    print("Wash(SSC) buffer: Done")
    time.sleep(2)


def imaging(mvp1, pump):
    """[summary]

    Args:
        mvp1 ([MVPObject]): Which MVP we should be moving
        pump ([GSIOC object]): The pump
    """
    print("Start imaging buffer")
    mvp.change_valve_pos(mvp1, 0, 4)
    time.sleep(5)
    pump.push(500)
    time.sleep(700)
    pump.stop()
    print("Imaging buffer: Done")
    time.sleep(2)


if __name__ == "__main__":
    # set all the variables
    gsioc_COM = "COM3" # important: choose correct communitcation port
    #mvp1_COM = "COM12"
    #mvp2_COM = "COM13"
    #mvp1 = mvp.MVP()
    #mvp2 = mvp.MVP()

    # connect the pump
    pump = gsioc.GSIOC()
    pump.connect(gsioc_COM)
    pump.push(500) # CW direction; 500 means 5 mL/min on display
    time.sleep(10) #pump for 10 s
    #pump.draw(14) CCW direction
    pump.stop()
