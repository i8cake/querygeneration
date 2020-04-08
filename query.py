#program to generate query
def gen(*stmts):                    #argument is of unkown number of lists
    k=len(stmts)                    #number of lists in argument
    con=-1;
    for i in range(k):              #for each list
        stmt=stmts[i]
        coll=stmt[0]                                                    
        if coll[0]!='1':                                                #to see if a collection is present
            print("ERROR:Statement does not specify collection name")
            return
        else:
            count=len(stmt)                             #find the number of items in list
            c,coll,val,key=0,'0','0','0'                #intialization
            op=[]
            flag=0
            for x in stmt:
                if x[0]=='1':           #for getting collection name
                    coll=x[2:]          
                elif x[0]=='2':         #for getting the attribute/key
                    key=x[2:]
                elif x[0]=='4':         #for getting the value of attribute
                    val=x[2:]
                elif x[0]=='5':
                    flag=1
                    if x[2:]=="and":
                        con=1
                    else:
                        con=0
                else:                   #for getting the operators
                    for j in x:
                        c=c+1               #counts number of operators
                    op=x[2:]
                    #op.append(item)
                    c=c-2
            if c==1:
                if op[0]=='<':
                    print("db."+coll+".find({"+key+":{$lt:"+val+"}}).pretty()")
                    if flag==1:
                        q1= { "coll": coll, "key": key, "val":val,"op":"$lt"}
                    else:
                        q2= { "coll": coll, "key": key, "val":val,"op":"$lt"}
                else:
                    print("db."+coll+".find({"+key+":{$gt:"+val+"}}).pretty()")
                    if flag==1:
                        q1= { "coll": coll, "key": key, "val":val,"op":"$gt"}
                    else:
                        q2= { "coll": coll, "key": key, "val":val,"op":"$gt"}
            elif c==2:
                if op=='<=':
                    print("db."+coll+".find({"+key+":{$lte:"+val+"}}).pretty()")
                    if flag==1:
                        q1= { "coll": coll, "key": key, "val":val,"op":"$lte"}
                    else:
                        q2= { "coll": coll, "key": key, "val":val,"op":"$lte"}
                elif op=='>=':
                    print("db."+coll+".find({"+key+":{$gte:"+val+"}}).pretty()")
                    if flag==1:
                        q1= { "coll": coll, "key": key, "val":val,"op":"$gte"}
                    else:
                        q2= { "coll": coll, "key": key, "val":val,"op":"$gte"}
                else:
                    print("db."+coll+".find({"+key+":{$ne:"+val+"}}).pretty()")
                    if flag==1:
                        q1= { "coll": coll, "key": key, "val":val,"op":"$ne"}
                    else:
                        q2= { "coll": coll, "key": key, "val":val,"op":"$ne"}
            else:                                                                   #equality
                print("db."+coll+".find({"+key+":"+val+"}).pretty()")
                if flag==1:
                    q1= { "coll": coll, "key": key, "val":val,"op":""}
                else:
                    q2= { "coll": coll, "key": key, "val":val,"op":""}
            
    if con!=-1:
        condition(q1,q2,con)

def condition(q1,q2,con):
    if con==1:
        query={ "coll": q1["coll"], "1key": q1["key"], "1val":q1["val"], "1op":q1["op"],"2key": q2["key"], "2val":q2["val"], "2op":q2["op"], "cond":"and"}
        #print("db."+q1["coll"]+".find({$and:[{"+q1["key"]+":"+q1["val"]+"},{"+q2["key"]+":"+q2["val"]+"}]}).pretty()")
    else:
        query={ "coll": q1["coll"], "1key": q1["key"], "1val":q1["val"], "1op":q1["op"],"2key": q2["key"], "2val":q2["val"], "2op":q2["op"], "cond":"or"}
        #print("db."+q1["coll"]+".find({$or:[{"+q1["key"]+":"+q1["val"]+"},{"+q2["key"]+":"+q2["val"]+"}]}).pretty()")
    generatequery(query)

def generatequery(query):
    if query["1op"]=="" and query["2op"]=="":
        print("hello")
        print("db."+query["coll"]+".find({$"+query["cond"]+":[{"+query["1key"]+":"+query["1val"]+"},{"+query["2key"]+":"+query["2val"]+"}]}).pretty()")
    elif query["1op"]=="":
        print("db."+query["coll"]+".find({$"+query["cond"]+":[{"+query["1key"]+":"+query["1val"]+"},{"+query["2key"]+":{"+query["2op"]+":"+query["2val"]+"}}]}).pretty()")
    elif query["2op"]=="":
       print("db."+query["coll"]+".find({$"+query["cond"]+":[{"+query["1key"]+":{"+query["1op"]+":"+query["1val"]+"}},{"+query["2key"]+":"+query["2val"]+"}]}).pretty()")
    else:
        print("db."+query["coll"]+".find({$"+query["cond"]+":[{"+query["1key"]+":{"+query["1op"]+":"+query["1val"]+"}},{"+query["2key"]+":{"+query["2op"]+":"+query["2val"]+"}}]}).pretty()")
    

gen(["1:collection", "2:age","3:<=","4:10","5:and"],["1:collection", "2:name", "4:tom"])

