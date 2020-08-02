latex-homework-template-chinese
=======================

![Build LaTeX document](https://github.com/solidhtwoo/latex-homework-template-chinese/workflows/Build%20LaTeX%20document/badge.svg?branch=master)

这是一份我自用的LaTeX作业模板, 修改和汉化自
https://github.com/jdavis/latex-homework-template

## 特性

1. 标题页
2. 代码高亮
3. 可调的题号
4. 常用数学宏

## 依赖与注意事项

需要安装xelatex,Python3以及pygments包(安装方式自行搜索
推荐使用texlive的最新版本
需要开启 -shell-escape 参数

## 自动生成脚本

提供了一个Python3脚本(Windows/Linux)自动生成和填入个人信息和课程信息

```
python auto_gen.py -t "第一次作业" -s "占卜学" -d "t+1"
```


## 感谢

感谢英文版本原作者jdavis.


## 协议

This code is distributed under the MIT license. For more info, read the
[LICENSE](/LICENSE) file distributed with the source code.
