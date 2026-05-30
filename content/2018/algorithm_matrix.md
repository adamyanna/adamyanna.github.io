# Algorithm Matrix

> 2018-10-26

Algorithm

2018-10-26 18:00:00 +0800

Algorithm requeirment

get shortest distance from 0 node for every non 0 node, save the value to the index of non 0 node, generate new matrix. Implementation

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
Draft

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
# if (i-1)
