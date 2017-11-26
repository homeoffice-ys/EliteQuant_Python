# EliteQuant_Python
Python quantitative trading and investment platform

* [Platform Introduction](#platform-introduction)
* [Project Summary](#project-summary)
* [Participation](#participation)
* [Installation](#installation)
* [Development Environment](#development-environment)
* [Architecture Diagram](#architecture-diagram)
* [Todo List](#todo-list)

---

## Platform Introduction

EliteQuant is an open source forever free unified quant trading platform built by quant traders, for quant traders. It is dual listed on both [github](https://github.com/EliteQuant) and [gitee](https://gitee.com/EliteQuant).

The word unified carries two features.
- First it’s unified across backtesting and live trading. Just switch the data source to play with real money.
- Second it’s consistent across platforms written in their native langugages. It becomes easy to communicate with peer traders on strategies, ideas, and replicate performances, sparing language details.

Related projects include
- [A list of online resources on quantitative modeling, trading, and investment](https://github.com/EliteQuant/EliteQuant)
- [C++](https://github.com/EliteQuant/EliteQuant_Cpp)
- [Python](https://github.com/EliteQuant/EliteQuant_Python)
- [Matlab](https://github.com/EliteQuant/EliteQuant_Matlab)
- [R]()
- [C#]()
- [Excel](https://github.com/EliteQuant/EliteQuant_Excel)
- [Java]()
- [Scala]()
- [Go]()
- [Julia]()

## Project Summary

EliteQuant_Python is Python3 based multi-threading, concurrent high-frequency trading platform that provides consistent backtest and live trading solutions. It follows modern design patterns such as event-driven, server/client architect, and loosely-coupled robust distributed system. It follows the same structure and performance metrix as other EliteQuant product line, which makes it easier to share with traders using other languages.

## Participation

Please feel free to report issues, fork the branch, and create pull requests. Any kind of contributions are welcomed and appreciated. Through shared code architecture, it also helps traders using other languges.

## Installation

No installation is needed, it's ready for use out of box. Just download the code and enjoy. 

### Backtest

Configure config_backtest.yaml in the source directory

* ticker: ticker names that are of interest to you
* datasource: historical data source
* hist_dir: local history data directory
* output_dir: output test results directory

Currently it supports data source from

* Quandl
* Tushare
* Local CSV

Then run backtest_engine.py for backtesting

## Live Trading

 Configure source/config.yaml
 
1. If you want to use interactive broker, open IB trader workstation (TWS), go to its menu File/Global Configuration/API/Settings, check "Enable ActiveX and Socket Client", uncheck "Read-Only API"
2. In the config file, change the account id to yours; IB account id usually can be found on the top right of the TWS window.
3. If you use CTP, change your brokerage account information and ctp addresses accordingly.
4. create folder for log_dir and data_dir respectively. The former records runtime logs, while the later saves tick data.
5. run live_engine.py

**Interactive Brokers**
is the most popular broker among retail traders. A lot of retail trading platform such as quantopian, quantconnect are built to support IB. If you don't have IB account but want to try it out, they provide demo account edemo with password demouser. Just download TWS trader workstation and log in with this demo account. Note that accound id changes everytime you log on to TWS with demo account so you have to change EliteQuant config file accordingly.

**CTP**
is the de-facto brokerage for Chinese futures market, including commodity futures and financial futures. They also offer free demo account [SimNow](http://simnow.com.cn/). After registration, you will get account, password, brokerid, along with market data and trading broker address. Replace them in EliteQuant config file accordingly.


## Development Environment

Below is the environment we are using
* Anaconda Python 3.6
* PyCharm Community version 2017.2.4

## Architecture Diagram

Backtest

![Backtest](/resource/Backtest_Diagram.PNG?raw=true "Backtest")

Live Trading

![Live Trading](/resource/Live_Trading_Diagram.PNG?raw=true "Live Trading")

Code Structure

![Code Structure](/resource/code_structure_en.PNG?raw=true "Code Structure")

## Todo List