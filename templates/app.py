from flask import Flask, render_template, request
from collections import deque

app = Flask(__name__)

def get_next_states(state, capA, capB):
    a, b = state
    states = []

    states.append((capA, b))        # Fill A
    states.append((a, capB))        # Fill B
    states.append((0, b))           # Empty A
    states.append((a, 0))           # Empty B

    pour = min(a, capB - b)         # Pour A → B
    states.append((a - pour, b + pour))

    pour = min(b, capA - a)         # Pour B → A
    states.append((a + pour, b - pour))

    return states

def bfs(capA, capB, goal):
    start = (0,0)
    queue = deque([(start,[start])])
    visited = set([start])
    tree=[]

    while queue:
        state,path = queue.popleft()
        tree.append(state)

        if state[0] == goal:
            return path, tree

        for nxt in get_next_states(state, capA, capB):
            if nxt not in visited:
                visited.add(nxt)
                queue.append((nxt, path + [nxt]))

    return [], tree

@app.route("/", methods=["GET","POST"])
def index():
    steps=[]
    tree=[]
    capA=4
    capB=3

    if request.method=="POST":
        capA = int(request.form["capA"])
        capB = int(request.form["capB"])
        goal = int(request.form["goal"])
        steps, tree = bfs(capA, capB, goal)

    return render_template("index.html", steps=steps, tree=tree, capA=capA, capB=capB)

if __name__=="__main__":
    app.run(debug=True)
