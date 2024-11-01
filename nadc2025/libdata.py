import os
import threading
import pandas as pd

from ursina import Vec3

# Global variables to store data
    #raw values
px = py = pz = vx = vy = vz = mass = None
time_min = None
    #calculated values
trajectory_points = []
time_sec = []
time_hour = []
time_perc = []
velocities = []

#completion checks
init_done_events = {# only really useful if we do a lot of data loading+processing
    "raw": threading.Event(),
    "trajectory": threading.Event(),
    "time": threading.Event(),
    "velocity": threading.Event(),
}
def print_load_info():
    print("[Loading Order] dataset: status")
    for i in range(len(init_done_events)):
        key = list(init_done_events.keys())[i]
        status="Working..."
        if init_done_events[key].is_set():
            status="Finished!"

        print(f"\t[{i}] {key}: {status}")


def init():
    # Start reading and calculating in a separate thread
    threading.Thread(target=async_init).start()

def wait_until_ready(goal):#call with the ordered check you're waiting for
    assert goal in init_done_events.keys()
    init_done_events[goal].wait()# Block until all data is ready

def async_init():
    read()
    init_done_events["raw"].set() # Signal that data initialization is complete
    gen_trajectory()
    init_done_events["trajectory"].set() # Signal that data initialization is complete
    gen_timestamps()
    init_done_events["time"].set() # Signal that data initialization is complete
    gen_velocity()
    init_done_events["velocity"].set()


def read():
    #format: read,read,  write,write (separate lines to group purpose)
    global px,py,pz,mass,time_min, vx, vy, vz

    # Load datafile
    data = pd.read_csv(os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'dataset.csv'))

    # Raw data
    px = data['Rx(km)[J2000-EARTH]']#p: probe
    py = data['Ry(km)[J2000-EARTH]']
    pz = data['Rz(km)[J2000-EARTH]']
    mass = data['MASS (kg)']
    time_min = data['MISSION ELAPSED TIME (mins)']
    vx = data['Vx(km/s)[J2000-EARTH]']
    vy = data['Vy(km/s)[J2000-EARTH]']
    vz = data['Vz(km/s)[J2000-EARTH]']

def gen_trajectory():
    global px,py,pz,  trajectory_points

    for i in range(len(px)):
        trajectory_points.append(Vec3(px[i]/1000, py[i]/1000, pz[i]/1000))  # 1u = 1km

def gen_timestamps():
    global time_min,  time_sec,time_hour,time_perc

    for i in time_min:
        time_sec   .append(i*60)
        time_hour  .append(i/60)
        time_perc  .append(i/time_min.iloc[-1]) # Using iloc for thread safety

def gen_velocity():
    global velocities, vx, vy, vz
    
    for i in range(len (vx)):
        velocities.append(Vec3(float(vx[i]), float(vy[i]), float(vz[i])))
    

if __name__ == "__main__":
    print_load_info()
    async_init()

    import time as t
    start=t.time()

    while not init_done_events[list(init_done_events.keys())[-1]].is_set():#debugging in case our load times get slow
        print_load_info()
        print(f"Time: {t.time()-start}s")
