
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.mlab as mlab
import math
#%matplotlib inline
#df["Unnamed: 0"] = df["Unnamed: 0"].astype("category").cat.codes
data = [1,2,3,4,5,6,7,8,9,10]
#for x in range(1,20):
#	data[x] = x

#plt.scatter(data,data)
plt.title('sensor values')
plt.xlabel("sensor")
plt.ylabel("distance")
#plt.show()

import matplotlib.pyplot as plt

mu = 15
variance = 0.1
sigma = math.sqrt(variance)
x = np.linspace(0, 100, 100)
plt.plot(x,5000*mlab.normpdf(x, mu, 5))

plt.grid()
plt.xlim(0,40)
#plt.ylim(0,0.25)
plt.show()
y=5000*mlab.normpdf(15, mu, 2)
print("y=", y)

# Plot between -10 and 10 with .001 steps.
#x_axis = np.arange(-10, 10, 0.001)
# Mean = 0, SD = 2.
#plt.plot(x_axis, norm.pdf(x_axis,0,2))

for x in range(1,20):
 	action = np.random.randint(0, 3)
 	print("-",action)