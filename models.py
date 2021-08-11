import nn
import math

class PerceptronModel(object):
    def __init__(self, dimensions):
        """
        Initialize a new Perceptron instance.

        A perceptron classifies data points as either belonging to a particular
        class (+1) or not (-1). `dimensions` is the dimensionality of the data.
        For example, dimensions=2 would mean that the perceptron must classify
        2D points.
        """
        self.w = nn.Parameter(1, dimensions)

    def get_weights(self):
        """
        Return a Parameter instance with the current weights of the perceptron.
        """
        return self.w

    def run(self, x):
        """
        Calculates the score assigned by the perceptron to a data point x.

        Inputs:
            x: a node with shape (1 x dimensions)
        Returns: a node containing a single number (the score)
        """

        return nn.DotProduct(x, self.get_weights())


    def get_prediction(self, x):
        """
        Calculates the predicted class for a single data point `x`.

        Returns: 1 or -1
        """
        "*** YOUR CODE HERE ***"
        number = nn.as_scalar(self.run(x))
        if number >= 0:
            return 1
        return -1

    def train(self, dataset):
        """
        Train the perceptron until convergence.
        """
        "*** YOUR CODE HERE ***"

        mistakes = True
        while mistakes:
        #i = 0
        #while i < 20:
            mistakes = False
            for d in dataset.iterate_once(1):
                x = d[0]
                y = d[1]
                prediction = self.get_prediction(x)
                if prediction != nn.as_scalar(y):
                    mistakes = True
                    self.w.update(x, nn.as_scalar(y))

class RegressionModel(object):
    """
    A neural network model for approximating a function that maps from real
    numbers to real numbers. The network should be sufficiently large to be able
    to approximate sin(x) on the interval [-2pi, 2pi] to reasonable precision.
    """
    def __init__(self):
        # Initialize your model parameters here
        "*** YOUR CODE HERE ***"
        self.batchSize = 20
        self.w1 = nn.Parameter(1, 30)
        self.b1 = nn.Parameter(1, 30)
        self.w2 = nn.Parameter(30, 1)
        self.b2 = nn.Parameter(1, 1)
        self.params = [self.w1, self.w2, self.b1, self.b2]
        self.learning = 0.03


    def run(self, x):
        """
        Runs the model for a batch of examples.

        Inputs:
            x: a node with shape (batch_size x 1)
        Returns:
            A node with shape (batch_size x 1) containing predicted y-values
        """
        "*** YOUR CODE HERE ***"
        b1 = self.b1
        b2 = self.b2
        xm = nn.Linear(x, self.w1)
        linear = nn.AddBias(xm, b1)
        secondLin = nn.Linear(nn.ReLU(linear), self.w2)
        predY = nn.AddBias(secondLin, b2)
        return predY

    def get_loss(self, x, y):
        """
        Computes the loss for a batch of examples.

        Inputs:
            x: a node with shape (batch_size x 1)
            y: a node with shape (batch_size x 1), containing the true y-values
                to be used for training
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"
        prediction = self.run(x)
        return nn.SquareLoss(prediction, y)

    def train(self, dataset):
        """
        Trains the model.
        """
        "*** YOUR CODE HERE ***"

        first = True
        while first or nn.as_scalar(loss) > 0.015:
            first = False
            for d in dataset.iterate_once(self.batchSize):
                x = d[0]
                y = d[1]
                #prediction = self.run(x)
                loss = self.get_loss(x, y)
                gradW1, gradW2, gradB1, gradB2 = nn.gradients(loss, self.params)
                #print('loss:', nn.as_scalar(loss))

                self.w1.update(gradW1, -self.learning)
                self.w2.update(gradW2, -self.learning)
                self.b1.update(gradB1, -self.learning)
                self.b2.update(gradB2, -self.learning)



class DigitClassificationModel(object):
    """
    A model for handwritten digit classification using the MNIST dataset.

    Each handwritten digit is a 28x28 pixel grayscale image, which is flattened
    into a 784-dimensional vector for the purposes of this model. Each entry in
    the vector is a floating point number between 0 and 1.

    The goal is to sort each digit into one of 10 classes (number 0 through 9).

    (See RegressionModel for more information about the APIs of different
    methods here. We recommend that you implement the RegressionModel before
    working on this part of the project.)
    """
    def __init__(self):
        # Initialize your model parameters here
        "*** YOUR CODE HERE ***"
        self.batchSize = 20
        #self.labels = nn.Parameter(self.batchSize, 10)
        self.w1 = nn.Parameter(784, 100)
        self.b1 = nn.Parameter(1, 100)
        self.w2 = nn.Parameter(100, 10)
        self.b2 = nn.Parameter(1, 10)
        self.params = [self.w1, self.w2, self.b1, self.b2]
        self.learning = 0.07


    def run(self, x):
        """
        Runs the model for a batch of examples.

        Your model should predict a node with shape (batch_size x 10),
        containing scores. Higher scores correspond to greater probability of
        the image belonging to a particular class.

        Inputs:
            x: a node with shape (batch_size x 784)
        Output:
            A node with shape (batch_size x 10) containing predicted scores
                (also called logits)
        """
        "*** YOUR CODE HERE ***"
        b1 = self.b1
        b2 = self.b2
        xm = nn.Linear(x, self.w1)
        linear = nn.AddBias(xm, b1)
        secondLin = nn.Linear(nn.ReLU(linear), self.w2)
        predY = nn.AddBias(secondLin, b2)
        return predY

    def get_loss(self, x, y):
        """
        Computes the loss for a batch of examples.

        The correct labels `y` are represented as a node with shape
        (batch_size x 10). Each row is a one-hot vector encoding the correct
        digit class (0-9).

        Inputs:
            x: a node with shape (batch_size x 784)
            y: a node with shape (batch_size x 10)
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"
        logits = self.run(x)
        return nn.SoftmaxLoss(logits, y)


    def train(self, dataset):
        """
        Trains the model.
        """
        "*** YOUR CODE HERE ***"
        first = True
        #print(dataset.get_validation_accuracy())
        while first or dataset.get_validation_accuracy() < .975:
            #print(dataset.get_validation_accuracy())
            first = False
            for d in dataset.iterate_once(self.batchSize):
                x = d[0]
                y = d[1]
                #prediction = self.run(x)
                loss = self.get_loss(x, y)
                gradW1, gradW2, gradB1, gradB2 = nn.gradients(loss, self.params)
                #print('loss:', nn.as_scalar(loss))
                self.w1.update(gradW1, -self.learning)
                self.w2.update(gradW2, -self.learning)
                self.b1.update(gradB1, -self.learning)
                self.b2.update(gradB2, -self.learning)

            print(dataset.get_validation_accuracy())




class LanguageIDModel(object):
    """
    A model for language identification at a single-word granularity.

    (See RegressionModel for more information about the APIs of different
    methods here. We recommend that you implement the RegressionModel before
    working on this part of the project.)
    """
    def __init__(self):
        # Our dataset contains words from five different languages, and the
        # combined alphabets of the five languages contain a total of 47 unique
        # characters.
        # You can refer to self.num_chars or len(self.languages) in your code
        self.num_chars = 47
        self.languages = ["English", "Spanish", "Finnish", "Dutch", "Polish"]

        # Initialize your model parameters here
        "*** YOUR CODE HERE ***"
        self.dimension = 5
        self.hiddenlayers = 250
        self.batchSize = 100
        self.w1 = nn.Parameter(self.num_chars, 250)
        self.b1 = nn.Parameter(1, 250)
        self.w2 = nn.Parameter(250, 5)
        self.b2 = nn.Parameter(1, 5)
        self.hiddenW = nn.Parameter(self.dimension, 250)
        self.params = [self.w1, self.w2, self.hiddenW, self.b1, self.b2]
        self.learning = .01

    def run(self, xs):
        """
        Runs the model for a batch of examples.

        Although words have different lengths, our data processing guarantees
        that within a single batch, all words will be of the same length (L).

        Here `xs` will be a list of length L. Each element of `xs` will be a
        node with shape (batch_size x self.num_chars), where every row in the
        array is a one-hot vector encoding of a character. For example, if we
        have a batch of 8 three-letter words where the last word is "cat", then
        xs[1] will be a node that contains a 1 at position (7, 0). Here the
        index 7 reflects the fact that "cat" is the last word in the batch, and
        the index 0 reflects the fact that the letter "a" is the inital (0th)
        letter of our combined alphabet for this task.

        Your model should use a Recurrent Neural Network to summarize the list
        `xs` into a single node of shape (batch_size x hidden_size), for your
        choice of hidden_size. It should then calculate a node of shape
        (batch_size x 5) containing scores, where higher scores correspond to
        greater probability of the word originating from a particular language.

        Inputs:
            xs: a list with L elements (one per character), where each element
                is a node with shape (batch_size x self.num_chars)
        Returns:
            A node with shape (batch_size x 5) containing predicted scores
                (also called logits)
        """
        "*** YOUR CODE HERE ***"
        i = 0
        b1 = self.b1
        b2 = self.b2
        #print('xs:', xs)
        for x in xs:
            #print(i, x)
            if i == 0:
                z = nn.Linear(x, self.w1)
                linear = nn.AddBias(z, b1)
                secondLin = nn.Linear(nn.ReLU(linear), self.w2)
                h = nn.AddBias(secondLin, b2)
                i += 1
            else:
                lin = nn.Linear(x, self.w1)
                hidden = nn.Linear(h, self.hiddenW)
                z = nn.Add(lin, hidden)
                linear = nn.AddBias(z, b1)
                secondLin = nn.Linear(nn.ReLU(linear), self.w2)
                h = nn.AddBias(secondLin, b2)
                i += 1
        #z = nn.Linear(h, self.w1)
        #linear = nn.AddBias(z, b1)
        #secondLin = nn.Linear(nn.ReLU(linear), self.w2)
        return h
        #return nn.AddBias(secondLin, b2)


    def get_loss(self, xs, y):
        """
        Computes the loss for a batch of examples.

        The correct labels `y` are represented as a node with shape
        (batch_size x 5). Each row is a one-hot vector encoding the correct
        language.

        Inputs:
            xs: a list with L elements (one per character), where each element
                is a node with shape (batch_size x self.num_chars)
            y: a node with shape (batch_size x 5)
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"

        logits = self.run(xs)
        return nn.SoftmaxLoss(logits, y)

    def train(self, dataset):
        """
        Trains the model.
        """
        "*** YOUR CODE HERE ***"
        first = True
        #print(dataset.get_validation_accuracy())
        while first or dataset.get_validation_accuracy() < .85:
            #print(dataset.get_validation_accuracy())
            first = False
            for d in dataset.iterate_once(self.batchSize):
                x = d[0]
                y = d[1]
                #prediction = self.run(x)
                loss = self.get_loss(x, y)
                gradW1, gradW2, gradhW, gradB1, gradB2 = nn.gradients(loss, self.params)
                #print('loss:', nn.as_scalar(loss))
                self.w1.update(gradW1, -self.learning)
                self.w2.update(gradW2, -self.learning)
                self.b1.update(gradB1, -self.learning)
                self.b2.update(gradB2, -self.learning)
                self.hiddenW.update(gradhW, -self.learning)

            #print(dataset.get_validation_accuracy())
