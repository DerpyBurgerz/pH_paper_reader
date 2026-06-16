def find_pH(pH_hue_dict, hue):
    for i in range(0, 15):
        for row in range(0, 4):
            hue_1 = pH_hue_dict[i][row]
            hue_2 = pH_hue_dict[i+1][row]
            current_hue = hue[row]


def is_between_hue(ref1, ref2, strip, inclusive=True):
    # Normalize angles to [0, 180)
    ref1 = ref1 % 180
    ref2 = ref2 % 180
    strip = strip % 180

    # Compute the clockwise distance from ref1 to ref2
    diff = (ref2 - ref1) % 180

    # If diff == 0, the two references are the same point – then "between" means equal to that point
    if diff == 0:
        return strip == ref1 if inclusive else False

    # Normalize strip relative to ref1
    strip_from_ref1 = (strip - ref1) % 180

    # strip is between if its normalized position is <= diff
    if inclusive:
        return strip_from_ref1 <= diff
    else:
        return 0 < strip_from_ref1 < diff


