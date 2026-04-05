define SQUARESIZE = 128 #135 #128

define LOYALTY_COLORS = [("#9fb39c","#789070"), ("#e2da89","#e5b24a"), ("#a0e79e","#47a878"),  ("#9ee0e7","#7584c2"), ("#ff93c5","#d55170")]
define INDEX_TO_LETTER = ['a','b','c','d','e','f','g','h','i','j','k']

define DEFAULT_ROBOT = {'#':'k', '*':'q', '+':'r', 'x':'b', 'L':'n', '^':'p', 'i':'i'}

define LOYALTY_TO_NAME = [_('Worst'),_('Bad'),_('Average'),_('Good'),_('Best')]

init python:
    def TRUST_TO_LOYALTY(trust):
        if trust < -5:
            return 0
        elif trust < 1:
            return 1
        elif trust < 5:
            return 2
        elif trust < 10:
            return 3
        else:
            return 4