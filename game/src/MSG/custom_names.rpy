default prefs.names = load_csv_names()
default prefs_substitution_name_table = name(None)
define config.say_menu_text_filter = replace_text

init -1 python:

    def load_csv_names():
        import csv
        prefs_names = {}
        with renpy.open_file("CUSTOM_NAMES.csv", encoding="utf8") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                if row['type'] == 'country':
                    id = row['id']
                    prefs_names[id] = {}
                    
                    prefs_names[id]['article'] = row['article']
                    prefs_names[id]['adjective'] = row['adjective'] 
                    prefs_names[id]['name'] = row['name']
                    prefs_names[id]['inhabitant'] = row['inhabitant']
                    if row['plural']:
                        prefs_names[id]['plural'] = row['plural']
                    else:
                        prefs_names[id]['plural'] = row['inhabitant'] + 's'

                    prefs_names[id]['desc'] = row['desc']
        return prefs_names

    def name(key_arg=None, sub_table=None):
        """
        usage: name('The Middle Kingdom') : gives the custom name for the middle kingdom
        name() returns the whole substitution list
        """
        global prefs

        default_names = load_csv_names()

        if key_arg is None: # initialization
            sub_table = {}
            for key,item in prefs.names.items():
                key_article = default_names[key]['article'].lower()
                key_adjective = default_names[key]['adjective'].lower()
                key_name = default_names[key]['name'].lower()

                # Empire
                sub_table[key_name] = item['name']

                # Holy Empire
                sub_table[key_adjective + ' ' + key_name] = item['adjective'] + ' ' + item['name']

                # The Empire
                sub_table[key_article + ' ' + key_name] = item['article'] + ' ' + item['name']
                
                # The Holy Empire
                sub_table[key_article + ' ' + key_adjective + ' ' + key_name] = item['article'] 
                if item['article'] :
                    sub_table[key_article + ' ' + key_adjective + ' ' + key_name] += ' ' 
                sub_table[key_article + ' ' + key_adjective + ' ' + key_name] += item['adjective']
                if item['adjective']:
                    sub_table[key_article + ' ' + key_adjective + ' ' + key_name] += ' ' 
                sub_table[key_article + ' ' + key_adjective + ' ' + key_name] += item['name']

                # imperial
                sub_table[item['inhabitant'].lower()] = item['inhabitant']
                # imperials
                sub_table[item['plural'].lower()] = item['plural']
            return sub_table
        
        if sub_table is None:
            sub_table = prefs_substitution_name_table

        key_lower = key_arg.lower()
        for item in sub_table:
            if key_lower in item:
                result = sub_table[key_lower]
                # Handle capitalizations
                if key_arg[0].isupper():
                    result = result[0].upper() + result[1:] # not just .capitalize() because it lowercases the rest of the letters
                    
                return result

        return f"NO KEY EXISTS FOR {key_arg}"

    def replace_text(s):
        # replace text to makes it *special* like bold or smth
        text_replace = ["CHESSMAN", "CHESSMEN","PAWN", "KNIGHT", "BISHOP", "ROOK", "QUEEN", "KING", "FAIRYLION", "CANNON", "GHOST", "JESTER"]
        # s = s.replace("NEUSUIT +", "{font=FONT_big}NEUSUIT{/font}{image=icon type + outline}")
        for i in text_replace:
            s = s.replace(i, "{font=FONT_big}"+i+"{/font}")
        return s

    def reset_names():
        global prefs_substitution_name_table
        prefs.names = load_csv_names()
        prefs_substitution_name_table = name(None)





#  ::::::::   ::::::::  :::::::::  :::::::::: :::::::::: ::::    ::: 
# :+:    :+: :+:    :+: :+:    :+: :+:        :+:        :+:+:   :+: 
# +:+        +:+        +:+    +:+ +:+        +:+        :+:+:+  +:+ 
# +#++:++#++ +#+        +#++:++#:  +#++:++#   +#++:++#   +#+ +:+ +#+ 
#        +#+ +#+        +#+    +#+ +#+        +#+        +#+  +#+#+# 
# #+#    #+# #+#    #+# #+#    #+# #+#        #+#        #+#   #+#+# 
#  ########   ########  ###    ### ########## ########## ###    #### 


style naming_nonselected_text is style_3d_big_txt:
    xalign 0.0
    size 50
    color "#bbb"

style naming_selected_text is style_3d_big_txt:
    xalign 0.0
    size 50
    color "#fff"

label l_rename(field1, *args, **kwargs):
    $ renpy.set_screen_variable('field_mode', 'article', screen='s_rename')
    $ prefs.names[field1]['article'] = renpy.input("{i}{size=-10}(optional) Article:\n", default=prefs.names[field1]['article'])
    $ renpy.set_screen_variable('field_mode', 'adjective', screen='s_rename')
    $ prefs.names[field1]['adjective']= renpy.input("{i}{size=-10}(optional) Adjective\n", default=prefs.names[field1]['adjective'])
    label .name:
    $ renpy.set_screen_variable('field_mode', 'name', screen='s_rename')
    $ prefs.names[field1]['name'] = renpy.input("{i}{size=-10}Name:\n", default=prefs.names[field1]['name'])
    if not prefs.names[field1]['name']:
        "This field cannot be empty."
        jump .name
    label .inhabitant:
    $ renpy.set_screen_variable('field_mode', 'inhabitant', screen='s_rename')
    $ i = renpy.input("{i}{size=-10}Single inhabitant:\n", default=prefs.names[field1]['inhabitant'])
    if i!= prefs.names[field1]['inhabitant']:
        $ prefs.names[field1]['inhabitant'] = i
        $ prefs.names[field1]['plural'] = prefs.names[field1]['inhabitant'] + "s"
    if not prefs.names[field1]['inhabitant']:
        "This field cannot be empty."
        jump .inhabitant
    $ renpy.set_screen_variable('field_mode', 'plural', screen='s_rename')
    $ prefs.names[field1]['plural'] = renpy.input("{i}{size=-10}(optional) Inhabitants plural form:\n", default=prefs.names[field1]['plural'])
    
    $ renpy.set_screen_variable('field_mode', None, screen='s_rename')
    $ prefs_substitution_name_table = name(None)
    return
    # jump start.loop


transform trs_insane_animation(end):
    easein 0.5 xalign end["xalign"] ypos end["ypos"]

screen s_rename():
    # screen to rename countries

    modal True

    default country_mode = None
    default rename_mode = False
    default field_mode = False
    default list_of_field1 = ['kingdom', 'empire', 'nation', 'dynasty']
    default list_of_field2 = ['article', 'adjective', 'name', 'inhabitant', 'plural']

    default scroll_x = -400
    default scroll_y = 100
    default scroll_z = 0.8
    default coordinates = {'kingdom':[1500,1000,2.0], 'empire':[880,-100,1.05], 'nation':[350,150,1.2], 'dynasty':[1070,400,1.1]}

    dismiss:
        action SetScreenVariable("country_mode", None), SetScreenVariable('scroll_z',0.8), SetScreenVariable('scroll_x',-400), SetScreenVariable('scroll_y',100), Return() # reset default values
        
    add "#4273ce"

    fixed:
        id 'map'
        xysize (0.4, 1.0)
        xalign 1.0
        add 'map_wide':
            at transform:
                ease 0.5 zoom scroll_z offset (scroll_x, scroll_y)

    add AlphaMask(Solid('#4f96d8'),'name_screen_mask', invert=True)

    text "{i}DATA BOOK" ypos 10 size 170  font "fonts/Venus+Cormier.otf" color "#fff"

    fixed: # BUTTONS
        xsize 0.6
        ypos 200
        vbox:
            for field1 in list_of_field1:
                hbox:
                    xalign 0
                    button at t_interactive:
                        # Button for the name of the country
                        if field1 == country_mode: # IF IS WAS SELECTED
                            style_prefix 'naming_selected'
                            action Call('l_rename', field1)
                        else: # FOR NON SELECTED COUNTRIES
                            style_prefix 'naming_nonselected'
                            action SetScreenVariable("country_mode", field1), SetScreenVariable('scroll_z',coordinates[field1][2]), SetScreenVariable('scroll_x',-coordinates[field1][0]), SetScreenVariable('scroll_y',-coordinates[field1][1])

                        has vbox
                        hbox:
                            text ">" color "#bbb"
                            for field2 in ['article', 'adjective', 'name']:
                                text prefs.names[field1][field2]:
                                    if country_mode == field1 and field_mode == field2:
                                        at t_highlight
                        
                        if country_mode == field1:               
                            fixed:
                                xpos 40
                                ysize 40
                                hbox:
                                    text "[prefs.names[field1]['inhabitant']]":
                                        if field_mode == 'inhabitant':
                                            at t_highlight
                                    text ", "
                                    text "[prefs.names[field1]['plural']]":
                                        if field_mode == 'plural':
                                            at t_highlight
                                
                                text " · rename?" color "#bbb" xalign 1.0

                
                # if rename_mode: old stuff where you would click on each field
                    #     frame:
                    #         background '#ff06'
                    #         has vbox
                    #         hbox:
                    #             xfill True
                    #             button at t_interactive:
                    #                 action Function(renpy.set_return_stack,[]), Call('l_rename', field1, 'article', '', default=prefs.names[field1]['article'])
                    #                 frame:
                    #                     vbox:
                    #                         text "{color=#666}(optional){/color}\nARTICLE" size 40 style 'default' font "fonts/DRAMEDYXY.ttf" xalign 0.5
                    #                         text prefs.names[field1]['article']
                    #             button at t_interactive:
                    #                 action Function(renpy.set_return_stack,[]), Call('l_rename', field1, 'adjective', '', default=prefs.names[field1]['adjective'])
                    #                 frame:
                    #                     vbox:
                    #                         text "{color=#666}(optional){/color}\nADJECTIVE" size 40 style 'default' font "fonts/DRAMEDYXY.ttf" xalign 0.5
                    #                         text prefs.names[field1]['adjective']
                    #             button at t_interactive:
                    #                 action Function(renpy.set_return_stack,[]), Call('l_rename', field1, 'name', '', default=prefs.names[field1]['name'])
                    #                 frame:
                    #                     vbox:
                    #                         text "{color=#c55}(mandatory){/color}\nNAME" size 40 style 'default' font "fonts/DRAMEDYXY.ttf"
                    #                         text prefs.names[field1]['name']
                    #         hbox:
                    #             xalign 0.5
                    #             xfill True
                    #             button at t_interactive:
                    #                 action Function(renpy.set_return_stack,[]), Call('l_rename', field1, 'inhabitant', '', default=prefs.names[field1]['inhabitant'])
                    #                 frame:
                    #                     vbox:
                    #                         text "{color=#c55}(mandatory)\n{/color}INHABITANT" size 40 style 'default' font "fonts/DRAMEDYXY.ttf" xalign 0.5
                    #                         text prefs.names[field1]['inhabitant']
                    #             button at t_interactive:
                    #                 action Function(renpy.set_return_stack,[]), Call('l_rename', field1, 'plural', '', default=prefs.names[field1]['plural'])
                    #                 frame:
                    #                     vbox:
                    #                         text "{color=#666}(optional){/color}\nPLURAL FORM" size 40 style 'default' font "fonts/DRAMEDYXY.ttf" xalign 0.5
                    #                         text prefs.names[field1]['plural']
                
                if country_mode == field1:
                    frame:
                        background '#000a'
                        padding 50,50
                        margin 20,20,20,20
                        text "{i}[prefs.names[country_mode]['desc']!i]" color '#fff' size 40 font 'fonts/Venus+Plomb.otf' line_spacing 10


        
    button at t_interactive:
        align 1.0, 1.0
        text "RESET" style 'style_3d_big_txt'
        
        action Confirm('Reset all names?', Function(reset_names), Hide('confirm'))

    button at t_interactive:
        align 0, 1.0
        text "BACK" style 'style_3d_big_txt'
        
        action Hide(None, dissolve_fast)