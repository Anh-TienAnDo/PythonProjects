from tkinter import Button
from static.css.FontType import FontType
from contants import *

class ButtonType:
  @staticmethod
  def normal(frame, text, font=FontType.normal(), text_color=TEXT_COLOR, bg_color=BG_COLOR_WHITE, bd=BUTTON_BD, cursor=BUTTON_CURSOR, overrelief=BUTTON_RELIEF, warp_length=BUTTON_WARP_LENGTH):
    button = Button(frame, text=text, font=font, fg=text_color, bg=bg_color, bd=bd, cursor=cursor, overrelief=overrelief, wraplength=warp_length)
    return button
  
  @staticmethod
  def primary(frame, text, font=FontType.normal(), activeforeground=TEXT_COLOR_BLUE, text_color=TEXT_COLOR_WHITE, bg_color=BG_COLOR_BLUE, bd=BUTTON_BD, cursor=BUTTON_CURSOR, overrelief=BUTTON_RELIEF, warp_length=BUTTON_WARP_LENGTH):
    button = Button(frame, text=text, font=font, activeforeground=activeforeground, fg=text_color, bg=bg_color, bd=bd, cursor=cursor, overrelief=overrelief, wraplength=warp_length)
    return button
  
  @staticmethod
  def success(frame, text, font=FontType.normal(), activeforeground=TEXT_COLOR_GREEN, text_color=TEXT_COLOR_WHITE, bg_color=BG_COLOR_GREEN, bd=BUTTON_BD, cursor=BUTTON_CURSOR, overrelief=BUTTON_RELIEF, warp_length=BUTTON_WARP_LENGTH):
    button = Button(frame, text=text, font=font, activeforeground=activeforeground, fg=text_color, bg=bg_color, bd=bd, cursor=cursor, overrelief=overrelief, wraplength=warp_length)
    return button
  
  @staticmethod
  def danger(frame, text, font=FontType.normal(), activeforeground=TEXT_COLOR_RED, text_color=TEXT_COLOR_WHITE, bg_color=BG_COLOR_RED, bd=BUTTON_BD, cursor=BUTTON_CURSOR, overrelief=BUTTON_RELIEF, warp_length=BUTTON_WARP_LENGTH):
    button = Button(frame, text=text, font=font, activeforeground=activeforeground, fg=text_color, bg=bg_color, bd=bd, cursor=cursor, overrelief=overrelief, wraplength=warp_length)
    return button
  
  @staticmethod
  def warning(frame, text, font=FontType.normal(), activeforeground=TEXT_COLOR_ORANGE, text_color=TEXT_COLOR_WHITE, bg_color=BG_COLOR_ORANGE, bd=BUTTON_BD, cursor=BUTTON_CURSOR, overrelief=BUTTON_RELIEF, warp_length=BUTTON_WARP_LENGTH):
    button = Button(frame, text=text, font=font, activeforeground=activeforeground, fg=text_color, bg=bg_color, bd=bd, cursor=cursor, overrelief=overrelief, wraplength=warp_length)
    return button
  
  @staticmethod
  def info(frame, text, font=FontType.normal(), activeforeground=TEXT_COLOR_LIGHT_BLUE, text_color=TEXT_COLOR_WHITE, bg_color=BG_COLOR_LIGHT_BLUE, bd=BUTTON_BD, cursor=BUTTON_CURSOR, overrelief=BUTTON_RELIEF, warp_length=BUTTON_WARP_LENGTH):
    button = Button(frame, text=text, font=font, activeforeground=activeforeground, fg=text_color, bg=bg_color, bd=bd, cursor=cursor, overrelief=overrelief, wraplength=warp_length)
    return button
  
  @staticmethod
  def light(frame, text, font=FontType.normal(), activeforeground=TEXT_COLOR, text_color=TEXT_COLOR, bg_color=BG_COLORLIGHT_GRAY, bd=BUTTON_BD, cursor=BUTTON_CURSOR, overrelief=BUTTON_RELIEF, warp_length=BUTTON_WARP_LENGTH):
    button = Button(frame, text=text, font=font, activeforeground=activeforeground, fg=text_color, bg=bg_color, bd=bd, cursor=cursor, overrelief=overrelief, wraplength=warp_length)
    return button
  
  @staticmethod
  def dark(frame, text, font=FontType.normal(), activeforeground=TEXT_COLOR, text_color=TEXT_COLOR_WHITE, bg_color=BG_COLOR_BLACK, bd=BUTTON_BD, cursor=BUTTON_CURSOR, overrelief=BUTTON_RELIEF, warp_length=BUTTON_WARP_LENGTH):
    button = Button(frame, text=text, font=font, activeforeground=activeforeground, fg=text_color, bg=bg_color, bd=bd, cursor=cursor, overrelief=overrelief, wraplength=warp_length)
    return button
