# 四位一体课表_数据源

针对四位一体课表，进行数据爬取与整理，导出数据文件。
是空闲教室查询系统的数据源支撑。

<h3 align="center">四位一体课表爬虫</h3>
  <p align="center">
    支持公网环境下部署，异步并发爬取数据并整理导出数据文件
    <br />
    <a href="https://github.com/cicidoll/QueryPpsucClassRoomSpider"><strong>项目链接 »</strong></a>
    <br />
    <br />
    <a href="https://github.com/cicidoll/QueryPpsucClassRoomSpider">查看Demo</a>
    ·
    <a href="https://github.com/cicidoll/QueryPpsucClassRoomSpider/issues">报告Bug</a>
    ·
    <a href="https://github.com/cicidoll/QueryPpsucClassRoomSpider/issues">提出新特性</a>
  </p>

</p>

具体逻辑都写在注释里。

## 目录

- [四位一体课表_数据源](#四位一体课表_数据源)
  - [目录](#目录)
    - [上手指南](#上手指南)
          - [开发前的配置要求](#开发前的配置要求)
          - [**安装步骤**](#安装步骤)
    - [文件目录说明](#文件目录说明)
    - [版本控制](#版本控制)
    - [原作者](#原作者)
    - [使用docker部署服务](#使用docker部署服务)
    - [接口格式](#接口格式)
    - [TODO](#todo)

### 上手指南

###### 开发前的配置要求

1. Python3.9+
2. 需要的包依赖：
   interval==1.0.0
   requests==2.26.0
   lxml==4.6.3
   selenium==3.141.0
   （此处selenium使用的是Chrome）

###### **安装步骤**

1. 安装上述所需包依赖
2. Clone the repo
3. 配置根目录下user.json中的username和password为自己的vpn登录账号密码。

```sh
git clone https://github.com/cicidoll/QueryPpsucClassRoomSpider.git
```

### 文件目录说明

```
filetree 
├── /data/
│  ├── classRoomData.json
│  └── mobilizeBorrow.json
├── /config/
│  ├── classRoomNumConfig.json
│  ├── createUrlDic.json
│  ├── dataTemplate.json
│  ├── mobilizeBorrowTemplate.json
│  └── requestConfig.json
├── /networkAppClass/
│  ├── __init__.py
│  ├── create_url_pool.py
│  ├── get_html.py
│  ├── get_urldata.py
│  ├── get_week.py
│  ├── login.py
│  └── process_text.py
├── .gitignore
├── main.py
├── README.md
├── requirements.txt
├── user.json
└── utils.py

```

### 版本控制

该项目使用Git进行版本管理。您可以在repository参看当前可用版本。

### 原作者

17M053

联系方式：ayaseemt@qq.com


### 使用docker部署服务

新的特性：使用sanic封装了接口，并且使用了docker进行部署，部署步骤如下：

在根目录下输入依次输入如下两条命令，耐心等待：

```plaintext
docker build -t classroomspider .
docker run --name ppsucClassRoomSpider -p 8000:8000 -d classroomspider
```
（这里docker容器的名字随便取就行，镜像的名字有不能大写的要求，满足这个要求后也可以随便取）
然后就可以访问8000端口获取服务


### 接口格式

 - 获取所有数据：

``http://localhost:8000/``

 - 获取课程数据：

``http://localhost:8000/detail/Class?bd=建筑名&t=时间段&dt=星期``

 - 获取换课数据：

``http://localhost:8000/detail/mobilize?bd=建筑名&rm=教室``

 - 获取借教室数据：

``http://localhost:8000/detail/borrow?bd=建筑名&rm=教室``

其中：建筑名包含：``tj zj zl xp``，时间段包含：``am12 am34 pm12 pm34``，星期包含``1 2 3 4 5``

对于不同的楼教室名称不同，一般就使用数字表示即可。特别的，团结的教室为：``tj1``（团阶一）、``tj2``（团阶二）...``tj8``（团阶八）、``tj9``（团报告厅）

 - Example

| url                                                        | 含义              |
|------------------------------------------------------------|-----------------|
| http://localhost:8000/                                     | 获取所有数据          |
| http://localhost:8000/detail/Class?bd=tj&t=am34&dt=3  | 获取tj星期1上午12节的课程数据 |
| http://localhost:8000/detail/mobilize?bd=tj&rm=tj9  | 获取tj楼团报告厅教室的换课数据 |
| http://localhost:8000/detail/borrow?bd=zj&rm=202  | 获取zj楼202教室的借教室数据 |

### TODO

 - 更新数据的方式确实很奇怪
 - 借教室的数据没有整合