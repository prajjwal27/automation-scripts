import sys, shutil, os
import fileinput

dirname = os.path.dirname(__file__)
origin = os.path.join(dirname, 'Base.vasp')


z1 = 6.28193 #z-coord of layer 1
z2 = 11.76564 #z-coord of layer 2
z3 = 17.274295 #z-coord of layer 3

def grid(file, layer, num):
    match layer:
        case 1:
            #boundary co-ords of lower interlayer
            x1 = 1.001600192
            x2 = 9.404923370
            y1 = -0.660339949
            y2 = 6.040559139
            z = z1
        case 2:
            #boundary co-ords of middle interlayer
            x1 = 1.001600192
            x2 = 8.503136057
            y1 = -1.330141360
            y2 = 5.731814145
            z = z2
        case 3:
            #boundary co-ords of upper interlayer
            x1 = 1.030751585
            x2 = 9.108764315
            y1 = -1.666393362
            y2 = 4.704472243
            z = z3

    for i in range(10):
        if num<=(i*i):
            n = i
            break

    x1_step = ((x2 - x1)/(n-1))
    y1_step = ((y2 - y1)/(n-1))

    if (num%2==0):
        k = int(num/2)
    else:
        k = int((num/2)+1)

    ctr = 1
    for a in range(n):
        if (ctr > k):
            break
        for b in range(n):
            if (ctr > k):
                break
            x_res = x1+(a*x1_step)
            y_res = y1+(b*y1_step)
            file.write("     %.9f" % x_res + '         ' + "%.9f" % y_res + '         ' + "%.9f" % z + '\n')
            ctr = ctr+1

    ctr = 1
    for a in range(n):
        if (ctr > (num-k)):
            break
        for b in range(n):
            if (ctr > (num-k)):
                break
            x_res = x2-(a*x1_step)
            y_res = y2-(b*y1_step)
            file.write("     %.9f" % x_res + '         ' + "%.9f" % y_res + '         ' + "%.9f" % z + '\n')
            ctr = ctr+1

'''
    ctr = 1
    for a in range(n-1, 0, -1):
        if(ctr > (num-k)):
            break
        for b in range(n-1, 0, -1):
            if(ctr > (num-k)):
                break
            x_res = x1+(a*x1_step)
            y_res = y1+(b*y1_step)
            file.write("     %.9f" % x_res + '         ' + "%.9f" % y_res + '         ' + "%.9f" % z + '\n')
            ctr = ctr+1
'''

#file = sys.argv[1]
num = [int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])]
n = num[0]+num[1]+num[2]

suffix = str(num[0])+'-'+str(num[1])+'-'+str(num[2])
destination = os.path.join(dirname, "Selected", str(n), suffix)
if not os.path.exists(destination):
    os.makedirs(destination)
destination = os.path.join(destination, 'POSCAR')
print(destination)
shutil.copyfile(origin, destination)
for line in fileinput.input(destination, inplace=1):
    line = line.replace('   64   48    1', ('   64   48    '+str(n)))
    print(line, end='')
with open (destination, 'a') as file:
    for ly in range(1, 4):
        grid(file, ly, num[ly-1])