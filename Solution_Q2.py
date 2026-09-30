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
    file.close()
    cost_model=None
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
    counter = itertools.count()  
    fringe = [(0,next(counter),root)]
    best_cost={initial_state:0}
    explored = set()
    n_expansions = 0

    while fringe:
        curr_cost,_,node=heapq.heappop(fringe)

        if node.state in explored:
            continue
        if curr_cost>best_cost.get(node.state,float("inf")):
            continue

        if goal(node.state):
            return node,n_expansions
        explored.add(node.state)
        n_expansions+=1

        for action,next_state,step_cost in successor_state(node.state,cost_mode):
            new_cost=node.cost+step_cost
            
            if next_state in explored:
                continue
            if new_cost<best_cost.get(next_state,float("inf")):
                best_cost[next_state]=new_cost
                child=Node(next_state,parent=node,action=action,cost=new_cost)
                heapq.heappush(fringe,(new_cost,next(counter),child))

    return None,n_expansions


#test:-

def run(question:str,search,initial_state:tuple,cost_mode):
    goal,expansions = search(initial_state,cost_mode)
    print("The solution of " +question+" is:")
    if goal is None:
        print("solution path: No solution")
        print("Total Cost: N/A")
        print("The number of node expansions: "+str(expansions))
    else:
        print("Solution Path: "+build_path(goal))
        print("Total Cost: "+str(goal.cost))
        print("The number of node expansions: "+str(expansions))

def main():
    initial_state,cost_model=parse_input("input.txt")

    if cost_model:
        if cost_model in ("A","a"):
            cost_mode=cost_a
            run("Q2.1 (UCS, cost model A)",ucs,initial_state,cost_mode)
        elif cost_model in ("B","b"):
            cost_mode=cost_b
            run("Q2.1 (UCS, cost model B)",ucs,initial_state,cost_mode)        
    else:
        run("Q2.1 (UCS, Cost model A)",ucs,initial_state,cost_a)
        run("Q2.1 (UCS, Cost model B)",ucs,initial_state,cost_b)

if __name__=="__main__":
    main()