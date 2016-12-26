#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt

#Training data set
#each element in x represents (x0,x1,x2)
#x = [(1, 0., 3), (1, 1., 3), (1, 2., 3), (1, 3., 2) , (1, 4., 4)]
x = [(1, 0.),  (1, 1),   (1, 1.5), (1, 2.), (1, 2.8), 
     (1, 3.),  (1, 3.4), (1, 4.),  (1, 4.1), (1, 8)]
#y[i] is the output of y = theta0 * x[0] + theta1 * x[1] +theta2 * x[2]
y = [2.362, 4.52, 7.35, 5.51, 10.82,
     6.2,  8.5,  12.3, 7.4,  15.35]

x_test_t = [1.2, 2.3, 3.5, 3.6, 3.8, 4.1, 4.6, 5.7, 7.5, 8.9, 11.2, 12.5, 15.5]

x_test = []
for i in range(len(x_test_t)):
    x_test.append((1, x_test_t[i]))



x_point = []
for i in range(len(x)):
    x_point.append(x[i][1])

print len(x),len(y),
colors = np.random.rand(len(x))
area = 50
plt.scatter(x_point, y, s = area, c = colors)

x_fin_point = []
for i in range(len(x_test)):
    x_fin_point.append(x_test[i][1])

#epsilon = 0.000001
epsilon = 0.0001
#learning rate
alpha  = 0.001
diff   = [0,0]
error1 = 0
error0 = 0
m      = len(x)

#init the parameters to zero
theta0 = 0
theta1 = 0
theta2 = 0

sum0 = 0
sum1 = 0
sum2 = 0

total_count = 0

def h(x):
    return theta0 + theta1 * x[1]

while True:
    total_count = total_count + 1
    #calculate the parameters
    for i in range(m):
    #begin batch gradient descent
        #diff[0] = y[i]-( theta0 + theta1 * x[i][1] + theta2 * x[i][2] )
        diff[0] = y[i]- h(x[i])
        sum0 = sum0 + alpha * diff[0]* x[i][0]
        sum1 = sum1 + alpha * diff[0]* x[i][1]
#        sum2 = sum2 + alpha * diff[0]* x[i][2]
    #end  batch gradient descent
    theta0 = sum0;
    theta1 = sum1;
#    theta2 = sum2;


    plt.plot(x_fin_point, [h(xi) for xi in x_test])
    #calculate the cost function
    error1 = 0
    for lp in range(len(x)):
        error1 += ( y[i] - h(x[i]) )**2/2

    if abs(error1-error0) < epsilon:
        break
    else:
        error0 = error1

#    print ' theta0 : %f, theta1 : %f, theta2 : %f, error1 : %f'%(theta0,theta1,theta2,error1)

print 'Done: theta0 : %f, theta1 : %f, theta2 : %f'%(theta0,theta1,theta2)
print 'total count: %d' % total_count

plt.plot(x_fin_point, [h(xi) for xi in x_test])
plt.xlabel('X1')
plt.ylabel('X2')
plt.show()

