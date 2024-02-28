###简介
使用python搭建的webUI自动化框架。

## 运行
cd testcases
#调度时使用
pytest -s -v 

#运行时使用
pytest -s -q --alluredir=allure-results 

#重试设置
pytest --reruns 3 
pytest --reruns 3 --reruns-delay 1 

#本地运行
brew install allure
allure serve allure-results  #这样就可以在本地生成报告了。
