import matplotlib.pyplot as plt 
from mypytable import MyPyTable
table = MyPyTable()

def bar_chart_example(x, y):
    plt.figure()
    plt.bar(x, y)
    plt.show()
    
def pie_chart_example(x, y):
    plt.figure()
    plt.pie(y, labels=x, autopct="%1.1f%%")
    plt.show()


def histogram_example(data, data2, data_label, data2_label, title, xlabel, ylabel):
    plt.figure()
    plt.hist(data, bins=10, edgecolor='black', color='blue',label=data_label) 
    plt.hist(data2, bins=10, edgecolor='black', color='red',label=data2_label, fc=(1,0,0,0.5)) 
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.show()

def simple_histogram_example(data2, data_label, color=()):
    plt.figure()
    plt.hist(data2, bins=10, edgecolor='black', color='red', label=data_label, fc=color) 
    plt.legend()
    plt.show()

def scatter_chart_example(x, y):
    plt.figure() 
    plt.scatter(x, y, marker=".", s=100, c="purple")

    plt.tight_layout() 
    plt.show()

def linreg_scatter_chart_example(x, y, m, b):
    plt.figure() 
    plt.scatter(x, y, marker=".", s=100, c="purple")

    plt.tight_layout() 
    plt.show()
    

def get_column(table, header, col_name):
    col = []
    col_index = header.index(col_name)
    for row in table:
        col.append(row[col_index])

    return col


def get_frequencies(table, header, col_name):
    col = get_column(table, header, col_name)
    col.sort() 

    values = [] 
    counts = []
    for value in col:
        if value not in values:
            values.append(value)
            counts.append(1)
        else:
            counts[-1] += 1
    return values, counts

def find_mean(var):
    return sum(var) / len(var)

def compute_slope_intercept(x, y):
    meanx = find_mean(x)
    meany = find_mean(y)
    
    m = sum([(x[i] - meanx) * (y[i] - meany) for i in range(len(x))]) / \
        sum([(x[i] - meanx) ** 2 for i in range(len(x))])

    b = meany - m * meanx

    return (m, b)

def box_plot_example(distributions, labels): 
    plt.figure()
    plt.boxplot(distributions)


    plt.xticks(list(range(1, len(distributions) + 1)), labels)
    
    plt.annotate("$\mu=100$", xy=(1.5, 105), xycoords="data", horizontalalignment="center")
    plt.annotate("$\mu=100$", xy=(0.5, 0.5), xycoords="axes fraction", 
                 horizontalalignment="center", color="blue")

    plt.show()