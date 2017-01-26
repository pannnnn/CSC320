## CSC320 Winter 2017 
## Assignment 1
## (c) Kyros Kutulakos
##
## DISTRIBUTION OF THIS CODE ANY FORM (ELECTRONIC OR OTHERWISE,
## AS-IS, MODIFIED OR IN PART), WITHOUT PRIOR WRITTEN AUTHORIZATION 
## BY THE INSTRUCTOR IS STRICTLY PROHIBITED. VIOLATION OF THIS 
## POLICY WILL BE CONSIDERED AN ACT OF ACADEMIC DISHONESTY

##
## DO NOT MODIFY THIS FILE ANYWHERE EXCEPT WHERE INDICATED
##

# import basic packages
import numpy as np
import scipy.linalg as sp
import cv2 as cv

# If you wish to import any additional modules
# or define other utility functions, 
# include them here

#########################################
## PLACE YOUR CODE BETWEEN THESE LINES ##
#########################################


#########################################

#
# The Matting Class
#
# This class contains all methods required for implementing 
# triangulation matting and image compositing. Description of
# the individual methods is given below.
#
# To run triangulation matting you must create an instance
# of this class. See function run() in file run.py for an
# example of how it is called
#
class Matting:
    #
    # The class constructor
    #
    # When called, it creates a private dictionary object that acts as a container
    # for all input and all output images of the triangulation matting and compositing 
    # algorithms. These images are initialized to None and populated/accessed by 
    # calling the the readImage(), writeImage(), useTriangulationResults() methods.
    # See function run() in run.py for examples of their usage.
    #
    def __init__(self):
        self._images = { 
            'backA': None, 
            'backB': None, 
            'compA': None, 
            'compB': None, 
            'colOut': None,
            'alphaOut': None, 
            'backIn': None, 
            'colIn': None, 
            'alphaIn': None, 
            'compOut': None, 
        }

    # Return a dictionary containing the input arguments of the
    # triangulation matting algorithm, along with a brief explanation
    # and a default filename (or None)
    # This dictionary is used to create the command-line arguments
    # required by the algorithm. See the parseArguments() function
    # run.py for examples of its usage
    def mattingInput(self): 
        return {
            'backA':{'msg':'Image filename for Background A Color','default':None},
            'backB':{'msg':'Image filename for Background B Color','default':None},
            'compA':{'msg':'Image filename for Composite A Color','default':None},
            'compB':{'msg':'Image filename for Composite B Color','default':None},
        }
    # Same as above, but for the output arguments
    def mattingOutput(self): 
        return {
            'colOut':{'msg':'Image filename for Object Color','default':['color.tif']},
            'alphaOut':{'msg':'Image filename for Object Alpha','default':['alpha.tif']}
        }
    def compositingInput(self):
        return {
            'colIn':{'msg':'Image filename for Object Color','default':None},
            'alphaIn':{'msg':'Image filename for Object Alpha','default':None},
            'backIn':{'msg':'Image filename for Background Color','default':None},
        }
    def compositingOutput(self):
        return {
            'compOut':{'msg':'Image filename for Composite Color','default':['comp.tif']},
        }
    
    # Copy the output of the triangulation matting algorithm (i.e., the 
    # object Color and object Alpha images) to the images holding the input
    # to the compositing algorithm. This way we can do compositing right after
    # triangulation matting without having to save the object Color and object
    # Alpha images to disk. This routine is NOT used for partA of the assignment.
    def useTriangulationResults(self):
        if (self._images['colOut'] is not None) and (self._images['alphaOut'] is not None):
            self._images['colIn'] = self._images['colOut'].copy()
            self._images['alphaIn'] = self._images['alphaOut'].copy()

    # If you wish to create additional methods for the 
    # Matting class, include them here

    #########################################
    ## PLACE YOUR CODE BETWEEN THESE LINES ##
    #########################################

    #########################################
            
    # Use OpenCV to read an image from a file and copy its contents to the 
    # matting instance's private dictionary object. The key 
    # specifies the image variable and should be one of the
    # strings in lines 54-63. See run() in run.py for examples
    #
    # The routine should return True if it succeeded. If it did not, it should
    # leave the matting instance's dictionary entry unaffected and return
    # False, along with an error message
    def readImage(self, fileName, key):
        success = False
        msg = 'Placeholder'

        #########################################
        ## PLACE YOUR CODE BETWEEN THESE LINES ##
        #########################################
        img = cv.imread(fileName)
        if img is not None:
            self._images[key] = img
            success = True
        else:
            msg = 'Read from image failed'
        #########################################
        return success, msg

    # Use OpenCV to write to a file an image that is contained in the 
    # instance's private dictionary. The key specifies the which image
    # should be written and should be one of the strings in lines 54-63. 
    # See run() in run.py for usage examples
    #
    # The routine should return True if it succeeded. If it did not, it should
    # return False, along with an error message
    def writeImage(self, fileName, key):
        success = False
        msg = 'Placeholder'

        #########################################
        ## PLACE YOUR CODE BETWEEN THESE LINES ##
        #########################################
        try:
            cv.imwrite(fileName, self._images[key])
            success = True
        except:
            msg = 'Write to image failed'
        #########################################
        return success, msg

    # Method implementing the triangulation matting algorithm. The
    # method takes its inputs/outputs from the method's private dictionary 
    # ojbect. 
    def triangulationMatting(self):
        """
	success, errorMessage = triangulationMatting(self)
        
        Perform triangulation matting. Returns True if successful (ie.
        all inputs and outputs are valid) and False if not. When success=False
        an explanatory error message should be returned.
        """

        success = False
        msg = 'Placeholder'
        #########################################
        ## PLACE YOUR CODE BETWEEN THESE LINES ##
        #########################################
        mat_1 = np.eye(3, 3)
        mat_2 = np.eye(3, 3)
        coefficient = np.concatenate((mat_1, mat_2), axis=0)
        backA = np.divide(self._images['backA'].astype(np.float64), 255)
        backB = np.divide(self._images['backB'].astype(np.float64), 255)
        compA = np.divide(self._images['compA'].astype(np.float64), 255)
        compB = np.divide(self._images['compB'].astype(np.float64), 255)        
        back = np.concatenate((backA, backB), axis=2) * (-1)
        delta = np.concatenate((compA - backA, compB - backB), axis=2)
        row, column, channel = back.shape
        self._images["colOut"] = np.zeros((row, column, 3), dtype=np.uint8)
        self._images["alphaOut"] = np.zeros((row, column, 3), dtype=np.uint8)
        for i in range(row):
            for j in range(column):
                column_back = back[i,j,:][np.newaxis].T
                A = np.concatenate((coefficient, column_back),axis=1)
                try:
                    inverseA = np.linalg.pinv(A)
                except:
                    msg = 'some error message here'
                pseudo_x = np.clip(np.matmul(inverseA, delta[i,j,:]), 0, 1)
                x = np.uint8(pseudo_x * 255)
                self._images["colOut"][i,j,:] = x[0:3]
                self._images["alphaOut"][i,j,:] = np.full((1,3), x[3])
        success = True
        #########################################
        return success, msg

        
    def createComposite(self):
        """
	success, errorMessage = createComposite(self)
        
        Perform compositing. Returns True if successful (ie.
        all inputs and outputs are valid) and False if not. When success=False
        an explanatory error message should be returned.
	"""
        
        success = False
        msg = 'Placeholder'

        #########################################
        ## PLACE YOUR CODE BETWEEN THESE LINES ##
        #########################################
        colIn_shape = self._images["colIn"].shape
        backIn_shape = self._images["backIn"].shape
        alphaIn_shape = self._images["alphaIn"].shape
        self._images["compOut"] = np.zeros((colIn_shape[0], colIn_shape[1], 3), dtype=np.uint8)
        if (colIn_shape != backIn_shape or colIn_shape != alphaIn_shape or backIn_shape != alphaIn_shape):
            msg = 'Input file are not of same length and width'
        else:
            alpha = self._images["alphaIn"].astype(np.float64)/255
            one_matrix = np.full((colIn_shape[0], colIn_shape[1], 3), 1)
            alpha_k = one_matrix - alpha
            c_k = alpha_k * self._images["backIn"].astype(np.float64)
            c_0 = self._images["colIn"].astype(np.float64)
            self._images["compOut"] = np.uint8(c_0 + c_k)
            success = True
        #########################################
        return success, msg
