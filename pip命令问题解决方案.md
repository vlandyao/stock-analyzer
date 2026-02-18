# pip命令问题解决方案

## 问题诊断

pip命令报错的原因是：**Python的Scripts目录没有添加到环境变量中**。

pip.exe文件位于：`C:/Users/vland/python-sdk/python3.13.2/Scripts/`

但是这个目录没有添加到PATH环境变量中，所以系统找不到pip命令。

## 解决方案

### 方法一：手动添加Scripts目录到环境变量（推荐）

**步骤：**

1. **打开环境变量设置**：
   - 按 `Win + R` 键
   - 输入 `sysdm.cpl` 并按回车
   - 点击"高级"标签
   - 点击"环境变量"按钮

2. **编辑用户变量**：
   - 在"用户变量"区域找到"Path"变量
   - 选中"Path"变量，点击"编辑"

3. **添加Scripts目录**：
   - 点击"新建"按钮
   - 输入：`C:/Users/vland/python-sdk/python3.13.2/Scripts`
   - 点击"确定"保存

4. **保存并重启**：
   - 点击"确定"保存所有设置
   - **关闭所有终端窗口**
   - **重新打开终端**
   - 测试：`pip --version`

### 方法二：使用Python运行pip（临时解决方案）

如果需要立即使用pip，可以通过Python来运行：

```powershell
python -m pip --version
python -m pip install requests beautifulsoup4
```

### 方法三：使用完整路径（临时解决方案）

```powershell
& "C:/Users/vland/python-sdk/python3.13.2/Scripts/pip.exe" --version
& "C:/Users/vland/python-sdk/python3.13.2/Scripts/pip.exe" install requests beautifulsoup4
```

### 方法四：运行自动设置脚本

我已经为您创建了自动设置脚本：`add_scripts_to_path.ps1`

运行脚本：
```powershell
powershell -ExecutionPolicy Bypass -File add_scripts_to_path.ps1
```

然后关闭并重新打开终端。

## 验证修复

修复后，运行以下命令验证：

```powershell
# 检查pip版本
pip --version

# 检查pip位置
where.exe pip
```

应该显示：
- `pip 26.0.1 from C:\Users\vland\python-sdk\python3.13.2\Lib\site-packages\pip (python 3.13)`
- `C:/Users/vland/python-sdk/python3.13.2/Scripts/pip.exe`

## 安装必要的包

修复后，可以安装Python包：

```powershell
pip install requests beautifulsoup4
```

## 运行爬虫脚本

安装好依赖后，运行爬虫：

```powershell
python tender_spider.py
```

## 为什么需要添加Scripts目录？

Python的可执行文件（如pip、pip3、pip3.13等）都安装在Scripts目录中，而不是Python主目录中。因此，需要将Scripts目录也添加到PATH环境变量中，才能直接使用这些命令。

## 完整的环境变量配置

正确的Python环境变量配置应该包含两个路径：

1. **Python主目录**：`C:/Users/vland/python-sdk/python3.13.2`
   - 用于运行：`python`、`pythonw`等命令

2. **Scripts目录**：`C:/Users/vland/python-sdk/python3.13.2/Scripts`
   - 用于运行：`pip`、`pip3`、`pip3.13`等命令

## 推荐做法

建议按照**方法一（手动添加Scripts目录）**操作，因为：
- 界面操作更直观
- 不容易出错
- 可以同时检查其他环境变量设置
- 便于后续维护和修改

## 如果问题仍然存在

如果按照上述方法操作后问题仍然存在：

1. **检查Scripts路径是否正确**：
   ```powershell
   Test-Path "C:/Users/vland/python-sdk/python3.13.2/Scripts/pip.exe"
   ```

2. **使用Python运行pip**：
   ```powershell
   python -m pip --version
   ```

3. **检查环境变量**：
   ```powershell
   $env:Path -split ';' | Select-String "Scripts"
   ```

4. **重启电脑**：有时需要重启才能使环境变量更改生效。

## 总结

问题的核心是**Scripts目录没有添加到PATH环境变量中**。通过添加`C:/Users/vland/python-sdk/python3.13.2/Scripts`到环境变量，就可以正常使用pip命令了。

添加Scripts目录后，您就可以：
- 直接使用`pip install`安装包
- 使用`pip list`查看已安装的包
- 使用`pip uninstall`卸载包
- 运行需要pip依赖的Python脚本
