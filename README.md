# 🍽️ meal needs prediction project 
배달식 수요를 예측하는 머신러닝 모델 구축 프로젝트


### 프로젝트 개요
(기획의 배경 및 의도 들어갈 자리) 

- 가설: '각 서비스센터별로 배달이 가능한 거리와 주문된 식수 간에는 양의 상관관계가 있을 것'
- 프로젝트의 목표: **배달식 수요를 예측**하고 **배달식 수요에 영향을 끼치는 요인**을 특정

### 파일 설명
- **code.ipynb** 분석을 위해 작성한 전체 코드(`google colab`에서 작업)
- **presentation.pdf** 프레젠테이션을 위해 제작한 ppt의 pdf 버전
- **model.pkl** 부호화한 모델(복호화 테스트 완료)

>💭 **작업환경** `google colab`
>
>📅 **진행기간** 1차 21.11.06 ~ 21.11.12 수정 22.08.00~

### 문제해결 과정
데이터 세트 정제 및 특성공학 적용 → 기준모델, 평가지표 설정 → 시각화를 기반으로 해석
- 145주간 누적된 배달식 데이터(주간 수요, 서비스센터별 정보, 제공되는 배달식 유형)를 분석
- 모델 설정: 선형/릿지 회귀, 의사결정나무, 랜덤포레스트, 그래디언트 부스팅의 4개 회귀 모델
- 평가 지표: MAE, Rsquare

### 데이터 세트의 특징

- 출처: [Meal delivery company](https://www.kaggle.com/datasets/ghoshsaptarshi/av-genpact-hack-dec2018?select=fulfilment_center_info.csv), SAPTARSHI GHOSH, Kaggle
- 구성: train.csv, fulfillment_center_info.csv, meal_info.csv 
  - train.csv: 주문 식별넘버, 주(week), 센터 식별넘버, 식사 식별넘버, 최종 결제금액, 기본 결제금액, 프로모션 대상 여부, 홈페이지 추천 여부, 주문수
  - fulfillment_center_info.csv: 센터 식별넘버, 각 도시와 지역의 고유 코드, 센터의 종류, 배달 가능 거리 
  - meal_info.csv : 식사 식별넘버, 식사 종류, 요리 종류
  

※데이터 세트 전처리 과정: 3종의 .csv 파일을 통합
그 외 결측치 제거, 대소문자 통일 등 기본적인 전처리 완료 

### 결과 요약

- 가설: 검증되었는지?
- 목표: 달성되었는지?
- 그 밖에 기대하지 않았던 인사이트가 있었다면?

### 한계점과 보완 방안
- 해결하지 못한 문제: 

#### 한계
- 
- 데이터 불균형과 이상치
- 하이퍼파라미터 튜닝

#### 보완방안
- 



### Update

- (2022.07.28~) 프로젝트 소개문 재작성

