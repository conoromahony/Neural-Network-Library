class neuralNetwork:

    def __init__(self, sizes, epochs, learning_rate):
        self.sizes = sizes
        self.epochs = epochs
        self.lr = learning_rate

        # The sizes argument contains a list of integers, where each integer represent the number of nodes in each
        # layer of the neural network. At present, this list is hardcoded to create a neural network with four layers.
        # TODO: Change this so it works with a neural network with any number of layers. We will require some number
        # in the object to indicate the number of layers.
        input_layer=self.sizes[0]
        hidden_1=self.sizes[1]
        hidden_2=self.sizes[2]
        output_layer=self.sizes[3]

        # The dimensions of each matrix depend on the number of nodes in the respective layers.
        # randn returns a random number, between 0 and 1. However, we want random numbers between -1.0 and +1.0 because
        # we can have negative weights. The typical approach is to sutract 0.5 from the generated random number.
        # However, a more sophisticated approach is to sample the weights from a normal distribution, centered around 0, 
        # with standard deviation that is related to the number of incoming links to the node (that is, 1 over the square 
        # root of the number of incoming links, which is the same as raising it to the power on -0.5).
        #   np.random.normal(0.0, pow(hidden_1, -0.5), (hidden_1, input_layer))
        # TODO: We will need some way to generate these weights that allows for a flexible number of layers. 
        self.params = {
            'W1':np.random.randn(hidden_1, input_layer) * np.sqrt(1. / hidden_1),
            'W2':np.random.randn(hidden_2, hidden_1) * np.sqrt(1. / hidden_2),
            'W3':np.random.randn(output_layer, hidden_2) * np.sqrt(1. / output_layer)
        }


    def sigmoid(self, x, derivative=False):
        if derivative:
            return (np.exp(-x))/((np.exp(-x)+1)**2)
        return 1/(1 + np.exp(-x))


    def softmax(self, x, derivative=False):
        # Numerically stable with large exponentials
        exps = np.exp(x - x.max())
        if derivative:
            return exps / np.sum(exps, axis=0) * (1 - exps / np.sum(exps, axis=0))
        return exps / np.sum(exps, axis=0)


    def forward_pass(self, x_train):
        params = self.params

        # input layer activations becomes sample
        params['A0'] = x_train

        # input layer to hidden layer 1
        params['Z1'] = np.dot(params["W1"], params['A0'])
        params['A1'] = self.sigmoid(params['Z1'])

        # hidden layer 1 to hidden layer 2
        params['Z2'] = np.dot(params["W2"], params['A1'])
        params['A2'] = self.sigmoid(params['Z2'])

        # hidden layer 2 to output layer
        params['Z3'] = np.dot(params["W3"], params['A2'])
        params['A3'] = self.softmax(params['Z3'])

        return params['A3']


    def backward_pass(self, y_train, output):
        '''
            This is the backpropagation algorithm, for calculating the updates
            of the neural network's parameters.

            Note: There is a stability issue that causes warnings. This is 
                    caused  by the dot and multiply operations on the huge arrays.
                    
                    RuntimeWarning: invalid value encountered in true_divide
                    RuntimeWarning: overflow encountered in exp
                    RuntimeWarning: overflow encountered in square
        '''
        params = self.params
        change_w = {}

        # Calculate W3 update
        error = 2 * (output - y_train) / output.shape[0] * self.softmax(params['Z3'], derivative=True)
        change_w['W3'] = np.outer(error, params['A2'])

        # Calculate W2 update
        error = np.dot(params['W3'].T, error) * self.sigmoid(params['Z2'], derivative=True)
        change_w['W2'] = np.outer(error, params['A1'])

        # Calculate W1 update
        error = np.dot(params['W2'].T, error) * self.sigmoid(params['Z1'], derivative=True)
        change_w['W1'] = np.outer(error, params['A0'])

        return change_w


    def update_network_parameters(self, changes_to_w):
        '''
            Update network parameters according to update rule from
            Stochastic Gradient Descent.

            θ = θ - η * ∇J(x, y), 
                theta θ:            a network parameter (e.g. a weight w)
                eta η:              the learning rate
                gradient ∇J(x, y):  the gradient of the objective function,
                                    i.e. the change for a specific theta θ
        '''
        
        for key, value in changes_to_w.items():
            self.params[key] -= self.lr * value

    def compute_accuracy(self, test_data, output_nodes):
        '''
            This function does a forward pass of x, then checks if the indices
            of the maximum value in the output equals the indices in the label
            y. Then it sums over each prediction and calculates the accuracy.
        '''
        predictions = []

        for x in train_list:
            all_values = x.split(',')
            # scale and shift the inputs
            inputs = (np.asfarray(all_values[1:]) / 255.0 * 0.99) + 0.01
            # create the target output values (all 0.01, except the desired label which is 0.99)
            targets = np.zeros(output_nodes) + 0.01
            # all_values[0] is the target label for this record
            targets[int(all_values[0])] = 0.99
            output = self.forward_pass(inputs)
            pred = np.argmax(output)
            predictions.append(pred == np.argmax(targets))
        
        return np.mean(predictions)


    def train(self, train_list, test_list, output_nodes):
        start_time = time.time()
        for iteration in range(self.epochs):
            for x in train_list:
                all_values = x.split(',')
                # scale and shift the inputs
                inputs = (np.asfarray(all_values[1:]) / 255.0 * 0.99) + 0.01
                # create the target output values (all 0.01, except the desired label which is 0.99)
                targets = np.zeros(output_nodes) + 0.01
                # all_values[0] is the target label for this record
                targets[int(all_values[0])] = 0.99
                output = self.forward_pass(inputs)
                changes_to_w = self.backward_pass(targets, output)
                self.update_network_parameters(changes_to_w)
            
            accuracy = self.compute_accuracy(test_list, output_nodes)
            print('Epoch: {0}, Time Spent: {1:.2f}s, Accuracy: {2:.2f}%'.format(
                iteration+1, time.time() - start_time, accuracy * 100
            ))


    def query():
      pass


dnn = DNN(sizes=[784, 128, 64, 10], epochs=10, lr=0.001)

# Need to define train_list and test_list!!!
dnn.train(train_list, test_list, 10)
