#!/usr/bin/env python3
import omni
from arduino import *

talker = ArduinoTalker()
talker.start()

talker.join()
