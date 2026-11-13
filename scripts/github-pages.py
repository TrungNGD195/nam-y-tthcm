"""Publish this project's new public repository with existing Git authentication.

The token stays in memory. Never pass it to Git, command arguments, logs or files.
Git's credential manager handles push authentication independently.
"""
import argparse
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")
parser=argparse.ArgumentParser()
parser.add_argument("action",choices=["create","enable-pages","status"])
parser.add_argument("--owner",required=True)
parser.add_argument("--repo",default="nam-y-tthcm")
args=parser.parse_args()
env=os.environ.copy()
env.update(GIT_TERMINAL_PROMPT="0",GCM_INTERACTIVE="never")
credential=subprocess.run(["git","-c","credential.interactive=never","credential","fill"],input="protocol=https\nhost=github.com\n\n",capture_output=True,text=True,env=env,timeout=20)
values=dict(line.split("=",1) for line in credential.stdout.splitlines() if "=" in line)
if credential.returncode or not values.get("password"):raise SystemExit("No noninteractive GitHub credential available.")
headers={"Authorization":"Bearer "+values["password"],"Accept":"application/vnd.github+json","X-GitHub-Api-Version":"2022-11-28","User-Agent":"Nam-Y-project-publisher"}

def api(path,method="GET",data=None):
    request=urllib.request.Request("https://api.github.com"+path,headers=headers,method=method,data=json.dumps(data).encode("utf-8") if data is not None else None)
    try:
        with urllib.request.urlopen(request,timeout=30) as response:
            text=response.read().decode("utf-8")
            return response.status,json.loads(text) if text else {}
    except urllib.error.HTTPError as error:
        body=error.read().decode("utf-8")
        try:result=json.loads(body)
        except json.JSONDecodeError:result={"message":"GitHub request failed."}
        return error.code,result

status,user=api("/user")
if status!=200 or user.get("login","").lower()!=args.owner.lower():raise SystemExit("Authenticated GitHub account differs from the explicitly selected owner.")
base=f"/repos/{args.owner}/{args.repo}"
if args.action=="create":
    status,existing=api(base)
    if status==200:raise SystemExit("Repository already exists; refusing to overwrite or reuse it automatically.")
    if status!=404:raise SystemExit(f"Cannot check repository availability: HTTP {status}")
    status,result=api("/user/repos","POST",{"name":args.repo,"description":"Ôn thi Tư tưởng Hồ Chí Minh: trắc nghiệm theo chương, keyword và ôn câu sai. Không cần đăng nhập.","private":False,"auto_init":False,"has_issues":True,"has_wiki":False})
    if status!=201:raise SystemExit(f"Repository creation failed: HTTP {status}, {result.get('message')}")
    print(json.dumps({"repository":result["html_url"],"remote":result["clone_url"],"private":result["private"]},ensure_ascii=False))
elif args.action=="enable-pages":
    status,result=api(base+"/pages","POST",{"build_type":"workflow"})
    if status==409:
        status,result=api(base+"/pages","PUT",{"build_type":"workflow"})
    if status not in [200,201,204]:raise SystemExit(f"Pages setup failed: HTTP {status}, {result.get('message')}")
    print(json.dumps({"status":status,"url":result.get("html_url"),"build_type":result.get("build_type","workflow")},ensure_ascii=False))
else:
    status,result=api(base+"/actions/runs?per_page=3")
    runs=[{"id":r["id"],"name":r["name"],"status":r["status"],"conclusion":r["conclusion"],"url":r["html_url"]} for r in result.get("workflow_runs",[])]
    pstatus,pages=api(base+"/pages")
    print(json.dumps({"workflow_status":status,"runs":runs,"pages_status":pstatus,"pages_url":pages.get("html_url"),"pages_build_type":pages.get("build_type")},ensure_ascii=False))
