#
#   THIS FILE HANDLES:
#       > THE SAY STATEMENTS CALLBACK (which changes how characters at put forward or backward)
#       > layers stuff
#       > custom show, hide, scene statements
#       > configurations on how images are displayed by default (like bg zorder -10 so it's always behind the chessboard)
#
# If you modify a character with a special zorder (anything besides 0 or 1), it wont update it's zorder
# this allows to display characters that are behind each others
default AUTO_CENTER_ON_SPEAK_CHAR_BATTLEFIELD = True # if True, it centers on character speaking when they are present on the battlefield
default STAGE_SCENE = [[],[]] # this holds the images of characters currently on the scene speaking, it's left right.
default SPEAKING_CHAR = None # used to track who is speaking for the shadow
default MOVE_SPEAK_CHAR_FORWRD = [True, True] # if True, on callback when a character speaks, it moves in front (default).
# set to false when someone is behind nunnally's wheelchair for example

init python:
    config.tag_zorder["bg"] = -10 # this makes bg always be on master with -10 zorder

init -1 python:
    def STAGE_SCENE_callback(who, interact=True, *args, **kwargs):
        """
        callback on say statements
        This does the stage mechanic where characters goes forward if they talk etc.
        """
        global SPEAKING_CHAR

        # SI LE CHAR EST SUR LE CHESSBOARD, center around it
        if AUTO_CENTER_ON_SPEAK_CHAR_BATTLEFIELD and chess and hasattr(who, 'char_on_battlefield'):
            piece = who.char_on_battlefield
            if piece in chess.get_pieces():
                chess.ui['camera'].center_on(piece.pos, 0.5)
        
        if type(who) is str: return (), {'interact' : interact} # if its not a character, ignore

        tag = who.image_tag
        if tag in STAGE_SCENE[0]:
            side = 0
        elif tag in STAGE_SCENE[1]:
            side = 1
        else: # a character not on stage
            renpy.hide('speaking_char')
            return (), {'interact' : interact}
            SPEAKING_CHAR = None

        stage_insert_char(tag, side)
        renpy.pause(0.1)
        if SPEAKING_CHAR != tag:
            zorder = get_new_zorder(tag, 1)
            renpy.show(tag, [t_speaking_sprite(side, STAGE_SCENE[side].index(tag))], zorder=zorder-1, tag='speaking_char') # show the talking char
            SPEAKING_CHAR = tag

        return (), {'interact' : interact}

    def custom_show(name, at_list=[], *args, **kwargs):
        global SPEAKING_CHAR

        SPEAKING_CHAR = None
        renpy.hide('speaking_char')
        renpy.with_statement(None)

        # default behavior, if not LEFT or RIGHT in transforms
        if not left in at_list and not right in at_list:
            renpy.show(name, at_list=at_list, *args, **kwargs)
            return

        index = 0 if at_list == [left] else 1
        tag = " ".join(name)

        if 'zorder' in kwargs:
            zorder = kwargs['zorder']
        else:
            zorder = 1
        stage_insert_char(tag, index, zorder)
            
    def custom_hide(tag, *args, **kwargs):
        for arg in args:
            print("arg:" + arg)
        for arg in kwargs:
            print("karg:" + arg)
        renpy.hide(tag, *args, **kwargs)

        if type(tag) == tuple: # hide img, img becomes a tuple usually
            tag = " ".join(tag)

        if renpy.last_say().who and renpy.last_say().who.image_tag == tag:
            SPEAKING_CHAR = None
            renpy.hide('speaking_char')
        if tag in STAGE_SCENE[0]:
            MOVE_SPEAK_CHAR_FORWRD[0] = True
            STAGE_SCENE[0].remove(tag)
            renpy.with_statement(moveoutleft)
            if len(STAGE_SCENE[0]) > 0: # if we hide someone but theres someone else, they get in front
                renpy.show(STAGE_SCENE[0][0], at_list=[left], zorder=0)
                renpy.with_statement(None)
        elif tag in STAGE_SCENE[1]:
            MOVE_SPEAK_CHAR_FORWRD[1] = True
            STAGE_SCENE[1].remove(tag)
            renpy.with_statement(moveoutright)
            if len(STAGE_SCENE[1]) > 0:
                renpy.show(STAGE_SCENE[1][0], at_list=[right], zorder=0)
                renpy.with_statement(None)
    
    # you can do
    # HIDE ONLAYER CHARACTERS or
    # SCENE ONLAYER CHARACTERS
    # to empty the stage_scene
    def custom_scene(layer):
        """
        scene onlayer characters: hide all chars from scene
        """
        global STAGE_SCENE, MOVE_SPEAK_CHAR_FORWRD, AUTO_CENTER_ON_SPEAK_CHAR_BATTLEFIELD
        renpy.scene(layer)
        if layer is None or layer == 'master' or layer == 'characters':
            MOVE_SPEAK_CHAR_FORWRD = [True, True]
            AUTO_CENTER_ON_SPEAK_CHAR_BATTLEFIELD = True
        if layer is None or layer == 'master':
            STAGE_SCENE = [[],[]]
        elif layer == 'characters':
            for side in STAGE_SCENE:
                while side:
                    custom_hide(side[0])
            STAGE_SCENE = [[],[]]

    #   Insert the char in the STAGE_SCENE,
    #   then render every char on the scene
    def stage_insert_char(tag, side, zorder=1):
        if any(pilot.id == tag for pilot in DEAD_OR_DESERT):
            return
        on_scene = True
        # remove it from both side
        if MOVE_SPEAK_CHAR_FORWRD[side]:
            if tag in STAGE_SCENE[0]: STAGE_SCENE[0].remove(tag)
            elif tag in STAGE_SCENE[1]: STAGE_SCENE[1].remove(tag)
            else: on_scene = False

            STAGE_SCENE[side].insert(0, tag) # insert it as first element
            if len(STAGE_SCENE[side])>=3:
                renpy.hide(STAGE_SCENE[side][2])
                STAGE_SCENE[side] = STAGE_SCENE[side][:2] # only keep 2 chars max

        # RENDER EVERY CHAR
        # when you refactor / simplify the code, be careful sometimes rollback messes up the transform
        # test map 1.00 to check
        for index, char in enumerate(STAGE_SCENE[side]):
            if char == tag:
                if not on_scene:
                    renpy.show(tag, at_list=[t_first_time_sprite(side)], zorder=zorder)
                else: # just push it up
                    zorder = get_new_zorder(tag, 1)
                    renpy.show(tag, [t_default_color, left_or_right(side, index)], zorder=zorder)
            else: 
            # push old chars
                zorder = get_new_zorder(char, 0)
                renpy.show(char, at_list=[t_shadow_sprite, left_or_right(side, index)], zorder=zorder)
        renpy.with_statement(None)

    # return new_value if the tag has a zorder of 0 or 1
    # otherwise return the custom zorder
    def get_new_zorder(tag, new_value):
        zorder = dict(renpy.get_zorder_list('master')).get(tag, new_value)
        return new_value if zorder in (0, 1) else zorder

define config.say_arguments_callback = STAGE_SCENE_callback
define config.show = custom_show
define config.hide = custom_hide
define config.scene = custom_scene

## xalign depending on 3 args: SIDE, INDEX and is_alone?
##                \ SIDE |     left        right
##  index   alone? \     |
##    0      yes                0.05        0.95
##    0      no                 0.1         0.9
##    1      yes                -.1         1.1
##    1      no                 -.1         1.1

init python:
    def get_sprite_xalign(side, index):
        is_alone = int(len(STAGE_SCENE[side]) == 1)
        return (1 - index) * ((0.1 + 0.8*side) + is_alone * (2*side - 1) * 0.05) + index * (-0.1 + 1.2*side)

transform t_first_time_sprite(side): # 0 = left, 1 = right
    yzoom 0.6
    xzoom 0.6 * (side-0.5)*2
    xalign float(side)
    matrixcolor IdentityMatrix()
    ease 0.2 xalign get_sprite_xalign(side, 0)

transform t_default_color():
    matrixcolor IdentityMatrix()

transform t_shadow_sprite:
    matrixcolor BrightnessMatrix(-0.2) * SaturationMatrix(0.4)

transform left_or_right(side, index):
    xzoom 0.6 * (side*2 - 1)
    ease 0.1 xalign get_sprite_xalign(side, index)

transform left(): # for character sprite talks
    matrixcolor IdentityMatrix()
    xzoom -0.6
    ease 0.1 xalign get_sprite_xalign(0, 0)
    
transform right(): # for character sprite talks
    matrixcolor IdentityMatrix()
    xzoom 0.6
    ease 0.1 xalign get_sprite_xalign(1, 0)

transform t_step_back(side): # 0 = left, 1 = right
    ease 0.1 xalign get_sprite_xalign(side, 1)

transform t_speaking_sprite(side, index):
    alpha 0.5
    blur 10
    xzoom 0.6 * (side-0.5)*2
    yzoom 0.6
    yoffset 20
    matrixcolor ColorizeMatrix("#000", "#000")
    xalign -10.0
    pause 0.1 xalign get_sprite_xalign(side, index)
    ease 0.1 xalign get_sprite_xalign(side, index) - 0.01

# A new detached layer to hold the contents of a broadcast.
# usage:
# show coin onlayer l_chess at chess.t_layer('e4')
define config.detached_layers += [ "l_chess" ]
image layer_chess_overlay = Layer("l_chess", clipping=False)


# custom animal crossing voice

# def splurt:
#     if event == "show":
#         beeps = 0
#         while beeps < 50:
#             random stuff
#             if/elif stuff
#             beeps +=1
#     elif event == "slow_done":
#         stop the sound cause Im too lazy to type it all out

# define e = Character("Schlorp", callback=splurt )