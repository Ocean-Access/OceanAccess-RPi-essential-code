
rep = [1.196 , 0.581, 0.569, 0.863,2.088,2.040,3.013,3.689,4.235]
act =[1.46 , 0.76, 0.76 , 1.1,2.8,2.9,4.3,5.8,6.9]
time = [60 , 30, 30,45,120,120,180,240,300,360]
ratio=[]
rratio=[]
for i in range(len(act)):
    ratio.append(act[i]/rep[i])
    rratio.append(rep[i]/act[i])
print(rratio)