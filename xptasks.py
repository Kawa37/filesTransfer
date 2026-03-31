import json
from pathlib import Path
import pyfiglet as pf
import os
import copy
from datetime import datetime

# data
# day:{tasks:{},checked:bool}

#30 black
#31 red
#32 green
#33 yellow
#34 blue
#35 magenta
#36 cyan
#37 white

file = '/storage/emulated/0/.~/doc/xptasks.json'
data = {}
run = True
today = datetime.strftime(datetime.now(),'%d-%m-%Y')
tmp_tasks = {
    'tasks':{
        'pray':0,
        'quran':False,
        'study':False,
        'exercise':False,
        'health':False,
        '!po':False,
    },
    'checked':False
}

def save_data():
    global data, file
    with open (file,'w') as f:
        json.dump(data,f,indent=2)

def load_data():
    global data, file

    try:
        with open (file,'r') as f:
            data = json.load(f)
    except Exception as e:
        print ("", e)

def c(t, n): return f"\033[{n}m{t}\033[0m"

def recalc():
    global data, today

    data["xp"] = 0

    if data:
        for day, content in data.items():
            if day != today and day != "xp" and day != "level" and content["checked"]:
                data[day]["checked"] = False


def edit_task(rqst):
    global data, run, today
    
    tasks = data[today]['tasks']
    if rqst == 'q':
        all_completed = any(not v for k,v in tasks.items() if k != "pray")
        if tasks["pray"] != 5:
            all_completed = False

        if not all_completed:
            print (" such a loser.")


        run = False
        return
    if rqst != 'pray' and rqst != "exercise" and rqst in tasks:
        tasks[rqst] = False if tasks[rqst] else True

    elif rqst == 'pray':
        co = input (" pray: ")

        if ( not co or not co.isdigit() ) and tasks["pray"]<5: 
            tasks["pray"] += 1
        elif co.isdigit() and int(co) > 5: 
            tasks["pray"] = 5
        elif co.isdigit():
            tasks['pray'] = int(co)

    elif rqst == "recalc":
        recalc()
    else:
        print (' invalid input')
        input(" ")
    save_data()

def calcex():
    global data, today 
    # check exercise 
    tasks = data[today]['tasks']
    ex_path = "/storage/emulated/0/.~/doc/exquests.json"
    if Path(ex_path).exists():
        with open(ex_path,"r") as f:
            ex_data = json.load(f)
        if today in ex_data:
            tasks["exercise"] = True
    
    

def addlvlxp():
    global data
    if "xp" not in data:
        data["xp"] = 0
    if "level" not in data:
        data["level"] = 0

def add_day_ifnot():
    global data, today

    if today not in data:
        data[today] = copy.deepcopy(tmp_tasks)

def calc_xp():
    global data, today

    xp = 0
    for day, content in data.items():
        if day == 'xp' or day == "level": continue

        if day != today and not content['checked']:
            for task, status in content['tasks'].items():
                if task != 'pray':
                    if status: xp += 2
                    elif status == False: xp -= 4

                elif task == 'pray':
                    if status:
                        for _ in range(status):
                            xp += 2
                    elif status < 5:
                        xp -= (5-status)*4
            content['checked'] = True
    
    data['xp'] += xp
    save_data()

def display():
    global data, today

    print ("",pf.figlet_format("XP","small"))

    if data:
        print (f' "{today}"')
        com, con = count_tasks()
        tasks = data[today]['tasks']
        xp_get = (com*2) - ((9-com)*4)
        xp_get_line = f"{'+' if xp_get > 0 else ""}{xp_get}xp"
        print (f" completed tasks: [{com}/{con}] -> {c(xp_get_line ,32) if xp_get_line[0] !='-' else c(xp_get_line,31)}")
        print (f" XP: [{data['xp']}] -> [{data['xp']+xp_get}]")
        print (f" level: [{data['level']}]")
        print ()
        checked, nochecked = "[x]","[ ]"
        for task,status in tasks.items():
            if task == "pray":
                
                line = f"{task}: [{c(status,32) if status==5 else status}]"
            else:
                line = f"{task}: [{c(status,32) if status else status}]"
            if task != "pray":
                checked_mark = c(checked,32) if status else c(nochecked,31)
            else:
                checked_mark = c(checked,32) if status == 5 else c(nochecked,31)

            print (f' {checked_mark} {line}')
    else:
        print (" No data found")
        input(" ")
    

def handle_lvl():
    global data

    xp = data["xp"]

    if xp < 0:
        data["level"] = 0
    else:
        data["level"] = max(1, (xp // 20) + 1)

    save_data()

def count_tasks():
    global data, today

    count = 0
    complete = 0
    for task,stat in data[today]["tasks"].items():
        if task == "pray":
            count += 5
            complete += stat
        else:
            count += 1
            if stat: complete += 1
    
    return complete,count

def main():
    global run

    while run:
        os.system('cls' if os.name == 'nt' else 'clear')
        load_data()
        addlvlxp()
        add_day_ifnot()

        calc_xp()
        calcex()
        handle_lvl()
        display()
        print()

        usr = input (' task: ').lower().strip()
        edit_task(usr)

if __name__ == '__main__':
    main()
