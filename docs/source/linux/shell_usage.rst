
.. _shell_usage:

##########################################
常用的shell命令详解
##########################################

Shell字符串截取
================

语法：
::
   
   ${string: start :length}

.. csv-table:: 字符截取使用方法
 :header: "格式", "说明"
 :widths: 15, 50

 ${string: start :length},从 string 字符串的左边第 start 个字符开始向右截取 length 个字符。
 ${string: start},从 string 字符串的左边第 start 个字符开始截取，直到最后。
 ${string: 0-start :length},从 string 字符串的右边第 start 个字符开始，向右截取 length 个字符。
 ${string: 0-start},从 string 字符串的右边第 start 个字符开始截取，直到最后。
 ${string#*chars},从 string 字符串第一次出现 chars 的位置开始，截取 chars 右边的所有字符。
 ${string##*chars},从 string 字符串最后一次出现 chars 的位置开始，截取 chars 右边的所有字符。
 ${string%chars*},从 string 字符串最后一次出现 chars 的位置开始，截取 chars 左边的所有字符。
 ${string%%chars*},从 string 字符串第一次出现 chars 的位置开始，截取 chars 左边的所有字符。

set用法
========

语法:
::

   set [-可选参数] [-o 选项]



shell中的变量符号
=================
.. csv-table:: shell中的变量符号
 :header: "格式", "说明"
 :widths: 15, 50

 $#, 是传给脚本的参数个数
 $0, 是脚本本身的名字
 $1, 是传递给该shell脚本的第一个参数
 $2, 是传递给该shell脚本的第二个参数
 $@, 是传给脚本的所有参数的列表
 $*, 是以一个单字符串显示所有向脚本传递的参数，与位置变量不同，参数可超过9个
 $$, 是脚本运行的当前进程ID号
 $?, 是显示最后命令的退出状态，0表示没有错误，其他表示有错误
