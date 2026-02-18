# Python环境变量设置指南

## 问题说明
您的Python安装在：`C:/Users/vland/python-sdk/python3.13.2/`
但是这个路径没有添加到系统环境变量中，导致无法直接使用`python`命令。

## 解决方案

### 方法一：手动设置环境变量（推荐）

1. **打开系统环境变量设置**：
   - 按下 `Win + R` 键
   - 输入 `sysdm.cpl` 并按回车
   - 点击"高级"标签
   - 点击"环境变量"按钮

2. **编辑用户变量**：
   - 在"用户变量"区域找到"Path"变量
   - 选中"Path"变量，点击"编辑"
   - 点击"新建"按钮
   - 输入：`C:/Users/vland/python-sdk/python3.13.2`
   - 点击"确定"保存

3. **验证设置**：
   - 关闭所有打开的终端窗口
   - 重新打开一个新的终端
   - 输入：`python --version`
   - 应该显示：`Python 3.13.2`

### 方法二：使用命令行设置（需要管理员权限）

1. **以管理员身份打开PowerShell**：
   - 右键点击"开始"菜单
   - 选择"Windows PowerShell (管理员)"

2. **运行以下命令**：
   ```powershell
   [Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:/Users/vland/python-sdk/python3.13.2", "User")
   ```

3. **重启终端并验证**：
   ```powershell
   python --version
   ```

### 方法三：临时设置（仅对当前终端有效）

如果只是临时需要使用Python，可以在当前终端中运行：

```powershell
$env:Path = $env:Path + ";C:/Users/vland/python-sdk/python3.13.2"
```

然后就可以使用`python`命令了，但关闭终端后设置会失效。

### 方法四：使用完整路径

在任何情况下，都可以直接使用完整路径运行Python：

```powershell
& "C:/Users/vland/python-sdk/python3.13.2/python.exe" --version
```

或者运行Python脚本：

```powershell
& "C:/Users/vland/python-sdk/python3.13.2/python.exe" your_script.py
```

## 验证Python安装

运行以下命令验证Python是否正常工作：

```powershell
# 检查Python版本
& "C:/Users/vland/python-sdk/python3.13.2/python.exe" --version

# 检查pip
& "C:/Users/vland/python-sdk/python3.13.2/python.exe" -m pip --version

# 测试Python
& "C:/Users/vland/python-sdk/python3.13.2/python.exe" -c "print('Hello, Python!')"
```

## 安装必要的包

设置好环境变量后，可以安装必要的Python包：

```powershell
pip install requests beautifulsoup4
```

或者使用完整路径：

```powershell
& "C:/Users/vland/python-sdk/python3.13.2/python.exe" -m pip install requests beautifulsoup4
```

## 运行爬虫脚本

设置好环境变量后，可以直接运行爬虫脚本：

```powershell
python tender_spider.py
```

或者使用完整路径：

```powershell
& "C:/Users/vland/python-sdk/python3.13.2/python.exe" tender_spider.py
```

## 注意事项

1. **环境变量更改需要重启终端**：修改环境变量后，必须关闭所有终端窗口并重新打开才能生效。

2. **路径分隔符**：Windows使用分号`;`作为路径分隔符，不要使用冒号`:`。

3. **用户变量 vs 系统变量**：建议修改用户变量而不是系统变量，这样不会影响其他用户。

4. **权限问题**：如果修改系统变量，需要管理员权限。

5. **路径格式**：确保使用正确的路径格式，建议使用正斜杠`/`或双反斜杠`\\`。

## 故障排除

如果设置后仍然无法使用`python`命令：

1. 检查路径是否正确：
   ```powershell
   Test-Path "C:/Users/vland/python-sdk/python3.13.2"
   ```

2. 检查Python.exe是否存在：
   ```powershell
   Test-Path "C:/Users/vland/python-sdk/python3.13.2/python.exe"
   ```

3. 查看当前环境变量：
   ```powershell
   $env:Path -split ';'
   ```

4. 尝试使用完整路径运行Python，确认Python本身没有问题。

## 推荐做法

建议使用**方法一（手动设置）**，因为：
- 界面操作更直观
- 不容易出错
- 可以同时检查其他环境变量设置
- 便于后续维护和修改
