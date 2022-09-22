# This is an implementation for Brian Beckman's paper "The Pysics of Racing" only the tire model with Pacejka Magic Formula, this project included the chapters 21,22,25.
# The parameters values are all from the paper!


from math import exp, sin
import math
import numpy as np
import matplotlib.pyplot as plt


# For Longitudinal Pacejka
b = [
    1.65,
    0,
    1688,
    0,
    229,
    0,
    0,
    0,
    -10,
    0,
    0,
    0,
    0,
    0,
]

# For Laterial Pacejka
a = [
    1.799,
    0,
    1688,
    4140,
    6.026,
    0,
    -0.3589,
    1,
    0,
    -6.111/1000,
    -3.224/100,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
]


def longPacejka(slip, Fz):
    D = Fz*(b[1]*Fz+b[2])
    B = (b[3]*Fz+b[4])*exp(-b[5]*Fz)/(b[0]*(b[1]*Fz+b[2]))
    E = (b[6]*Fz*Fz+b[7]*Fz+b[8])
    S = 100*slip+b[9]*Fz+b[10]

    return D*sin(b[0]*math.atan(S*B+E*(math.atan(S*B)-S*B)))+0


def latPacejka(slip, Fz, Y):
    D = (a[1]*Fz+a[2])*Fz
    B = a[3]*sin(2*math.atan(Fz/a[4]))*(1-a[5]*abs(Y))/(a[0]*(a[1]*Fz+a[2])*Fz)
    E = a[6]*Fz+a[7]
    S = slip+a[8]*Y+a[9]*Fz+a[10]
    Sv = ((a[11]*Fz+a[11])*Y+a[12])*Fz+a[13]
    return D*sin(a[0]*math.atan(S*B+E*(math.atan(S*B)-S*B)))+Sv

# longitudinal Version in chapter 21


xLong = []
yLong = []
for i in range(0, 1000):
    # Slip Ratio (Divided by 100 for the graph resolution so it is okay to put the for loop range from 0 to 1)
    slip = i/1000

    # Inside the function the slip ratio will be converted to percentage
    F = longPacejka(slip, 3.3)

    xLong.append(slip)
    yLong.append(F)

maxSlipRatio = yLong.index(np.max(yLong))/100
maxSlipRatio = .0796

# Laterial Version in chapter 22

xLat = []
yLat = []
for i in range(0, 10000):
    # Slip angle (Divided by 100 for the graph resolution so it is okay to put the for loop range from 0 to 100)
    slip = i / 100
    Fz = 500*9.81/1000
    Y = 0  # Camber Angle

    F = latPacejka(slip, 3.3, Y)

    xLat.append(slip)
    yLat.append(F)


# Divided by 100 because the graph resolution
maxSlipAngle = yLat.index(np.max(yLat))/100
# maxSlipAngle = 3.273

print(maxSlipRatio, maxSlipAngle)

plt.plot(xLong, yLong, label='longitudinal Force')
plt.xlabel('Slip Ratio')
plt.ylabel('longitudinal Force')
plt.savefig('Pacejka\'s Magic Formla (Long Version).png')
plt.show()

plt.plot(xLat, yLat, label='Laterial Force')
plt.xlabel('Slip Angle')
plt.ylabel('Lateral Force')
plt.savefig('Pacejka\'s Magic Formla (Lat Version).png')
plt.show()

# Combined Grip in chapter 25


steps = 50+1

xCombined = np.zeros((steps, steps))
yCombined = np.zeros((steps, steps))
zCombined = np.zeros((steps, steps))


for j in range(0, steps):
    for i in range(0, steps):

        # slipRatio = ((i/(steps/2))-1)*.2 #From -.2 to +.2 slip ratio
        # slipAngle = ((j/(steps/2))-1)*20 #From -20 to +20 slip angle
        # S = slipRatio/maxSlipRatio
        # A = slipAngle/maxSlipAngle

        S = (i/(steps/2))-1  # From 0 to 1
        A = (j/(steps/2))-1  # From 0 to 1

        p = math.sqrt(S * S + A * A)

        Fz = 3.3

        if (p == 0):
            p = 0.00001

        fx = (S/p)*longPacejka(p*maxSlipRatio, Fz)
        fy = (A/p)*latPacejka(p*maxSlipAngle, Fz, 0)

        xCombined[j, i] = S
        yCombined[j, i] = A
        zCombined[j, i] = math.sqrt(fx * fx + fy * fy)


ax = plt.axes(projection='3d')
ax.plot_surface(xCombined, yCombined, zCombined, rstride=1, cstride=1,
                cmap='winter', edgecolor='none')

ax.set_xlabel('Slip Ratio')
ax.set_ylabel('Slip Angle')
ax.set_zlabel('longitudinal Force')
plt.savefig('Traction Circle.png')
plt.show()

# ax = plt.axes(projection='3d')

# ax.contour3D(xCombined, yCombined, zCombined, 50, cmap='winter')
# ax.set_xlabel('Slip Ratio')
# ax.set_ylabel('Slip Angle')
# ax.set_zlabel('longitudinal Force')
# plt.savefig('Combined Grip 2.png')
# plt.show()
