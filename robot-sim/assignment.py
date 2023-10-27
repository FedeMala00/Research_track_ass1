from __future__ import print_function

import time
from sr.robot import *


a_th = 2.0
""" float: Threshold for the control of the orientation"""

d_th = 0.4
""" float: Threshold for the control of the linear distance"""


R = Robot()


def drive(speed, seconds):
    """
    Function for setting a linear velocity

    Args: speed (int): the speed of the wheels
          seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0


def turn(speed, seconds):
    """
    Function for setting an angular velocity

    Args: speed (int): the speed of the wheels
          seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

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


def find_token(code_list):
    """
    Function to find the closest token

    Returns:
        dist (float): distance of the closest token (-1 if no token is detected)
        rot_y (float): angle between the robot and the token (-1 if no token is detected)
    """
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


def reach_token(code):
    var = True
    while var:
        dist, rot_y = find_token(code)  # we look for markers
        if dist == -1:
            print("I don't see any token!!")
            turn(10, 1)  # if no markers are detected, the program ends

        elif dist < d_th:
            print("Found it!")
            R.grab()  # if we are close to the token, we grab it.
            print("Gotcha!") 
            var = False             
            dist_list = []
            for i in R.see():
                dist_list.append(i.centre.polar.length)

            min_val = min(dist_list)
            min_index = dist_list.index(min_val)                                
            return R.see()[min_index].info.code            

        elif -a_th <= rot_y <= a_th:  # if the robot is well aligned with the token, we go forward
            print("Ah, here we are!.")
            drive(25, 0.5)
        elif rot_y < -a_th:  # if the robot is not well aligned with the token, we move it on the left or on the right
            print("Left a bit...")
            turn(-2, 0.5)
        elif rot_y > a_th:
            print("Right a bit...")
            turn(+2, 0.5)

def lista_codici():

    lista_codici = []

    for i in R.see():
        lista_codici.append(i.info.code)

    return lista_codici


def dist_rot(code):
    while True:
        code_list = lista_codici()
        if code in code_list:
         for i in R.see():
            if i.info.code == code:
                dist = i.dist
                ang = i.rot_y
                return dist, ang
                False
        else:
             turn(+3, 0.5)
             True

def reach_dist_rot(code,variabile):
    var = True
    d_th_new = 0.6
    while var:
        dist, rot_y = find_token_new(code) # we look for markers
        if dist == -1:
            print("I don't see any token!!")
            turn(10, 1)  # if no markers are detected, the program ends

        elif dist < d_th_new and variabile == 1:
            print("Found it!")
            R.release()
            var = False
            return 0
        
        elif dist < d_th_new and variabile != 1:
            time.sleep(0.2)
            var = False
            #exit()
        
        elif -a_th <= rot_y <= a_th:  # if the robot is well aligned with the token, we go forward
            print("Ah, here we are!.")
            drive(30, 0.5)
        elif rot_y < -a_th:  # if the robot is not well aligned with the token, we move it on the left or on the right
            print("Left a bit...")
            turn(-2, 0.5)
        elif rot_y > a_th:
            print("Right a bit...")
            turn(+2, 0.5)


def exploration():
    drive(40,7)
    lista = []
    first_ang = R.see()[0].centre.polar.rot_y
    token_code_correspondent = R.see()[0].info.code
    while True:
        turn(2, 0.5)
        for token in R.see():
         lista.append(token.info.code)
        for token in R.see():
            if token.info.code == token_code_correspondent and first_ang-2 <= token.centre.polar.rot_y <= first_ang-0.5:
                lista_elem_unici = set(lista)
                False
                #print(lista_elem_unici)
                return len(lista_elem_unici)





def main():
    #print(R.see())
    dist_list = []
    for i in R.see():
        dist_list.append(i.centre.polar.length)

    min_val = min(dist_list)
    min_index = dist_list.index(min_val)

    print(min_val)
    print(min_index)
    list_grabbed_token = []
    list_grabbed_token.append(R.see()[min_index].info.code)
    print(list_grabbed_token)

    num_tot_token = exploration()

    while True:

        codice = reach_token(list_grabbed_token)
        print(list_grabbed_token)    
        print(find_token(list_grabbed_token))
        reach_dist_rot(list_grabbed_token,1)
        list_grabbed_token.append(codice)
        if len(list_grabbed_token) ==  num_tot_token:
            var = False
            print("Grouped every token")
            exit() 

    
main()