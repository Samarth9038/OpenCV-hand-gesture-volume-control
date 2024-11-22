import numpy as np
import pandas as pd


def standardization(dataset):
  mean =np.mean(dataset)
  deviation = np.std(dataset)
  dataset = (dataset-mean)/deviation
  return dataset, mean, deviation


def model(new_Data, theta, mean, deviation):
  new_Data = np.array([[float(new_Data)]])
  new_Data = (new_Data-mean)/deviation
  new_Data = np.column_stack((np.ones(len(new_Data)), new_Data))
  res = np.dot(new_Data, theta)
  return int(round(float(res[0][0]),2)*100)


def gradient_descent(dataset, y_target, alpha, iterations):
  m = len(dataset) 
  theta = np.array([[1.0], [0.15302957]])

  for i in range(iterations):
    prediction = np.dot(dataset, theta)
    error = prediction - y_target
    gradient = (1 / m) * np.dot(dataset.T, error)
    theta = theta - alpha * gradient

  return theta

def newWeights():
    data = pd.read_csv('allData.csv', header = None, index_col=None, usecols=[0])
    dataset = np.array(data)
    y_Trgt = np.array(pd.read_csv('allData.csv', header = None, index_col=None, usecols=[1]))
    alpha = 0.01
    iterations = 10000

    m = len(dataset)
    dataset, mean, dev = standardization(dataset)
    dataset = np.column_stack((np.ones(len(dataset)), dataset))
    weights = gradient_descent(dataset, y_Trgt, alpha, iterations)

    # out = model(4, weights, mean, dev)
    np.savez('data.npz', mean = mean, dev = dev, out = weights)
    # print(out)


def call(number):
    try:
        data = np.load('data.npz')
        return (model(number, data['out'], data['mean'], data['dev']))

    except:
       print("NO OLD DATA, EXITING")
       return 'False'
       
       

# if __name__ == '__main__':
   # print(call(5)