import itertools
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from scipy import stats
import warnings
from sklearn import metrics
from model import *
from evaluate import *
warnings.filterwarnings("ignore")
from scipy.stats import boxcox
from scipy.stats import yeojohnson
from sklearn.metrics import recall_score, precision_score, classification_report, roc_auc_score, roc_curve, \
    confusion_matrix
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

# models = [logistic_model,decisiontree_model,randomforest_model,svm_model,gaussion_model,KNN_model]
# models_Name = ['logistic_model','decisiontree_model','randomforest_model','svm_model','gaussion_model','KNN_model']

models = [gaussion_model]
models_Name = ['gaussion_model']
df = pd.read_csv("adult_new.csv")

qualvariables=['workclass','education','marital-status','occupation','relationship','race','sex','native-country']
quanvariables=['age','fnlwgt','education-num','hours-per-week','capital-gain','capital-loss']
skewnesslist=[]
kurtosislist=[]
minandmax=[]
maxvalue=[]

for i in quanvariables:
    skewnesslist.append(df[i].skew())
    kurtosislist.append(df[i].kurt())
    minandmax.append(abs(max(df[i])-min(df[i])))
    maxvalue.append(max(df[i]))


nomofskewness=np.std(skewnesslist)
nomofkurtosis=np.std(kurtosislist)

if (max(minandmax) / min(minandmax) >= 3):
    print("数据要标准化处理")
if (max(maxvalue) / min(maxvalue) >= 3):
    print("数据要归一化处理")

for i in quanvariables:
    if(abs(df[i].skew()/nomofskewness)<=1.96 and abs(df[i].kurt()/nomofkurtosis)<=1.96):
        print(i+"可以正态化")

#正态化
def normalization(df):
    df["age"] = yeojohnson(df["age"])[0]
    df["fnlwgt"] = yeojohnson(df["fnlwgt"])[0]
    df["education-num"] = yeojohnson(df["education-num"])[0]
    df["hours-per-week"] = yeojohnson(df['hours-per-week'])[0]
    df["capital-loss"] = yeojohnson(df['capital-loss'])[0]
    return df
#标准化
def standardization(df):
    from sklearn.preprocessing import StandardScaler
    StandardScaler = StandardScaler()
    columns_to_scale = ['age','fnlwgt','education-num','hours-per-week','capital-gain','capital-loss']
    df[columns_to_scale] = StandardScaler.fit_transform(df[columns_to_scale])
    return df
#归一化
def preprocessing(df):
    from sklearn import preprocessing
    min_max_scaler = preprocessing.MinMaxScaler()
    columns_to_scale = ['age','fnlwgt','education-num','hours-per-week','capital-gain','capital-loss']
    df[columns_to_scale] = min_max_scaler.fit_transform(df[columns_to_scale])
    return df
#哑变量
def dummyvariable(df):
    a = pd.get_dummies(df['workclass'], prefix = "workclass")#get_dummies进行ont hot编码
    c = pd.get_dummies(df['marital-status'], prefix="marital-status")
    d = pd.get_dummies(df['occupation'], prefix="occupation")
    e = pd.get_dummies(df['relationship'], prefix="relationship")
    f = pd.get_dummies(df['race'], prefix="race")
    g = pd.get_dummies(df['sex'], prefix="sex")
    h = pd.get_dummies(df['native-country'], prefix="native-country")
    frames = [df, a, c, d, e,f,g,h]
    df = pd.concat(frames, axis=1)
    df = df.drop(columns=['workclass','marital-status','occupation','relationship','race','sex','native-country'])
    return df

for i in range(len(models)):
       df = pd.read_csv("adult_new.csv")
       if(models_Name[i]=="logistic_model"):
           df = dummyvariable(df)
           df = normalization(df)
           df = preprocessing(df)
           base_model = models[i]
           X = df.drop(['income'], axis=1)
           y = df['income']
           X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=40)
           result, y_score = base_model(X_train, X_test, y_train, y_test)
           eva = evaluate(result, y_score, models_Name[i])
           Re = eva.show_all()
           Re.to_csv('1.csv', mode='a', float_format='%.4f')
       elif(models_Name[i]=="decisiontree_model"):
           df = normalization(df)
           df = preprocessing(df)
           base_model = models[i]
           X = df.drop(['income'], axis=1)
           y = df['income']
           X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=40)
           result, y_score = base_model(X_train, X_test, y_train, y_test)
           eva = evaluate(result, y_score, models_Name[i])
           Re = eva.show_all()
           Re.to_csv('1.csv', mode='a', float_format='%.4f')
       elif(models_Name[i]=="randomforest_model"):
           df = normalization(df)
           df = preprocessing(df)
           base_model = models[i]
           X = df.drop(['income'], axis=1)
           y = df['income']
           X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=40)
           result, y_score = base_model(X_train, X_test, y_train, y_test)
           eva = evaluate(result, y_score, models_Name[i])
           Re = eva.show_all()
           Re.to_csv('1.csv', mode='a', float_format='%.4f')
       elif(models_Name[i]=="svm_model"):
           df = dummyvariable(df)
           df = normalization(df)
           df = preprocessing(df)
           base_model = models[i]
           X = df.drop(['income'], axis=1)
           y = df['income']
           X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=40)
           result, y_score = base_model(X_train, X_test, y_train, y_test)
           eva = evaluate(result, y_score, models_Name[i])
           Re = eva.show_all()
           Re.to_csv('1.csv', mode='a', float_format='%.4f')
       elif (models_Name[i] == "gaussion_model"):
           df = normalization(df)
           df = preprocessing(df)
           base_model = models[i]
           X = df.drop(['income'], axis=1)
           y = df['income']
           X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=40)
           result, y_score = base_model(X_train, X_test, y_train, y_test)
           eva = evaluate(result, y_score, models_Name[i])
           Re = eva.show_all()
           Re.to_csv('1.csv', mode='a', float_format='%.4f')
       elif (models_Name[i] == "KNN_model"):
           df = dummyvariable(df)
           df = normalization(df)
           df = preprocessing(df)
           base_model = models[i]
           X = df.drop(['income'], axis=1)
           y = df['income']
           X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=40)
           result, y_score = base_model(X_train, X_test, y_train, y_test)
           eva = evaluate(result, y_score, models_Name[i])
           Re = eva.show_all()
           Re.to_csv('1.csv', mode='a', float_format='%.4f')
       else:
           df = dummyvariable(df)
           df = normalization(df)
           df = preprocessing(df)
           base_model = models[i]
           X = df.drop(['income'], axis=1)
           y = df['income']
           X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=40)
           result, y_score = base_model(X_train, X_test, y_train, y_test)
           eva = evaluate(result, y_score, models_Name[i])
           Re = eva.show_all()
           Re.to_csv('1.csv', mode='a', float_format='%.4f')

