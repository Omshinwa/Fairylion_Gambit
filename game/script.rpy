default chess = Chess_control((8,8))
default engine = Engine()

label main_menu:
    return
    if renpy.can_load('current_run', test=False):
        $ renpy.load('current_run') # delete_save()     if a var is lacking
    else:
        return

# Q:
# why didnt i just use the persistent feature?
# A:
# to save the pilots' stats between runs.
init python:
    "Creating new save."
    if not hasattr(store, 'lelouch'):
        init_pilots()


label start:
    $ load_callback()
    scene
    scene onlayer screens
    if not renpy.can_load('current_run', test=False): # init
        "Creating new save."
        $ init_pilots()
    scene onlayer screens
    show screen main_menu
    with Dissolve(.25)

    python: # restore health
        for pilot in PILOTLIST:
            globals()[pilot].health = globals()[pilot].max_health

    $ renpy.take_screenshot()
    if config.developer:
        'saving'
    $ renpy.save('current_run')
    label .loop:
    call screen s_pauseScreen(True)
    jump .loop