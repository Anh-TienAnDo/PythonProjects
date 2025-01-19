from tkinter import Entry
from static.css.FontType import FontType
from contants import *

class EntryType:
  @staticmethod
  def normal(frame, text_var, font=FontType.normal(), text_color=TEXT_COLOR, bg_color=BG_COLOR_WHITE, bd=ENTRY_BD):
    entry = Entry(frame, textvariable=text_var, font=font, fg=text_color, bg=bg_color, bd=bd)
    return entry
  
  @staticmethod
  def h4(frame, text_var, font=FontType.h4(), text_color=TEXT_COLOR, bg_color=BG_COLOR_WHITE, bd=ENTRY_BD):
    entry = Entry(frame, textvariable=text_var, font=font, fg=text_color, bg=bg_color, bd=bd)
    return entry
  
  @staticmethod
  def view(frame, text_var, font=FontType.normal(), text_color=TEXT_COLOR, bg_color=BG_COLOR_LIGHT_GRAY, bd=ENTRY_BD):
    entry = Entry(frame, textvariable=text_var, font=font, fg=text_color, bg=bg_color, state='readonly', bd=bd)
    return entry
  
  @staticmethod
  def view_h4(frame, text_var, font=FontType.h4(), text_color=TEXT_COLOR, bg_color=BG_COLOR_LIGHT_GRAY, bd=ENTRY_BD):
    entry = Entry(frame, textvariable=text_var, font=font, fg=text_color, bg=bg_color, state='readonly', bd=bd)
    return entry
  
  @staticmethod
  def blue(frame, text_var, font=FontType.normal(), text_color=TEXT_COLOR_BLUE, bg_color=BG_COLOR_WHITE, bd=ENTRY_BD):
    entry = Entry(frame, textvariable=text_var, font=font, fg=text_color, bg=bg_color, bd=bd)
    return entry
  
  @staticmethod
  def red(frame, text_var, font=FontType.normal(), text_color=TEXT_COLOR_RED, bg_color=BG_COLOR_WHITE, bd=ENTRY_BD):
    entry = Entry(frame, textvariable=text_var, font=font, fg=text_color, bg=bg_color, bd=bd)
    return entry
  
  @staticmethod
  def green(frame, text_var, font=FontType.normal(), text_color=TEXT_COLOR_GREEN, bg_color=BG_COLOR_WHITE, bd=ENTRY_BD):
    entry = Entry(frame, textvariable=text_var, font=font, fg=text_color, bg=bg_color, bd=bd)
    return entry
  
  @staticmethod
  def blue_day(frame, text_var, font=FontType.normal(), text_color=TEXT_COLOR_BLUE, bg_color=BG_COLOR_WHITE, bd=ENTRY_BD, width=5):
    entry = Entry(frame, textvariable=text_var, font=font, fg=text_color, bg=bg_color, bd=bd, width=width)
    return entry
