default prefs.style.pieces = "merida"
default persistent.style_colors = ["#fff","#e9d7b4", "#b18967", "#000"]
default prefs.style.gradient_color = ['#ffffe2', '#dfe3f8']
define prefs.style.board = None

# Acier < Plomb < Carrare < Martre < Cormier
define config.font_name_map["FONT_small"] = FontGroup().add("Venus+Acier.otf", 0x0000, 0xffff)
define config.font_name_map["FONT_normal"] = FontGroup().add("Venus+Plomb.otf", 0x0000, 0xffff)
define config.font_name_map["FONT_bold"] = FontGroup().add("Venus+Carrare.otf", 0x0000, 0xffff)
define config.font_name_map["FONT_big"] = FontGroup().add("Venus+Martre.otf", 0x0000, 0xffff)

define config.font_name_map["FONT_title"] = FontGroup().add("Venus+Cormier.otf", 0x0000, 0xffff)

define g.colors = {'bluesky':'#00c3ff', 'magenta':'#f64dff', 'green':"#23c634"}

############################
#
# TRANSITION
#
############################

define pointillisme = ImageDissolve("misc/mask/mask_pointillisme.webp", 0.5)
define transition_bars = ImageDissolve("misc/mask/transition_bars.webp", 2, time_warp=_warper.easein)
define transition_bars_fast = ImageDissolve("misc/mask/transition_bars.webp", 1)
define transition_queen = ImageDissolve("misc/mask/transition_queen.webp", 1)

define dissolve_fast = Dissolve(0.15)
init python:
    define.move_transitions("move", 0.1, time_warp=_warper.pause, in_time_warp=_warper.pause, out_time_warp=_warper.ease)

#              ███  █████████  ███████████ █████ █████ █████       ██████████
#            ███░  ███░░░░░███░█░░░███░░░█░░███ ░░███ ░░███       ░░███░░░░░█
#          ███░   ░███    ░░░ ░   ░███  ░  ░░███ ███   ░███        ░███  █ ░ 
#        ███░     ░░█████████     ░███      ░░█████    ░███        ░██████   
#      ███░        ░░░░░░░░███    ░███       ░░███     ░███        ░███░░█   
#    ███░          ███    ░███    ░███        ░███     ░███      █ ░███ ░   █
#  ███░           ░░█████████     █████       █████    ███████████ ██████████
# ░░░              ░░░░░░░░░     ░░░░░       ░░░░░    ░░░░░░░░░░░ ░░░░░░░░░░ 

style default:
    font "FONT_bold"
    size 50
    text_align 0.5 
    
style big_numbers:
    font 'FONT_bold'
    size 40
    anchor (1.0, 1.0)
    pos(100, 105) 
    color "#fff"
    outlines [ (4, "#555", 0, 0) ]

style style_info_field:
    font "FONT_normal" color "#000000" size 35 outlines [ (4, "#ffffff", 0, 0) ] align(0.5, 0.5)

style style_3d_big_txt:
    font "FONT_title" size 60 color "#ffffff" outlines [ (3, "#000000", 0, 3) ]
style style_3d_big_txt_vertical:
    font "FONT_title" size 60 color "#ffffff" outlines [ (4, "#000000", 4, 0) ]
style style_3d_txt:
    font "FONT_title" size 35 color "#ffffff" outlines [ (3, "#000000", 0, 3) ]
style style_purple_text:
    font "FONT_bold" size 50 outlines [ (3, "#540c4d", 0, 0) ] color COLOR_HIGHLIGHT()
style style_big_white_text:
    font "FONT_title" color "#ffffff" size 40 textalign 1.0

style style_text_handwritten:
    font "fonts/Trattatello.ttf"

style sty_btn_button:
    background Frame('gui/bubble_frame.webp', 55, 55, 40, 40)
    padding (30,30)
    margin (5,5)

style sty_btn_text:
    font 'FONT_title'
    yoffset 5
    color "#ffffff" outlines [ (4, "#000000", 0, 1) ]
    align (0.5,0.5)

#
#   used in s_chess
#

transform t_low_health:
    matrixcolor ColorizeMatrix("#000", "#fff")
    block:
        ease 0.5 matrixcolor ColorizeMatrix("#c22323", "#fdd")
        pause 0.5
        ease 0.3 matrixcolor ColorizeMatrix("#000", "#fff")
    repeat

transform t_highlight:
    matrixcolor ColorizeMatrix("#000", "#fff")
    block:
        ease 0.5 matrixcolor ColorizeMatrix("#a46134", "#ff8")
        pause 0.5
        ease 0.3 matrixcolor ColorizeMatrix("#000", "#fff")
    repeat

transform t_flashing:
    block:
        ease 0.5 alpha 1.0
        pause 0.5
        ease 0.3 alpha 0.0
    repeat
    on hide:
        ease 0.2 alpha 0

# transform t_interactive:
#     on idle:
#         matrixcolor IdentityMatrix()
#     on hover:
#         matrixcolor ColorizeMatrix("#700", "#ffa")
#     on insensitive:
#         matrixcolor ColorizeMatrix("#333", "#777")
transform t_interactive:
    on idle:
        matrixcolor IdentityMatrix()
    on hover:
        matrixcolor ColorizeMatrix("#644", "#fff5aa")
    on insensitive:
        matrixcolor ColorizeMatrix("#333", "#777")