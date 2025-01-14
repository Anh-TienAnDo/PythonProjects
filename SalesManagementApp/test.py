from tkinter import *
from static.css.ButtonType import ButtonType
from static.css.LabelType import LabelType

# Tạo cửa sổ chính
root = Tk()
root.geometry("1920x1080")
root.title("Sales Management - MatHang")

# Tạo hai Frame (container)
frame1 = Frame(root, bg="lightblue", width=400, height=600)
frame2 = Frame(root, bg="lightgreen", width=400, height=600)

# Sử dụng pack để đặt các Frame trong cửa sổ chính
frame1.pack(side="left", fill="both", expand=True)
frame2.pack(side="right", fill="both", expand=True)

# Create a StringVar to associate with the label
text_var = StringVar()
text_var.set("Hello, World! anhdsdfhhuiu")
# Create the label widget with all options
label = Label(frame1,
              textvariable=text_var,  # Hiển thị văn bản
              anchor=CENTER,  # Canh lề văn bản
              bg="lightblue",  # Màu nền
              height=3,  # chiều cao của label
              width=30,  # độ rộng của label
              bd=3,  # độ rộng viền
              font=("Arial", 16, "bold"),  # Font and size of text
              cursor="hand2",  # Hình dạng con trỏ chuột
              fg="red",  # Text color
              padx=15,  # Padding on left and right
              pady=15,  # Padding on top and bottom
              justify=LEFT,  # văn bản canh trái
              relief=RAISED,  # kiểu viền
              wraplength=250  # Độ rộng tối đa của văn bản trước khi xuống dòng
              )
# Pack the label into the window
label.pack(pady=20)  # Add some padding to the top

label1 = LabelType.normal_blue_white(frame1, "Hello, World!")
label1.pack(pady=20)

label2 = LabelType.normal_red_white(frame1, "Hello, World!")
label2.pack(pady=50)



def button_clicked():
    print("Button clicked!")


text_btn = "Click Me!"
# Creating a button with specified options
button = Button(frame1,
                text=text_btn,  # Text on the button
                # command=button_clicked,  # gọi hàm khi click
                # activebackground="blue",  # Màu nền khi click
                activeforeground="red",  # Màu văn bản khi click
                anchor="center",  # Canh lề văn bản
                bd=3,  # độ rộng viền
                bg="red",  # Màu nền
                cursor="hand2",  # Hình dạng con trỏ chuột
                # disabledforeground="gray",  # Màu văn bản khi disable
                fg="white",  # Màu văn bản
                font=("Arial", 12),  # Font and size of text
                # height=2,  # chiều cao của button
                # highlightbackground="green",  # Màu viền khi focus
                highlightcolor="green",  # Màu viền khi focus
                # highlightthickness=4,  # Độ rộng viền khi focus
                # justify="center",  # Canh lề văn bản
                overrelief="raised",  # Kiểu viền khi hover
                # padx=5,  # Padding on left and right
                # pady=5,  # Padding on top and bottom
                # width=15,  # Độ rộng của button
                wraplength=100)  # Độ rộng tối đa của văn bản trước khi xuống dòng

button.config(command=lambda: button_clicked())  # Gán hàm xử lý sự kiện click
button.pack(padx=20, pady=20)

button1 = ButtonType.info(frame1, "Click Me!")
button1.pack(pady=20)

button2 = ButtonType.primary(frame1, "Click Me!")
button2.pack(pady=20)


# Entry # Hộp văn bản


def on_button_toggle():
    if var.get() == 1:
        print("Checkbutton is selected")
    else:
        print("Checkbutton is deselected")


# Creating a Checkbutton
var = IntVar()
checkbutton = Checkbutton(frame1, text="Enable Feature", variable=var,
                          onvalue=1, offvalue=0, command=on_button_toggle)

# Setting options for the Checkbutton
checkbutton.config(bg="lightgrey", fg="black", font=("Arial", 12),
                   selectcolor="white", relief="raised", padx=10, pady=5)

# Placing the Checkbutton in the window
checkbutton.pack(padx=40, pady=40)

# Thêm nội dung vào frame2 với Scrollbar
canvas = Canvas(frame2)
scrollbar_y = Scrollbar(frame2, orient="vertical", command=canvas.yview)
scrollbar_x = Scrollbar(frame2, orient="horizontal", command=canvas.xview)
scrollable_frame = Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar_y.set,
                 xscrollcommand=scrollbar_x.set)

# Hàm xử lý sự kiện lăn chuột


def on_mouse_wheel(event):
    if event.state & 0x0001:  # Shift key is held
        canvas.xview_scroll(int(-1*(event.delta/120)), "units")
    else:
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")


# Liên kết sự kiện lăn chuột với canvas
canvas.bind_all("<MouseWheel>", on_mouse_wheel)

# Hàm xử lý khi nhấn phím lên, xuống, trái, phải


def on_key_press(event):
    if event.keysym == "Up":
        canvas.yview_scroll(-1, "units")
    elif event.keysym == "Down":
        canvas.yview_scroll(1, "units")
    elif event.keysym == "Left":
        canvas.xview_scroll(-1, "units")
    elif event.keysym == "Right":
        canvas.xview_scroll(1, "units")


# Liên kết sự kiện phím với canvas
canvas.bind_all("<KeyPress-Up>", on_key_press)
canvas.bind_all("<KeyPress-Down>", on_key_press)
canvas.bind_all("<KeyPress-Left>", on_key_press)
canvas.bind_all("<KeyPress-Right>", on_key_press)

# Hàm xử lý khi nhấn nút "Xem chi tiết/Sửa"


def view_edit_item(row, col):
    print(f"Xem chi tiết/Sửa: Row {row}, Column {col}")

# Hàm xử lý khi nhấn nút "Xóa"


def delete_item(row, col):
    print(f"Xóa: Row {row}, Column {col}")


# Thêm các Label và Button vào scrollable_frame
for i in range(50):
    for j in range(10):
        label = Label(scrollable_frame, text=f"Row {i}, Column {j}")
        if i % 2 == 0:
            label.config(bg="lightblue")
        if j % 2 == 0:
            label.config(fg="red")

        label.grid(row=i, column=j, padx=5, pady=5)

    # Thêm nút "Xem chi tiết/Sửa"
    view_edit_button = Button(scrollable_frame, text="Xem chi tiết/Sửa",
                              command=lambda row=i, col=j: view_edit_item(row, col))
    view_edit_button.grid(row=i, column=10, padx=5, pady=5)

    # Thêm nút "Xóa"
    delete_button = Button(scrollable_frame, text="Xóa",
                           command=lambda row=i, col=j: delete_item(row, col))
    delete_button.grid(row=i, column=11, padx=5, pady=5)

canvas.pack(side="left", fill="both", expand=True)
scrollbar_y.pack(side="right", fill="y")
# scrollbar_x.pack(side="bottom", fill="x")


root.mainloop()
