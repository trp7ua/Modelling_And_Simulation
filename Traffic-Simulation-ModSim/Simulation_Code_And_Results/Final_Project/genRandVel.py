import numpy as np
import random 
from numpy import float64


vel_max = 50
vel_min = 1
def returnRandomVelocity(segment_id):

    while True:

        #Section1
        cofOfFitCurve1= [-6.0636e-09  , 9.8999e-07 , -6.0960e-05 ,  1.3069e-03 ,  1.9313e-02 ,  9.3002e-02 - random.random()]
        
        #Section2
        cofOfFitCurve2= [1.6393e-08  , -2.4995e-06 ,   1.2355e-04 , -2.3032e-03 ,  3.5049e-02 ,  5.0025e-02 - random.random()]

        #Section3
        cofOfFitCurve3= [3.5041e-09 , -1.0241e-06 ,  6.8177e-05 , -1.6021e-03 ,  3.3640e-02 ,  7.4744e-02 - random.random()]

        #Section4
        cofOfFitCurve4= [2.8866e-09 , -1.1793e-06 ,  8.0935e-05 , -1.5814e-03 ,  2.4992e-02  , 9.0847e-03 - random.random()]

        #Section5
        cofOfFitCurve5= [6.2729e-09 , -1.7217e-06 , 1.1167e-04 , -2.3583e-03 ,  3.3446e-02 ,  8.7636e-03 - random.random()]

        #Section6
        cofOfFitCurve6= [-8.2051e-09 ,  3.4266e-06 , -3.1312e-04  , 1.0054e-02 , -7.8402e-02 ,  1.3946e-01 - random.random()]


        cofOfFitCurve = [cofOfFitCurve1, cofOfFitCurve2, cofOfFitCurve3, cofOfFitCurve4, cofOfFitCurve5, cofOfFitCurve6]


        c = cofOfFitCurve[segment_id-1]

        roots_all = np.roots(c)
        roots_real = []

        for index in range(0 , len(c)-1):
            if roots_all[index].imag == 0:
                if (roots_all[index].real >= vel_min) & (roots_all[index].real <= vel_max):
                    roots_real.append(roots_all[index].real)
        
        if len(roots_real) == 1:
            break
    
    
    return roots_real[0]

