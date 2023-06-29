import cv2
import numpy as np
import pandas as pd
from model import ClassScore 


path = 'images/image0000013A.tif'
path_to_key = 'images/key.png'
path_to_key_csv = 'images/key.csv'

test1 = ClassScore(path,path_to_key ) 
# print(test1.score())
# test1.representation()
# test1.save_status("outputfile.csv")
test1.save_allstatus("outputfile2.csv")

ClassScore.save_allstatus()

#----------------- Presentation  -----------------

# presentation(df, path)