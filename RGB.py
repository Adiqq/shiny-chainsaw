#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division  # Division in Python 2.7
import matplotlib
import colorsys

matplotlib.use('Agg')  # So that we can render files without GUI
import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np

from matplotlib import colors


def plot_color_gradients(gradients, names):
    # For pretty latex fonts (commented out, because it does not work on some machines)
    # rc('text', usetex=True)
    # rc('font', family='serif', serif=['Times'], size=10)
    rc('legend', fontsize=10)

    column_width_pt = 400  # Show in latex using \the\linewidth
    pt_per_inch = 72
    size = column_width_pt / pt_per_inch

    fig, axes = plt.subplots(nrows=len(gradients), sharex=True, figsize=(size, 0.75 * size))
    fig.subplots_adjust(top=1.00, bottom=0.05, left=0.25, right=0.95)

    for ax, gradient, name in zip(axes, gradients, names):
        # Create image with two lines and draw gradient on it
        img = np.zeros((2, 1024, 3))
        for i, v in enumerate(np.linspace(0, 1, 1024)):
            img[:, i] = gradient(v)

        im = ax.imshow(img, aspect='auto')
        im.set_extent([0, 1, 0, 1])
        ax.yaxis.set_visible(False)

        pos = list(ax.get_position().bounds)
        x_text = pos[0] - 0.25
        y_text = pos[1] + pos[3] / 2.
        fig.text(x_text, y_text, name, va='center', ha='left', fontsize=10)

    fig.savefig('my-gradients.pdf')


def hsv2rgb(h, s, v):
    if (s == 0):
        return (v, v, v)

    while (h >= 360):
        h = h - 360
    while (h < 0):
        h = h + 360

    h = h / 60
    i = np.floor(h)
    ulamek = h - i
    a = v * (1 - s)
    b = v * (1 - s * ulamek)
    c = v * (1 - s * (1 - ulamek))

    return {
        0: (v, c, a),
        1: (b, v, a),
        2: (a, v, c),
        3: (a, b, v),
        4: (c, a, v),
        5: (v, a, b)
    }[i]
    # return (r, g, b)


def gradient_rgb_bw(v):
    return (v, v, v)


def gradient_rgb_gbr(v):
    if (v * 2 < 1):
        return (0, 1 - v * 2, v * 2)
    else:
        return ((v - 0.5) * 2, 0, 1 - (v - 0.5) * 2)
        # return ((v-0.5)*2, 0, 0)
        # return (0,0,0)


def gradient_rgb_gbr_full(v):
    if (v < 0.25):
        return (0, 1, v * 4)
    elif (v < 0.5):
        return (0, 1 - (v - 0.25) * 4, 1)
    elif (v < 0.75):
        return ((v - 0.5) * 4, 0, 1)
    else:
        return (1, 0, 1 - (v - 0.75) * 4)


def gradient_rgb_wb_custom(v):
    (r, g, b) = (0, 0, 0)
    if (v < 0.125):  # 1,1,1
        r = 1
        g = (0.125 - v) * 8
        b = (0.125 - v) * 8
    elif (v < 0.25):  # 1,0,0
        r = 1
        g = 1 - (0.25 - v) * 8
        b = 0
    elif (v < 0.375):  # 1,1,0
        r = (0.375 - v) * 8
        g = 1
        b = 1 - (0.375 - v) * 8
    elif (v < 0.5):  # 0,1,1
        r = 0
        g = (0.5 - v) * 8
        b = 1
    elif (v < 0.625):  # 0,0,1
        r = 1 - (0.625 - v) * 8
        g = 0
        b = 1
    elif (v < 0.75):  # 1,0,1
        r = (0.75 - v) * 8
        g = 1 - (0.75 - v) * 8
        b = (0.75 - v) * 8
    elif (v < 0.875):  # 0,1,0
        r = 0
        g = 1
        b = 0
    elif (v < 1):  # 0,0,0
        r = 0
        g = (1 - v) * 8
        b = 0
    return (r, g, b)


def gradient_hsv_bw(v):
    return hsv2rgb(0, 0, v)


def gradient_hsv_gbr(v):
    return hsv2rgb(v * 240 + 120, 1, 1)


def gradient_hsv_unknown(v):
    return hsv2rgb(480 - v * 120, 0.5, 1)


def gradient_hsv_custom(v):
    if (v < 0.8):
        x = 1
    else:
        x = (1 - v) * 5

    return hsv2rgb(v * 540, x, 1 - x * (1 - (np.sin(v * 14) + 1) / 2))


if __name__ == '__main__':
    def toname(g):
        return g.__name__.replace('gradient_', '').replace('_', '-').upper()


    gradients = (gradient_rgb_bw, gradient_rgb_gbr, gradient_rgb_gbr_full, gradient_rgb_wb_custom,
                 gradient_hsv_bw, gradient_hsv_gbr, gradient_hsv_unknown, gradient_hsv_custom)

    plot_color_gradients(gradients, [toname(g) for g in gradients])
