import time
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import collections

TIME_FRAME = 60
FREQUENCY = 1

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
ax1.spines["right"].set_visible(False)
ax1.spines["top"].set_visible(False)

x = [0-(1.0/FREQUENCY)*v for v in reversed(range(TIME_FRAME * FREQUENCY))]
wattage_d = collections.deque(maxlen=TIME_FRAME * FREQUENCY)
for i in range(TIME_FRAME * FREQUENCY):
    wattage_d.append(0)

def update_wattage(frame):
    with open("/sys/class/power_supply/BAT0/current_now", "r") as current:
        current_A = int(current.readline())/1000000.0
    with open("/sys/class/power_supply/BAT0/voltage_now", "r") as voltage:
        voltage_V = int(voltage.readline())/1000000.0
    wattage = current_A * voltage_V
    wattage_d.append(wattage)
    ax1.clear()
    ax1.plot(x,wattage_d)
    ax1.set_ylim(bottom=0)
    ax1.text(0.0, wattage, f"{wattage:9.2f}") 


ani = animation.FuncAnimation(fig, update_wattage, interval=1000/FREQUENCY)
plt.show()
