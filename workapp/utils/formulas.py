import math


def rpm_from_sfm(sfm, diameter):
    if diameter <= 0:
        return 0
    return (sfm * 12) / (math.pi * diameter)


def sfm_from_rpm(rpm, diameter):
    if diameter <= 0:
        return 0
    return (rpm * math.pi * diameter) / 12


def ipm_from_ipr(ipr, rpm):
    return ipr * rpm


def ipr_from_ipm(ipm, rpm):
    if rpm == 0:
        return 0
    return ipm / rpm


def drill_feed_ipm(rpm, ipr):
    return rpm * ipr


def tap_feed_ipm_from_tpi(rpm, tpi):
    if tpi <= 0:
        return 0
    return rpm / tpi


def tap_feed_mm_min_from_pitch(rpm, pitch_mm):
    return rpm * pitch_mm
