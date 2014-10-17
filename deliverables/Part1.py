import json

count_list = [i.split(" ") for i in open("train_data_count.out","r").read().split("\n") if(len(i)>0)]
rare_list = [i[-1] for i in count_list if(i and i[1]=="UNARYRULE" and int(i[0])<5)]
train_tree = open("parse_train.dat").read().split("\n")
train_tree = [json.loads(i) for i in train_tree if(len(i)>0)]

def traverse(i):
    global count
    if(len(i)==2): 
        if(i[1] in rare_list): i[1] = "_RARE_"
        return i
    elif(len(i)>=3):
        i[1] = traverse(i[1])
        i[2] = traverse(i[2])
        return i
mod_train_tree = [traverse(i) for i in train_tree]
g = open("parse_train_mod.dat","w")
for i in mod_train_tree:
    g.write(json.dumps(i)+"\n")
