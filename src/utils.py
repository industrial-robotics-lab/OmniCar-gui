def rescale(value, oldMin, oldMax, newMin, newMax):
    oldSpan = oldMax - oldMin
    newSpan = newMax - newMin
    normValue = float(value - oldMin) / oldSpan
    return newMin + (normValue * newSpan)