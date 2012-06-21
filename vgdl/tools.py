'''
Video game description language -- utility functions.

@author: Tom Schaul
'''


def triPoints(rect, direction):
    """ Returns the pointlist for a triangle 
    in the middle of the provided rect, pointing in the direction (given as angle from upwards,
    or direction vector) """    
    p1 = (rect.center[0]+direction[0]*rect.size[0]/2.,
          rect.center[1]+direction[1]*rect.size[1]/2.)
    p2 = (rect.center[0]-direction[0]*rect.size[0]/4.,
          rect.center[1]-direction[1]*rect.size[1]/4.)
    orthdir = (direction[1], -direction[0])
    p2a = (p2[0]-orthdir[0]*rect.size[0]/6.,
           p2[1]-orthdir[1]*rect.size[1]/6.)
    p2b = (p2[0]+orthdir[0]*rect.size[0]/6.,
           p2[1]+orthdir[1]*rect.size[1]/6.)    
    return [(p[0], p[1]) for p in [p1, p2a, p2b]]


class Node(object):
    """ Lightweight indented tree structure, with automatic insertion at the right spot. """
    
    parent = None
    def __init__(self, content, indent, parent=None):
        self.children = []
        self.content = content
        self.indent = indent
        if parent:
            parent.insert(self)
        else:
            self.parent = None
    
    def insert(self, node):
        if self.indent < node.indent:
            if len(self.children) > 0:
                assert self.children[0].indent == node.indent, 'children indentations must match'
            self.children.append(node)
            node.parent = self
        else:
            assert self.parent, 'Root node too indented?'
            self.parent.insert(node)

    def __repr__(self):
        if len(self.children) == 0:
            return self.content
        else:
            return self.content+str(self.children)
                        
    def getRoot(self):
        if self.parent: return self.parent.getRoot()
        else:           return self


def indentTreeParser(s, tabsize=8):
    """ Produce an unordered tree from an indented string. """
    # insensitive to tabs, parentheses, commas
    s = s.expandtabs(tabsize)
    s.replace('(', ' ')
    s.replace(')', ' ')
    s.replace(',', ' ')
    lines = s.split("\n")            
                     
    last = Node("",-1)
    for l in lines:
        # remove comments starting with "#"
        if '#' in l:
            l = l.split('#')[0]
        # handle whitespace and indentation
        content = l.strip()
        if len(content) > 0:
            indent = len(l)-len(l.lstrip())
            last = Node(content, indent, last)
    return last.getRoot()