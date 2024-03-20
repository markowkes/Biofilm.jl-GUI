import matplotlib.pyplot as plt
import numpy as np


time = np.linspace(0, 10, 1000)
per_tstart = 2
per_amplitude = 2
per_period = 3
per_duration = .25
#if duration > period, make message stating that funciton will remain at high value

heavi_y_values = np.zeros(len(time))
#for i in range(len(time)):
#    heavi_y_values[i] = 0 if time[i] < per_tstart else per_amplitude*(1 - np.heaviside(((time[i] - per_tstart) % per_period) - per_duration, 0.5))
    #heavi_y_values[i] = (((time[i] - per_tstart) % per_period) - per_duration)
#print(heavi_y_values)

heavi_y_values = np.heaviside(time - per_tstart, 0.5)*(per_amplitude*(1 - np.heaviside(((time - per_tstart) % per_period) - per_duration, 0.5))) #put this in
fig, con_ax = plt.subplots()
con_ax.plot(time, heavi_y_values)
plt.show()