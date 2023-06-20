import numpy as np
import cv2

def trng_generator():
    def inRange(value):
        if value > 1 & value < 254:
            return True
        return False

    def binary_array_to_decimal(binary_array):
        binary_string = ''.join(str(bit) for bit in binary_array)
        decimal = int(binary_string, 2)
        return decimal

    def split_into_2048_bit_numbers(binary_array):
        result = []
        start = 0
        while start + 512 <= len(binary_array):
            number = binary_array[start:start + 512]
            decimal = binary_array_to_decimal(number)
            result.append(decimal)
            start += 512
        return result

    # 1.Initialize the camera and set variables
    video = cv2.VideoCapture('input.mp4')
    width = 0
    height = 0
    numSoFar = 0
    numNeeded = 10000
    numberSize = 8
    frameNumber = 0

    # 2.Allocate square array
    dimension = np.floor(np.sqrt(numNeeded)).astype(int)  # The matrix dimension is |_√RequiredLength_|
    finalList = np.zeros((dimension, dimension))
    print(finalList.shape)

    if video.isOpened():
        width = int(video.get(3))  # wyznaczanie szerokosci
        height = int(video.get(4))  # wyznaczanie wysokosci
        # print('width: ', width, ' height: ', height)
        # 3.Generation
        while numSoFar < numNeeded:
            frameNumber += 1
            iterator = 1
            # print('numSoFar: ',numSoFar)
            # 4.Take snapshot
            ret, frame = video.read()

            ###########################################
            # if ret == True:
            # Display the resulting frame
            #    cv2.imshow('Frame', frame)
            # When everything done, release
            # the video capture object
            # video.release()

            # Closes all the frames
            # cv2.destroyAllWindows()
            ###########################################

            # 5.Pick out the brightness ∈ [2, 253]
            subList = []
            for column in range(0, width):
                for row in range(0, height):
                    # 6.Take the last bits as a SubList
                    # BRG = [0,1,2]
                    blue = frame[row, column, 0]
                    if inRange(blue):
                        subList.append(np.bitwise_and(blue,
                                                      1))  # np.bitwise_and(blue,1) czy tu chodzi o ostatni bit liczby przy pomocy BitAnd?
                        iterator += 1
                    red = frame[row, column, 1]
                    if inRange(red):
                        subList.append(np.bitwise_and(red, 1))  # np.bitwise_and(red,1)
                        iterator += 1
                    green = frame[row, column, 2]
                    if inRange(green):
                        subList.append(np.bitwise_and(green, 1))  # np.bitwise_and(green,1)
                        iterator += 1
            # 7.If (Frame is even) ip the bits in SubList
            if frameNumber % 2:
                subList = subList[::-1]
            # 8.Add SubList to FinalList in row-major order
            addedNumbers = 0
            for column in range(0, dimension):
                for row in range(0, dimension):
                    if addedNumbers < iterator:
                        if finalList[row, column] == 0:
                            if len(subList) != 0:
                                addedNumbers += 1
                                # stringerson = "row" + str(row) + " col " + str(column)
                                # print(stringerson)
                                # cos sie popsuło i raz działa, czasem wychodzi poza zakres tablicy a czasem nie
                                try:
                                    finalList[row, column] = subList[addedNumbers]
                                except Exception as e:
                                    print()

            # 9.NumSoFar = NumSoFar + SubList.Length
            numSoFar += len(subList)
    else:
        print("Failed")

    finalList = np.transpose(finalList)

    one_dimensional_array = []
    for column in range(0, dimension):
        for row in range(0, dimension):
            one_dimensional_array.append(int(finalList[row, column]))

    numbers_to_generator = split_into_2048_bit_numbers(one_dimensional_array)
    return numbers_to_generator