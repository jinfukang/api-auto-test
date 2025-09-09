# API自动化测试框架

一个基于Python的现代化API自动化测试框架，支持YAML驱动的测试用例管理、数据驱动测试、Allure报告生成等功能。

## 🚀 核心特性

### 📋 测试管理
- **YAML驱动**: 使用YAML文件定义测试用例，支持复杂的数据结构和参数化
- **数据驱动测试(DDT)**: 支持参数化测试，一次编写多场景执行

### 🔧 测试执行
- **多断言支持**: 支持equals、contains、greater、not_None等多种断言方式
- **数据提取**: 使用JSONPath从响应中提取数据，支持测试用例间的数据传递
- **数据库验证**: 支持MySQL数据库验证，确保数据一致性
- **动态参数**: 支持随机数据生成和动态参数替换

### 📊 报告与日志
- **Allure报告**: 自动生成美观的Allure测试报告
- **详细日志**: 支持多级别日志记录，便于调试和问题定位
- **性能监控**: 记录接口响应时间，支持性能断言

## 📁 项目结构

```
api-auto-test/
├── 📁 data/                    # 测试用例数据目录
│   ├── 📁 user/               # 用户相关测试用例
│   │   ├── add.yaml           # 用户注册测试
│   │   ├── login.yaml         # 用户登录测试
│   │   ├── update.yaml        # 用户更新测试
│   │   └── delete.yaml        # 用户删除测试
│   └── 📁 project/            # 项目相关测试用例
│       ├── add.yaml           # 项目创建测试
│       └── delete.yaml        # 项目删除测试
├── 📁 testcase/               # 测试执行文件
│   ├── conftest.py           # pytest配置和fixture
│   ├── test_01user.py        # 用户接口测试
│   ├── test_02project.py     # 项目接口测试
│   └── test_03delete.py      # 删除接口测试
├── 📁 utils/                  # 工具类
│   ├── request_util.py       # HTTP请求工具
│   ├── assert_util.py        # 断言工具
│   ├── yaml_util.py          # YAML文件操作
│   ├── mysql_util.py         # 数据库操作
│   ├── parameterize_util.py  # 参数化工具
│   └── logger_util.py        # 日志工具
├── 📁 debugTalk/             # 调试工具
│   └── debug_talk.py         # 调试函数集合
├── 📁 api-docs/             # API文档
├── 📁 logs/                 # 日志文件
├── 📁 reports/              # 测试报告
├── 📁 temps/                # 临时文件
├── config.yaml              # 配置文件
├── pytest.ini              # pytest配置
├── run.py                   # 测试执行入口
└── extract.yaml             # 数据提取文件
```

## 🛠️ 技术栈

- **Python 3.7+**: 主要开发语言
- **pytest**: 测试框架
- **requests**: HTTP请求库
- **PyYAML**: YAML文件处理
- **PyMySQL**: MySQL数据库连接
- **Allure**: 测试报告生成
- **JSONPath**: 数据提取

## 📦 安装与配置

### 环境要求
- Python 3.7+
- MySQL 5.7+ (可选，用于数据库验证)

### 安装依赖
```bash
pip install -r requirements.txt
```

### 配置文件
编辑 `config.yaml` 文件：

```yaml
base:
  url: http://localhost:80  # API基础URL

log:
  log_name: logs_           # 日志文件名前缀
  log_level: info           # 日志级别
  log_format: '[%(asctime)s] %(filename)s->%(funcName)s line:%(lineno)d [%(levelname)s] %(message)s'

db:                        # 数据库配置（可选）
  user: root
  host: 127.0.0.1
  password: your_password
  port: 3306
  db: your_database
```

## 🚀 快速开始

### 1. 运行测试
```bash
# 运行所有测试
python run.py

# 运行特定测试文件
pytest testcase/test_01user.py -v

# 运行特定测试方法
pytest testcase/test_01user.py::TestUser::test_add -v
```

### 2. 查看测试报告
测试完成后，在 `reports/` 目录下查看Allure报告：
```bash
allure serve ./temps/
```

## 📝 测试用例编写

### YAML测试用例格式

```yaml
- feature: "$ddt{feature}"                    # 测试用例名称
  base_url: "${read_config_yaml(base,url)}"   # 基础URL
  request:                                    # 请求配置
    url: "/v1/user"                          # 接口路径
    method: "post"                           # HTTP方法
    headers:                                 # 请求头
      Content-Type: "application/json"
    json:                                    # 请求体
      username: "$ddt{username}"
      password: "$ddt{password}"
  extract:                                   # 数据提取
    - id: "$..ID"                           # 使用JSONPath提取ID
    - token: "$..token"                     # 提取token
  validate:                                 # 断言配置
    - equals: { code: "$ddt{code}" }        # 相等断言
    - equals: { msg: "$ddt{msg}" }          # 消息断言
    - greater: { time: 2000 }               # 性能断言
    - not_None: { sql: "$ddt{check_sql}" }  # 数据库断言
  parameterize:                             # 参数化数据
    - ["feature", "username", "password", "code", "msg", "check_sql"]
    - ["正常登录", "admin", "123456", 200, "success", "select * from users where username='admin'"]
    - ["密码错误", "admin", "wrong", 400, "密码错误", ""]
```

### 支持的断言类型

1. **equals**: 相等断言
   ```yaml
   - equals: { code: 200, msg: "success" }
   ```

2. **contains**: 包含断言
   ```yaml
   - contains: { message: "登录成功" }
   ```

3. **greater**: 大于断言（通常用于性能测试）
   ```yaml
   - greater: { time: 1000 }  # 响应时间小于1000ms
   ```

4. **not_None**: 非空断言（通常用于数据库验证）
   ```yaml
   - not_None: { sql: "select * from users where id = 1" }
   ```

### 数据提取

使用JSONPath语法从响应中提取数据：

```yaml
extract:
  - user_id: "$..id"           # 提取用户ID
  - token: "$..data.token"     # 提取嵌套的token
  - username: "$..username"    # 提取用户名
```

### 动态参数

支持多种动态参数生成：

```yaml
# 随机用户名
username: "${get_random_username()}"

# 随机手机号
phone: "${get_random_phone()}"

# 读取配置文件
base_url: "${read_config_yaml(base,url)}"

# 读取提取的数据
user_id: "${read_extract_yaml(id)}"
```

## 🔧 高级功能

### 数据库验证
框架支持MySQL数据库验证，确保API操作的数据一致性：

```yaml
validate:
  - not_None: { sql: "select * from users where username = '${read_extract_yaml(username)}'" }
```

### 性能测试
支持接口响应时间断言：

```yaml
validate:
  - greater: { time: 2000 }  # 响应时间必须小于2000ms
```

### 数据传递
支持测试用例间的数据传递：

```yaml
# 在登录用例中提取token
extract:
  - token: "$..token"

# 在后续用例中使用token
headers:
  Authorization: "${read_extract_yaml(token)}"
```

### 随机数据生成
内置多种随机数据生成函数：

```python
# 随机用户名（20位字母数字组合）
"${get_random_username()}"

# 随机手机号（符合中国手机号格式）
"${get_random_phone()}"
```

## 📊 测试报告

### Allure报告
框架自动生成Allure测试报告，包含：
- 测试用例执行结果
- 接口响应时间统计
- 失败用例详细信息
- 测试环境信息

### 日志记录
支持多级别日志记录：
- **DEBUG**: 详细调试信息
- **INFO**: 一般信息记录
- **WARNING**: 警告信息
- **ERROR**: 错误信息

## 🐛 故障排除

### 常见问题

1. **数据库连接失败**
   - 检查 `config.yaml` 中的数据库配置
   - 确保MySQL服务正在运行
   - 验证数据库用户权限

2. **测试用例执行失败**
   - 检查YAML文件格式是否正确
   - 验证API接口是否可访问
   - 查看日志文件获取详细错误信息


### 调试技巧

1. **启用详细日志**
   ```yaml
   log:
     log_level: debug
   ```

2. **查看测试报告**
   ```bash
   allure serve ./temps/
   ```

3. **检查数据提取**
   查看 `extract.yaml` 文件确认数据是否正确提取

## 🤝 贡献指南

欢迎贡献代码和建议！请遵循以下步骤：

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 📞 联系方式

如有问题或建议，请通过以下方式联系：

- 创建 Issue
- 发送邮件
- 提交 Pull Request

---

**API自动化测试框架** - 让API测试更简单、更高效！ 🚀