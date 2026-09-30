import heapq
import itertools

from Solution_Q1 import(is_valid,goal,successor_state,Node,action_string,state_str,build_path)

def parse_input(path):
    file = open(path,'r')
    line1 = file.readline().strip()
    parts = [part.strip() for part in line1.split(',')]
    m_left=int(parts[0])
    c_left=int(parts[1])
    m_right=int(parts[2])
    c_right=int(parts[3])
    boat = parts[4]

    line2=file.readline().strip()
    if line2 in ("A",'a','B','b'):
        cost_model=line2
    state = (m_left,c_left,m_right,c_right,boat)

    return state,cost_model

def cost_a(m_moved,c_moved,direction):
    return 2*m_moved + 1* c_moved

def cost_b(m_moved,c_moved,direction):
    if direction =="L->R":
        cost=2
    else:
        cost=1
    return cost

def ucs(initial_state,cost_mode):
    root = Node(initial_state)
    