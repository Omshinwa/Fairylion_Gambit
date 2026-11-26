# ROBOT UPGRADES (story mode). See Robots in ai_prompt/prompt.md.
#   - A robot's upgrades are robot.upgrades, a set of ids of ROBOT_UPGRADES. They stay when the robots are made
#     again for a new board (story_robots_refresh in src/story_battles.rpy).
#   - They'll be bought from the United Nations (not done yet): for now only the test labels give them.
#   - 'tech', the RESEARCH LAB: when this robot doesn't fight, +2 TECH at the new day (ship_new_day in src/ship.rpy).

define ROBOT_UPGRADES = { # id: (name, what it does)
    'tech': (_("RESEARCH LAB"), _("When this robot doesn't fight: +2 TECH.")),
}
define ROBOT_UPGRADE_TECH = 2 # TECH a day from a resting robot with a RESEARCH LAB

init python:
    def robot_upgrades(robot):
        """The ids of the robot's upgrades."""
        return getattr(robot, 'upgrades', set())

    def robot_has_upgrade(robot, upgrade):
        return upgrade in robot_upgrades(robot)

    def robot_add_upgrade(robot, upgrade):
        robot.upgrades = set(robot_upgrades(robot)) | {upgrade}
