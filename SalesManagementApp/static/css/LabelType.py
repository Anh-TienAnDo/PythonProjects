from tkinter import Label, StringVar
from static.css.FontType import FontType
from contants import *


class LabelType:
    @staticmethod
    def normal(frame, text, font=FontType.normal(), text_color=TEXT_COLOR, bg_color=BG_COLOR_WHITE, warplength=WARP_LENGTH):
        textvariable = StringVar()
        textvariable.set(text)
        label = Label(frame, textvariable=textvariable, font=font, fg=text_color, bg=bg_color, wraplength=warplength)
        return label

    @staticmethod
    def h1(frame, text, font=FontType.h1(), text_color=TEXT_COLOR, bg_color=BG_COLOR_WHITE, warplength=WARP_LENGTH):
        textvariable = StringVar()
        textvariable.set(text)
        label = Label(frame, textvariable=textvariable, font=font, fg=text_color, bg=bg_color, wraplength=warplength)
        return label

    @staticmethod
    def h2(frame, text, font=FontType.h2(), text_color=TEXT_COLOR, bg_color=BG_COLOR_WHITE, warplength=WARP_LENGTH):
        textvariable = StringVar()
        textvariable.set(text)
        label = Label(frame, textvariable=textvariable, font=font, fg=text_color, bg=bg_color, wraplength=warplength)
        return label

    @staticmethod
    def h3(frame, text, font=FontType.h3(), text_color=TEXT_COLOR, bg_color=BG_COLOR_WHITE, warplength=WARP_LENGTH):
        textvariable = StringVar()
        textvariable.set(text)
        label = Label(frame, textvariable=textvariable, font=font, fg=text_color, bg=bg_color, wraplength=warplength)
        return label

    @staticmethod
    def h4(frame, text, font=FontType.h4(), text_color=TEXT_COLOR, bg_color=BG_COLOR_WHITE, warplength=WARP_LENGTH):
        textvariable = StringVar()
        textvariable.set(text)
        label = Label(frame, textvariable=textvariable, font=font, fg=text_color, bg=bg_color, wraplength=warplength)
        return label
    
    @staticmethod
    def normal_red_white(frame, text, font=FontType.normal(), warplength=WARP_LENGTH):
        textvariable = StringVar()
        textvariable.set(text)
        label = Label(frame, textvariable=textvariable, font=font, fg=TEXT_COLOR_RED, bg=BG_COLOR_WHITE, wraplength=warplength)
        return label
    
    @staticmethod
    def normal_blue_white(frame, text, font=FontType.normal(), warplength=WARP_LENGTH):
        textvariable = StringVar()
        textvariable.set(text)
        label = Label(frame, textvariable=textvariable, font=font, fg=TEXT_COLOR_BLUE, bg=BG_COLOR_WHITE, wraplength=warplength)
        return label
    
    @staticmethod
    def normal_green_white(frame, text, font=FontType.normal(), warplength=WARP_LENGTH):
        textvariable = StringVar()
        textvariable.set(text)
        label = Label(frame, textvariable=textvariable, font=font, fg=TEXT_COLOR_GREEN, bg=BG_COLOR_WHITE, wraplength=warplength)
        return label
    
    @staticmethod
    def normal_lightblue_white(frame, text, font=FontType.normal(), warplength=WARP_LENGTH):
        textvariable = StringVar()
        textvariable.set(text)
        label = Label(frame, textvariable=textvariable, font=font, fg=TEXT_COLOR_LIGHT_BLUE, bg=BG_COLOR_WHITE, wraplength=warplength)
        return label