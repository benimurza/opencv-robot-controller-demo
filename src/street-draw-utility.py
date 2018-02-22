# WORK IN PROGRESS
# Use separately - has no project dependency except cv2
# Callback for mouse click
import cv2


def draw_circle(event, mouse_x, mouse_y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        print("Mouse event!: " + str(mouse_x) + ", " + str(mouse_y))


cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

cv2.namedWindow('frame')
cv2.setMouseCallback('frame', draw_circle)
while 1:
    # Take each frame
    _, frame = cap.read()

    cv2.imshow('frame', frame)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
