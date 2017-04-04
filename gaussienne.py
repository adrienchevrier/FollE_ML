
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
plt.title('relation tension/rapport cyclique')
plt.xlabel("rapport cyclique (%)")
plt.ylabel("tension (V)")
#plt.show()


mu = 0
variance = 1
sigma = math.sqrt(variance)
x = np.linspace(-3, 3, 100)
#plt.plot(x,mlab.normpdf(x, mu, sigma))

x2 = []
y2 = []
for x in range(0,100):
	x2.append(x)
	y2.append(12*x/100)

plt.plot(x2,y2)
plt.show()
'''plt.plot(x,(1700*mlab.normpdf(readings[0], 20, 2)))
plt.plot(x,(400*mlab.normpdf(x, 15, 2)))
plt.plot(x,(200*mlab.normpdf(x, 15, 2)))
plt.plot((150*100*mlab.normpdf(x2, 215, 100)))

plt.grid()
plt.xlim(0,500)
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
 	print("-",action)'''