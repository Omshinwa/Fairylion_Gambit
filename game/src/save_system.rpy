"""
Save system:
autosaves before every battle start and when getting to overworld, only keeps 1 save for each.
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

# dev-only: filenames of save slots protected against overwrite/delete
default persistent.dev_locked_saves = set()

init python:
    def is_save_locked(filename:str):
        """A slot is locked only in developer mode, and only if it still holds a save."""
        return (config.developer
            and filename in (persistent.dev_locked_saves or ())
            and renpy.can_load(filename))

    def toggle_save_lock(filename:str):
        locked = set(persistent.dev_locked_saves or ())
        if filename in locked:
            locked.discard(filename)
        else:
            locked.add(filename)
        persistent.dev_locked_saves = locked
        renpy.save_persistent()
        renpy.restart_interaction()

    def format_progress(progress:int):
        return "Chapter " + str(progress//100) + "-" + str(progress%100)

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
        if is_save_locked(filename):
            renpy.notify(_("This save is locked."))
            return
        print(f"saving checkpoing {filename}")
        notes = save_name
        if not notes and renpy.can_load(filename): # overwriting a slot: keep its notes when this save has none
            notes = (renpy.slot_json(filename) or {}).get('_save_name', '')
        renpy.save(filename, extra_info=notes)
        renpy.copy_save(LOCAL_CHECKPOINT_SLOT, filename + CHECKPOINT_SUFFIX)

    def load_slot_with_checkpoint(filename:str):
        print(f"loading {filename}")
        slot_checkpoint = filename + CHECKPOINT_SUFFIX
        if renpy.can_load(slot_checkpoint):
            renpy.copy_save(slot_checkpoint, LOCAL_CHECKPOINT_SLOT)
        else:
            print(f"Failed to load the checkpoint related to {filename}")
        renpy.load(filename)

    def delete_slot_with_checkpoint(filename:str):
        if is_save_locked(filename):
            renpy.notify(_("This save is locked."))
            return
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