#program to create queries
def gen(*stmts):
    global flag
    k=len(stmts)            #find number of list in argument
    if k==1:
        q,s=simple(stmts[0])          #it is a simple query
        print(s)
    else:
        flag=1
        multi(stmts)              #uses and/or

#function to generate simple queries
def simple(stmt):
    global flag
    #print(stmt)
    coll=stmt[0] 
    con=-1
    if coll[0]!='1':                                                #to see if a collection is present
        print("ERROR:Statement does not specify collection name")
        return
    else:
        count=len(stmt)                             #find the number of items in simple list
        c,coll,val,key=0,'0','0','0'                #intialization
        op=[]
        for x in stmt:
            if x[0]=='1':           #for getting collection name
                coll=x[2:]          
            elif x[0]=='2':         #for getting the attribute/key
                key=x[2:]
            elif x[0]=='4':         #for getting the value of attribute
                val=x[2:]
            elif x[0]=='5':         #for checking condition
                #flag=1
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

        
        if c==1:                        #operation is either greater than or lesser than
            if op[0]=='<':
                s="db."+coll+".find({"+key+":{$lt:"+val+"}}).pretty()"
                q1= { "coll": coll, "key": key, "val":val,"op":"$lt"}
            else:
                s="db."+coll+".find({"+key+":{$gt:"+val+"}}).pretty()"
                q1= { "coll": coll, "key": key, "val":val,"op":"$gt"}
        
        elif c==2:                      #operation is >= or <= or not equal to
            if op=='<=':
                s="db."+coll+".find({"+key+":{$lte:"+val+"}}).pretty()"
                q1= { "coll": coll, "key": key, "val":val,"op":"$lte"}
            elif op=='>=':
                s="db."+coll+".find({"+key+":{$gte:"+val+"}}).pretty()"
                q1= { "coll": coll, "key": key, "val":val,"op":"$gte"}
            else:
                s="db."+coll+".find({"+key+":{$ne:"+val+"}}).pretty()"
                q1= { "coll": coll, "key": key, "val":val,"op":"$ne"}
                
        else:                           #operation is equal to
            s="db."+coll+".find({"+key+":"+val+"}).pretty()"
            q1= { "coll": coll, "key": key, "val":val,"op":""}
    
    if flag==0:
        #print(s)        
        return q1,s
    else:
        return q1,con
    

#function to generate multiple queries
def multi(stmts):
    k=len(stmts)
    q={}
    for x in range(k-1):            #to get individual queries for all except the last one
        q[x],con=simple(stmts[x])
    q[k-1],r=simple(stmts[k-1])       #to get the last individual query
    
    if con==1:
        con="and"
    else:
        con="or"
    

    
    s="db."+q[0]["coll"]+".find({$"+con+":["    
    
    for x in range(k):
        if q[x]["op"]=="":
            s=s+"{"+q[x]["key"]+":"+q[x]["val"]+"}"
        else:
            s=s+"{"+q[x]["key"]+":{"+q[x]["op"]+":"+q[x]["val"]+"}}"
        if x<=k-2:
            s=s+","
        else:
            s=s+"]}).pretty()"
    
    print(s)
   
flag=0
gen(["1:collection", "2:age","3:<=","4:10","5:or"],["1:collection", "2:name", "4:tom","5:and"],["1:collection", "2:mark", "4:100"])
