

def parse_input(path):
    file = open(path,"r")
    line = file.readline().strip()
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

class Node:
    __parts__=("state","parent","action","cost")

    def __init__(self,state,parent=None,action=None,cost=0):
        self.state=state
        self.parent=parent
        self.action=action
        self.cost=cost

def build_path(node):
    chain = []
    while node is not None:     #append from end, then reverse to show start to end
         chain.append(node)
         node=node.parent
    chain.reverse()

    parts = [state_str(chain[0].state)]           #Start - > action-state -> action-state...
    for n in chain[1:]:
        parts.append(action_string(n.action))    
        parts.append(state_str(n.state))
    return " ".join(parts)


def graph_search(initial_state:tuple ,stack:bool):
    root = Node(initial_state)

    if goal(root.state):
        return root

    fringe=[root]
    explored = set()
    n_expansions=0

    while fringe:
        if stack:
            node=fringe.pop()  #LIFO
        else:
            node = fringe.pop(0)  #FIFO

        if node.state in explored:
            continue
        explored.add(node.state)
        n_expansions+=1

        for action,next_state,step_cost in successor_state(node.state):
            if next_state in explored:
                continue
            child = Node(next_state, parent=node,action=action,cost=node.cost+step_cost)
            if goal(child.state):
                return child,n_expansions
            fringe.append(child)
    return None,n_expansions

def dfs(initial_state):
    return graph_search(initial_state,True)
def bfs (initial_state):
    return graph_search(initial_state,False)



#test : -
def run(question:str,search,initial_state:tuple):
    goal,expansions=search(initial_state)
    print("The solution of " + question + " is:")
    if goal is None:
        print("Solution Path: No Solution")
        print("Total Cost: NA")
        print("Number of Node Expansions =" +str(expansions))
    else:
        print("Solution Path: " + build_path(goal))
        print("Total Cost: "+ str(goal.cost))
        print("Number of Node Expansions =" +str(expansions))

def main():
    initial_state=parse_input("input.txt")
    run("Q1.1.a (DFS)",dfs,initial_state)
    run("Q1.1.b (BFS)",bfs,initial_state)

if __name__=="__main__":
    main()