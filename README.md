# Moodle习题gifg格式批量转换工具

## 介绍
Giften是一个批量将试题转换为gift格式的工具，支持功能：

* 批量转换多道习题
* 输出为gift格式，可直接导入moodle平台
* 支持单选题、多选题、判断题三种题型
* 支持html标签
* c语言等其它高级语言程序的题目，能保留原有换行和缩进
* 不支持图片

## 用法

### 准备试题

本工具输入为txt格式的试题文件，因此需要将word试题转换为txt格式。

你将word文档格式的试题另存为txt格式，编码选择Unicode(utf-8)。

也可以直接复制word文档内所有内容，然后新建一个txt文件，粘贴后保存即可，注意，保存时要选择编码格式为utf-8

### 开始转换

#### 方法一

将试题拷贝到docs目录，然后打开命令行，进入程序根目录，输入：

```python
python .\run.py
```
docs目录下的所有txt文件都会被转换为gift文件，各自转换后的gift文件保存在gift文件夹里面，文件名为 x.gift.txt

#### 方法二

打开命令行，进入程序根目录，输入：

```python
python .\run.py docs\a.txt docs\b.txt
```
docs文件夹下的a.txt、b.txt文件将会被转换为a.gift.txt、b.gift.txt文件，保存在gift文件夹中。

## 试题文件格式

试题模板见：docs\sample.txt

```txt

Category:题目名称(如果分级的话，级别之间用/隔开）

选择题
1、题干(A)
A、选项
B、选项
C、...
D、...
{Explanation:}题目解析内容.如果没有注释，则去掉该部分

多选题
1、题干(ABC)
A、选项
B、选项
C、...
D、...
E、...

判断题
1、题干(答案)
{Explanation:}题目解析内容，注意判断题答案A表示True，B表示False

Category:题目名称(如果分级的话，级别之间用/隔开）

选择题
...

多选题
...

判断题
...

```

**注意:** Explanation:里的冒号是半角冒号。
