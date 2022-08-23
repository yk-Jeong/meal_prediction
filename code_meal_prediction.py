# -*- coding: utf-8 -*-
"""code_meal_prediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/13e0aoLoZEBsEMhagQqkjwL_ieNLJMUrS

### 라이브러리 import 및 구글 드라이브 연동
"""

from google.colab import drive 
drive.mount('/content/drive')

import pandas as pd
import numpy as np
import pandas_profiling

pip install pandas-profiling==2.11.0 --upgrade

"""lib for visualization"""

import matplotlib.pyplot as plt
import seaborn as sns

pip install pdpbox

pip install shap

import shap
from pdpbox.pdp import pdp_isolate, pdp_plot #단일 feature
from pdpbox.pdp import pdp_interact, pdp_interact_plot #복수 features

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline

"""lib for modeling"""

#data split
from sklearn.model_selection import train_test_split

pip install --upgrade category_encoders

#ordinal-encoder, target encoder
from sklearn.preprocessing import OrdinalEncoder
from category_encoders import TargetEncoder

#make pipeline
from sklearn.pipeline import make_pipeline

#선형회귀
from sklearn.linear_model import LinearRegression

#RF회귀
from sklearn.ensemble import RandomForestRegressor

#ridge 회귀
from sklearn.linear_model import RidgeCV

#decision tree
from sklearn.tree import DecisionTreeRegressor

#xgboost
from xgboost import XGBRegressor

#로그변환을 위한 lib
from sklearn.compose import TransformedTargetRegressor

#표준화 
from sklearn.preprocessing import StandardScaler

#결측치 처리
from sklearn.impute import SimpleImputer

#하이퍼파라미터 탐색을 위한 RandomizedSearchCV
from sklearn.model_selection import RandomizedSearchCV

#gradient boosting model
from xgboost import XGBRegressor

from scipy.stats import randint, uniform

"""평가지표를 위한 lib """

from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import r2_score

"""### 데이터 로드
Kaggle의 Saptarshi Ghosh가 제공하는 Meal delivery company dataset(2018.12.)를 준비하였음 (https://www.kaggle.com/ghoshsaptarshi/av-genpact-hack-dec2018)
"""

test = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/CS-AIB08/N2-ML/S2/meal_dataset/test.csv')
train = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/CS-AIB08/N2-ML/S2/meal_dataset/train.csv')
meal_info = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/CS-AIB08/N2-ML/S2/meal_dataset/meal_info.csv')
fulfilment_center_info = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/CS-AIB08/N2-ML/S2/meal_dataset/fulfilment_center_info.csv')

"""### 데이터 확인"""

train.head(), test.head()

fulfilment_center_info.head(),meal_info.head()

"""결측치 확인"""

train.isna().sum().sort_values(), test.isna().sum().sort_values()

fulfilment_center_info.isna().sum().sort_values(), meal_info.isna().sum().sort_values()

meal_info['meal_id'].unique()

meal_info['category'].unique()

meal_info['cuisine'].unique() #Continental food = European food

test.shape, train.shape, fulfilment_center_info.shape, meal_info.shape

train.info()

"""target을 num_orders로 하는 회귀 문제로 가정하고, target의 분포를 확인해 봄"""

target = 'num_orders'

train[target].describe()

"""극단적으로 right-skewed함을 확인

### Data Wrangling

#### 1. merge
"""

len(train.meal_id.unique()) == len(meal_info)

"""meal_info.csv와 fulfilment_center_info를 train과 병합 """

train = train.merge(meal_info, on='meal_id')
train = train.merge(fulfilment_center_info, on='center_id')

"""test set에도 같은 작업을 진행"""

test = test.merge(meal_info, on='meal_id')
test = test.merge(fulfilment_center_info, on='center_id')

"""#### 2. feature engineering"""

train

"""####def for feature engineering

컬럼 추가: `discount` (할인 여부를 Y, N으로 계산), `difference` (최종가와 기본가 간의 차액 계산)
"""

def engineering(df):
  df = df.copy()
  
  #컬럼 추가: `discount` (할인 여부를 Y, N으로 계산), `difference` (최종가와 기본가 간의 차액 계산)
  df['discount'] = np.where(((df['checkout_price']-df['base_price']).values < 0), 1, 0)
  df['difference'] = (df['checkout_price']-df['base_price'])
  
  return df

engineering(train)

engineering(test)

"""#### 3. target 상위 5%를 제거"""

train[target] = train[train['num_orders'] < np.percentile(train['num_orders'], 95)]['num_orders']

train = train.dropna(axis=0)

train[target].describe()

#이상치 제거 후의 분포 확인
sns.displot(train[target], kde=True);
plt.axvline(196, color='red')
plt.show()

"""로그 변환"""

plots = pd.DataFrame()
plots['original'] = train[target]
plots['transformed'] = np.log1p(train[target])
plots['backtoOriginal'] = np.expm1(np.log1p(train[target]))

fig, ax = plt.subplots(1, 3, figsize = (15, 5))
sns.histplot(plots['original'], ax = ax[0])
sns.histplot(plots['transformed'], ax = ax[1])
sns.histplot(plots['backtoOriginal'], ax = ax[2])

plt.show()

"""### Data Split
hold-out validation: train data set을 valid/train으로 임의로 분리

"""

target = 'num_orders'
data = train[train[target].notna()]

train, val = train_test_split(data, test_size = 0.2, random_state = 2)
features = train.drop(columns = [target]).columns

X_test = test

X_train = train[features]
y_train = train[target]
X_val = val[features]
y_val = val[target]

"""*stratify = target을 쓸 수 없었던 이유가 무엇일까?*

참고: https://stackoverflow.com/questions/43179429/scikit-learn-error-the-least-populated-class-in-y-has-only-1-member
"""

X_train.shape, X_val.shape, y_train.shape, y_val.shape

"""k-fold cross validation"""

pipe = make_pipeline(
    TargetEncoder(min_samples_leaf=1, smoothing=1), 
    SimpleImputer(strategy='median'), 
    RandomForestRegressor(max_depth = 10, n_jobs=-1, random_state=2)
)

k = 3

scores = cross_val_score(pipe, X_train, y_train, cv=k, 
                         scoring='neg_mean_absolute_error')

print(f'MAE for {k} folds:', -scores)

-scores.mean(), scores.std()

"""###기준모델과 평가지표 설정

회귀모델이므로 baseline을 target의 평균으로 설정
"""

predict = train[target].mean()
predict

#훈련 에러
y_pred_train = [predict] * len(y_train)
MAE_train = mean_absolute_error(y_train, y_pred_train)
MAE_train

#검증 에러
y_pred_val = [predict] * len(y_val)
MAE_val = mean_absolute_error(y_val, y_pred_val)
MAE_val

"""### modeling

####(1) target encoding
"""

enc = TargetEncoder(min_samples_leaf=1, smoothing=1000) 
X_train_encoded = enc.fit_transform(X_train, y_train)
X_val_encoded = enc.fit_transform(X_val, y_val)

X_test_encoded = enc.transform(X_test)

"""####(2) 표준화 """

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train_encoded)
X_val_scaled = scaler.transform(X_val_encoded)
X_test_scaled = scaler.transform(X_test_encoded)

X_train_scaled, X_val_scaled, X_test_scaled

"""#### RF regression"""

pipe_RF_reg = make_pipeline(
    SimpleImputer(), 
    RandomForestRegressor(random_state = 2, n_jobs=-1, oob_score=True)
)

pipe_RF_reg.fit(X_train_scaled, y_train)
print('검증 정확도', pipe_RF_reg.score(X_val_scaled, y_val))

y_pred = pipe_RF_reg.predict(X_train_scaled)
MAE = mean_absolute_error(y_train, y_pred)
print(f'훈련 에러: {MAE:.2f}')

y_pred = pipe_RF_reg.predict(X_val_scaled)
MAE = mean_absolute_error(y_val, y_pred)
print(f'검증 에러: {MAE:.2f}')

"""### decision tree """

pipe_dc = make_pipeline(
    SimpleImputer(), 
    DecisionTreeRegressor()
)

pipe_dc.fit(X_train_scaled, y_train)
print('검증 정확도', pipe_dc.score(X_val_scaled, y_val))

y_pred = pipe_dc.predict(X_train_scaled)
MAE = mean_absolute_error(y_train, y_pred)
print(f'훈련 에러: {MAE:.2f}')

y_pred = pipe_dc.predict(X_val_scaled)
MAE = mean_absolute_error(y_val, y_pred)
print(f'검증 에러: {MAE:.2f}')

"""### Gradient boosting"""

pipe_gb = make_pipeline(
    SimpleImputer(), 
    XGBRegressor()
)

pipe_gb.fit(X_train_scaled, y_train)
print('검증 정확도', pipe_gb.score(X_val_scaled, y_val))

y_pred = pipe_gb.predict(X_train_scaled)
MAE = mean_absolute_error(y_train, y_pred)
print(f'훈련 에러: {MAE:.2f}')

y_pred = pipe_gb.predict(X_val_scaled)
MAE = mean_absolute_error(y_val, y_pred)
print(f'검증 에러: {MAE:.2f}')

"""### linear regression"""

pipe_lr = make_pipeline(
    TargetEncoder(), 
    SimpleImputer(), 
    LinearRegression(n_jobs=-1)
)
pipe_lr.fit(X_train_scaled, y_train)
print('검증세트 정확도', pipe_lr.score(X_val_scaled, y_val))

y_pred = pipe_lr.predict(X_train_scaled)
MAE = mean_absolute_error(y_train, y_pred)
print(f'훈련 에러: {MAE:.2f}')

y_pred = pipe_lr.predict(X_val_scaled)
MAE = mean_absolute_error(y_val, y_pred)
print(f'검증 에러: {MAE:.2f}')

"""### ridge Regression"""

pipe_ridge = make_pipeline(
    SimpleImputer(), 
    RidgeCV()
)

pipe_ridge.fit(X_train_scaled, y_train)
print('검증 정확도', pipe_ridge.score(X_val_scaled, y_val))

y_pred = pipe_ridge.predict(X_train_scaled)
MAE = mean_absolute_error(y_train, y_pred)
print(f'훈련 에러: {MAE:.2f}')

y_pred = pipe_ridge.predict(X_val_scaled)
MAE = mean_absolute_error(y_val, y_pred)
print(f'검증 에러: {MAE:.2f}')

"""### cf.TransformTargetRegressor

"""

tt = TransformedTargetRegressor(regressor=pipe_RF_reg,
                                func=np.log1p, inverse_func=np.expm1)

tt.fit(X_train_scaled, y_train)
tt.score(X_val_scaled, y_val)

y_pred5 = tt.predict(X_train_scaled)
MAE = mean_absolute_error(y_train, y_pred5)
MAE

"""###시각화

RF에 한정해 하이퍼파라미터를 조정
"""

param_distributions = { 
    'n_estimators': randint(50, 500), 
    'max_depth': [10, 15, 20], 
    'max_features': uniform(0, 1), 
}

search = RandomizedSearchCV(
    RandomForestRegressor(random_state=2), 
    param_distributions=param_distributions, 
    n_iter=3, 
    cv=3, 
    scoring='neg_mean_absolute_error', 
    verbose=10, 
    return_train_score=True, 
    n_jobs=-1, 
    random_state=2
)

search.fit(X_train_encoded, y_train);

print('최적 하이퍼파라미터: ', search.best_params_)
print('CV MAE: ', -search.best_score_)
model = search.best_estimator_

explainer = shap.Explainer(model)
shap_values = explainer.shap_values(X_train_encoded.iloc[:20])

shap.initjs()
shap.force_plot(
    base_value = explainer.expected_value,
    shap_values = shap_values,
    features = X_train
)

shap.initjs()
shap.force_plot(explainer.expected_value, shap_values[0,:], X_train_encoded.iloc[20,:])

shap.initjs()
shap.summary_plot(shap_values, X_train_encoded.iloc[:20], plot_type = "violin")

