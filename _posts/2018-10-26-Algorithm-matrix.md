---
title: Algorithm Matrix
author: Teddy
date: 2018-10-26 18:00:00 +0800
categories: [实践, 算法训练]
tags: [Algorithm]
---


# Algorithm requeirment
* **get shortest distance from 0 node for every non 0 node, save the value to the index of non 0 node, generate new matrix.**

# Implementation
```python
#!/usr/bin/python
import random

def matrix_distance(origin_matrix):
    one_list = []
    zero_list = []
    m_edge = len(origin_matrix[0])
    n_edge = len(origin_matrix)
    for i, v_list in enumerate(origin_matrix):
        for j, v in enumerate(v_list):
            if v > 0:
                one_list.append((i, j))
            else:
                zero_list.append((i, j))
    matrix_plus_one(origin_matrix, zero_list, one_list, m_edge, n_edge)


def matrix_plus_one(origin_matrix, outter_node_list, inner_node_list, m_edge, n_edge):
    n_outter_list = []
    n_inner_list = []
    for i, j in inner_node_list:
        if 0 <= i - 1 < n_edge and (i - 1, j) in outter_node_list:
            n_outter_list.append((i, j))
        elif 0 <= i + 1 < n_edge and (i + 1, j) in outter_node_list:
            n_outter_list.append((i, j))
        elif 0 <= j - 1 < m_edge and (i, j - 1) in outter_node_list:
            n_outter_list.append((i, j))
        elif 0 <= j + 1 < m_edge and (i, j + 1) in outter_node_list:
            n_outter_list.append((i, j))
        else:
            n_inner_list.append((i, j))
    for i, j in n_inner_list:
        origin_matrix[i][j] += 1
    if len(n_inner_list) > 0:
        matrix_plus_one(origin_matrix, n_outter_list, n_inner_list, m_edge, n_edge)
    else:
        print_matrix(origin_matrix)


def print_matrix(matrix):
    for v in matrix:
        print v

def generate_random_number():
    # return random.randint(0, 1)
    if random.randint(0,100) > 1:
        return 1
    else:
        return 0

def main():
    matrix_size = 30
    matrix = []
    for _ in range(matrix_size):
        tmp_list = []
        for _ in range(matrix_size):
            tmp_list.append(generate_random_number())
        matrix.append(tmp_list)
    print_matrix(matrix)
    print "result:"
    matrix_distance(matrix)

if __name__ == '__main__':
    main()
```


# Draft
```python
#!/usr/bin/python


# | 1, 0, 1, 0, 0 |
# | 1, 0, 1, 0, 0 |
# | 1, 0, 1, 0, 0 |
# | 1, 0, 1, 0, 0 |
# | 1, 0, 1, 0, 0 |
# | 1, 0, 1, 0, 0 |
# get shortest distance from 0 node for every node
# map
#
# m = range(origin_matrix)
# n = range(v_list)
# if (i-1) in m and origin_matrix[i-1][j] == 0:
#                     z_list.append((i,j))
#                 elif (i+1) in m and origin_matrix[i+1][j] == 0:
#                     z_list.append((i,j))
#                 elif (j-1) in n and v_list[j-1] == 0:
#                     z_list.append((i,j))
#                 elif (j+1) in n and v_list[j+1] == 0:
#                     z_list.append((i,j))
#                 else

import random


def matrix_distance(origin_matrix):
    print_matrix(origin_matrix)
    # find all 1
    one_list = []
    zero_list = []
    m_edge = len(origin_matrix[0])
    n_edge = len(origin_matrix)
    print m_edge
    print n_edge
    for i, v_list in enumerate(origin_matrix):
        for j, v in enumerate(v_list):
            if v > 0:
                one_list.append((i, j))
            else:
                zero_list.append((i, j))
    matrix_plus_one(origin_matrix, zero_list, one_list, m_edge, n_edge)


def matrix_plus_one(origin_matrix, outter_node_list, inner_node_list, m_edge, n_edge):
    n_outter_list = []
    n_inner_list = []
    for i, j in inner_node_list:
        # print i, j
        # print m_edge
        # if 0 <= j-1 < m_edge:
        #     print i, j
        #     if (i, j-1) in outter_node_list:
        #         print "============================"
        #         print i, j-1
        if 0 <= i - 1 < n_edge and (i - 1, j) in outter_node_list:
            n_outter_list.append((i, j))
        elif 0 <= i + 1 < n_edge and (i + 1, j) in outter_node_list:
            n_outter_list.append((i, j))
        elif 0 <= j - 1 < m_edge and (i, j - 1) in outter_node_list:
            n_outter_list.append((i, j))
        elif 0 <= j + 1 < m_edge and (i, j + 1) in outter_node_list:
            n_outter_list.append((i, j))
        else:
            n_inner_list.append((i, j))
    # print "OUTTER:"
    # print n_outter_list
    # print "INNER:"
    # print n_inner_list
    # print n_outter_list
    # tmp_i, tmp_j = outter_node_list[0]
    # print tmp_i, tmp_j
    # if origin_matrix[tmp_i, tmp_j] > 0:
    print "========================================"
    print_matrix(origin_matrix)
    print "========================================"
    for i, j in n_inner_list:
        origin_matrix[i][j] += 1
    print_matrix(origin_matrix)
    if len(n_inner_list) > 0:
        matrix_plus_one(origin_matrix, n_outter_list, n_inner_list, m_edge, n_edge)
    else:
        print "--------------------------------------------------------------------"
        print_matrix(origin_matrix)


def print_matrix(matrix):
    # print "-".join(map(str,range(len(matrix[0]))))
    # for v in matrix:
    #     # separate = " , "
    #     print v
    # for sub_v in v:
    #     print sub_v
    for i, v_list in enumerate(matrix):
        for j, v in enumerate(v_list):
            print matrix[i][j]
            if matrix[i][j] == 2:
                print "&&&&&&&&&&&&&&&&&&&&"
                print i, j
            matrix[i][j] += 1
    for v in matrix:
        print v


def generate_random_number():
    return random.randint(0, 1)


def main():
    # m = len(list_1)

    list_1 = [0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1]
    list_2 = [0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1]
    list_3 = [0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1]
    list_4 = [0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1]
    list_5 = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1]
    list_6 = [1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1]
    list_7 = [1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1]
    list_8 = [1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1]
    list_9 = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1]
    list_10 = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1]
    list_11 = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1]
    list_12 = [1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1]
    list_13 = [0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1]
    list_14 = [1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1]
    list_15 = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1]
    list_16 = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1]
    list_17 = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1]
    list_18 = [1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1]
    # v = len(v_list)
    list_1.extend(list_1)
    list_2.extend(list_2)
    list_3.extend(list_3)
    list_4.extend(list_4)
    list_5.extend(list_5)
    list_6.extend(list_6)
    list_7.extend(list_7)
    list_8.extend(list_8)
    list_9.extend(list_9)
    list_10.extend(list_10)
    list_11.extend(list_11)
    list_12.extend(list_12)
    list_13.extend(list_13)
    list_14.extend(list_14)
    list_15.extend(list_15)
    list_16.extend(list_16)
    list_17.extend(list_17)
    list_18.extend(list_18)
    v_list = [list_1, list_2, list_3, list_4, list_5, list_6, list_7, list_8, list_9, list_10, list_11, list_12,
              list_13, list_14, list_15, list_16, list_17, list_18]
    # v_list = [list_1, list_2, list_3, list_4, list_5, list_6,  list_7, list_8, list_9, list_10, list_11, list_12, list_13, list_14, list_15, list_16, list_17, list_18,]
    # matrix_distance(v_list)
    # print_matrix(v_list)

    # v_list_n = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
    input_list = []
    for i in range(16):
        tmp_list = []
        for i in range(16):
            tmp_list.append(generate_random_number())
        input_list.append(tmp_list)
    print_matrix(input_list)
    print generate_random_number()


if __name__ == '__main__':
    main()

# !/usr/bin/python

# | 1, 0, 1, 0, 0 |
# | 1, 0, 1, 0, 0 |
# | 1, 0, 1, 0, 0 |
# | 1, 0, 1, 0, 0 |
# | 1, 0, 1, 0, 0 |
# | 1, 0, 1, 0, 0 |
# get shortest distance from 0 node for every node
# map
#
# m = range(origin_matrix)
# n = range(v_list)
# if (i-1) in m and origin_matrix[i-1][j] == 0:
#                     z_list.append((i,j))
#                 elif (i+1) in m and origin_matrix[i+1][j] == 0:
#                     z_list.append((i,j))
#                 elif (j-1) in n and v_list[j-1] == 0:
#                     z_list.append((i,j))
#                 elif (j+1) in n and v_list[j+1] == 0:
#                     z_list.append((i,j))
#                 else

import random


def matrix_distance(origin_matrix):
    print_matrix(origin_matrix)
    # find all 1
    one_list = []
    zero_list = []
    m_edge = len(origin_matrix[0])
    n_edge = len(origin_matrix)
    print m_edge
    print n_edge
    for i, v_list in enumerate(origin_matrix):
        for j, v in enumerate(v_list):
            if v > 0:
                one_list.append((i, j))
            else:
                zero_list.append((i, j))
    matrix_plus_one(origin_matrix, zero_list, one_list, m_edge, n_edge)


def matrix_plus_one(origin_matrix, outter_node_list, inner_node_list, m_edge, n_edge):
    n_outter_list = []
    n_inner_list = []
    for i, j in inner_node_list:
        # print i, j
        # print m_edge
        # if 0 <= j-1 < m_edge:
        #     print i, j
        #     if (i, j-1) in outter_node_list:
        #         print "============================"
        #         print i, j-1
        if 0 <= i - 1 < n_edge and (i - 1, j) in outter_node_list:
            n_outter_list.append((i, j))
        elif 0 <= i + 1 < n_edge and (i + 1, j) in outter_node_list:
            n_outter_list.append((i, j))
        elif 0 <= j - 1 < m_edge and (i, j - 1) in outter_node_list:
            n_outter_list.append((i, j))
        elif 0 <= j + 1 < m_edge and (i, j + 1) in outter_node_list:
            n_outter_list.append((i, j))
        else:
            n_inner_list.append((i, j))
    # print "OUTTER:"
    # print n_outter_list
    # print "INNER:"
    # print n_inner_list
    # print n_outter_list
    # tmp_i, tmp_j = outter_node_list[0]
    # print tmp_i, tmp_j
    # if origin_matrix[tmp_i, tmp_j] > 0:
    print "========================================"
    print_matrix(origin_matrix)
    print "========================================"
    for i, j in n_inner_list:
        origin_matrix[i][j] += 1
    print_matrix(origin_matrix)
    if len(n_inner_list) > 0:
        matrix_plus_one(origin_matrix, n_outter_list, n_inner_list, m_edge, n_edge)
    else:
        print "--------------------------------------------------------------------"
        print_matrix(origin_matrix)


def print_matrix(matrix):
    # print "-".join(map(str,range(len(matrix[0]))))
    # for v in matrix:
    #     # separate = " , "
    #     print v
    # for sub_v in v:
    #     print sub_v
    for i, v_list in enumerate(matrix):
        for j, v in enumerate(v_list):
            print matrix[i][j]
            if matrix[i][j] == 2:
                print "&&&&&&&&&&&&&&&&&&&&"
                print i, j
            matrix[i][j] += 1
    for v in matrix:
        print v


def generate_random_number():
    return random.randint(0, 1)


def main():
    # m = len(list_1)

    list_1 = [0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1]
    list_2 = [0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1]
    list_3 = [0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1]
    list_4 = [0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1]
    list_5 = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1]
    list_6 = [1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1]
    list_7 = [1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1]
    list_8 = [1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1]
    list_9 = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1]
    list_10 = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1]
    list_11 = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1]
    list_12 = [1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1]
    list_13 = [0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1]
    list_14 = [1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1]
    list_15 = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1]
    list_16 = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1]
    list_17 = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1]
    list_18 = [1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1]
    # v = len(v_list)
    list_1.extend(list_1)
    list_2.extend(list_2)
    list_3.extend(list_3)
    list_4.extend(list_4)
    list_5.extend(list_5)
    list_6.extend(list_6)
    list_7.extend(list_7)
    list_8.extend(list_8)
    list_9.extend(list_9)
    list_10.extend(list_10)
    list_11.extend(list_11)
    list_12.extend(list_12)
    list_13.extend(list_13)
    list_14.extend(list_14)
    list_15.extend(list_15)
    list_16.extend(list_16)
    list_17.extend(list_17)
    list_18.extend(list_18)
    v_list = [list_1, list_2, list_3, list_4, list_5, list_6, list_7, list_8, list_9, list_10, list_11, list_12,
              list_13, list_14, list_15, list_16, list_17, list_18]
    # v_list = [list_1, list_2, list_3, list_4, list_5, list_6,  list_7, list_8, list_9, list_10, list_11, list_12, list_13, list_14, list_15, list_16, list_17, list_18,]
    # matrix_distance(v_list)
    # print_matrix(v_list)

    # v_list_n = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
    input_list = []
    for i in range(16):
        tmp_list = []
        for i in range(16):
            tmp_list.append(generate_random_number())
        input_list.append(tmp_list)
    print_matrix(input_list)
    print generate_random_number()


def fib_alg():
    pass

if __name__ == '__main__':
    main()
```
