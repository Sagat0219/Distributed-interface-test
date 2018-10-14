# Distributed-interface-test

本套自动化接口测试框架是利用scrapy爬虫框架来实现的。  
可将整个项目文件夹（xlstest-Distributed）部署到scrapyd服务程序中，通过schedule.json调度运行：  
`curl http://127.0.0.1:6800/schedule.json -d project=xlstest -d spider=httpbin`  

**推荐的用法是部署到docker容器中，通过本地安装Gerapy进行分布式管理**  
## 架构图  
![Image text](https://github.com/Sagat0219/Distributed-interface-test/blob/master/frame.jpg)  

## 本地安装：  
**Docker**  
**Redis**  
**Gerapy**  
> PS: redis记得要设置允许远程访问。  
> 设置文件在：C:\Program Files\Redis\redis.windows-service.conf  
`# bind 127.0.0.1 -- 注释掉`  
`protected-mode no --设置为 no,表明不已保护模式运行`  

## 容器要求：
已安装python3.6及相关第三方库（xlrd，prettytable，setuptools，Scrapy）  
或可直接使用我创建的镜像来生成容器：  
`docker pull sagat0219/scrapyd`  
`docker run -d -p 6800:6800 sagat0219/scrapyd:v1 scrapyd`  

## 关于测试用例：  
位置在 ~\xlstest-Distributed\xlstest\case\test.xlsx  
样本中测试用例主要为GET和POST请求，每行即一条用例。通过框架会导入到redis队列中被调度执行。  
  
因为使用gerapy打包成egg时不会自动包含用例文件，所以需要对gerapy中的打包脚本（build.py）做修改：  
假设文件安装位置在 C:\Program Files\Python36\Lib\site-packages\gerapy\server\core\build.py  
原文件中的相关代码为：
```python
_SETUP_PY_TEMPLATE = \
        """# Automatically created by: gerapy
    from setuptools import setup, find_packages
    setup(
        name='%(project)s',
        version='1.0',
        packages=find_packages(),
        entry_points={'scrapy':['settings=%(settings)s']},
    )"""
```
修改为对其添加一行：
```python
_SETUP_PY_TEMPLATE = \
    """# Automatically created by: gerapy
from setuptools import setup, find_packages
setup(
    name='%(project)s',
    version='1.0',
    packages = find_packages(),
    package_data = {'':['case/*.xlsx']},
    entry_points = {'scrapy':['settings=%(settings)s']},
)"""
```
## Gerapy使用方法：
将整个xlstest-Distributed文件夹拷贝到Gerapy的projects文件夹下(~\gerapy\projects)  
通过浏览器访问Gerapy(http://127.0.0.1:8000/)  
在“项目管理”中进行打包并部署到指定的主机（主机即是docker容器）  
然后就可以在“主机管理”选择对应的主机点击“运行”来执行调度了。  

### 相关截图  
> *项目管理*  
![Image text](https://github.com/Sagat0219/Distributed-interface-test/blob/master/ss1.png)  
> *项目打包和部署*  
![Image text](https://github.com/Sagat0219/Distributed-interface-test/blob/master/ss2.png)  
> *主机管理*  
![Image text](https://github.com/Sagat0219/Distributed-interface-test/blob/master/ss3.png)  
> *任务调度运行*  
![Image text](https://github.com/Sagat0219/Distributed-interface-test/blob/master/ss4.png)  
> *执行完后的日志查看*  
![Image text](https://github.com/Sagat0219/Distributed-interface-test/blob/master/ss5-log.png)    
