# coding: utf-8

import numpy as np
import os
import itertools

# data position
INPUT_DATA = r'.../'

file_list = []
count = 0

# go through all the subfolders and files
for parent, dir_names, file_names in sorted(os.walk(INPUT_DATA)):
    for file_name in file_names:
        file_list.append(file_name)  # get the list of all filenames
        count += 1

rank_all = []
group_number = 10   # how many groups
every_group_people =   # how many people in each group
every_people_images =   # how many images of each person in each group
every_group_images = int(len(file_list)/group_number)  # how many images in each group

for i in range(group_number):  
    file_group = file_list[every_group_images*i:(every_group_images*(i+1)-1)]
    rank_group_same = []
    rank_group_diff = []
    list_str = ''

    for j in range(every_group_people):  
        file_50 = file_group[every_people_images*j:(every_people_images*(j+1)-1)]
        all_rank_1 = list(itertools.combinations(file_50, 2))
        
        # select 300 combinations for the same people pairs among images in each group
        # in each group, the former n-1 people have the same images(aliquot),
        # while the last person has a different number of images(remainder)
        # then sample at equal intervals for 'same people pairs' for each person
        if j < every_group_people - 1:   

            # judge whether the remainder is zero, if it's zero, it can't be used as 'end_postion'
            if int(len(all_rank_1) % ((3000/group_number) // (every_group_people - 1))) == 0:
                rank_1 = all_rank_1[::int(len(all_rank_1) // ((3000 / group_number) // (every_group_people - 1)))]
            else:                       
                rank_1 = all_rank_1[0:(-1) * int(len(all_rank_1) % ((3000/group_number) // (every_group_people - 1))):
                                int(len(all_rank_1) // ((3000/group_number) // (every_group_people - 1)))]
        else:
            if int(len(all_rank_1) % ((3000 / group_number) % (every_group_people - 1))) == 0:
                rank_1 = all_rank_1[::int(len(all_rank_1) // ((3000 / group_number) % (every_group_people - 1)))]
            else:
                rank_1 = all_rank_1[0:(-1) * int(len(all_rank_1) % ((3000 / group_number) % (every_group_people - 1))):
                                    int(len(all_rank_1) // ((3000 / group_number) % (every_group_people - 1)))]

        # combine the 300 'same people pairs'
        rank_group_same.extend(rank_1)
        list_str = list_str + str(j)

    # when selecting 'different people pairs', compute the permutations
    # implement permutations for images for each person using 'Cartesian Product' to obtain pairs, then sample at equal intervals for pairs
    list_index = list(itertools.combinations(list_str, 2))  # for example, if there are 8 people in each group, then the list is '01234567'

    combination_number = int(every_group_people * (every_group_people - 1) / 2)  # in the example, it's 8*7/2=28
   
   for k in range(combination_number):
   
        pair = list_index[k]
        
        people1 = file_group[every_people_images*int(pair[0]):(every_people_images*(int(pair[0])+1)-1)]
        people2 = file_group[every_people_images*int(pair[1]):(every_people_images*(int(pair[1])+1)-1)]

        pairs = list(itertools.product(people1, people2))

        if k < combination_number - 1:  # in the example, it's < 28-1
            if int(len(pairs) % ((3000 / group_number) // (combination_number - 1))) == 0:
                rank_2 = pairs[::int(len(pairs) // ((3000 / group_number) // (combination_number - 1)))]
            else:
                rank_2 = pairs[0:(-1) * int(len(pairs) % ((3000 / group_number) // (combination_number - 1))):
                                    int(len(pairs) // ((3000 / group_number) // (combination_number - 1)))]
        else:                           # in the example, it's = 28
            if int(len(pairs) % ((3000 / group_number) % (combination_number - 1))) == 0:
                rank_2 = pairs[::int(len(pairs) // ((3000 / group_number) % (combination_number - 1)))]
            else:
                rank_2 = pairs[0:(-1) * int(len(pairs) % ((3000 / group_number) % (combination_number - 1))):
                                    int(len(pairs) // ((3000 / group_number) % (combination_number - 1)))]

        # combine the 300 pairs for 'different people pairs'
        rank_group_diff.extend(rank_2)

    print(len(rank_group_same))  # 300
    print(len(rank_group_diff))  # 300

    # combine 300 'same people pairs' and 300 'different people pairs' as a group(there are 10 groups in total, that is 6000 pairs)
    rank_all.extend(rank_group_same)
    rank_all.extend(rank_group_diff)

print(len(rank_all))  # 6000
print(rank_all)       # 6000 list of results

# ############################## begin to write to the txt file #############################
file = open(r'.../pairs_6000.txt', 'w')

for iter in range(6000):

    content1 = rank_all[iter][0]  # fileL
    content2 = rank_all[iter][1]  # fileR
    group_num = str(iter//600 + 1)  # fold, also is the group number, from 1 to 10

    # flag, also is the label, 1 for 'same people pairs, -1 for 'different people pairs'
    if (iter // 300) % 2 == 0:
        flag = str(1)
    else:
        flag = str(-1)

    # write the content, don't forget the delimiter and enter
    file.write(content1 + '\t' + content2 + '\t' + group_num + '\t' + flag + '\t' + '\n')

# release memory the txt file used
file.close()




##########################################################
# @author : sjy-1995
# time : 2019/8/24
# place : Beijing
##########################################################






