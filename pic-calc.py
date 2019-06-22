import numpy as np
import sys

def calc_points(num_angles):
    angles = [float(ii_angle) * 2.0 * np.pi /float(num_angles) for ii_angle in range(num_angles)]
    return [(np.cos(angle),np.sin(angle)) for angle in angles]

def calc_midpoints(num_angles,scale=1):
    points = calc_points(num_angles)
    points.append(points[0])
    return [(scale*(points[ii_mid][0]+points[ii_mid+1][0])/2.0,scale*(points[ii_mid][1]+points[ii_mid+1][1])/2.0) for ii_mid in range(num_angles)]

def grad_calc(ii,alpha,num_angles,forward):
    
    points  = calc_points(num_angles)

    
    if forward:

        return (points[ii][0] + alpha*(points[ii][0]-points[ii-1][0]),points[ii][1] + alpha*(points[ii][1]-points[ii-1][1]))

    else:

        return (points[ii][0] - alpha*(points[ii+1][0]-points[ii][0]),points[ii][1] - alpha*(points[ii+1][1]-points[ii][1]))

if __name__ == "__main__":

    alpha = float(sys.argv[2])
    
    num_angles = int(sys.argv[3])

    print(calc_points(num_angles))
    
    print(grad_calc(int(sys.argv[1]),alpha,num_angles,bool(int(sys.argv[4]))))
    
    print(calc_midpoints(num_angles,alpha))
