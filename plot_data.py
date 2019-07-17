from numpy import *
import pandas as pd
import os
import matplotlib.pyplot as plt
import sys

def hsv_to_rgb(h, s, v):
    h_i = int(h*6)
    f = h*6 - h_i
    p = v * (1 - s)
    q = v * (1 - f*s)
    t = v * (1 - (1 - f) * s)
    if h_i == 0:
        r, g, b = v, t, p
    elif h_i==1:
      r, g, b = q, v, p 
    elif h_i==2:
        r, g, b = p, v, t
    elif h_i==3:
        r, g, b = p, q, v
    elif h_i==4:
        r, g, b = t, p, v
    elif h_i==5:
        r, g, b = v, p, q
    return [int(r*256), int(g*256), int(b*256)]

def generate_colors(n):
    gold = 0.618033988749895
    h = 0
    colors = []
    for i in range(n):
        colors.append(hsv_to_rgb(h, .5, .95))
        h += gold
        h %= 1
    return colors

save_plots = False
if len(sys.argv) > 1:
    if sys.argv[1] == 'save':
        save_plots = True

sample_length = .1 #m
monofilament_diameter = .0002 #m
flourocarbon_diameter = .00022 #m

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
    if 'monofilament' in filename:
        max_stress = df['N'].max()/monofilament_diameter
        point['Max Stress'] = max_stress/1000
        point['Material'] = 'monofilament'
        point['Condition'] = fileinfo[0]
        point['Length'] = float(fileinfo[2][0:-2])
        point['Rate'] = float(fileinfo[3][0:-4])
        point['Diameter'] = monofilament_diameter
        if fileinfo[0] == 'exposed':
            point['Exposure Time'] = float(fileinfo[4][0:-1])
        else:
            point['Exposure Time'] = 0

    elif 'flourocarbon' in filename:
        max_stress = df['N'].max()/flourocarbon_diameter
        point['Max Stress'] = max_stress/1000
        point['Material'] = 'flourocarbon'
        point['Condition'] = fileinfo[0]
        point['Length'] = float(fileinfo[2][0:-2])
        point['Rate'] = float(fileinfo[3][0:-4])
        point['Diameter'] = flourocarbon_diameter
        if fileinfo[0] == 'exposed':
            point['Exposure Time'] = float(fileinfo[4][0:-1])
        else:
            point['Exposure Time'] = 0

    data.append(point)

    plt.figure()
    plt.plot(df['mm'], df['N'])
    plt.plot(df['mm'].iloc[df['N'].idxmax()], df['N'].max(),'or')
    plt.title(filename)
    plt.xlabel('Extension [mm]')
    plt.ylabel('Load [N]')
    if save_plots:
        plt.savefig(filename.replace('.csv', '.png'), bbox_inches = 'tight')


data = pd.DataFrame(data)
data.to_pickle('all_data.pkl')
print(data)


exposures = []
for time in data["Exposure Time"]:
    if (not time in exposures) and (not isnan(time)):
        exposures.append(time)

num_bars = len(exposures)
colors = ['C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9']
total_width = .8
width = total_width/num_bars
fig, ax = plt.subplots()
material_labels = []
for x, material in enumerate(set(data['Material'])):
    temp_df = data[data['Material'] == material]
    material_labels.append(material)
    for y, exposure in enumerate(set(temp_df['Exposure Time'])):
        xpos = x - (total_width - width)/2 + y*width
        exp_df = temp_df[temp_df['Exposure Time'] == exposure]
        error = exp_df['Max Stress'].std()/len(exp_df['Max Stress']) 
        mean = exp_df['Max Stress'].mean()
        ax.bar(xpos, mean, width, yerr = error, capsize = 10, color = colors[y], alpha = .8)


ax.set_ylabel('Max Stress [kPa]')
ax.set_xlabel('Material')
ax.set_xticks(range(len(set(data['Material']))))
ax.set_xticklabels(material_labels)
ax.set_title('Material Properties vs Exposure Time')
plt.legend([str(x) + ' days' for x in set(data['Exposure Time'])])
plt.savefig('Material Properties vs Exposure Time.png',bbox_inches = 'tight')

plt.show()


# mono_mean = data['monofilament'].mean()/1000
# mono_std = data['monofilament'].std()/1000
# flouro_mean = data['flourocarbon'].mean()/1000
# flouro_std = data['flourocarbon'].std()/1000

# stresses = [mono_mean, flouro_mean]
# errors = [mono_std, flouro_std]

# fig, ax = plt.subplots()
# ax.bar([0,1], stresses, yerr = errors, capsize = 10)
# ax.set_ylabel('Max Stress [kPa]')
# ax.set_xlabel('Material')
# ax.set_xticks([0,1])
# ax.set_xticklabels(['Monofilament', 'Flourocarbon'])
# ax.set_title('Pristine Material Properties')
# plt.savefig('Pristine Material Properties.png',bbox_inches = 'tight')


# plt.show()