# Message-Passing-For-Factor-Graphs
A simple implementation of sum-product algorithm for computing marginals over tree-structured factor graphs.

# Sample run
python sumproduct.py

The example in the code is depicted pictorially in factor_graph.jpeg. This means that we have a function f of 8 variables, such that it can be factorized as follows

f(X1,...,X_8) = f1(X1,X2,X3) * f2(X3,X4,X6) * f3(X4,X5,X7,X8)

The program computes the marginal of a variable in an efficient way. For instance, the marginal of X4, f(X4) is the summation of evaluation of f() over all other variables except X4. 



