"""
Save system:
autosaves before every battle start and when getting to overworld, only keeps 1 save for each
save_name is formatted 'Chapter 1-0' and is used to check for uniqueness
A local _checkpoint saves exists. It is loaded when the played loses. It saves on the last overworld.
Saving saves the associated _checkpoint.
Loading a save also loads the associated _checkpoint.
"""

define LOCAL_CHECKPOINT_SLOT = "local_checkpoint"
define CHECKPOINT_SUFFIX = "_checkpoint"
define config.has_autosave = True
define config.autosave_slots = 6
define config.autosave_on_choice = False
define config.autosave_on_input = False
define config.autosave_frequency = 9999999
define config.autosave_on_quit = False

init python:
    def format_progress(progress:int):
        return "Chapter " + str(progress//100) + "-" + str(progress%100)

    def load_checkpoint():
        renpy.load(LOCAL_CHECKPOINT_SLOT)

    def update_local_checkpoint_and_autosave():
        global save_name
        renpy.take_screenshot()
        renpy.save(LOCAL_CHECKPOINT_SLOT)
        autosave()
    
    def autosave(suffix:str = None):
        global save_name
        save_name = format_progress(g.progress)
        if suffix:
            save_name += " " + suffix
        # check if an autosave has the same name, autosave if not
        for i in range(config.autosave_slots):
            filename = 'auto-' + str(i+1)
            if not renpy.can_load(filename): # break if empty save
                print(f"autosave at `{save_name}`")
                renpy.force_autosave(True)
                break
            # break if autosave with same chapter name exists
            if save_name == renpy.slot_json(filename)['_save_name']:
                print(f"autosave of `{save_name}` already exists, overwriting")
                renpy.save(filename, extra_info=save_name)
                break

    def save_slot_with_checkpoint(filename:str):
        print(f"saving checkpoing {filename}")
        renpy.save(filename, extra_info=save_name)
        renpy.copy_save(LOCAL_CHECKPOINT_SLOT, filename + CHECKPOINT_SUFFIX)

    def load_slot_with_checkpoint(filename:str):
        print(f"loading {filename}")
        slot_checkpoint = filename + CHECKPOINT_SUFFIX
        if renpy.can_load(slot_checkpoint):
            renpy.copy_save(slot_checkpoint, LOCAL_CHECKPOINT_SLOT)
        else:
            print(f"Failed to load the checkpoint related to {filename}")
        try:
            renpy.load(filename)
        except Exception as e:
            print(f"Failed to load {filename}: {e}, falling back to checkpoint")
            if renpy.can_load(LOCAL_CHECKPOINT_SLOT):
                renpy.load(LOCAL_CHECKPOINT_SLOT)

    def delete_slot_with_checkpoint(filename:str):
        print(f"deleting {filename}")
        renpy.unlink_save(filename)
        renpy.unlink_save(filename + CHECKPOINT_SUFFIX)

    def get_save_runtime(filename):
        metadata = renpy.slot_json(filename)
        if not metadata:
            return ''
        runtime = metadata.get('_game_runtime', 0)
        hours = int(runtime // 3600)
        minutes = int((runtime % 3600) // 60)
        seconds = int(runtime % 60)
        runtime_formatted = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        return runtime_formatted
