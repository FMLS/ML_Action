#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt

#Training data set
#each element in x represents (x0,x1,x2)
#x = [(1, 0., 3), (1, 1., 3), (1, 2., 3), (1, 3., 2) , (1, 4., 4)]
x = [(1, 0., 1.8),  (1, 1.2, 2.3),   (1, 1.5, 4.3), (1, 3., 2.4), (1, 2.8, 7.2), 
     (1, 3., 5.3),  (1, 3.4, 6.2), (1, 5.2, 4.43),  (1, 4.1, 8.5), (1, 8, 12.3),
     (1, 6.2, 8.8), (1, 7.5, 9.1)]

#y[i] is the output of y = theta0 * x[0] + theta1 * x[1] +theta2 * x[2]
y = [2.362, 4.52, 7.35, 5.51, 10.82,
     6.2,  8.5,  12.3, 7.4,  15.35,
     8.23, 17.2]

x_test_set = [(1, 1.2, 2.0), (1, 2.3, 3.44),   (1, 3.5, 7.8),  (1, 13.5, 29), (1, 4.1, 6.6), 
              (1, 21.33, 9.2), (1, 18.3, 40.4), (1, 27.5, 13.2), (1, 12.2, 7.32)]


x1 = []
for i in range(len(x)):
    x1.append(x[i][1])

x2 = []
for i in range(len(x)):
    x2.append(x[i][2])

colors = np.random.rand(len(x))
area = 50
plt.scatter(x1, x2, s = area, c = colors)
plt.xlabel('X1')
plt.ylabel('X2')

#epsilon = 0.000001
epsilon = 0.0001
#learning rate
alpha  = 0.001
diff   = [0,0]
error1 = 0
error0 = 0
m      = len(x)

#init the parameters to zero
theta0 = 1
theta1 = 1
theta2 = 1

sum0 = 0
sum1 = 0
sum2 = 0

total_count = 0


def h(x):
    return theta0 + theta1 * x[1] + theta1 * x[2]

def gradAscent(x, y):
    dataMatrix = np.mat(x)
    labelMat  = np.mat(y).transpose()
    m, n = np.shape(dataMatrix)
    weights = np.ones((n, 1))
    error0 = 0
    error1 = 0
    while True:
        hx       = dataMatrix * weights
        err      = labelMat - hx 
        weights  = weights + alpha * dataMatrix.transpose() * err

        error1 = 0
        for lp in range(len(x)):
            error1 += ( y[i] - h(x[i]) )**2/2
    
        if abs(error1 - error0) < epsilon:
            break
        else:
            error0 = error1
    return weights

def h2x(x, weights):
    return (weights[0] + weights[1] * x[1] + weights[2] * x[2])

weights = gradAscent(x, y)
#print [float(h2x(xi, weights)) for xi in x_test_set]
plt.plot([float(h2x(xi, weights)) for xi in x_test_set])
print weights


error0 = 0

while True:
    total_count = total_count + 1
    #calculate the parameters
    for i in range(m):
    #begin batch gradient descent
        diff[0] = y[i]- h(x[i])
        sum0 = sum0 + alpha * diff[0]* x[i][0]
        sum1 = sum1 + alpha * diff[0]* x[i][1]
        sum2 = sum2 + alpha * diff[0]* x[i][2]
    #end  batch gradient descent
    theta0 = sum0;
    theta1 = sum1;
    theta2 = sum2;


#    plt.plot([h(xi) for xi in x_test_set])
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

plt.plot([h(xi) for xi in x_test_set])
plt.plot([h(xi) for xi in x])
plt.show()

