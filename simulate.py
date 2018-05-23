import sys
import random
import math
import numpy
import matplotlib.pyplot as plot
from matplotlib.animation import FuncAnimation

#Run simulate.py, input number of particles and watch animation

# Setting up variables
pi = math.pi
RoF = 1
RoP = 5
Visc = 0.0001
R = 0.001
t = 0.01
Volume = (4/3) * pi * pow(R, 3)
particles = []
nEl = int(input('Enter amount of particles: '))
x = [None]*nEl
y = [None]*nEl
print('Simulation will run with ', nEl, ' elements.')

# Particle Class
class Particle:
    def __init__(self):
        self.x = random.random() * 2 * pi
        self.y = random.random() * 2 * pi
        self.up = 0
        self.vp = 0
        self.fx = 0
        self.fy = 0
    # Position fnctions
    def xpos(self):
        self.x = self.x + t*self.up

    def ypos(self):
        self.y = self.y + t*self.vp
    # Particle velocity functions
    def uparticle(self):
        self.up = self.up + (t*self.fx) / (RoP*Volume)

    def vparticle(self):
        self.vp = self.vp + (t*self.fy) / (RoP*Volume)
    # Force acting on particle functions
    def xforce(self, uf):
        self.fx = 6 * pi * RoF * Visc * R * (uf - self.up)

    def yforce(self, vf):
        self.fy = 6 * pi * RoF * Visc * R * (vf - self.vp)

# Fluid Class
class Fluid:
    def __init__(self, N):
        self.uf = 0
        self.vf = 0
        self.nElements = N
        self.particles = [None]*N
        # initializing particles in fluid
        for k in range(N):
            self.particles[k] = Particle()
    # Fluid flow velocity functions
    def uflow(self, x, y):
        self.uf = math.cos(x) * math.sin(y)

    def vflow(self, x, y):
        self.vf = -math.sin(x) * math.cos(y)

class Printer():
    def __init__(self, data):
        sys.stdout.write("\r\x1b[K"+data.__str__())
        sys.stdout.flush()

# Initializing fluid
fl = Fluid(nEl)
# Initializing plot
fig = plot.figure()
ax = plot.axes(xlim=(0, 2*pi), ylim=(0, 2*pi))

# update position of each particles
def update(i):
    ax.clear()
    for j in range(nEl):
        while fl.particles[j].x > 2*pi:
            fl.particles[j].x = numpy.remainder(fl.particles[j].x, 2*pi)
        while fl.particles[j].x < 0:
            fl.particles[j].x = numpy.remainder(fl.particles[j].x, 2*pi)
        while fl.particles[j].y > 2*pi:
            fl.particles[j].y = numpy.remainder(fl.particles[j].y, 2*pi)
        while fl.particles[j].y < 0:
            fl.particles[j].y = numpy.remainder(fl.particles[j].y, 2*pi)
        fl.uflow(fl.particles[j].x, fl.particles[j].y)
        fl.vflow(fl.particles[j].x, fl.particles[j].y)
        fl.particles[j].uparticle()
        fl.particles[j].vparticle()
        fl.particles[j].xforce(fl.uf)
        fl.particles[j].yforce(fl.vf)
        fl.particles[j].xpos()
        fl.particles[j].ypos()
        #output = "uflow = %f, vflow = %f" % (fl.uf, fl.vf)
        #Printer(output)
    for j in range(nEl):
        x[j] = fl.particles[j].x
        y[j] = fl.particles[j].y
    return ax.scatter(x, y, color='g', alpha=0.5)

# animate
animation = FuncAnimation(fig, update, interval=5)
plot.show()
