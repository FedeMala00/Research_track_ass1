from __future__ import print_function

import time
from sr.robot import *

a_th = 2.0
""" float: Threshold for the control of the orientation"""

d_th = 0.4
""" float: Threshold for the control of the linear distance"""

R = Robot()


def drive(speed, seconds):

    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0


def turn(speed, seconds):

    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

# Function which returns the distance and relative angle 
# to the token in the robot field of view and that is in "code" which is a list 
def find_token_new(code):
    
    dist = 100
    for token in R.see():
       if token.info.code in code:
        if token.dist < dist:
            dist = token.dist
            rot_y = token.rot_y
    if dist == 100:
        return -1, -1
    else:
        return dist, rot_y

# Function which returns the distance and the relative angle to the closest token
# that is NOT in the code_list given as input.
# This function will be used in order to avoid grabbing all the tokens already grabbed
def find_token(code_list):
 
    dist = 100
    for token in R.see():
      if token.info.code not in code_list:
        if token.dist < dist:
            dist = token.dist
            rot_y = token.rot_y
    if dist == 100:
        return -1, -1
    else:
        return dist, rot_y

# Function which makes the robot grab the closest token whose code is absent in the code list given as input,
# and returns the code of the grabbed token (this return is necessary for adding the correspondent token to the already grabbed token list)
def reach_token(code):
    var = True
    while var:
        dist, rot_y = find_token(code)  # we look for markers absent in code that is a list
        if dist == -1:
            turn(10, 1)  # if no tokens are detected it turns

        elif dist < d_th:
            print("Found it!")
            R.grab()  # if we are close to the token, we grab it.
            print("Gotcha!") 
            var = False             
            dist_list = []
            # for loop to create a list containing all the dist values of the token
            for i in R.see():
                dist_list.append(i.centre.polar.length)
            
            min_val = min(dist_list)  # select the minimum distance token (that is the grabbed one)
            min_index = dist_list.index(min_val)  # find the correspondent index                             
            return R.see()[min_index].info.code  # return the code of the grabbed token     

        elif -a_th <= rot_y <= a_th:  # if the robot is well aligned with the token, we go forward
            print("Ah, here we are!.")
            drive(25, 0.5)
        elif rot_y < -a_th:  # if the robot is not well aligned with the token, we move it on the left or on the right
            print("Left a bit...")
            turn(-2, 0.5)
        elif rot_y > a_th:
            print("Right a bit...")
            turn(+2, 0.5)

# Function to reach the clustering point 
def reach_dist_rot(code):
    var = True
    d_th_new = 0.6 # chosen this value because 0.4 is used to grab, so release should consider the fact that the robot is holding the token 
    while var:
        dist, rot_y = find_token_new(code) # we look for markers whose code is in the given list "code" because it contains the code of the clustering point 
        if dist == -1:                     # + all the already released tokens. So every time one is released is added to this list 
            print("Turning to see clustering point")
            turn(10, 1)  # the robot turns

        elif dist < d_th_new:
            print("Arrived to clustering point")
            R.release() # the token is released 
            var = False
            return 0

        elif -a_th <= rot_y <= a_th:  # if the robot is well aligned with the token, we go forward
            print("Ah, here we are!.")
            drive(30, 0.5)
        elif rot_y < -a_th:  # if the robot is not well aligned with the token, we move it on the left or on the right
            print("Left a bit...")
            turn(-2, 0.5)
        elif rot_y > a_th:
            print("Right a bit...")
            turn(+2, 0.5)

# Function used to perform an exploration in order to count how many tokens are present 
def exploration():
    drive(40,7) # Valued chosen after several trials which allows the robot to go near the center
    lista = []
    first_ang = R.see()[0].centre.polar.rot_y  # selecting the relative angle of the first seen token  
    token_code_correspondent = R.see()[0].info.code  # storing the code of the first seen token
    while True:
        turn(2, 0.5) 
        for token in R.see():
         lista.append(token.info.code) # add all the seen token while the robot rotates
        for token in R.see():
            # condition to stop turning the robot because when the robot sees the first seen token and its relative angle is slightly less than the starting one, the robot has make a rotation of about 360 deg
            if token.info.code == token_code_correspondent and first_ang-2 <= token.centre.polar.rot_y <= first_ang-0.2:  
                lista_elem_unici = set(lista)                                                                      
                False
                #print(lista_elem_unici)
                return len(lista_elem_unici)  # return number of tokens





def main():
    # Creation of a list that will store all the distances of the tokens that can be seen by the robot
    dist_list = []
    for i in R.see():
        dist_list.append(i.centre.polar.length)

    # Returning the minimum distance and the index of the correspondent token 
    min_val = min(dist_list)
    min_index = dist_list.index(min_val)
    print(min_val)
    print(min_index)

    # Creation of the list containing the code of the nearest token (that will be the one near which the others will be deposited),
    # and all the already grabbed tokens 
    list_grabbed_token = []
    list_grabbed_token.append(R.see()[min_index].info.code)
    print(list_grabbed_token)

    # Calling the function to perform an exploration in order to identify how many tokens are present
    num_tot_token = exploration()

    # While cycle used to to grab every token,
    # it stops when the number of released tokens is equal to the number of tokens seen by the robot in the exploration
    while True:

        codice = reach_token(list_grabbed_token)  # codice is equal to the code of the the grabbed token which CAN'T be the token corresponding to clustering point
        print(list_grabbed_token)                 # because it is already contained in list_grabbed_token
        print(find_token(list_grabbed_token))
        reach_dist_rot(list_grabbed_token)  # the grabbed token is carried to the clustering point and released 
        list_grabbed_token.append(codice)  # the code of the grabbed token is added to the list of already grabbed token 
        if len(list_grabbed_token) ==  num_tot_token:  # condition to stop the execution when all tokens are grouped 
            False
            print("Grouped every token")
            exit() 

    
main()