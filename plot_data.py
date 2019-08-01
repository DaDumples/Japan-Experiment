from numpy import *
import pandas as pd
import os
import matplotlib.pyplot as plt
import sys


data = pd.read_pickle('all_data.pkl')

colors = ['C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9']
total_width = .8
results = []

print(data)

wavelengths = set(data['Wavelength'])
materials = set(data['Material'])


groups = data.groupby(['Wavelength', 'Material','Exposure Time'])
means = groups['Max Stress'].mean()
stds = groups['Max Stress'].std()
counts = groups['Max Stress'].count()
print(counts)

for wavelength in wavelengths:
    plt.figure()
    ax = plt.axes()




    material_labels = []
    for x, material in enumerate(materials):
        material_labels.append(material)

        temp = data[data['Material'] == material]
        temp = temp[temp['Wavelength'] == wavelength]
        exposures = sort(list(set(temp['Exposure Time'])))

        width = total_width/len(exposures)
        for y, exposure in enumerate(exposures):
            xpos = x - (total_width - width)/2 + y*width

            mean = means.loc[(wavelength, material, exposure)]
            error = stds.loc[(wavelength, material, exposure)]/sqrt(counts.loc[(wavelength, material, exposure)])

            ax.bar(xpos, mean, width, yerr = error, capsize = 10, color = colors[y], alpha = .8)


    ax.set_ylabel('Max Stress [GPa]')
    ax.set_xlabel('Material')
    ax.set_xticks(range(len(materials)))
    ax.set_xticklabels(material_labels)
    ax.set_title('Material Properties vs Exposure Time at '+str(wavelength)+'nm')
    plt.legend([str(x) + ' ESH' for x in exposures])
    plt.savefig('Material Properties vs Exposure Time at '+str(wavelength)+'nm.png',bbox_inches = 'tight')

plt.show()












# wavelengths = [x for x in set(data['Wavelength']) if x != 0]
# for wavelength in wavelengths:

#     relevant = data['Wavelength'] == wavelength
#     zero = data['Wavelength'] == 0
#     wave_data = data[relevant or zero]

#     exposures = set(wave_data['Exposure Time'])
#     num_bars = len(exposures)
    
#     width = total_width/num_bars
#     fig, ax = plt.subplots()
#     material_labels = []
    
#     order = sort(list(set(wave_data['Exposure Time'])))
#     for x, material in enumerate(set(wave_data['Material'])):
#         temp_df = wave_data[wave_data['Material'] == material]
#         temp_df.sort_values(by = 'Exposure Time')
#         material_labels.append(material)
#         for y, exposure in enumerate(order):
#             xpos = x - (total_width - width)/2 + y*width
#             exp_df = temp_df[temp_df['Exposure Time'] == exposure]
#             error = exp_df['Max Stress'].std()/len(exp_df['Max Stress']) 
#             mean = exp_df['Max Stress'].mean()
#             ax.bar(xpos, mean, width, yerr = error, capsize = 10, color = colors[y], alpha = .8)

#             results.append({'Material':material, 'Exposure Time': exposure, 'Failure Load': mean, 'Error': error, 'Wavelength': wavelength})


#     ax.set_ylabel('Max Stress [GPa]')
#     ax.set_xlabel('Material')
#     ax.set_xticks(range(len(set(wave_data['Material']))))
#     ax.set_xticklabels(material_labels)
#     ax.set_title('Material Properties vs Exposure Time')
#     plt.legend([str(x) + ' ESH' for x in order])
#     plt.savefig('Material Properties vs Exposure Time at '+str(wavelength)+'nm.png',bbox_inches = 'tight')

# results = pd.DataFrame(results)
# print(results)

# plt.show()


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