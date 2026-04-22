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

transform t_interactive:
    on idle:
        matrixcolor IdentityMatrix()
    on hover:
        matrixcolor ColorizeMatrix("#644", "#fff5aa")
    on insensitive:
        matrixcolor ColorizeMatrix("#333", "#777")

init python:
    # whatever, TODO
    class AmbientMatrix(ColorMatrix):
        def __init__(self, dark_color, light_color):
            self.dark_color = Color(color)
            self.light_color = Color(color)

        def __call__(self, other, done):
            if type(other) is not type(self):
                r, g, b = self.color.rgb
                a = self.color.alpha
            else:
                oldr, oldg, oldb = other.color.rgb
                olda = other.color.alpha
                r, g, b = self.color.rgb
                a = self.color.alpha

                r = oldr + (r - oldr) * done
                g = oldg + (g - oldg) * done
                b = oldb + (b - oldb) * done
                a = olda + (a - olda) * done

            r *= a
            g *= a
            b *= a

            return Matrix([ 1, 0, 0, r,
                            0, 1, 0, g,
                            0, 0, 1, b,
                            0, 0, 0, 1 ])

init python:

    renpy.register_shader("gradient_map",
        variables="""
            uniform vec4 u_gm0;
            uniform vec4 u_gm1;
            uniform vec4 u_gm2;
            uniform vec4 u_gm3;
            uniform vec4 u_gm4;
            uniform vec4 u_gm5;
            uniform vec4 u_gm6;
            uniform vec4 u_gm7;
            uniform float u_gm_n;
        """,
        fragment_300="""
            vec4 src = texture2D(tex0, v_tex_coord.xy);
            float a = src.a;
            vec3 rgb = (a > 0.001) ? src.rgb / a : vec3(0.0);
            float lum = clamp(dot(rgb, vec3(0.299, 0.587, 0.114)), 0.0, 1.0);

            vec4 stops[8];
            stops[0] = u_gm0; stops[1] = u_gm1;
            stops[2] = u_gm2; stops[3] = u_gm3;
            stops[4] = u_gm4; stops[5] = u_gm5;
            stops[6] = u_gm6; stops[7] = u_gm7;

            int n = int(u_gm_n);
            float fn = float(n - 1);
            vec4 mapped = stops[0];
            bool found = false;

            for (int i = 0; i < 7; i++) {
                if (!found && i < n - 1) {
                    float t0 = float(i) / fn;
                    float t1 = float(i + 1) / fn;
                    if (lum >= t0 && lum < t1) {
                        mapped = mix(stops[i], stops[i + 1], (lum - t0) / (t1 - t0));
                        found = true;
                    }
                }
            }
            if (!found) {
                mapped = stops[n - 1];
            }

            gl_FragColor = vec4(mapped.rgb * a, a);
        """
    )

    def GradientMap(d, colors):
        """
        Apply a gradient map to displayable d.
        Pass any list of 2-8 colors; lum=0 maps to colors[0], lum=1 to colors[-1].

            image foo = GradientMap("sprite.png", ["#1a1a2e", "#e94560", "#fff"])
            add GradientMap("icon.webp", ["#000", "#ff6633"])
        """
        if colors == 'neon':
            colors = ["#000", "#2600ff", "#b61de1", "#fd4bb3", "#ff7589", "#ffa955", "#ffff00", "#fff"]
        elif colors == 'pale god':
            colors = ["#000","#6b6668", "#808688", "#99a2a8", "#c4beb8", "#dbcdc6", "#f6edea", "#fff"]
        elif colors == 'pink':
            colors = ["#110116", "#4b0e2b", "#79536d", "#b2719b","#ed91cc", "#f6c9e7", "#fbedc5"]
        elif colors == 'noir':
            colors = ["#000102", "#201524", "#953d39", "#d54f48"]


        n = min(max(2, len(colors)), 8)
        stops = [(Color(c)[0]/255.0, Color(c)[1]/255.0, Color(c)[2]/255.0, Color(c)[3]/255.0) for c in colors[:n]]
        while len(stops) < 8:
            stops.append(stops[-1])
        return Transform(d,
            shader="gradient_map",
            u_gm0=stops[0], u_gm1=stops[1],
            u_gm2=stops[2], u_gm3=stops[3],
            u_gm4=stops[4], u_gm5=stops[5],
            u_gm6=stops[6], u_gm7=stops[7],
            u_gm_n=float(n),
        )