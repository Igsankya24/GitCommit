import os
import subprocess
import requests
import random
import threading
import time
from datetime import datetime, timedelta

import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx

repo_path = r"D:\Projects\GitCommit"

github_user = "Igsankya24"
repo_name = "GitCommit"
token = os.getenv("GITHUB_TOKEN")

headers = {"Authorization": f"token {token}"}

running=False
paused=False

html_files=["index.html","about.html","services.html"]
css_files=["style.css","layout.css"]
js_files=["app.js","main.js"]


# --------------------
# UI LOG
# --------------------

def log(msg):
    console.insert("end",msg+"\n")
    console.see("end")


# --------------------
# FILE GENERATORS
# --------------------

def generate_html(file):

    html=f"""
<!DOCTYPE html>
<html>
<head>
<title>Page</title>
<link rel="stylesheet" href="style.css">
<script src="app.js"></script>
</head>
<body>

<h1>Frontend Page</h1>

<p>{datetime.now()}</p>

</body>
</html>
"""

    with open(file,"w") as f:
        f.write(html)


def generate_css(file):

    css=f"""
body {{
background:#{random.randint(100000,999999)};
font-family:Arial;
}}
"""

    with open(file,"w") as f:
        f.write(css)


def generate_js(file):

    js=f"""
console.log("Update {datetime.now()}");

function component(){{
return {random.randint(1,100)};
}}
"""

    with open(file,"w") as f:
        f.write(js)


# --------------------
# BATCH COMMIT
# --------------------

def batch_commit():

    os.chdir(repo_path)

    subprocess.run(["git","checkout","main"])

    files=[]

    for i in range(random.randint(2,4)):

        t=random.choice(["html","css","js"])

        if t=="html":
            f=random.choice(html_files)
            generate_html(f)

        elif t=="css":
            f=random.choice(css_files)
            generate_css(f)

        else:
            f=random.choice(js_files)
            generate_js(f)

        files.append(f)

    subprocess.run(["git","add","."])

    msg=f"batch update {random.randint(1000,9999)}"

    subprocess.run(["git","commit","-m",msg])

    subprocess.run(["git","push","origin","main"])

    log(f"Batch commit: {files}")


# --------------------
# BRANCH WORKFLOW
# --------------------

def create_feature_branch():

    os.chdir(repo_path)

    branch=f"feature-{random.randint(1000,9999)}"

    subprocess.run(["git","checkout","-b",branch])

    generate_html("index.html")

    subprocess.run(["git","add","."])

    subprocess.run(["git","commit","-m","feature update"])

    subprocess.run(["git","push","-u","origin",branch])

    log(f"Branch created: {branch}")

    create_pull_request(branch)

    subprocess.run(["git","checkout","main"])


# --------------------
# PR AUTOMATION
# --------------------

def create_pull_request(branch):

    url=f"https://api.github.com/repos/{github_user}/{repo_name}/pulls"

    data={
        "title":f"Auto PR {branch}",
        "head":branch,
        "base":"main"
    }

    r=requests.post(url,headers=headers,json=data)

    if r.status_code==201:

        pr=r.json()

        log(f"PR created #{pr['number']}")

        threading.Thread(target=merge_pr_delay,args=(pr['number'],),daemon=True).start()


def merge_pr_delay(pr_number):

    time.sleep(random.randint(60,180))

    url=f"https://api.github.com/repos/{github_user}/{repo_name}/pulls/{pr_number}/merge"

    requests.put(url,headers=headers)

    log(f"PR merged #{pr_number}")


# --------------------
# CONTRIBUTION HEATMAP
# --------------------

def draw_heatmap():

    url=f"https://api.github.com/repos/{github_user}/{repo_name}/commits"

    r=requests.get(url,headers=headers)

    commits=r.json()

    days=[c["commit"]["author"]["date"][:10] for c in commits]

    counts={}

    for d in days:
        counts[d]=counts.get(d,0)+1

    today=datetime.now()

    values=[]

    for i in range(365):

        d=(today-timedelta(days=i)).strftime("%Y-%m-%d")

        values.append(counts.get(d,0))

    grid=[values[i:i+7] for i in range(0,len(values),7)]

    fig=plt.figure(figsize=(4,2))

    plt.imshow(grid,cmap="Greens")

    plt.title("GitHub Contributions")

    plt.axis("off")

    for w in heatmap_frame.winfo_children():
        w.destroy()

    canvas=FigureCanvasTkAgg(fig,heatmap_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both",expand=True)


# --------------------
# DAG GRAPH
# --------------------

def draw_dag():

    os.chdir(repo_path)

    result=subprocess.run(
        ["git","log","--pretty=%H %P"],
        capture_output=True,
        text=True
    )

    lines=result.stdout.splitlines()

    G=nx.DiGraph()

    for l in lines:

        parts=l.split()

        commit=parts[0]

        parents=parts[1:]

        for p in parents:
            G.add_edge(p,commit)

    fig=plt.figure(figsize=(4,3))

    nx.draw(G,node_size=50,arrows=False)

    plt.title("Git DAG")

    for w in dag_frame.winfo_children():
        w.destroy()

    canvas=FigureCanvasTkAgg(fig,dag_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both",expand=True)


# --------------------
# AUTOMATION
# --------------------

def automation():

    global running,paused

    while running:

        if paused:
            time.sleep(2)
            continue

        batch_commit()

        if random.random()<0.4:
            create_feature_branch()

        delay=random.randint(120,300)

        log(f"Cooldown {delay}s")

        time.sleep(delay)


# --------------------
# UI CONTROL
# --------------------

def start():

    global running

    if running:
        return

    running=True

    threading.Thread(target=automation,daemon=True).start()

    log("Automation started")


def pause():
    global paused
    paused=True

def resume():
    global paused
    paused=False

def stop():
    global running
    running=False


def toggle_theme():

    if ctk.get_appearance_mode()=="Dark":
        ctk.set_appearance_mode("Light")
    else:
        ctk.set_appearance_mode("Dark")


# --------------------
# UI
# --------------------

ctk.set_appearance_mode("Dark")

app=ctk.CTk()

app.geometry("1400x800")

top=ctk.CTkFrame(app)
top.pack(fill="x")

ctk.CTkButton(top,text="Start",command=start).pack(side="left")
ctk.CTkButton(top,text="Pause",command=pause).pack(side="left")
ctk.CTkButton(top,text="Resume",command=resume).pack(side="left")
ctk.CTkButton(top,text="Stop",command=stop).pack(side="left")
ctk.CTkButton(top,text="Theme",command=toggle_theme).pack(side="left")
ctk.CTkButton(top,text="Heatmap",command=draw_heatmap).pack(side="left")
ctk.CTkButton(top,text="DAG",command=draw_dag).pack(side="left")


main=ctk.CTkFrame(app)
main.pack(fill="both",expand=True)


left=ctk.CTkFrame(main,width=250)
left.pack(side="left",fill="y")

center=ctk.CTkFrame(main)
center.pack(side="left",fill="both",expand=True)

right=ctk.CTkFrame(main,width=400)
right.pack(side="right",fill="y")


file_box=ctk.CTkTextbox(left,width=250)
file_box.pack(fill="both",expand=True)

console=ctk.CTkTextbox(center)
console.pack(fill="both",expand=True)


heatmap_frame=ctk.CTkFrame(right,height=250)
heatmap_frame.pack(fill="both",expand=True)

dag_frame=ctk.CTkFrame(right)
dag_frame.pack(fill="both",expand=True)


for f in os.listdir(repo_path):
    file_box.insert("end",f+"\n")


app.mainloop()