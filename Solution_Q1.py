

def parse_input(path):
    file = open(path,"r")
    line = file.readlines().strip()
    file.close()

    parts = [part.strip() for part in line.split(',')]
    m_left=int(parts[0])
    c_left=int(parts[1])
    m_right=int(parts[2])
    c_right=int(parts[3])
    boat= parts[4]

    return (m_left,c_left,m_right,c_right,boat)

def is_valid(state):
    m_left,c_left,m_right,c_right,boat=state

    if m_left<0 or c_left<0 or m_right<0 or c_right<0:
        return False
    if m_left>0 and m_left<c_left:
        return False
    if m_right>0 and m_right<c_right:
        return False
    return True

def goal(state):
    m_left,c_left,m_right,c_right,boat=state
    return m_left==0 and c_left==0

LOADS = [(1,0),(2,0),(0,1),(0,2),(1,1)]

def successor_state(state):
    m_left,c_left,m_right,c_right,boat=state
    successor_states=[]

    for (m,c) in LOADS:
        if boat == "L":
            if m_left>=m and c_left>= c:
                successor=(m_left-m, c_left-c, m_right+m, c_right+c,"R")
                if is_valid(successor):
                    action=(m,c,"L->R")
                    successor_states.append((action,successor,1))
        if boat == "R":
                    if m_right>=m and c_right>= c:
                        successor=(m_left+m, c_left+c, m_right-m, c_right-c,"L")
                        if is_valid(successor):
                            action=(m,c,"R->L")
                            successor_states.append((action,successor,1))
    return successor_states

# Strings : -

def action_string(action):
    m,c,direction = action
    parts = []

    if m:
         parts.append(str(m)+'M')
    if c:
         parts.append(str(c)+'C')

    return f"[{','.join(parts)} {direction} ]"

def state_str(state):
    m_left,c_left,m_right,c_right,boat = state

    return f"({str(m_left)},{str(c_left)},{str(m_right)},{str(c_right)},{boat})"

