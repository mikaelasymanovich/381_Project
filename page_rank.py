import numpy

def main():
	Hhat = [[ 0.33333333  0.5         0.          0.        ]
 [ 0.33333333  0.          0.          0.        ]
 [ 0.          0.5         0.          0.        ]
 [ 0.33333333  0.          0.          0.        ]]
	
	pi = [1.0/4, 1.0/4, 1.0/4, 1.0/4]

	N_row = [1.0, 1.0, 1.0, 1.0]
	N_col = [[1.0/4],[1.0/4],[1.0/4],[1.0/4]]
	theta = 0.85
	N = 4.0;

	G_x = numpy.array(Hhat)*theta
	G_y = (1.0-theta)*numpy.array(N_row)*numpy.array(N_col)
	G = G_x + G_y

	print(G)

	for i in range(0,40):
		pi = numpy.dot(numpy.transpose(pi), G)

	
	print pi
if  __name__ =='__main__':main()