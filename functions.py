import cv2
import numpy as np
import pandas as pd
import csv

#  ---------------- 1. Generate the Key ----------------------
# Define a custom function to compute the value of the new column
def find_the_answer(row):
    if 1 <= row['col'] <= 3:
        return 1
    elif 5 <= row['col'] <= 7:
        return 2
    elif 9 <= row['col'] <= 11:
        return 3
    elif 13 <= row['col'] <= 16:
        return 4
    else:
        return row['col']

def generate_key(path_to_key): 
    # Load the image
    image = cv2.imread(path_to_key)

    # Crop 400 pixels from the top of the image
    image = image[400:, :]

    # Convert the image from BGR to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define the range of green color in HSV
    lower_green = np.array([40, 40, 40])
    upper_green = np.array([70, 255, 255])

    # Create a mask for the green color
    mask = cv2.inRange(hsv, lower_green, upper_green)

    # Find the contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Create an empty list to store the correct answers
    correct_answers = []

    # Define the minimum area for a contour to be considered a fully green cell
    min_area = 500

    # Iterate over each contour
    for contour in reversed(contours):
        
        x, y, w, h = cv2.boundingRect(contour)
        cx = x + w // 2
        cy = y + h // 2
        
        col = (cx - 50) // 100
        row = (cy - 50) // 100

        # Check if the area of the contour is above the minimum area
        if cv2.contourArea(contour) >= min_area:

            # Store the row and column indices in the correct_answers list
            correct_answers.append({
                'row': row,
                'col': col
            })
        else: 
            correct_answers.append({
                'row': row,
                'col': 0, 
            }) 
            

    # Create a DataFrame from the correct_answers list
    key_df = pd.DataFrame(correct_answers)
    key_df.index = key_df.index + 1

    key_df['correct'] = key_df.apply(find_the_answer, axis=1)

    # Save the DataFrame to a CSV file
    # df.to_csv(path_to_key_csv, index=True, index_label='question')
    key_df['question'] = key_df.index 

    # Print a message to indicate that the data has been saved
    # print('The Key has been saved to the "key.csv" file.')
    return key_df 


#  ---------------- 2. Answer Sheet ----------------------
#  ---------------- 2.1 Detect Asnwers ----------------------

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
    # csv_file = 'C:/Users/Hassan/Desktop/Projects/ResponseLetter/answers_sheet.csv'
    # with open(csv_file, 'w', newline='') as file:
    #     writer = csv.writer(file)
    #     writer.writerow(['x', 'y', 'x2', 'y2'])  # Write the header
    #     for (x, y, x2, y2) in reversed(filtered_contours):
    #         writer.writerow([x, y, x2, y2])

    data = [(x, y, x2, y2) for (x, y, x2, y2) in reversed(filtered_contours)]

    # Create a DataFrame from the data
    answer_sheet_df = pd.DataFrame(data, columns=['x', 'y', 'x2', 'y2'])

    # Display the image with rectangles
    # cv2.imshow('Answer Sheet', image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    return answer_sheet_df

#  ---------------- 2.2 Detect Answers In DataSheet ----------------------

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


def add_answers_to_datasheet(datasheet_df): 
    
    datasheet_df['answer'] = 0     
    for item in range(len(datasheet_df)): 
        datasheet_df['answer'][item] = find_the_answer_datasheet(datasheet_df['x2'][item]) 

    return datasheet_df

#  ---------------- 2.3 Detect Questions In DataSheet ----------------------

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
    
def detect_questions_in_datasheet(datasheet_df): 

    datasheet_df['question'] = 0
    for item in range(len(datasheet_df)): 
        datasheet_df['question'][item] = find_the_question(datasheet_df['x2'][item], datasheet_df['y2'][item]) 
        
    return datasheet_df

#  ------ 2.4 Add Checked In DataSheet ----------- 

def add_checked_to_datasheet(key_df, df):
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

    return df

#------------- 3. Evaluation ------------------

def evaluation(df):
    
    # Count the number of right and wrong questions
    num_right = df[df['checked'] == True].shape[0]
    num_wrong = df[df['checked'] == False].shape[0]

    # Calculate the score
    score = (num_right / (165)) * 100

    # Print the results
    # print("Number of Right Questions:", num_right)
    # print("Number of Wrong Questions:", num_wrong)
    # print("Score:", score)

    return score 


#------------- 4. Presentation ------------------

def presentation(df, path_to_answer_sheet):
    height = 800
    width = 600

    # Load your image here
    image = cv2.imread(path_to_answer_sheet)
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
