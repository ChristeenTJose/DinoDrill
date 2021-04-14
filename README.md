# DinoDrill
## Let's Play Chrome Dinosaur Game without touching the Keyboard!!
### Author: Christeen T Jose
#### [Click here]() to Watch the project demonstration video for more explanation.

![](https://github.com/ChristeenTJose/DinoDrill/blob/main/poster.JPG) 

---
### Requirements before executing the [python file](https://github.com/ChristeenTJose/DinoDrill/blob/main/DinoDrill.py):

* Download [Chrome Driver](https://chromedriver.chromium.org/downloads) and save it in the same directory as the python file
* Install Selenium
  * pip install selenium
* Install OpenCv
  * pip install opencv-python

---
### Idea:
The basic idea behind the project is to build a bot that uses Chrome Driver and then to control the bot based on conclusions drawn after applying a combination of colour detection and contour detection on a live camera feed to track movements of the colourful object we are using.

Whenever our object moves from ground to air, the bot will automatically press the space bar.

Note that we are keeping track of the centroid of the object having the largest area. (Centroid is denoted by the red dot, and the boundaries of the object having the largest area are coloured in orange)

---


 



