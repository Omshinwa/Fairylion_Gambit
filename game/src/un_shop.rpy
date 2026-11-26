# THE UNITED NATIONS' SHOP (story mode). See Robots in ai_prompt/prompt.md.
#   - Click the United Nations on the world map (s_map_select in maps/s_map_select.rpy), once the random battles started.
#   - Money: g.money, from the won random battles (STORY_MONEY_PER_WIN in src/story_battles.rpy).
#   - CHESSMEN at their chess value. A bought robot joins the player's robots, ROBOTS (src/story_battles.rpy).
#   - Upgrades for the player's robots (src/robot_upgrades.rpy): the RESEARCH LAB. Not for the KING: it always fights.
# Looks like the roguelite's shop (s_shop_rogue in src/roguelike_events.rpy).

define UN_ROBOT_PRICE = {'p': 1, 'n': 3, 'b': 3, 'r': 5, 'q': 9}
define UN_UPGRADE_PRICE = {'tech': 6}

init python:
    def un_shop_open():
        """The shop opens with the random battles (and the player's robots)."""
        return not rogue and story_random_part()

    def un_buy_robot(fen):
        price = UN_ROBOT_PRICE[fen]
        if g.money < price:
            return
        g.money -= price
        ROBOTS.append(story_new_robot(fen))
        renpy.play('sound/rogue/ghost.wav', channel='audio')

    def un_can_upgrade(robot, upgrade):
        return robot.type != '#' and not robot_has_upgrade(robot, upgrade)

    def un_buy_upgrade(robot, upgrade):
        price = UN_UPGRADE_PRICE[upgrade]
        if g.money < price or not un_can_upgrade(robot, upgrade):
            return
        g.money -= price
        robot_add_upgrade(robot, upgrade)
        renpy.play('sound/misc/boost.wav', channel='audio')

label l_un_shop:
    play audio 'sound/rogue/shop.wav'
    $ renpy.retain_after_load() # a save made in the shop keeps what was bought
    call screen s_shop_un
    return

# the player's money, with the roguelite's coin
screen s_money(size=50):
    hbox:
        spacing 10
        fixed: # trs_coin turns the coin around its center
            xysize (size*2, size*2)
            add Transform("coin", xysize=(size*2, size*2), pos=(size, size)) at trs_coin
        text str(g.money) font "fonts/Venus+Cormier.otf" color "#ffffa0" outlines [ (5, "#a98a46", 0, 2) ] size size yalign 0.5

screen s_shop_un():
    zorder 2
    modal True

    fixed:
        at transform:
            on show:
                ypos -1.0
                easein 0.5 ypos 0
            on hide:
                ypos 0
                easeout 0.5 ypos -1.0

        add 'shop_bg' nearest True xysize (1.0, 1.0)
        text name('The united nations').upper() color "#ff0" font 'Lithops-Regular.otf' xalign 0.5 ypos 50 size 120
        fixed:
            pos (60, 60)
            use s_money()

        vbox:
            xalign 0.5
            ypos 250
            spacing 20

            text _("CHESSMEN") style 'style_3d_txt' xalign 0.5
            hbox:
                xalign 0.5
                spacing 40
                for fen, price in UN_ROBOT_PRICE.items():
                    button at t_interactive:
                        sensitive g.money >= price
                        action Function(un_buy_robot, fen)
                        vbox:
                            fixed:
                                xysize (180, 180)
                                add f"white {c.FEN_TO_PIECE[fen]} merida":
                                    blur 10 matrixcolor BrightnessMatrix(-1) zoom 1.1 alpha 0.5 align (0.5, 0.5)
                                add f"white {c.FEN_TO_PIECE[fen]} merida" align (0.5, 0.5)
                            text _("COST {size=+20}[price]") style 'style_3d_txt' xalign 0.5

            null height 30
            $ upgrade_name, upgrade_desc = ROBOT_UPGRADES['tech']
            text _("{} (COST {}): {}").format(__(upgrade_name), UN_UPGRADE_PRICE['tech'], __(upgrade_desc)) style 'style_3d_txt' xalign 0.5
            text _("Click one of your CHESSMEN to give it one.") style 'style_big_white_text' size 30 xalign 0.5
            hbox:
                xalign 0.5
                xmaximum 1600
                box_wrap True
                spacing 10
                for robot in ROBOTS:
                    button at t_interactive: # greyed: the KING, or it has one already
                        xysize (120, 140)
                        sensitive un_can_upgrade(robot, 'tech') and g.money >= UN_UPGRADE_PRICE['tech']
                        action Function(un_buy_upgrade, robot, 'tech')
                        add f"white {c.FEN_TO_PIECE[DEFAULT_ROBOT[robot.type]]} merida" xysize (110, 110) xalign 0.5
                        if robot_has_upgrade(robot, 'tech'):
                            text _("LAB") style 'style_3d_big_txt' size 30 align (0.5, 1.0)

        textbutton _("LEAVE") at t_interactive:
            align (0.97, 0.95)
            text_style 'style_3d_big_txt'
            action Return()
