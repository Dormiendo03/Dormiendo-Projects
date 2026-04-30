from tkinter import *

window = Tk()
window.title("Elementary House Typeshi")
window.geometry("400x300")


Canvas = Canvas(window, width=400, height=300)
Canvas.pack()

# House base
Canvas.create_rectangle(90, 160, 170, 210, fill="lightblue")
# Right side of house base
Canvas.create_polygon(171, 159,
210, 139,
210, 185, 
171, 210, fill="#6E7FFF")

# Door
Canvas.create_rectangle(120, 180, 140, 210, fill="#CA814C")

# Windows 
Canvas.create_polygon(180, 165,
200, 154,
201, 170,
181, 182, fill = "#D33E3E")

# Roof
Canvas.create_polygon( 130, 110, 90, 160, 170, 160, fill="#DC1A00") #front roof
Canvas.create_polygon(130, 110, 
190, 110, 
210, 140, 
170, 160, fill="#C41104")  # Right side of house roof

#fences
Canvas.create_line(50, 230, 350, 230, fill="black", width=2) # fence base
for x in range(50, 351, 20):
    Canvas.create_line(x, 220, x, 250, fill="black", width=2) # vertical fence posts



# The Sun
Canvas.create_oval(300, 50, 350, 100, fill="yellow")  # Sun
# 8 sun rays
Canvas.create_line(325, 25, 325, 45, fill="black", width=2)  # Ray 1 top center
Canvas.create_line(325, 105, 325, 125, fill="black", width=2)  # Ray 2 bottom center
Canvas.create_line(295, 75, 275, 75, fill="black", width=2)  # Ray 3 left center
Canvas.create_line(355, 75, 375, 75, fill="black", width=2)  # Ray 4 right center
Canvas.create_line(305, 55, 285, 35, fill="black", width=2)  # Ray 5 top left
Canvas.create_line(345, 55, 365, 35, fill="black", width=2)  # Ray 6 top right
Canvas.create_line(305, 95, 285, 115, fill="black", width=2)  # Ray 7 bottom left
Canvas.create_line(345, 95, 365, 115, fill="black", width=2)  # Ray 8 bottom right


Canvas.create_text(290, 265, text="Dormiendo, Harvey L.", font=("Arial", 12, "bold"), fill="black")
Canvas.create_text(290, 290, text="BSIT-3PM.", font=("Arial", 12, "bold"), fill="black")



window.mainloop()