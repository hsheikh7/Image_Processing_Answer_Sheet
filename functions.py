import cv2
import numpy as np
import pandas as pd
import csv


def detect_answers(path): 

    # Load the image
    image = cv2.imread(path)
    image = image[600:-200, 80:-80]
    height = 800
    width = 600
    image = cv2.resize(image, (width, height))

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply adaptive thresholding
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 4)

    # Perform morphological operations
    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)

    # Find contours
    contours, _ = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter contours based on area and aspect ratio
    filtered_contours = []
    for contour in contours:
        area = cv2.contourArea(contour)
        x, y, w, h = cv2.boundingRect(contour)
        aspect_ratio = w / float(h)

        # Filter based on area and aspect ratio
        if 40 < area < 120 and 0.5 < aspect_ratio < 2:
            filtered_contours.append((x, y, x + w , y + h))

    # Draw rectangles around the filtered contours
    for (x, y, x2, y2) in filtered_contours:
        cv2.rectangle(image, (x, y), (x2, y2), (0, 255, 0), 2)

        # Crop the regions within the rectangles
        cropped_region = image[y:y2, x:x2]


    # Save the locations to a CSV file
    csv_file = 'C:/Users/Hassan/Desktop/Projects/ResponseLetter/answers_sheet.csv'
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['x', 'y', 'x2', 'y2'])  # Write the header
        for (x, y, x2, y2) in reversed(filtered_contours):
            writer.writerow([x, y, x2, y2])

    # Display the image with rectangles
    cv2.imshow('Answer Sheet', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return csv_file

########### Detect Answers In DataSheet  ###############
def find_the_answer_datasheet(number):
    if 32 <= number <= 36:
        return 1
    elif 46 <= number <= 50:
        return 2
    elif 60 <= number <= 64:
        return 3
    elif 75 <= number <= 78:
        return 4
    elif 137 <= number <= 141:
        return 1
    elif 151 <= number <= 155:
        return 2
    elif 164 <= number <= 169:
        return 3
    elif 179 <= number <= 184:
        return 4
    elif 240 <= number <= 246:
        return 1
    elif 255 <= number <= 261:
        return 2
    elif 270 <= number <= 276:
        return 3
    elif 285 <= number <= 300:
        return 4
    elif 340 <= number <= 353:
        return 1
    elif 358 <= number <= 370:
        return 2
    elif 374 <= number <= 380:
        return 3
    elif 385 <= number <= 395:
        return 4
    
    else:
        return number

########### Detect Questions In DataSheet  ###############

def find_the_row(y): 
    if 0 <= y <= 170:
        num = int((y-26)/14) +1
        return num 
    elif 171 <= y <= 331:
        num = int((y-186)/14) +11
        return num
    elif 332 <= y <= 491:
        num = int((y-346)/14) +21
        return num
    elif 492 <= y <= 651:
        num = int((y-506)/14) +31
        return num 
    elif 652 <= y <= 811:
        num = int((y-666)/14) +41
        return num 
    
def find_the_question(x , y): 
    if 0 <= x <= 100:
        return find_the_row(y)
    elif 101 <= x <= 200:
        return find_the_row(y)+ 50
    elif 201 <= x <= 300:
        return find_the_row(y)+ 100
    elif 301 <= x <= 400:
        return find_the_row(y)+150 
    

#------------- Evaluation ------------------
def evaluation(key_df, df):
    # Sort the key dataframe based on questions and answers
    key_df = key_df.sort_values(by=['question', 'correct']).reset_index(drop=True)

    # Create a new column 'Checked' in the main dataframe
    df['checked'] = '-'

    # Iterate over the rows of the main dataframe
    for index, row in df.iterrows():
        question = row['question']
        answer = row['answer']
        
        # Find the corresponding answer in the key dataframe
        key_row = key_df[(key_df['question'] == question) & (key_df['correct'] == answer)]
        
        if not key_row.empty:
            # The answer is correct
            df.at[index, 'checked'] = True
        else:
            # The answer is wrong
            df.at[index, 'checked'] = False

    # Count the number of right and wrong questions
    num_right = df[df['checked'] == True].shape[0]
    num_wrong = df[df['checked'] == False].shape[0]

    # Calculate the score
    score = (num_right / (num_right + num_wrong)) * 100

    # Print the results
    print("Number of Right Questions:", num_right)
    print("Number of Wrong Questions:", num_wrong)
    print("Score:", score)

    df.to_csv('C:/Users/Hassan/Desktop/Projects/ResponseLetter/answers_sheet.csv' )


    ## ------------ Presentation --------------------

def presentation(df, path):
    height = 800
    width = 600

    # Load your image here
    image = cv2.imread(path)
    image = image[600:-200, 80:-80]
    image = cv2.resize(image, (width, height))

    # Create a copy of the image to draw circles on
    circles_image = image.copy()

    # Iterate over the rows of the dataframe
    for index, row in df.iterrows():
        x = int(row['x2']) - 8
        y = int(row['y2']) - 8
        checked = row['checked']
        
        # Set circle color based on 'Checked' column
        circle_color = (0, 255, 0) if checked else (0, 0, 255)
        
        # Draw a circle on the circles image
        cv2.circle(circles_image, (x, y), radius=5, color=circle_color, thickness=-1)

    # Display the resulting image
    cv2.imshow('Circles Image', circles_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
