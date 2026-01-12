from flask import Flask, render_template, request
from collections import deque

app = Flask(__name__)

def bfs(capA, capB, goal):
    start = (0, 0)
    q = deque([(start, [start])])
    visited = set([start])

    while q:
        (a, b), path = q.popleft()

        if a == goal:
            return path

        states = [
            (capA, b),
            (a, capB),
            (0, b),
            (a, 0),
            (a - min(a, capB - b), b + min(a, capB - b)),
            (a + min(b, capA - a), b - min(b, capA - a))
        ]

        for s in states:
            if s not in visited:
                visited.add(s)
                q.append((s, path + [s]))

    return []

@app.route("/", methods=["GET", "POST"])
def index():
    steps = None
    if request.method == "POST":
        capA = int(request.form["capA"])
        capB = int(request.form["capB"])
        goal = int(request.form["goal"])
        steps = bfs(capA, capB, goal)
        return render_template("index.html",
            steps=steps, capA=capA, capB=capB, goal=goal)

    return render_template("index.html", steps=None)

if __name__ == "__main__":
    app.run(debug=True)
