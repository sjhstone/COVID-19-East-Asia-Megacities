# COVID-19 in East Asian Megacities

This repository holds original code for processing and visualization COVID-19 data from East Asian megacities including 

## Dependencies
```
pip install -r requirements.txt
```
* [`requests`](https://github.com/psf/requests)
* [`pandas`](https://pandas.pydata.org/)
* [`matplotlib`](https://matplotlib.org/)

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
| [Shanghai](./DataAPI/China.py#L37) | Manually maintained CSV file |

## Preview
![daily cases vs accumulated cases in Shanghai](./doc/output_sample.svg)
