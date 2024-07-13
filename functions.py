# Function required for deforestation.

# Function to create to skip the frame where deforestation calculation in not required.
def skipFrame(frame, frameStatus = True):

    # skip the frame which are not required for analysis.
    if frame >= 345 and frame <= 700:
        frameStatus = False
    elif frame >= 1000 and frame <= 1430:
        frameStatus = False

    elif frame>= 1750 and frame <= 2130:
        frameStatus = False


    return frameStatus
