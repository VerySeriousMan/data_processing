# data_processing
a software about sunny data processing
version:V1.4.1

## 版本更新日志

### V1.4.1（2024.08.07）
**1、优化界面显示，增加界面整体自适应缩放，适配不同的分辨率，解决在高分辨率显示器下文字过小的问题**<br>

### V1.4（2024.07.19）
**1、优化了界面与按键合理性：**<br>
① 添加Qwidget分页框架，将数据预处理内容划分为5大功能页面<br>
② 合并ID修改与属性修改，合并两个文件夹导入，简化数据操作<br>
③ 丰富与完善提示信息，增加输入检测<br>
④ 增加按键保护，在打开文件夹后，才能使用其他控件<br>
**2、增加了新的功能：**<br>
① 增加文件查重功能，并可自定义修改相似度，可选择自查重与对比查重，选择对比查重后，
才会显示打开对比文件夹按键<br>
② 增加错误数据检测功能，并且：（1）导入文件与修改内容后，都会自动进行多余空格删除与身份证x转X；
（2）修改文件后，会检测文件名中的中文与错误属性，并导出问题数据地址txt<br>
③ 文件查重可根据setting选择去重或保存唯一图像，并生成重复图像的txt以供检查<br>
④ 增加错误数据修改功能，点击按键后会进入错误修改界面<br>
**3、错误数据修改界面：**<br>
① 自动错误数据txt导入，若主界面生成错误数据txt，会自动进行导入，若无，可自主导入txt<br>
② 自动实时显示当前处理数据地址，剩余数据数量，并在修改输入框中自动导入当前处理文件名<br>
③ 可选择单张处理与批量处理，对于批量处理，软件会通过文件地址正则化比对排除，
找到同类文件进行批量同时处理<br>
④ 具有修改按键与跳过按键，可选择是否进行修改<br>
**4、增加外部配置文件：**<br>
① visible控制控件可见性，分全部功能可见与部分功能可见<br>
② dedup_cover控制查重后直接删除重复数据或将查重后文件导入新文件夹<br>
③ space_enabled与Idcard控制多余空格删除和身份证x转X的自动检测与修复<br>
④ project_name控制导入项目类型，以匹配对应数据检测与正则化匹配<br>
**5、优化代码架构与代码效率：**<br>
**6、软件打包spec编写**<br>