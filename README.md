# 🍽️ 배달식 수요를 예측하는 머신러닝 모델 구축 프로젝트

<br>

>💭 **작업환경** `google colab`
>
>📅 **진행기간** 1차 21.11.06 ~ 21.11.12 수정 22.08.31

<br>

### 프로젝트 개요
🍿 코로나19 이후 크게 성장한 한국 내 배달음식 시장(* 2020.02. 1조1천353억원 →  2022.02. 2조2천443억원).<br>
만약 배달식 수요에 영향을 끼치는 여러 요인을 토대로 앞으로의 식수를 예측할 수 있다면?

버려지는 식재료를 줄이고, 합리적인 마케팅 전략을 수립할 수 있을 것이라는 판단 하에 캐글에 공개된 해외 배달식 수요 데이터를 바탕으로 식수를 예측하는 머신러닝 모델을 만들어 보고자 함.
<br><br>
  
- 프로젝트의 목표
  - **배달식 수요**에 **가장 큰 영향을 끼치는 요인**을 특정
  - **배달식 수요**를 **예측**하는 머신러닝 모델 구축
  

<br>

### 파일 설명
- **code_meal_prediction.ipynb** 분석을 위해 작성한 전체 코드(`google colab`에서 작업)
- **presentation.pdf** 프레젠테이션을 위해 제작한 ppt의 pdf 버전

<br>

### 결과 요약


![image](https://user-images.githubusercontent.com/90163856/186164677-df254650-dcad-441b-b3c7-294edde09f66.png)

→ 식료품의 분류(category)가 주문식수에 가장 큰 음의 영향을, 음식 종류(cuisine)가 가장 큰 양의 영향을 끼치고 있음을 확인할 수 있었음

---

### 데이터 세트의 특징

- 출처: [Meal delivery company](https://www.kaggle.com/datasets/ghoshsaptarshi/av-genpact-hack-dec2018?select=fulfilment_center_info.csv), SAPTARSHI GHOSH, Kaggle
- 구성: train.csv, test.csv, fulfillment_center_info.csv, meal_info.csv 
  - **train.csv / test.csv**: 주문 식별넘버, 주(week), 센터 식별넘버, 식사 식별넘버, 최종 결제금액, 기본 결제금액, 프로모션 대상 여부, 홈페이지 추천 여부, 주문수<br>
  (검증 데이터 32573건, 훈련 데이터 456548건)
  - **fulfillment_center_info.csv**: 센터 식별넘버, 각 도시와 지역의 고유 코드, 센터의 종류, 배달 가능 거리 
  - **meal_info.csv** : 식사 식별넘버, 식사 종류, 요리 종류
  
  ※데이터 세트 전처리 과정: train/test set와 fulfillment_center_info.csv, meal_info.csv 파일을 병합<br>
    할인 여부, 최종가-기본가 간의 차액 칼럼 추가(특성공학)<br>
    주문량의 극단적 우편향을 해결하고자 **상위 5% 주문량 제거** 후 **로그를 취함**
    
    ![image](https://user-images.githubusercontent.com/90163856/186162509-84671bf6-2e02-478a-ae3e-4ba05aa9f3e0.png)

    그 외 결측치 제거, 대소문자 통일 등 기본적인 전처리 완료

<br>

### 문제해결 과정
- **145주간 누적된 배달식 데이터**(주간 수요, 서비스센터별 정보, 제공되는 배달식 유형)를 분석
- 주 사용 라이브러리: scikitlearn, 
- 모델 설정
  - 예측: 선형/릿지 회귀, 의사결정나무, 랜덤포레스트, 그래디언트 부스팅의 4개 회귀 모델(sklearn 활용)
  - 시각화: seaborn, pyplot, shap 
- 평가 지표: MAE, Rsquare

1. 기준모델과 평가지표 설정 
**훈련 에러** `150.13046297451018` 
**검증 에러** `149.9609293712721` 

#### 시각화 결과 

![image](https://user-images.githubusercontent.com/90163856/186163606-48f4183d-3dd9-41f5-817d-a6a82d3c87f3.png)



<br>

### 한계점과 보완 방안
#### 한계
- **데이터상의 한계**
    - 국내가 아닌 외국 데이터로 분석을 진행 → 해당 요인이 한국 배달 시장에서도 식수요에 동등하게 적용되는지 알 수 없음
    - 불균형과 이상치가 많아 절삭 및 로짓변환을 진행하였으나 여전히 상당한 우편향을 보임
- **모델상의 한계** 
    - Google colab의 메모리 한계로 세세한 하이퍼파라미터 튜닝을 진행하지 못함

#### 보완방안
- **국내 배달식 수요 데이터**를 확보하여 모델링 
- Google colab 이상의 고성능 컴퓨팅 자원을 활용하여 hyper-parameter 재설정 

#### 참고한 자료 
- [2021년 음식배달 시장 규모, 어떻게든 알아본 썰](https://contents.premium.naver.com/connectx/us/contents/220214173319668hn), 하진우, 네이버 커넥터스 프리미엄
- ['코로나 펜데믹 2년간 배달음식 시장 규모 2배 커져'](http://news.imaeil.com/page/view/2022040115442137996), 채정민 기자, 매일신문



---

### Update

- (2022.08.23 ~ 2022.09.19) 프로젝트 소개문 재작성

