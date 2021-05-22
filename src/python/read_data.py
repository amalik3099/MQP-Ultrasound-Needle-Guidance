from PIL import Image
import sys
import numpy as np
import pandas as pd
import skinematics as skin


if __name__ == "__main__":

    path = "/home/amalik/Documents/listener/src/python/IMU_data/imu_data.csv"

    data = pd.read_csv(path)

    np_data = np.array(data.sort_values(by=['time']))
    np_data = np.delete(np_data, 0, 0)
    acc_data = np_data[:,0:3]*9.81
    augular_data = np.deg2rad(np_data[:,3:6])
    mag_data = np_data[:,6:9] 
    rt = np.mean(np_data[:,13:14])

    # print(rt)
    
    # To check difault orientation visit : https://github.com/clariusdev/motion
    # Fick ... Rz * Ry * Rx
    # quater_data = np.round(np_data[:,9:13], 5)
    # q = skin.quat.Quaternion(quater_data)
    # rotation_matrix = skin.quat.Quaternion.export(q)

    # print(rotation_matrix.shape)
     

    # fick_rad = skin.quat.Quaternion.export(q,'Fick')
    # fick_deg = np.degrees(fick_rad)
    
    # # position
    # pos = skin.imus.analytical(omega = augular_data , accMeasured = acc_data , rate = rt)


    # print(fick_deg)
    # print(pos[1])

    print(data.sort_values(by=['time']))