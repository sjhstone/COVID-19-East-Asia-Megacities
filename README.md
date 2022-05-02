# COVID-19 in East Asian Megacities

This repository holds Python source code for processing and visualization COVID-19 data in East Asian megacities amid Omicron variant outbreak including Seoul (서울), Tokyo (東京), Osaka (大阪), Hong Kong (香港) and Shanghai (上海).

Omicron 毒株造成的 COVID-19 疫情正在东亚的几座代表性城市蔓延，本代码仓库存放着一些用来进行简单数据处理与可视化的源代码。

## Data Scheme

### Omicron Wave in 5 Cities

https://sjhstone.github.io/covid/

The processed data has the following fields:
* date
* daily new cases (raw)
* daily new cases (7-day moving average)
* accumulated cases

The first day in the processed data is set to be the day of initial local Omicron case discovery.

The processed data can be found in [`data`](./data/) folder as CSV files.

### Shanghai District-wise Data
（上海市按各行政区疫情公开统计数据）

https://sjhstone.github.io/covid/districts/

[处理前的原始数据](./raw_data/shanghai_districts.csv)包含各区自2022年2月26日起的每日实际新增感染者（即确诊病例+无症状感染者-由无症状感染者转为确诊）人数。

[处理后的数据](./data/shanghai_by_district.csv)有如下数据列：
* 日期
* 各区新增 (原始数据)
* 各区新增 (7日移动平均)
* 各区累计确诊
为了避免对数—对数坐标下数据点值为0导致的问题，处理后的数据自2022年3月27日，即浦东浦南崇明封控前一天开始。

数据均以CSV逗号分隔表格文件格式表示。

## Preview
![daily cases vs accumulated cases in Shanghai](./doc/output_sample.svg)

## Dependencies
* [`requests`](https://github.com/psf/requests)
* [`pandas`](https://pandas.pydata.org/)
* [`matplotlib`](https://matplotlib.org/)
```
pip install -r requirements.txt
```

## Usage
Data can be updated by running [collect_data.py](./collect_data.py)

To make plots, please refer to [the example iPython notebook](./example.ipynb).

## Data Sources
| City | Notes | 
|--|--|
| [Seoul](./DataAPI/Korea.py#L13) | JSON API |
| [Tokyo](./DataAPI/Japan.py#L11) | JSON API |
| [Osaka](./DataAPI/Japan.py#L11) | JSON API |
| [Hong Kong](./DataAPI/China.py#L13) | JSON API |
| [Shanghai](./DataAPI/China.py#L52) | [Manually maintained CSV file](./raw_data/shanghai.csv) |
| [Beijing](./DataAPI/China.py#L37) | [Manually maintained CSV file](./raw_data/beijing.csv) |

## Appendix

### Keyword in Local Language
| Region | COVID-19 | Omicron variant |
|--|--|--|
| Korea | 코로나바이러스감염증-19 (코로나19) | 오미크론 변이 | 감염병 유행 |
| Japan | 新型コロナウイルス感染症 | オミクロン変異株 | 感染症の流行 |
| Hong Kong SAR, China | 2019冠狀病毒病 | Omicron變異株 | 疫情 |
| China (Mainland) | 新型冠状病毒肺炎 (新冠肺炎) | 奥密克戎变异株 | 疫情 |
