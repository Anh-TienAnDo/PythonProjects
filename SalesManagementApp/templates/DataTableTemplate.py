from tkinter import Frame, Canvas, Scrollbar
from contants import *


class DataTableTemplate:
    def __init__(self, frame: Frame):
        self.frame = frame
        # Thêm nội dung vào frame2 với Scrollbar
        self.canvas = Canvas(self.frame)
        self.scrollbar_y = Scrollbar(
            self.frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar_x = Scrollbar(
            self.frame, orient="horizontal", command=self.canvas.xview)
        self.scrollable_frame = Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar_y.set,
                              xscrollcommand=self.scrollbar_x.set)

        # Liên kết sự kiện lăn chuột với self.canvas
        self.canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)

        # Liên kết sự kiện phím với self.canvas
        self.canvas.bind_all("<KeyPress-Up>", self.on_key_press)
        self.canvas.bind_all("<KeyPress-Down>", self.on_key_press)
        self.canvas.bind_all("<KeyPress-Left>", self.on_key_press)
        self.canvas.bind_all("<KeyPress-Right>", self.on_key_press)

    # Hàm xử lý sự kiện lăn chuột
    def on_mouse_wheel(self, event):
        if event.state & 0x0001:  # Shift key is held
            self.canvas.xview_scroll(int(-1*(event.delta/120)), "units")
        else:
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    # Hàm xử lý khi nhấn phím lên, xuống, trái, phải
    def on_key_press(self, event):
        if event.keysym == "Up":
            self.canvas.yview_scroll(-1, "units")
        elif event.keysym == "Down":
            self.canvas.yview_scroll(1, "units")
        elif event.keysym == "Left":
            self.canvas.xview_scroll(-1, "units")
        elif event.keysym == "Right":
            self.canvas.xview_scroll(1, "units")
            
    def get_canvas(self):
        return self.canvas
      
    def get_scrollbar_y(self):
        return self.scrollbar_y
      
    def get_scrollbar_x(self):
        return self.scrollbar_x
      
    def get_scrollable_frame(self):
        return self.scrollable_frame
