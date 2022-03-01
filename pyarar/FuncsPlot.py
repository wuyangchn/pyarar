#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File   : FuncsPlot.py
# @Author : Yang Wu
# @Date   : 2022/1/5
# @Email  : wuy@cug.edu.cn

from matplotlib import pyplot, patches
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

"""----------------"""
"""--Draw Figures--"""
"""----------------"""
def get_default_canvas(**kwargs):
    """
    :kwargs: properties including x_label, y_label, title
    :return: canvas: FigureCanvasQTAgg
    """
    '''create fig and canvas'''
    fig = pyplot.Figure(dpi=100, constrained_layout=True)
    canvas = FigureCanvas(fig)
    '''set axes'''
    canvas.axes = fig.subplots()
    canvas.axes.tick_params(labelsize=6, direction='in')
    font = {'family': 'Microsoft YaHei Ui', 'size': 12, 'style': 'normal'}
    canvas.axes.set_xlabel(kwargs.pop('x_label', ''), fontdict=font)
    canvas.axes.set_ylabel(kwargs.pop('y_label', ''), fontdict=font)
    font = {'family': 'Microsoft YaHei Ui', 'size': 16, 'weight': 'bold'}
    canvas.axes.set_title(kwargs.pop('title', ''), fontdict=font)
    return canvas
