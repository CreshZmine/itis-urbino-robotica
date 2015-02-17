import movimenti

def batch_sense(robot):
    print str(robot.sense(0))
    print str(robot.sense(1))
    print str(robot.sense(2))
    print str(robot.sense(3))

rb = movimenti.Robo_moves()
batch_sense(rb)
rb.turn_right()
batch_sense(rb)
rb.turn_left()
batch_sense(rb)
rb.forward()
batch_sense(rb)
