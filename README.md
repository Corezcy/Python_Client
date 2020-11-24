## **Python Client for Simulator**

针对`LGSVL Simulator`的`Python API`。



## 环境要求

`Python` >=3.5



## 安装运行

**step.1**

在`release`中下载`Python_Client_v0.0.1`，解压，进入当前文件夹

**step.2**

下载所使用`python`库：

```shell
pip3 install --user .
```

>    ps. install in development mode
>
>    ```shell
>    pip3 install --user -e .
>    ```

**step.3**

修改`config.yaml`中的配置信息（配置介绍见**配置说明**）

**step.4**

开始运行（默认仿真时间50）

```
./main.par
```

用户可修改仿真时间（例如，30s）

```shell
./main --t=30
```



## 编译(可选)

**step.1**

进入当前文件夹

**step.2**

```shell
pip3 install --user .
```

>    ps. install in development mode
>
>    ```shell
>    pip3 install --user -e .
>    ```

**step.3**

bazel编译

```shell
bazel build //gui:main
```

bazel运行（默认仿真时间50）

```shell
bazel-bin/gui/main
```

用户可修改仿真时间（例如，30s）

```shell
bazel-bin/gui/main --t=30
```



## 文件结构

```
.
├── BUILD																			#BUILD
├── LICENSE					
├── README.md
├── WORKSPACE																	#WORKSPACE
├── config.yaml																#配置文件
├── gui																				#Python Client程序
│   ├── BUILD
│   ├── check_report.py												#3.检测报告模块
│   ├── choose_the_scene.py										#1.选择场景模块
│   ├── json																	#场景文件夹(json)
│   ├── log																		#日志文件夹
│   ├── logger.py															#日志处理类(封装了logger类)
│   ├── main.py																#main
│   ├── report																#报告文件夹
│   ├── scenario_run.py												#SimConnection类，模拟器链接类，定义了__enter__和__exit__
│   └── start_simulation.py										#2.仿真程序的入口						
├── lgsvl																			#lg API入口
│   ├── BUILD
│   ├── agent.py
│   ├── controllable.py
│   ├── dreamview.py
│   ├── geometry.py
│   ├── remote.py
│   ├── sensor.py
│   ├── simulator.py
│   └── utils.py
├── requirements.txt													#需要使用的python库
└── setup.py																	#安装文件
```



## 配置说明

在 `config.yaml`中，配置如下：

```yaml
configuration:
    MongoDB:
        #数据库名
        database: "mydb"
        #集合名
        collection: "test"
        #存储MongoDB数据库的服务器IP
        host: "10.78.7.62"
        #端口，默认27017
        port: 27017
    Simulation:
        #lg host 或者 proxy host
        host: "192.168.2.2"
        #lg port 或者 proxy port
        port: 9193
        #apollo host
        apollo_host: "10.78.4.163"
        #apollo port
        apollo_port: 9090
```





## 使用说明

### 1. Welcome to Python Client：

```
*---------Welcome to Python Client!----------*
|                 --Menu--                   |
|              1.Choose the Scene            |
|              2.Start Simulation            |
|              3.Check Report                |
|              4.Exit                        |
*--------------------------------------------*
Please enter your option :
```



### 2. Choose the Scene：

```
*---------Welcome to Python Client!----------*
|                 --Menu--                   |
|              1.Choose the Scene            |
|              2.Start Simulation            |
|              3.Check Report                |
|              4.Exit                        |
*--------------------------------------------*

Please enter your option :1

1.Check all the scenes[ default ]
2.Search scenes by keywords
Please enter your option : 
```

`1`选项检索所有场景，`2`选项按照关键字检索

#### 2.1.Check all the scenes：

```
Here are scenes : 
*--------------------------------------------*
                01.haha
                02.mongo
                03.Compass
                04.Window
                05.View
*--------------------------------------------*
Please choose the scene number (input 'all' to download all scenes):
```

输入`1`，下载`1`号场景到本地`./json`下；输入`all`，下载所有场景到本地`./json`下。

输入`1`后，显示如下：

```
The scene [ 01.haha ] is choosed
The scene [ 01.haha ] is saved in /Users/core/Desktop/python_Client/json/01.haha.json
```

界面再次跳转到菜单界面：

```
*---------Welcome to Python Client!----------*
|                 --Menu--                   |
|              1.Choose the Scene            |
|              2.Start Simulation            |
|              3.Check Report                |
|              4.Exit                        |
*--------------------------------------------*
Please enter your option :
```

#### 2.2. Search scenes by keywords:

提示信息如下：

```
Note: Searching scene name according to regular expression rules
Please enter key word :
```

输入关键字`mon`后检索如下：

```
Here is(are) scene(s) according to rules : 
*--------------------------------------------*
                1. 02.mongo
*--------------------------------------------*
Please choose the scene number (input 'all' to download all scenes): 
```

输入`1`后，下载场景，显示如下：

```
Please choose the scene number (input 'all' to download all scenes): 1
The scene [ 02.mongo ] is choosed
The scene [ 02.mongo ] is saved in /Users/core/Desktop/python_Client/json/02.mongo.json
```



### 3. Start Simulation

#### 3.1. Simulating the scene choosed in step.1

输入`2`，开始仿真（选择场景时已经默认保存了待仿真场景的路径）

> ps，如果第一步选择下载所有场景，第二步不会保存待仿真场景的路径，只能仿真所有的场景

开始仿真后，界面如下：

```
*---------       Simulation        ----------*
1.Simulating the scene choosed in step.1[ default ]
2.Simulating all scenes in /json ?
Please enter your option : 
Please enter simulation times：1
ps. r(un),s(top)
simulation num: 1
```

> `Please enter your option`直接回车默认选择第一项；
>
> `Please enter simulation times`，选择仿真次数；
>
> 仿真开始后，按`s`开启暂停，按`r`继续运行。

运行结果如下所示：

```
current scene: BorregasAve
srsrsr(r(un),s(top))
50.562045097351074s reached,simulation finished,test report is generating
```

#### 3.2. Simulating all scenes in /json

```
*---------Welcome to Python Client!----------*
|                 --Menu--                   |
|              1.Choose the Scene            |
|              2.Start Simulation            |
|              3.Check Report                |
|              4.Exit                        |
*--------------------------------------------*

Please enter your option :2

*---------       Simulation        ----------*
1.Simulating the scene choosed in step.1[ default ]
2.Simulating all scenes in /json ?
Please enter your option : 2
```

显示内容：

```
filenum : 5
./json/05.View.json
./json/02.mongo.json
./json/04.Window.json
./json/01.haha.json
./json/03.Compass.json
Start simulating all scenes !
current scene: BorregasAve
simulation finished,please check the test report
current scene: BorregasAve
50.44996213912964s reached,simulation finished,test report is generating
current scene: BorregasAve
50.036195039749146s reached,simulation finished,test report is generating
current scene: BorregasAve
50.54975605010986s reached,simulation finished,test report is generating
current scene: BorregasAve
50.26683592796326s reached,simulation finished,test report is generating
```

> 第一次仿真结果和其他四次不同，因为中间暂停了仿真。
>
> 报告按照执行顺序保存在`./report`目录下



### 4. Check Report

输入`3`查看报告，显示如下：

```
*---------        Checking         ----------*
filenum : 14
1. ./report/report_01.haha_2020-10-28_14:00:32.txt
2. ./report/report_01.haha_2020-10-28_14:12:31.txt
3. ./report/report_05.View_2020-10-28_13:55:21.txt
4. ./report/report_04.Window_2020-10-28_13:59:38.txt
5. ./report/report_01.haha_2020-10-28_14:11:14.txt
6. ./report/report_01.haha_2020-10-28_13:57:31.txt
7. ./report/report_02.mongo_2020-10-28_13:58:45.txt
8. ./report/report_03.Compass_2020-10-28_13:57:37.txt
9. ./report/report_05.View_2020-10-28_13:57:52.txt
10. ./report/report_01.haha_2020-10-28_13:52:39.txt
11. ./report/report_01.haha_2020-10-28_14:08:29.txt
12. ./report/report_03.Compass_2020-10-28_14:01:26.txt
13. ./report/report_02.mongo_2020-10-28_13:56:14.txt
14. ./report/report_04.Window_2020-10-28_13:57:08.txt
```

输入序号，在终端查看相应报告。报告在`./report`目录下，命名格式`report_02.mongo_2020-10-28_13:56:14`（根据场景名、时间命名）。报告内容如下：

```
 *--------------------------------------------------------------------------------------                                                     
 *             scenario name:./report/report_02.mongo_2020-10-28_13:56:14.txt                         

 *             simulation result:['FAIL']                     

 *             destination reached:[]                   

 *             collsion:[]                              

 *             over speed:[]                            

 *             brake light:[]                           

 *             sim time:50.32158589363098                              

 *             stop position:Vector(6.73277568817139, -2.21925330162048, -25.1717529296875)                         

 *                                                      
 *--------------------------------------------------------------------------------------
```



### 5. Exit

返回主界面，输入`4`退出：

```
---------Welcome to Python Client!----------*
|                 --Menu--                   |
|              1.Choose the Scene            |
|              2.Start Simulation            |
|              3.Check Report                |
|              4.Exit                        |
*--------------------------------------------*

Please enter your option :4

bye
```

