from numpy import *
import pandas as pd
import os
import matplotlib.pyplot as plt

sample_length = .1 #m
monofilament_diameter = .0002 #m
flourocarbon_diameter = .00022 #m

filenames = []
for file in os.listdir():
    if file.split('.')[1] == 'csv':
        filenames.append(file)


data = {'flourocarbon':[], 'monofilament':[]}
for filename in filenames:
    df = pd.read_csv(filename, skiprows = 19)
    if 'monofilament' in filename:
        max_stress = df['N'].max()/monofilament_diameter
        data['monofilament'].append(max_stress)
    elif 'flourocarbon' in filename:
        max_stress = df['N'].max()/flourocarbon_diameter
        data['flourocarbon'].append(max_stress)

    plt.figure()
    plt.plot(df['mm'], df['N'])
    plt.plot(df['mm'].iloc[df['N'].idxmax()], df['N'].max(),'or')
    plt.title(filename)
    plt.xlabel('Extension [mm]')
    plt.ylabel('Load [N]')
    plt.savefig(filename.replace('.csv', '.png'), bbox_inches = 'tight')


data = pd.DataFrame(data)
mono_mean = data['monofilament'].mean()/1000
mono_std = data['monofilament'].std()/1000
flouro_mean = data['flourocarbon'].mean()/1000
flouro_std = data['flourocarbon'].std()/1000

stresses = [mono_mean, flouro_mean]
errors = [mono_std, flouro_std]

fig, ax = plt.subplots()
ax.bar([0,1], stresses, yerr = errors, capsize = 10)
ax.set_ylabel('Max Stress [kPa]')
ax.set_xlabel('Material')
ax.set_xticks([0,1])
ax.set_xticklabels(['Monofilament', 'Flourocarbon'])
ax.set_title('Pristine Material Properties')
plt.savefig('Pristine Material Properties.png',bbox_inches = 'tight')


plt.show()

