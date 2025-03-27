import pyautogui
import time 

pyautogui.PAUSE = 0.3
print(pyautogui.position())
print(pyautogui.size())


pyautogui.hotkey("win")
pyautogui.write("YAT")
pyautogui.hotkey("enter")
