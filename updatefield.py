from random import randint
dice = lambda: str(randint(1,6))
from copy import deepcopy
import itertools
flatten = itertools.chain.from_iterable
from time import sleep # for debugging
import pdb # also for debugging

def killed(char):
    """
    returns dead version of char
    """
    if char in "123456":
        return 't'
    if char == 'F':
        return 'f'
    else:
        print "you just sent me:", char
        return '?'

def grabtype(f, typpe):
    """
    returns coords of all cells of a certain type
    """
    return ((height, width)
            for (height, row) in enumerate(f)
            for (width, char) in enumerate(row)
            if char in typpe)


def replace(f, old, new):
    """
    returns field where all occurences of old are replaced by new
    """
    return [ [(new if char==old else char)
             for (width, char) in enumerate(row)]
             for (height, row) in enumerate(f)]

def neighbors(f, (y,x), wantcorners):
    """
    returns coords of cells  adjacent to given cell
    """
    adjCells = [(y+1,x),(y-1,x),(y,x+1),(y,x-1)]
    if wantcorners:
        adjCells.extend([(y+1,x+1),(y+1,x-1),(y-1,x+1),(y-1,x-1)])
    adjCells = [(y,x) for (y,x) in adjCells if 0<=y<len(f) and 0<=x<len(f[0])]
    return adjCells

def issurrounded(f, (y,x)):
    """
    returns whether or not a cell is surrounded by living cells
    """
    return all((f[y2][x2] in "F123456") for (y2,x2) in neighbors(f, (y,x), False))

def fillsurrounded(f):
    """
    returns field where all surrounded empty spaces are replaced by Forts
    """
    wf = deepcopy(f)
    for (y,x) in grabtype(f, '-'):
        if issurrounded(f, (y, x)):
            wf[y][x] = 'F'
    return wf

def makeGroup(f, seed, types): # kind of bad code
    """
    returns a conneccted group of cells of a certain type
    """
    group = set([seed])
    while True:
        lastgroup = deepcopy(group)
        for coords in lastgroup:
            for (y,x) in neighbors(f, coords, True):
                if f[y][x] in types:
                    group.add((y, x))
        if lastgroup == group:
            break
    return group

def makeGroups(f, types): # kind of bad code
    """
    returns a list of connected groups of a certain type
    """
    groups = []
    for (height, row) in enumerate(f):
        for (width, char) in enumerate(row):
            if char not in types:
                continue
            if (height, width) in flatten(groups):
                continue
            groups.append(makeGroup(f, (height, width), types))
    return groups

def killIsolated(f, groups, colonies):
    """
    returns field where the groups that contain no colonies are killed
    """
    wf = deepcopy(f)
    for group in groups:
        if not any(wf[y][x] in colonies for (y,x) in group):
            for (y,x) in group:
                wf[y][x] = killed(wf[y][x])
    return wf

def updatefield(f):
    """
    returns field after evaluation
    """

    wf = deepcopy(f)

    wf = fillsurrounded(wf)

    roll = dice()
    wf = replace(wf, roll, killed(roll))

    livinggroups = makeGroups(wf, "F123456")
    wf = killIsolated(wf, livinggroups, "F")

    livinggroups = makeGroups(wf, "F123456")
    wf = killIsolated(wf, livinggroups, "123456")

    return wf

def pprint(f):
    """
    prints the field prettily (for debugging)
    """
    print " ",
    for i in xrange(len(f[0])):
        print i,
    print
    for (height,row)  in enumerate(f):
        print height,
        for cell in row:
            print cell,
        print
