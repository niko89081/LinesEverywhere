import cv2 as cv
import numpy as np
import math

above = []
below = []
actual = []

def averager(lines):
    sum = 0
    total = len(lines)
    for i in lines:
        sum += i[0][0]
    return sum / total

img = cv.imread("IMG_1696.jpg")
scale_percent = 20
width = int(img.shape[1] * scale_percent / 100)
height = int(img.shape[0] * scale_percent / 100)
dim = (width, height)
img = cv.resize(img, dim, interpolation=cv.INTER_AREA)
grayed = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
dst = cv.Canny(grayed, 575, 600)
blurred = cv.blur(dst, (3, 3))
line1 = cv.HoughLinesP(blurred, 2, np.pi / 180, 150, None, 275, 0)
for i in line1:
    if i[0][0] < averager(line1):
        below.append(i)
    else:
        above.append(i)
maxIndex = 0
dist = 0
curr = 0
for j in below:
    i = j[0]
    max = math.dist([i[0], i[1]], [i[2], i[3]])
    if max > dist:
        maxIndex = curr
        dist = max
    curr += 1

actual += [above[0], below[maxIndex]]

curr = 0
while curr < len(actual):
    if actual[curr][0][3] > actual[curr][0][1]:
        print(actual[curr])
        x = actual[curr][0][2]
        y = actual[curr][0][3]
        actual[curr] = np.insert(actual[curr], 0, y)
        actual[curr] = np.insert(actual[curr], 0, x)
        print(actual[curr])
    else:
        actual[curr] = actual[curr][0]
    curr+=1
print(actual)
if line1 is not None:
    for i in actual:
        cv.line(img, (i[0], i[1]), (i[2], i[3]), (0, 255, 0), 10, cv.LINE_AA)

cv.circle(img, (actual[0][0],actual[0][1]),4, (0,0,0), -1)
cv.circle(img, (actual[1][0],actual[1][1]),4, (0,0,0), -1)
cv.arrowedLine(img, (int((actual[0][0] + actual[1][0])/2), int((actual[0][1] + actual[1][1])/2)), (int((actual[0][2] + actual[1][2])/2), int((actual[0][3] + actual[1][3])/2)), (255,0,0),3)

cv.imshow("img", img)
cv.waitKey(0)
cv.destroyAllWindows()
