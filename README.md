Research Track First Assignment
================================

Federico Malatesta (S4803603)
---------------

This is a simple, portable robot simulator developed by [Student Robotics](https://studentrobotics.org).
Some of the arenas and the exercises have been modified for the Research Track I course.

The goal of this first assignment is to group all the tokens in a point of your choice.

Installing and running
----------------------

The simulator requires a Python 2.7 installation, the [pygame](http://pygame.org/) library, [PyPyBox2D](https://pypi.python.org/pypi/pypybox2d/2.1-r331), and [PyYAML](https://pypi.python.org/pypi/PyYAML/).

Once the dependencies are installed, simply run the `test.py` script to test out the simulator.


Robot API
---------

The API for controlling a simulated robot is designed to be as similar as possible to the [SR API][sr-api].

### Motors ###

The simulated robot has two motors configured for skid steering, connected to a two-output [Motor Board](https://studentrobotics.org/docs/kit/motor_board). The left motor is connected to output `0` and the right motor to output `1`.

The Motor Board API is identical to [that of the SR API](https://studentrobotics.org/docs/programming/sr/motors/), except that motor boards cannot be addressed by serial number. So, to turn on the spot at one quarter of full power, one might write the following:

```python
R.motors[0].m0.power = 25
R.motors[0].m1.power = -25
```

### The Grabber ###

The robot is equipped with a grabber, capable of picking up a token which is in front of the robot and within 0.4 metres of the robot's centre. To pick up a token, call the `R.grab` method:

```python
success = R.grab()
```

The `R.grab` function returns `True` if a token was successfully picked up, or `False` otherwise. If the robot is already holding a token, it will throw an `AlreadyHoldingSomethingException`.

To drop the token, call the `R.release` method.

Cable-tie flails are not implemented.

### Vision ###

To help the robot find tokens and navigate, each token has markers stuck to it, as does each wall. The `R.see` method returns a list of all the markers the robot can see, as `Marker` objects. The robot can only see markers which it is facing towards.

Each `Marker` object has the following attributes:

* `info`: a `MarkerInfo` object describing the marker itself. Has the following attributes:
  * `code`: the numeric code of the marker.
  * `marker_type`: the type of object the marker is attached to (either `MARKER_TOKEN_GOLD`, `MARKER_TOKEN_SILVER` or `MARKER_ARENA`).
  * `offset`: offset of the numeric code of the marker from the lowest numbered marker of its type. For example, token number 3 has the code 43, but offset 3.
  * `size`: the size that the marker would be in the real game, for compatibility with the SR API.
* `centre`: the location of the marker in polar coordinates, as a `PolarCoord` object. Has the following attributes:
  * `length`: the distance from the centre of the robot to the object (in metres).
  * `rot_y`: rotation about the Y axis in degrees.
* `dist`: an alias for `centre.length`
* `res`: the value of the `res` parameter of `R.see`, for compatibility with the SR API.
* `rot_y`: an alias for `centre.rot_y`
* `timestamp`: the time at which the marker was seen (when `R.see` was called).

For example, the following code lists all of the markers the robot can see:

```python
markers = R.see()
print "I can see", len(markers), "markers:"

for m in markers:
    if m.info.marker_type in (MARKER_TOKEN_GOLD, MARKER_TOKEN_SILVER):
        print " - Token {0} is {1} metres away".format( m.info.offset, m.dist )
    elif m.info.marker_type == MARKER_ARENA:
        print " - Arena marker {0} is {1} metres away".format( m.info.offset, m.dist )
```

[sr-api]: https://studentrobotics.org/docs/programming/sr/

### Functions descriptions ###
Brief description of all the functions used.

#### `find_token_new(code_list)` and `find_token(code_list)` ####
These functions are used in order to retrieve the relative distance and angle to a token that is in the input (`code_list`) which is a list containg codes of tokens.  
`find_token_new` is used for the first time in the `reach_dist_rot` function which allows the robot to reach the clustering point that corresponds to the code of the first seen token that is added to (`code_list`).  
`find_token` works the same way however allows the robot to avoid grabbing a token which has already been grabbed beacause it checks between all the tokens in its field of view if the code is NOT contained in the `code_list` input and if so, relative distance and angle are returned.

#### `reach_token(code_list)` and `reach_dist_rot(code_list)` ####
`reach_token` allows the robot to go grabbing a token that is identified by `find_token` function, once grabbed the the correspondent code is computed and retrived in order to be added in the `list_grabbed_token` (when it will be released).  
`reach_dist_rot` works in a similar way but uses `find_token_new` in order to drive the robot to the clustering point.

#### `exploration()` ####
It is used for computing the total number of tokens, at first by means of `drive(40,7)` the robot is dirven to the center and here it performs a rotation of about 360 degrees.
This is possible by calculating the relative angle within respect to the first seen token and then rotate untill the relative angle is: `relative starting angle ` - 2 <=  `relative angle ` <=  `relative starting angle ` - 0.2  
The subsequently step is to compute how many tokens the robot sees during the rotation and return this number in order to make the robot stopable.

### `main` function description ### 
The first step is to find the token closest to the robot that is in its field of view, and it will be the clustering point. This is done by a `for` loop which allows to fill a list with the `i.centre.polar.length` that is the current token's distance to the robot, then it is possible to retrieve the minimum value and the correspondent index which indicate the closest token.  
The code thus obtained is stored in a new list `list_grabbed_token`. 

The next step is to perform an exploration with the robot in order to determine the number of total tokens, to do this the robot moves towards the center with `drive(40,7)` which is a particular value chosen after several trials and after assuming that the robot is not facing the wall (there would be a problem otherwise).  
There it performs a rototation of about 360 degree and collect all the seen tokens in a list and their number is returned.

Subsequently is executed a `while` loop in which by means of `reach_token` a token is grabbed (the process is more detailed in the comments) and the correspondent code is returned.  
Once grabbed the token is brought to the clustering point thanks to `reach_dist_rot` that needs `list_grabbed_token` as input in order to know the position of the clustering point and there it's released, at this point the token's code returned by `reach_token` is added to `list_grabbed_token`. 

The `while` loop ends when `list_grabbed_token` contains the same number of tokens as the one obtained by the exploration.


### Flowchart ###
Flowchart containing the representation of the code, with:
- actions represented by rectangles
- decisions represented by rhombuses

[![Flowchart.drawio.png](https://github.com/FedeMala00/Research_track_ass1/blob/main/Flowchart.drawio.png)](https://viewer.diagrams.net/?tags=%7B%7D&highlight=0000ff&edit=_blank&layers=1&nav=1&title=Flowchart.drawio.png#R7VrbdqM2FP0aP04WiIvtx9hx08tMmq5Mm6YvXQKEUUdIVMixPV9fCQSYS2ySjGMP6UuCDpJAZ599tHXwyJrHm2sOk%2BgTCxAZASPYjKyrEQCm4Rjyn7Jsc4tjg9yw5DjQnSrDHf6KipHausIBSmsdBWNE4KRu9BmlyBc1G%2BScrevdQkbqT03gErUMdz4kbes9DkSUWydgXNl%2FRHgZFU823Wl%2BJ4ZFZ72SNIIBW%2B%2BYrMXImnPGRH4Vb%2BaIKOcVfrn%2FaXtPPn5xr3%2F%2BLf0X%2Fj775fPNHx%2FyyX54zpByCRxR8eKpF%2F5qfjtFN0I4f336dTPbPNyvP7h6aWJb%2BAsF0n26ybiI2JJRSBaVdcbZigZIzWrIVtXnI2OJNJrS%2BA8SYqtjAa4Ek6ZIxETf7bkcveyUrbiP9qxBwyMgXyKxp5%2BT91ML3AkN7axrxGIk%2BFZ24IhAgR%2Fr8QN1GC7LfpWr5YX29jM8r9%2F6EZKVftLnCKmnM08GlBosvYND9UIwm01ktwX7gmiq7lP1R6jLECNJCmCwUE2I0boFagWZ8v86wgLdJTDz6lrSvg5PiAmZM8J4NtYKHDQJbGlPBZcP37kzAZ7lus8G9BFxgTZ7IdB3gaG9pHOPOdHtdcVks6BntMNi1zgSatYA%2BFJk4UN8Mc6KL0XwVHwZAZfI95958mKpLi5znhQMkf5S7kDScVBI%2FwMXxirUqZcmmVfz4fJtyhna6BIiNyr0fNJANAn9LtK4%2FgR54RuS5vScmZ6CNNKrfPunGn%2FhFM0HPV3WuNrUWlvd%2BsZkc3qSzTwvtjlP7E6%2B1IfFTpNvSD5hKUpFQbwRmKtYi7AfZTGXPcpDO91XqUAc06XyMsM02%2BvSLDwYVywd5tYFxqem4fRwAl1sEukhGV6MvihbSt%2BIOiB1x1NGUQMlbYIEL6ls%2BhIGJO0z5WksVfylvhHjICBP5eF6sjgWpHYdUdtuIzrpANQ%2BFqAm6ED0%2B1cnfeW8aZ5VxjQPCfqAq3dQaXINeZBWGTEP%2BRbfhpkHrZPLETA5rRypiZFKm7yNHDH7in9zfF7sasv%2FOrs4E1LkZ7LfYytlsVQEGQFSQgPSoH6kzqlHV7GnqKf1jD44DJN49smJZ7ZFZcvZuZ%2BKQh1oiIkIJqpfvFmqWuVFSNjajyAXF5BShb%2FULX%2BDHTVBUKj0CIEeIrcsxZmwsa54vthZJj8RXzxK16cv2s36w1G6ek8edDrQMI%2BXB42W99%2FPsaxIb4fz4PS88uD4UB5EMDt5PXE4K09mEVS5kmZjPJTdgkQODtRaJL08T53FdOLUkzHOUZowqtJodRbMD2%2FwsavCMoxU6jTLkEZHKrU7yDs5GncHofSnPTkIzkzpt0%2FSdQ56qrxRCfyCetKd%2B6og74M75XfBQ9wZH4s71vgd73ugr%2F633LPiHGjrfxm9hXJPkSaYrvxnHYyyvMWrglU5pNriilGH%2BBex2Fulz%2BZeGIbA7%2FwSELie67wl96y%2B3DOBcyzydeHYZCMNLtWH%2F1FZHdzx7mtKfQdj%2BYAWL2y9Q14%2F4VaXuTUsbqOQaI1BfYqcxXpU5fDWROPmmaI5Uc7y1kQZcuWyXwFmnwLkwME8iMFLwWxqx2Njaf2PpTPeD8H3AmW7znLDWmAO%2B1uNazVk58RpbX1uRyRZR1Odbge%2FGp%2Ff8lNEwpkUJ7FSJojHmOqy5hqLaNTxW6BMy7BVkh2%2FB%2FmDBsesY2m7HTKmq5J5tON3sYHvgPmA2pXjYVPMaWQ5G7RheVOK2T3qyztbmE9gmmJ%2FeLuYO71wvsk%2B1p6prHy9eiuTzeqXs3n36vfH1uI%2F)

