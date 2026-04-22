screen s_tooltip_test():
    $ tooltip = GetTooltip()
    $ print(tooltip)

    text ("tooltip: [tooltip!r]") xalign 0.5 yalign 0.05

    draggroup:
        drag:
            draggable False # if True, no problem
            clicked f_function
            tooltip "hello"
            xysize (400, 400)
            pos (300, 200)
            fixed:
                add "#f005"
                text "drag" xalign 0.5 yalign 0.5

init python:
    def f_function():
        return