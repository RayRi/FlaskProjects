#coding:utf8
"""
项目可安装化
项目可安装化是指创建一个项目 发行 文件，以使用项目可以安装到其他环境， 就像在你的项目中安装
 Flask 一样。这样可以使你的项目如同其他库一样进行部署， 可以使用标准的 Python 工具来管理项目。

可安装化还可以带来如下好处，这些好处在教程中可以不太明显或者初学者可能没 注意到：
1. Python 和 Flask 能够理解如何 recommendation 包，是因为你是在项目 文件夹中运行的。
    可安装化后，可以从任何地方导入项目并运行。
2. 可以和其他包一样管理项目的依赖，即使用 pip install yourproject.whl 来安装项目并安装相关依赖。
3. 测试工具可以分离测试环境和开发环境。


packages 告诉 Python 包所包括的文件夹（及其所包含的 Python 文件）。 
    find_packages() 自动找到这些文件夹，这样就不用手动写出来。 为了包含其他文件夹，如静态文件
    和模板文件所在的文件夹，需要设置 include_package_data 。 Python 还需要一个名为
     MANIFEST.in 文件来说明这些文件有哪些
"""
from setuptools import find_packages, setup

setup(name="recommenation", version="1.0.0", packages=find_packages(), \
    include_package_data=True, zip_sale=False, \
        install_requires=['flask', ])