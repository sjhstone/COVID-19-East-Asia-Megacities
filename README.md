# COVID-19 in East Asia Megacities

Online visualization is available at: https://sjhstone.github.io/covid/

This repository holds Python source code for processing and visualization COVID-19 data in East Asian megacities amid Omicron variant outbreak including Seoul (서울), Tokyo (東京), Osaka (大阪), Hong Kong (香港), Shanghai (上海) and Beijing (北京).

SARS-CoV-2 病毒 Omicron 变异株所造成的 COVID-19 疫情正在东亚的几座代表性城市蔓延，本代码仓库存放着一些用来进行简单数据处理与可视化的源代码。

You may also find links to official data sources of DPRK and Taiwan region [in the appendix below](#related-data-sources).

你也可以在[下方附录中](#related-data-sources)找到指向朝鲜民主主义人民共和国与中国台湾地区官方数据披露来源的链接。

## Data Scheme

### Omicron Wave in East Asian Megacities

https://sjhstone.github.io/covid/

The processed data has the following fields:
* date
* daily new cases (raw)
* daily new cases (7-day moving average)
* accumulated cases

The first day (indexed as day zero) in the processed data is set to be the day of initial disclosure of local Omicron case discovery.

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
Please follow the links in the table below. The links points to the data source URL in the source code file.

Note that data with note "parsed and processed" may deviate from the original official data source due to human-induced error.

| Geographical Coverage | Source Format | Notes |
|--|--|--|
| [Seoul](./DataAPI/Korea.py#L13), South Korea | JSON API | Native source |
| [Tokyo](./DataAPI/Japan.py#L11), Japan | JSON API | Native source |
| [Osaka](./DataAPI/Japan.py#L11), Japan | JSON API | Native source |
| [Hong Kong](./DataAPI/China.py#L13), China | JSON API | Native source |
| [Shanghai](./DataAPI/China.py#L52), China | [Manually maintained CSV file](./raw_data/shanghai.csv) | Parsed and processed |
| [Beijing](./DataAPI/China.py#L37), China | [Manually maintained CSV file](./raw_data/beijing.csv) | Parsed and processed |
| [Greater Taipei Area](./DataAPI/China.py#L80), China | Extracted from JS source | Parsed and processed |
| [Pyongyang](./DataAPI/Dprk.py#L14), North Korea | [Manually maintained CSV file](./raw_data/pyongyang.csv) | Parsed and processed |

## Appendix

### Keyword in Local Language
| Geographical Region | COVID-19 | Omicron variant |
|--|--|--|
| Sorth Korea | 코로나바이러스감염증-19 (코로나19) | 오미크론 변이 | 감염병 유행 |
| Japan | 新型コロナウイルス感染症 | オミクロン変異株 | 感染症の流行 |
| Hong Kong SAR, China | 2019冠狀病毒病 | Omicron變異株 | 疫情 |
| China (Mainland) | 新型冠状病毒肺炎 (新冠肺炎) | 奥密克戎变异株 | 疫情 |
