# Lab-1: Uniform Cost Search

Here we will apply UCS to any given graph. Show the whole path if found, otherwise print "Unreachable".

- Sample input:

- ```markdown
  Start A 2
  Start B 1 
  A B 1 
  A C 3 
  A D 1 
  B D 5
  B Goal 10 
  C Goal 7 
  D Goal 4 
  END
  ```

where `node1 node2 c` denotes a path from `node1` to `node2` with cost `c`.

- Sample output: 

- ```markdown
  Start->A->D->Goal
  ```

Other test cases are available [here](https://github.com/zhangshun97/Artificial-Intelligence/tree/master/Labs/Lab_1_search/test_cases).