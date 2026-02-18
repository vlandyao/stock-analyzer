# Python命令无反应问题解决方案

## 问题诊断

经过检查，发现了问题的根本原因：

您的系统中存在**两个Python安装**：
1. **Windows Store的Python启动器**：`C:\Users\vland\AppData\Local\Microsoft\WindowsApps\python.exe`
2. **您实际安装的Python**：`C:\Users\vland\python-sdk\python3.13.2\python.exe`

当您输入`python --version`时，系统会优先使用Windows Store的Python启动器，这个启动器通常会：
- 打开Microsoft Store
- 显示提示信息
- 或者没有任何反应

## 解决方案

### 方法一：调整环境变量优先级（推荐）

**步骤：**

1. **打开环境变量设置**：
   - 按 `Win + R` 键
   - 输入 `sysdm.cpl` 并按回车
   - 点击"高级"标签
   - 点击"环境变量"按钮

2. **编辑用户变量**：
   - 在"用户变量"区域找到"Path"变量
   - 选中"Path"变量，点击"编辑"

3. **调整Python路径优先级**：
   - 找到路径：`C:/Users/vland/python-sdk/python3.13.2`
   - 使用"上移"按钮将其移动到列表的**最顶部**
   - 确保它在WindowsApps路径之前

4. **保存并重启**：
   - 点击"确定"保存所有设置
   - **关闭所有终端窗口**
   - **重新打开终端**
   - 测试：`python --version`

### 方法二：删除Windows Store的Python启动器

如果您不需要Windows Store的Python启动器，可以删除它：

1. **打开文件资源管理器**
2. **导航到**：`C:\Users\vland\AppData\Local\Microsoft\WindowsApps\`
3. **删除或重命名**：`python.exe` 和 `python3.exe`
4. **重启终端**并测试

### 方法三：使用Python启动器（py命令）

Windows系统自带Python启动器，可以直接使用：

```powershell
py --version
```

这个命令会自动找到系统中的Python安装并运行。

### 方法四：使用完整路径（临时解决方案）

如果需要立即使用Python，可以使用完整路径：

```powershell
& "C:/Users/vland/python-sdk/python3.13.2/python.exe" --version
& "C:/Users/vland/python-sdk/python3.13.2/python.exe" your_script.py
```

或者设置临时别名：

```powershell
Set-Alias python "C:/Users/vland/python-sdk/python3.13.2/python.exe"
python --version
```

## 验证修复

修复后，运行以下命令验证：

```powershell
# 检查Python版本
python --version

# 检查pip
python -m pip --version

# 查找Python位置
where.exe python
```

应该显示：
- `Python 3.13.2`
- `pip x.x.x from C:/Users/vland/python-sdk/python3.13.2/...`
- `C:/Users/vland/python-sdk/python3.13.2\python.exe`（第一个结果）

## 安装必要的包

修复后，可以安装Python包：

```powershell
pip install requests beautifulsoup4
```

## 运行爬虫脚本

修复后，可以直接运行爬虫：

```powershell
python tender_spider.py
```

## 为什么会出现这个问题？

1. **Windows 10/11的Python启动器**：微软在Windows 10/11中添加了Python启动器，当用户输入`python`命令时，会优先使用这个启动器。

2. **环境变量优先级**：WindowsApps路径通常在用户PATH的前面，所以会优先被找到。

3. **安装顺序**：如果先安装了Windows Store的Python启动器，后安装了实际的Python，就会出现这个问题。

## 预防措施

为了避免将来出现类似问题：

1. **安装Python时勾选"Add Python to PATH"**
2. **检查环境变量优先级**，确保自定义的Python路径在系统路径之前
3. **使用Python启动器（py命令）**，它可以自动找到正确的Python版本

## 推荐做法

建议使用**方法一（调整环境变量优先级）**，因为：
- 不会删除系统文件
- 保留了Windows Store的Python启动器作为备选
- 解决了根本问题
- 便于后续维护

## 如果问题仍然存在

如果按照上述方法操作后问题仍然存在：

1. **检查环境变量是否正确保存**：
   ```powershell
   [System.Environment]::GetEnvironmentVariable("Path", "User") -split ';'
   ```

2. **确认Python文件存在**：
   ```powershell
   Test-Path "C:/Users/vland/python-sdk/python3.13.2/python.exe"
   ```

3. **使用Python启动器**：
   ```powershell
   py --version
   ```

4. **重启电脑**：有时需要重启才能使环境变量更改生效。

## 总结

问题的核心是**环境变量优先级**导致的。通过将您的Python路径移动到PATH变量的最前面，就可以确保系统优先使用您安装的Python，而不是Windows Store的Python启动器。
