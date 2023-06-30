import cv2
import numpy as np
import pandas as pd
from model import ClassScore 


path = 'images/image0000013A.tif'
path_to_key = 'images/key.png'
path_to_key_csv = 'images/key.csv'
path_folder = 'images'

test1 = ClassScore(path,path_to_key ) 
print(test1.score())
#test1.representation()
#test1.save_status("outputfile.csv")

#ClassScore.save_allstatus(path, path_to_key, "outputfile2.csv")

# ClassScore.save_all(path_folder, path_to_key, "output_save_all.csv")
