# RA2 python + opencv 小工具盒

目前包含： INI 自动分类整理器， 适配戴子玲渲染脚本的 SHP GIF 一键生成, 以及一些实例

# 一键帧序列带阴影转GIF （需要 opencv）
没什么可说的，能调的参数都注释了，直接塞进戴子玲脚本的输出文件夹然后双击运行，等几秒找 output.gif
![alt text](https://github.com/NordlichtS/RA2-py-cv-toybox/blob/main/EXAMPLES/GDI%20alchemy%20table.gif)

# ini auto sort:
python script to sort rules.ini into multiple files by object types, so you can [#include] with Ares and make mod editing more organized.

（中文教程懒得写了，需要的话可以直接问我）

how to use:

0, Back up your ini file just in case it mess up. Put the script and your rules.ini, your object registry index, all in one new folder

it's better to get object registry (the list under [VehicleTypes] [WeaponTypes] and so on) from the game engine, because the registries in rules.ini are incomplete

1, Use remove_duplicates.py to remove duplicating sections and duplicating option in each section. This is to prevent python's config parser give you duplicate error. 

You might want to remove comments and percentage symbols too, i don't know if its neccessary, but sometimes the config parser gives you error when encoutering "%" symbol.

I suggest replacing all "%" symbol with a text placeholder, and change them all back after everything is done. (use win10 notepad or VScode's replacement function, it's not in the script)

2, Use ares_sort_rules.py for making the new categorized files. This is the most important step! Watch the terminal in case of any error.

3, Use negative_techlevel_sort.py to process the newly created sort_BuildingTypes.ini and sort_VehicleTypes.ini, this will separate stuff you cannot build (neutral objects) 

if something has "deploysinto=" or "undeploysinto=" it will not be separated, regardless of TechLevel value. like construction yard and tick tank.

4, Use cleanup_after_sort.py to remove already sorted sections from rules.ini. For the sections that are not sorted, you need to manually sort them or write your own list into the index file.

In the example i provided, I used the rules registry index from Tiberian Sun Another World. 
The rulesmd.ini was quickly sorted into 27 different files. 
Dont forget the final step, you need to do it by hand : [#include]  function of Ares 2.0+

![alt text](https://github.com/NordlichtS/RA2-ini-organizer/blob/main/EXAMPLES/ARES%20RULES%20INCLUDE.png)

the "old copy ini files .py" is my early version which used brute force text management, and is not limited by the bug of config parser. thus it wont give you duplication error or problem with percentage symbols. however it might be less stable



