
# 功能介绍

基于PyQt5开发的位图工具生成器

- 依赖Python3.7环境
- 依赖Pycharm开发工具
- 依赖Qt Designer

下图为工具界面效果展示


![image](https://github.com/KingSun5/font_creator/blob/main/assets/git_img/img_1.png)

--------------

# 使用介绍

![image](https://github.com/KingSun5/font_creator/blob/main/assets/git_img/img_3.png)


1. 当前版本需要准备对应字体的散图
2. 散图命名按照实际对应的字符去命名，例如数字1，图片命名为数字1
3. 通过拖拽文件夹或者通过顶部打开按钮选择对应图片
4. 在右侧设置栏设置字体全局宽度和行高
5. 空格宽度选填
6. 一键等宽在设置完全局宽度后可以使用
7. 可以通过右下侧设置栏为单个字体调整宽度和偏移
8. 通过上方导出按钮可以导出字体文件，png图片+fnt描述文件

--------------

# 目录介绍

![image](https://github.com/KingSun5/font_creator/blob/main/assets/git_img/img_2.png)


- assets
> 资源目录
- main_win
> 主界面UI工程目录
- utils
> 独立的工具目录，需要单独引入
> 地址：https://github.com/KingSun5/sun_py_tools


--------------


# 版本更新记录

- 2023/07/13   -----V1.0
    - 字体创建工具第一版提交
    - 补充散图合图功能
    - 补充fnt文件导出功能
    - 补充一键等宽功能
