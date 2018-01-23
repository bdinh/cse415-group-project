# Rubik's Cube

This program was implemented solely for the purpose of learning about reinforcement learning. 

## What the program is supposed to do

This program will attempt solve a rubik's cube using reinforcement learning. To narrow the scope of the project, I worked only on solving a 2x2x2 cube. I had to formulate the problem first and decided to represent the state of the faces of the rubiks cube in a numpy array. I allowed for 90 degree turns in the problem formulation. This proved to be cumbersome as it resulted in a lot of possible states for the rubiks cube.

## Techniques used and brief description of how that technique works. 

I first formulated the rubiks cube, in order to apply searching algorithms within the state space. The state of the cube was defined through a numpy array that maps the indices of the array to correspond to the faces of the cube, as well as to a particular color. When defining the operators and the state transformation function, I decided on allowing our cube to permit 90 degree turns. This resulted in us having 12 operators that correspond to 6 faces and the 2 direction in which these faces can be turn, clockwise and counterclockwise. When it came to actually implementing reinforcement learning, I used Markov Decision Process. Through it, I implemented value iteration that calculated the q values for each state, q learning which helped finds the optimal policy. I also tried to implement iterative deepening A* to help generate more optimal states. With that, I implemented backtracking to find the optimal path. The code currently still needs to be optimize in order to efficiently explore worthy potential states. I read Richard Korf’s article on finding the optimal solution to a rubiks cube using pattern database but didn’t really fully understand it to attempt to break up our cube into sub problems to actually implement it. Though this would definitely be worthy attempt in the future.



