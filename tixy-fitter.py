import matplotlib.pyplot as plt
import numpy as np
import os
from PIL import Image
from scipy.optimize import curve_fit

#----------------------------------Parameters--------------------------------------------------------------

# tixy size
tixy_size = 16

# produces rendered preview of video if true
render = True

# number of iterations to fit for each function
maxfev_ = 5000

#----------------------------------Directories------------------------------------------------------------

#Input dir
directory_in = "Images"

#Output dir
directory_out = "Out_test"

#racket output file name
rkt_out = "fitted-tixy.rkt"

#racket function name
func_name = "fitted-tixy"

# n images
n_images = 16

#----------------------------------Script----------------------------------------------------------------

# polynomialfunction that each image line is fit to.

def polynomial(i, a, b, c, d, e,f, g):
    return(a + (b * i) + (c * (i * i)) + (d * (i * i * i))+ (e * (i * i * i * i))+ (f * (i * i * i * i * i))+ (g* (i * i * i * i * i* i)))

# string with racket output, more is added dynamically per image
str_ = "#lang racket \n (define polynomial (lambda (x a b c d e f g) (+ a (* b (expt (/ x 16) 1)) (* c (expt (/ x 16) 2)) (* d (expt (/ x 16) 3)) (* e (expt (/ x 16) 4)) (* f (expt (/ x 16) 5)) (* g (expt (/ x 16) 6)))))\n"

str_ += "(define "+ str(func_name) +"\n (lambda (t i x y)\n(let ((list_ind (modulo (* t 28) "+ str(n_images)+")))\n ( ( list-ref (list "


# objective funktion, needed to fit polynomial

def objective1(x, *params):
    x = x / 16 # normalize

    res = polynomial(x, params[0], params[1], params[2], params[3], params[4], params[5], params[6])

    return res

laufindex = 0 #used for progress display

if(render):
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(36, 36)) # creates Matplotlib figure

for file in os.listdir(directory_in):

    if(laufindex % 100 == 0):
        print(laufindex)

    laufindex += 1


    if(render):
    	ax1.clear()
    	ax2.clear()
    	ax3.clear()
    	ax4.clear()
    filename = os.fsdecode(file)

    image = Image.open(os.path.join(directory_in, filename)).convert('L')

    # add lambda function per image
    str_ += "( lambda (x) \n"
    str_ += "(cond \n"


    # scale to tixy and convert to numpy array, interpolate between -1 and 1
    newsize = (tixy_size, tixy_size)
    im1 = image.resize(newsize)
    arr = np.asarray(im1, dtype=np.float32)
    arr_i = np.interp(arr, (arr.min(), arr.max()), (-1, +1))

    # create x array for fitting, fit each row of the array to a polynomial, record the polynomial weights
    i = 1
    weights = []
    for row in arr_i:

        str_ += "((= y " + str(i) + ") (polynomial x" # polynomial call for row i

        x_vals = [x for x in range(1, tixy_size + 1)]
        a_, b = curve_fit(objective1, x_vals, row, p0=np.random.normal(size=7), maxfev= maxfev_)

        for val in a_:
            str_ += " " + str(val) #add parameters to polynomial function

        weights += [a_]

        i += 1

        str_ += "))\n" # close brackets

    res_vals = []

    str_ += "))\n"

    # translate the image using fitted polynomials for visualization

    if(render):
        for y in range(0, tixy_size):
            for x in range(1, tixy_size + 1):

                val = objective1(x, *weights[y])

                if (val > 1):
                    val = 1
                if (val < -1):
                    val = -1
                res_vals += [val]

        flarr = np.asarray(res_vals).reshape(tixy_size, tixy_size)

        # simulate tixy view
        i_ = tixy_size
        for row in flarr:
            j_ = 0
            for val in row:
                j_ += 1

                if (val > 1):
                    val = 1
                if (val < -1):
                    val = -1

                if (val > 0):
                    ax4.scatter(j_, i_, c="red", s=abs(val) * 1500)
                else:
                    ax4.scatter(j_, i_, c="white", s=abs(val) * 1500)
            i_ -= 1

        #render using Matplotlib
        ax4.set_facecolor((0, 0, 0))
        ax4.set_aspect('equal')

        ax1.matshow(image)
        ax2.matshow(arr_i)
        ax3.matshow(flarr)

        ax1.set_title('Original image', fontsize=75)
        ax2.set_title('Pixelated image', fontsize=75)
        ax3.set_title('Reconstructed image', fontsize=75)
        ax4.set_title('Simulated TIXY view', fontsize=75)
        plt.savefig(os.path.join(directory_out, filename))
        

str_ += " ) list_ind) x) )))\n"
str_ += "(provide "+ str(func_name)+")" # provies function for other racket files so the file can be imported with require

#write racket file
with open(os.path.join(directory_out, rkt_out), "w") as f:
    f.write(str_)