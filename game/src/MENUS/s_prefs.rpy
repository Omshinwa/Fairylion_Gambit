
style _console_text:
    font "DejaVuSansMono.ttf"
    prefer_emoji False

## Preferences screen ##########################################################
##
## The preferences screen allows the player to configure the game to better suit
## themselves.
##
## https://www.renpy.org/doc/html/screen_special.html#preferences

screen s_prefs():

    tag menu

    use game_menu(_("Preferences"), scroll="viewport"):

        vbox:

            hbox:
                box_wrap True

                if renpy.variant("pc") or renpy.variant("web"):

                    vbox:
                        style_prefix "radio"
                        label _("Board layout")
                        textbutton _("Left") action SetField(prefs, "battlefield_layout_left", True)
                        textbutton _("Right") action SetField(prefs, "battlefield_layout_left", False)

                vbox:
                    # style_prefix "check"
                    style_prefix "radio"
                    label _("Piece style")
                    textbutton _("Merida") action SetVariable('prefs.style.pieces', 'merida')
                    textbutton _("Internet") action SetVariable('prefs.style.pieces', 'internet')
                    textbutton _("Robot") action SetVariable('prefs.style.pieces', 'robot')

                vbox:
                    # style_prefix "check"
                    style_prefix "radio"
                    label _("BG colors")
                    
                    hbox:
                        spacing 50
                        default color_field = [['#aaa', '#555'], ["#ffccff","#0000ff"], ['#ffffe2', '#dfe3f8']]
                        for i in color_field:
                            button at t_interactive:
                                xsize 100
                                vbox:
                                    add Solid(i[0]) xysize(50,50)
                                    add Solid(i[1]) xysize(50,50)
                                action SetDict(prefs.style.gradient_color, 0, i[0]), SetDict(prefs.style.gradient_color, 1, i[1])

                ## Additional vboxes of type "radio_pref" or "check_pref" can be
                ## added here, to add additional creator-defined preferences.

            null height (4 * gui.pref_spacing)

            # hbox:
            #     style_prefix "slider"
            #     box_wrap True
