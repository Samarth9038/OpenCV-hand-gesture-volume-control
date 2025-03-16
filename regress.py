import numpy as np
import pandas as pd


def standardization(dataset):
  mean =np.mean(dataset)
  deviation = np.std(dataset)
  dataset = (dataset-mean)/deviation
  return dataset, mean, deviation


def model(new_Data, theta, mean, deviation, degree=2):
  new_Data = np.array([[float(new_Data)]])
  new_Data = (new_Data-mean)/deviation
  new_Data = np.column_stack([new_Data**i for i in range(degree+1)])
  new_Data = np.column_stack((np.ones(len(new_Data)), new_Data))
  res = np.dot(new_Data, theta)
  print(res)
  return int(round(float(res[0]),2)*100)


def gradient_descent(dataset, y_target, alpha, iterations):
  m = len(dataset) 
  theta = np.zeros(dataset.shape[1])

  for i in range(iterations):
    prediction = np.dot(dataset, theta)
    error = prediction - y_target
    gradient = (1 / m) * np.dot(dataset.T, error)
    theta = theta - alpha * gradient

  return theta

def newWeights(degree=2, alpha=0.01, iterations=10000):
    #Linear Regression Upgraded to Polynomial Regression
    # data = pd.read_csv('allData.csv')
    # y_Trgt = data['val']
    # data = data['dist']
    # alpha = 0.01
    # iterations = 10000
    # dataset, mean, dev = standardization(data)
    # plt.scatter(y_Trgt, dataset)
    # plt.show()
    # dataset = np.column_stack((np.ones(len(dataset)), dataset))
    # weights = gradient_descent(dataset, y_Trgt, alpha, iterations)
    # np.savez('data.npz', mean = mean, dev = dev, out = weights)

    data = pd.read_csv('allData.csv')
    y_Trgt = data['val'].values
    data = data['dist'].values.reshape(-1, 1)

    dataset, mean, dev = standardization(data)
    dataset_poly = np.column_stack([dataset**i for i in range(degree + 1)])
    dataset_poly = np.column_stack((np.ones(len(dataset_poly)), dataset_poly))

    weights = gradient_descent(dataset_poly, y_Trgt, alpha, iterations)
    np.savez('data.npz', mean=mean, dev=dev, out=weights, degree = degree)

    return weights


def call(number):
    try:
      data = np.load('data.npz')
      return (model(number, data['out'], data['mean'], data['dev']))

    except:
       print("NO OLD DATA, EXITING")
       return 'False'
       
       

# if __name__ == '__main__':
#    newWeights()
#    print(call(2))
