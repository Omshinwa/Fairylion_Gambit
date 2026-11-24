# CHARACTER RULES
# Unique Trust rules of some characters (see Characters in ai_prompt/prompt.md). Story mode only.
#
#   suzaku: -2 Trust every battle he's deployed in, +2 every battle he isn't.
#           Once he has talked with lelouch, being deployed no longer costs him Trust.
#           That talk sets the flag with: $ done_flag['oncePerRun'].add('suzaku_trusts_lelouch')
#
# kallen's starting affinities are in AFFINITY_START (src/affinity.rpy).

define SUZAKU_DEPLOYED_TRUST = -2
define SUZAKU_BENCHED_TRUST = 2

init python:
    def character_rules_battle_start():
        """Called when a battle starts (l_start_battle), once the player's pieces are on the board."""
        if rogue:
            return

        if suzaku in TEAM: # dead or departed pilots are removed from TEAM
            deployed = any(suzaku in piece.pilots for piece in chess.get_pieces(chess.player))
            if not deployed:
                gain_trust(suzaku, SUZAKU_BENCHED_TRUST)
            elif not has_done('suzaku_trusts_lelouch'):
                gain_trust(suzaku, SUZAKU_DEPLOYED_TRUST)
