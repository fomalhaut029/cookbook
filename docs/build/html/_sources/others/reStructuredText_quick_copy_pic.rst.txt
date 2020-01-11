##################################
reStructuredText 实现粘贴图片
##################################

在使用用reStructuredText写作的时候经常要插入图片，我们一般的操作是：

1. 截图
2. 保存图片
3. 在文档中引用图片 比如 ``.. figure:: /_static/images/20191101_151415.png``

这样总是很麻烦,通过度娘。找到有人在使用  **markdown** 工具的使用也有相同的困扰 
`参考  <https://github.com/wanglong001/ClipMd>`_

根据这个我做了一点修改。可以轻松支持reStructuredText 的相关操作，修改如下：

.. figure:: /_static/images/20191101_153336.png

修改后的效果如下：

.. figure:: /_static/images/20191101_154016.png






