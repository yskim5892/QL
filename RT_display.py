from tkinter import *

def coordinate_transform(w, h, map_x, map_w, map_h):
    margin = 1/6
    return (w * margin + map_x[0] * ((1- 2 * margin) * w  /  map_w), h * (1 -  margin) - map_x[1] * ((1- 2 * margin) * h / map_h))


def RT_display(step, map, dest, state_history, action_history):
    window = Tk()
    w = 900
    h = 900
    window.title("Racetrack" + str(step))
    window.geometry("900x900+100+100")
    window.resizable(False, False)
    canvas = Canvas(window, relief='solid', bd=2)

    map_w = 0
    map_h = 0
    for x in map.keys():
        if x[0] > map_w:
            map_w = x[0]
        if x[1] > map_h:
            map_h = x[1]

    pixel_w = coordinate_transform(w, h, (1, 0), map_w, map_h)[0] - coordinate_transform(w, h, (0, 0), map_w, map_h)[0]
    pixel_h = coordinate_transform(w, h, (0, 1), map_w, map_h)[1] - coordinate_transform(w, h, (0, 0), map_w, map_h)[1]

    pixels = dict()
    for x in map.keys():
        coord = coordinate_transform(w, h, x, map_w, map_h)
        pixels[x] = canvas.create_polygon(coord[0], coord[1], coord[0] + pixel_w, coord[1], coord[0] + pixel_w, coord[1] + pixel_h, coord[0], coord[1] + pixel_h, fill='white', outline='black')

    canvas.itemconfig(pixels[dest], fill='blue')

    def recolor(prev_state, state):
        if(prev_state is not None):
            canvas.itemconfig(pixels[prev_state.x], fill='white')
        try:
            canvas.itemconfig(pixels[state.x], fill='red')
        except(KeyError):
            coord = coordinate_transform(w, h, state.x, map_w, map_h)
            canvas.create_polygon(coord[0], coord[1], coord[0] + pixel_w, coord[1], coord[0] + pixel_w, coord[1] + pixel_h, coord[0], coord[1] + pixel_h, fill='red', outline='black')

    prev_state = None
    i = 0
    canvas.pack(fill=BOTH, expand=1)
    for state in state_history:
        if(state.is_terminal):
            print(state)
        else:
            print(state, action_history[i])
        window.after(500 * (i + 1), recolor, prev_state, state)
        prev_state = state
        i += 1
    window.mainloop()