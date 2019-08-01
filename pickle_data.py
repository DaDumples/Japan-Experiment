from numpy import *
import pandas as pd
import os
import matplotlib.pyplot as plt
import sys


save_plots = False
if len(sys.argv) > 1:
    if sys.argv[1] == 'save':
        save_plots = True

sample_length = .1 #m
monofilament_diameter = .2/1000 #m
flourocarbon_diameter = .22/1000 #m


paper_mono_max = 7.2/2.2*10/(pi*(8/1000)**2/4)/1e6
paper_floro_max = 10.7/2.2*10/(pi*(11/1000)**2/4)/1e6

rated_mono_max = 4/2.2*10/(pi*monofilament_diameter**2/4)/1e6
rated_floro_max = 6/2.2*10/(pi*flourocarbon_diameter**2/4)/1e6

filenames = []
for file in os.listdir():
    try:
        if file.split('.')[-1] == 'csv':
            filenames.append(file)
    except:
        pass


data = []
for filename in filenames:
    df = pd.read_csv(filename, skiprows = 19)
    point = {}
    fileinfo = filename.lower().split('_')
    # if fileinfo[-1][:-4] == '4':
    #     continue
    
    point['Condition'] = fileinfo[0]
    point['Length'] = float(fileinfo[2][0:-2])
    point['Rate'] = float(fileinfo[3][0:-4])
    point['Number'] = int(fileinfo[-1][:-4])
    

    if 'monofilament' in filename:
        point['Material'] = 'monofilament'
        max_stress = df['N'].max()/(pi*flourocarbon_diameter**2/4)
        point['Max Stress'] = max_stress/1e6
        point['Diameter'] = monofilament_diameter

    elif 'flourocarbon' in filename:
        point['Material'] = 'flourocarbon'
        max_stress = df['N'].max()/(pi*flourocarbon_diameter**2/4)
        point['Max Stress'] = max_stress/1e6
        point['Diameter'] = flourocarbon_diameter

    if fileinfo[0] == 'exposed':
        point['Exposure Time'] = float(fileinfo[5][0:-3])
        if fileinfo[4] == '12nm':
            point['Wavelength'] = '100-200'
        elif fileinfo[4] == '24nm':
            point['Wavelength'] = '200-400'

        data.append(point)
    else:
        point['Exposure Time'] = 0
        a = point.copy()
        b = point.copy()
        a['Wavelength'] = '100-200'
        b['Wavelength'] = '200-400'

        data.append(a)
        data.append(b)
    

    plt.figure()
    plt.plot(df['mm'], df['N'])
    plt.plot(df['mm'].iloc[df['N'].idxmax()], df['N'].max(),'or')
    plt.title(filename)
    plt.xlabel('Extension [mm]')
    plt.ylabel('Load [N]')
    if save_plots:
        plt.savefig(filename.replace('.csv', '.png'), bbox_inches = 'tight')
    plt.close()


data = pd.DataFrame(data)
data.to_pickle('all_data.pkl')
print(data)