count_list = [i.split(" ") for i in open("parse_train_counts.out","r").read().split("\n") if(len(i)>0)]

unary = {}
binary = {}
nonterm = {}

for i in count_list:
    if i[1] == "NONTERMINAL": nonterm[i[2]] = int(i[0])
    elif i[1] == "UNARYRULE": unary[(i[2],i[3])] = int(i[0])
    else: binary[(i[2],i[3],i[4])] = int(i[0])

def q_unary(rule):
    return float(unary[rule])/nonterm[rule[0]]

def q_binary(rule):
    return float(binary[rule])/nonterm[rule[0]]

def CKY(s):
    pi = {}
    bp = []
    words = s.split(" ")
    for i in range(len(words)):
        flag = 1
        for j in unary.keys():
            if(words[i] in j): 
                flag = 0;
                break;
        if(flag): words[i] = "_RARE_"
    n = len(words)
    for x in nonterm.keys():
        for i in range(1,n+1):
            if(unary.get((x,words[i-1]))): pi[(i,i,x)]=q_unary((x,words[i-1]))
            else: pi[(i,i,x)] = 0
    for l in range(1,n):
        for i in range(1,n-l+1):
            j = i+l
            for x in nonterm.keys():
                temp = []
                for y in binary.keys():
                    for s in range(i,j):
                        temp.append(q_binary(y)*pi[(i,s,y[1])]*pi[(s+1,j,y[2])])
                pi[(i,j,x)] = max(temp)
    tp = {}
    for i in pi.keys():
        if(pi[i]>0):
            if tp.get(tuple(words[i[0]-1:i[1]])):
                if(pi[i]>tp[tuple(words[i[0]-1:i[1]])]):
                    tp[tuple(words[i[0]-1:i[1]])] = [pi[i],i[2]]
            else:
                tp[tuple(words[i[0]-1:i[1]])] = [pi[i],i[2]]
    for i in tp.keys():        
        print i,tp[i]
            
CKY("What does the Peugeot company manufacture ?")
