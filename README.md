# sponge_py 渗透测试工具🐍🧽
### 端口扫描工具scanner.py
#### 使用方法示例：
#### 以下代码将对本机开放端口进行扫描
```
from scanner.py import Scanner


scanner = Scanner()
scanner.scan('localhost')
```
#### 也可以通过指定命令行参数的方式运行
```
python3 scanner.py -H '127.0.0.1' -P '7000','8000' # 扫描127.0.0.1的7000,8000端口
python3 scanner.py -P '102.168.0.1'                # 扫描192.168.0.1的所有端口
python3 scanner.py                                 # 扫描localhost的所有端口
```
