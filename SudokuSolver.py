from ppadb.client import Client
from os import system
import numpy as np
import cv2
import time


def ClearScreen():
 system("clear")
 print("___Sudoku Automatization___")
 time.sleep(1)

def TakeScreenshot():
 print("Processing screenshot...")
 image = device.screencap()
 print("Screenshot taked")

 with open(f"sudoku.png", "wb") as fp:
  fp.write(image)

#If you want optimice this GetCellsCoordinates def
def GetCellsCoordinates(grid_coordinates):
 x=grid_coordinates[1] #grid columns lines
 y=grid_coordinates[0] #grid rows lines
  #returning xCells and yCells coordinates (mid points of grid colums and rows lines)
 return (
  (
   (x[0]+x[1])//2,
   (x[1]+x[2])//2,
   (x[2]+x[3])//2,
   (x[3]+x[4])//2,
   (x[4]+x[5])//2,
   (x[5]+x[6])//2,
   (x[6]+x[7])//2,
   (x[7]+x[8])//2,
   (x[8]+x[9])//2
  ),
  (
   (y[0]+y[1])//2,
   (y[1]+y[2])//2,
   (y[2]+y[3])//2,
   (y[3]+y[4])//2,
   (y[4]+y[5])//2,
   (y[5]+y[6])//2,
   (y[6]+y[7])//2,
   (y[7]+y[8])//2,
   (y[8]+y[9])//2
  )
 )

def SetMatrixValues():
 ClearScreen()
 global sudoku
 sudoku_image= cv2.imread("./sudoku.png")

 #Getting each cell value
 for row in range(9):
  sudoku.append([])
  for column in range(9):
   sudoku[row].append([])
   width= column
   height= row
   cell = sudoku_image[
    (grid_coordinates[1][height])+4:(grid_coordinates[1][height+1])-4,
    (grid_coordinates[0][width])+4:(grid_coordinates[0][width+1])-4
   ]
   cell = cv2.cvtColor(cell, cv2.COLOR_BGR2GRAY)
   cv2.imwrite("./numbers/cell.png", cell)
   cell_value= GetCellValue()
   sudoku[row][column]= cell_value

def GetCellValue():
 cell_image= cv2.imread("./numbers/cell.png")
 for threshold in range(100, 90, -2):
  for i in range(len(numbers)):
   res = cv2.matchTemplate(cell_image, numbers[i], cv2.TM_CCOEFF_NORMED)
   loc = np.where(res >= threshold/100)
   if len(loc[0])>0:
    return i+1
 return 0

def SolveSudoku(sudoku):
 for row in range(9):
  for column in range(9):
   if sudoku[row][column]== 0:
    for number in range(1, 10):
     if IsTheNumberUsable(row, column, number, sudoku):
      sudoku[row][column]= number
      SolveSudoku(sudoku) #Recursivity
      sudoku[row][column]= 0 #Backtracking
    return
  SaveSudoku(sudoku)
 return
     
def IsTheNumberUsable(row, column, number, sudoku):
 #Chek row
 if number in sudoku[row]:
  return False
 
 #Check columnn
 for i in range(9):
  if number== sudoku[i][column]:
   return False

 #Get cellGrid elements
 cellGrid= GetCellGrid(row, column, sudoku)
 
 # Check cellGrid
 if number in cellGrid:
  return False
 
 return True

def GetCellGrid(row, column, sudoku):
 cellGrid=[]
 
 if row <=2: i=0
 elif row <=5: i=3
 elif row <=8: i=6
  
 if column <=2: j=0
 elif column <=5: j=3
 elif column <=8: j=6

 for x in range(i, i+3):
  for y in range(j, j+3):
   cellGrid.append(sudoku[x][y])
 
 return cellGrid

def PrintSudoku(sudokuToPrint, message):
 print(f"\n{message}:")
 for row in range(9):
  print(f" {sudokuToPrint[row]}")

def SaveSudoku(sudoku):
 global sudoku_solved
 global sudoku_saved
 if sudoku_saved== False:
  sudoku_solved=[]
  for row in range(9):
   sudoku_solved.append([])
   for column in range(9):
    if sudoku[row][column]==0:
     return
    sudoku_solved[row].append(sudoku[row][column])
  sudoku_saved= True

def SolveADBSudoku(sudoku, sudoku_solved):
 answer_coordinates=(
  15,100,185,275,360,445,535,620,705
 )

 cells_coordinates= GetCellsCoordinates(grid_coordinates)

 for row in range(9):
  for column in range(9):
   cell_row= row
   cell_index= column
   if sudoku[row][column] != sudoku_solved[row][column]:
    answer_index= (sudoku_solved[row][column])-1
    #time.sleep(.1) #if you want uncomment this line
    device.shell(f"input tap {cells_coordinates[1][cell_index]} {cells_coordinates[0][cell_row]}") #tap cell
    #time.sleep(.1) #if you want uncomment this line
    device.shell(f"input tap {answer_coordinates[answer_index]} 1305") #tap answer number
    
    
#""" Variables """
device=""
grid_coordinates=(
 (0,70,150,235,315,400,485,570,650,720), #X grid lines
 (295,375,460,545,625,710,795,880,960,1045) #Y grid lines
)
restart_coordinates=(360,1200)
sudoku= []
sudoku_solved= []
sudoku_saved= False
numbers = (
 cv2.imread('./numbers/1.png'),
 cv2.imread('./numbers/2.png'),
 cv2.imread('./numbers/3.png'),
 cv2.imread('./numbers/4.png'),
 cv2.imread('./numbers/5.png'),
 cv2.imread('./numbers/6.png'),
 cv2.imread('./numbers/7.png'),
 cv2.imread('./numbers/8.png'),
 cv2.imread('./numbers/9.png'),
)
level_mode=(350, 570, 790, 1020)


#""" Automatization main code """
adb = Client(host="127.0.0.1", port=5037)
devices = adb.devices()

if len(devices)== 0:
 print("No devices attached")
 quit()
else:
 device= devices[0]

#device.shell(f"input tap {restart_coordinates[0]} {restart_coordinates[1]}")
time.sleep(2)
#device.shell(f"input tap 360 {level_mode[3]}")
time.sleep(3)

ClearScreen()
TakeScreenshot()

print("\nProcessing the data from the Sudoku image...")
SetMatrixValues()
print("\n Solving sudoku...")
SolveSudoku(sudoku)
ClearScreen()

PrintSudoku(sudoku, "Initial Sudoku")
time.sleep(1)
PrintSudoku(sudoku_solved, "Solved Sudoku")

print("\nSolving sudoku on ADB device...")
SolveADBSudoku(sudoku, sudoku_solved)
print("Sudoku solved on ADB device.")
time.sleep(2)
ClearScreen()

##By Dustin MC
##License BY, NC, ND