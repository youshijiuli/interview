





# Python 打包与 pip 安装完全指南

> 目标：搞懂「自己怎么做一个包，然后通过 `pip install` 装到任何环境」。
> 适用：个人工具脚本整理、内部库分发、带 C++/二进制产物的包（对标 IVCLibs 那种 tar.gz）。

---

## 0. 先看懂本质：pip 装的到底是什么

`pip install` 只认两种「发行包」形态：

| 形态 | 文件 | 本质 | 安装时 | 特点 |
|---|---|---|---|---|
| **sdist**（源码发行包） | `.tar.gz`（也可 `.zip`） | 一个标准压缩包 | 解压 → 现场构建 wheel → 安装 | 跨平台，不挑系统；要装到目标机器上构建 |
| **wheel**（二进制发行包） | `.whl` | 本质是 zip | 直接解压到 site-packages | 安装最快；带平台/版本标签，跨平台要分别构建 |

**pip 判断「能不能装」的唯一依据**：压缩包/目录内部是否是标准 Python 包结构 —— 即有没有 `pyproject.toml`（PEP 517 规范）或 `setup.py`/`setup.cfg`（向后兼容的老方式）。有，就能装；没有，就报 `ERROR: ... 找不到 setup.py / pyproject.toml`。

所以 IVCLibs 那种「20M 的 tar.gz、看着不像 Python 库」也能装，是因为它内部带了构建描述文件，外面套了标准 sdist 的壳。

`pip install` 的输入来源非常多，这也是「方法多」的根源：

```bash
pip install 包名                       # 从配置的索引（默认 PyPI）下载
pip install ./路径/xxx.tar.gz          # 本地 sdist 文件
pip install ./路径/xxx.whl             # 本地 wheel 文件
pip install ./某目录                   # 本地目录（含 pyproject.toml/setup.py）
pip install https://xxx/xxx.tar.gz     # URL 直链
pip install git+https://git地址@分支   # 直接从 git 仓库装
```

---

## 1. 方法总览（七种常见路线）

| # | 方法 | 适用场景 | 产出 |
|---|---|---|---|
| 1 | **setuptools + pyproject.toml** 标准包 | 绝大多数情况，最主流 | `tar.gz` + `.whl` |
| 2 | 换构建后端（flit / hatchling / poetry） | 想更现代/更简单 | 同上 |
| 3 | 带 C 扩展 / 预编译二进制 / 数据文件 | 底层库、so/pyd、资源文件 | 带平台标签的 `.whl` |
| 4 | **不构建，直接装目录 / 手搓 tar.gz** | 快速验证、内部小工具；IVCLibs 那种 | 目录或压缩包 |
| 5 | 只发 wheel | 只给同平台同事 | `.whl` |
| 6 | git 直装 | 源码在 git 仓库，不发布 | 无（临时装） |
| 7 | 私有 PyPI 索引 | 团队/公司内规范分发 | 上传到索引 |

下面逐个展开。

---

## 2. 环境准备

```bash
python -m pip install --upgrade pip
python -m pip install build     # 构建工具（python -m build）
python -m pip install twine     # 上传索引用（方法7需要）
```

> 建议所有打包/安装都在虚拟环境里做，避免污染系统 Python：
> `python -m venv .venv`，Windows 激活：`.venv\Scripts\activate`。

---

## 3. 方法一：最标准的 setuptools 纯 Python 包（重点）

### 3.1 目录结构

推荐 **src 布局**（更规范，避免误把源码目录当包装进去）：

```
mypkg/                          # 项目根目录（名字随意）
├── pyproject.toml              # ★ 核心：包的所有元数据 + 构建配置
├── README.md                   # 可选，写在包描述里
├── LICENSE                     # 可选
└── src/
    └── mypkg/                  # ★ 包目录：import 时用的名字（必须合法标识符）
        ├── __init__.py         # 包初始化，写 __version__ 等
        ├── core.py             # 你的代码，随便加模块
        └── utils.py
```

也可以扁平布局（`mypkg/` 直接放根目录），小项目也行，但 src 布局更不容易踩坑。

### 3.2 pyproject.toml 逐段详解

```toml
[build-system]                        # 告诉 pip 用什么工具构建
requires = ["setuptools>=61"]         # 构建时需要安装的依赖
build-backend = "setuptools.build_meta"  # setuptools 的构建后端

[project]                             # PEP 621 元数据
name = "mypkg"                        # ★ 发行名：pip 安装时用的名字
version = "0.1.0"                     # PEP 440 版本号，必须合法
description = "我的第一个 pip 包"
readme = "README.md"
requires-python = ">=3.8"
license = {text = "MIT"}              # 可选
dependencies = [                      # 运行时依赖，装包时自动装
    "pandas>=2.0",
    "openpyxl",
]

[project.optional-dependencies]       # 可选：额外功能
all = ["rich", "tabulate"]

[project.scripts]                     # ★ 可选：安装后生成命令行命令
mypkg = "mypkg.cli:main"              # 生成 mypkg 命令，执行 mypkg.cli.main()

[tool.setuptools.packages.find]       # 自动发现包（src 布局）
where = ["src"]
```

字段要点：

- **`name` ≠ import 名**：`name` 是 install 用的，可以带 `-`（如 `my-tool`，但这样 `import my-tool` 不合法，所以包里 import 名要另起，如 `mytool`）。简单做法：两者同名、小写、下划线。
- **`[project.scripts]`** 是把 Python 函数变成命令行工具的关键，装完直接敲命令，不用 `python -m`。
- **`dependencies`** 依赖会在安装时自动解析安装。

### 3.3 写一点包代码

`src/mypkg/__init__.py`：

```python
__version__ = "0.1.0"
```

`src/mypkg/core.py`：

```python
def hello(name: str = "world") -> str:
    return f"hello, {name}"
```

`src/mypkg/cli.py`（配合 scripts 用）：

```python
def main() -> None:
    from .core import hello
    print(hello())
```

### 3.4 构建

```bash
python -m build
```

成功后 `dist/` 下出现两个文件：

```
dist/
├── mypkg-0.1.0.tar.gz                       # sdist
└── mypkg-0.1.0-py3-none-any.whl             # wheel（py3-none-any = 纯 Python 通用）
```

### 3.5 安装（四种方式任选）

```bash
pip install .                               # ① 直接装项目目录（自动构建）
pip install dist/mypkg-0.1.0.tar.gz         # ② 装 sdist —— 等价于 IVCLibs 的用法
pip install dist/mypkg-0.1.0-py3-none-any.whl  # ③ 装 wheel
pip install -e .                            # ④ 开发模式：代码改了立即生效，不用重装
```

### 3.6 验证

```bash
python -c "import mypkg; print(mypkg.__version__)"
mypkg          # 如果配了 [project.scripts]，直接敲命令
pip show mypkg # 看安装信息/路径
```

### 3.7 升级 / 卸载 / 重装

```bash
pip install --force-reinstall dist/mypkg-0.1.0.tar.gz   # 重装（同版本覆盖）
pip install --upgrade 包名                              # 按更高版本升级（索引方式）
pip uninstall mypkg
```

---

## 4. 方法二：换现代构建后端

`pyproject.toml` 里换 `build-backend` 即可，结构一样：

**hatchling**（简单、快）：

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "mypkg"
version = "0.1.0"

[tool.hatch.build.targets.wheel]
packages = ["src/mypkg"]
```

**flit**（纯 Python 包最快上手）：

```toml
[build-system]
requires = ["flit_core>=3.2"]
build-backend = "flit_core.buildapi"

[project]
name = "mypkg"
version = "0.1.0"
```

**poetry**（依赖管理体验好，但构建配置语法不同，教程多、略复杂）。

结论：**新手/大多数场景直接用 setuptools（方法一）就够了**，其他后端属于口味问题。

---

## 5. 方法三：带二进制 / 数据文件的包（对标 IVCLibs）

如果你的包里有预编译的 `.so` / `.pyd` / DLL / 配置文件 / 模型文件，关键是**把它们声明为包数据**，让 wheel 把它们也打进去。

目录结构：

```
mypkg/
├── pyproject.toml
└── src/
    └── mypkg/
        ├── __init__.py
        ├── core.py
        ├── libs/
        │   ├── ivc_core.pyd        # 预编译产物（放包内）
        │   └── ivc_core.so
        └── config/
            └── channels.json
```

`pyproject.toml` 增加：

```toml
[tool.setuptools.packages.find]
where = ["src"]

[tool.setuptools.package-data]        # ★ 关键：哪些非 .py 文件要进 wheel
mypkg = ["libs/*.so", "libs/*.pyd", "config/*.json"]
```

若还要让它们进 **sdist**（tar.gz），在项目根目录加 `MANIFEST.in`：

```
include src/mypkg/libs/*.so
include src/mypkg/libs/*.pyd
include src/mypkg/config/*.json
```

构建后注意：**wheel 会带平台标签**，例如：

```
mypkg-0.1.0-cp312-cp312-win_amd64.whl         # Windows x64 + Python 3.12
mypkg-0.1.0-cp39-cp39-manylinux_2_17_x86_64.whl  # Linux
```

意味着：**换 Python 版本、换操作系统都要重新构建 wheel**；而 sdist（tar.gz）在目标机器上「现场构建」所以不受限 —— 这正是你们内网大量分发 tar.gz 的原因。

### 场景 A：setup.py 里用 setuptools.Extension 真编译 C/C++

```python
# setup.py（可选老方法，或配合 pyproject 使用）
from setuptools import setup, Extension

setup(
    ext_modules=[
        Extension("mypkg._native", sources=["src/native/ivc_core.c"]),
    ]
)
```

目标机器需要编译器（Windows 需要 Visual Studio Build Tools / MSVC，Linux 需要 gcc）才能装得动。

### 场景 B：不编译，只是「搬运」预编译产物（更接近 IVCLibs）

用上面的 `package-data` 就够了，`setup.py` 完全可以没有，或只有一个空壳。安装时就是拷贝。

---

## 6. 方法四：不构建，直接得到「能 pip install 的东西」

### 6.1 直接装目录

只要目录里有 `pyproject.toml` 或 `setup.py`，什么都不用打：

```bash
pip install ./mypkg
```

pip 会自动走 PEP 517 构建（等价于临时帮你 `python -m build`）。

### 6.2 手动「手搓」一个 sdist tar.gz（了解原理）

跟 IVCLibs 一个套路——不需要 `python -m build`，手动打包一个目录：

```
随便起名/
├── pyproject.toml（或 setup.py）   # ★ 必须有，pip 才认
├── PKG-INFO（可选）                # sdist 里常见的元数据文件
└── mypkg/
    ├── __init__.py
    └── core.py
```

```bash
tar -czf mypkg-0.1.0.tar.gz <上面的目录内容>
pip install ./mypkg-0.1.0.tar.gz
```

> 装的时候 pip 会把 tar.gz 解压到临时目录，找 `pyproject.toml`/`setup.py` 现场构建。**只要壳是标准的，内容是什么都行**。

---

## 7. 方法五：只发 wheel

对「同一平台 + 同一 Python 版本」的队友，发 `.whl` 最省事（不用现场构建）：

```bash
python -m pip wheel . -w dist     # 只产 wheel
pip install dist/mypkg-0.1.0-py3-none-any.whl
```

跨平台要多平台分别 build（CI 里配多系统构建），或回到发 sdist。

---

## 8. 方法六：git 直装（不用发任何文件）

```bash
pip install git+https://内网git地址/group/mypkg.git
pip install git+https://内网git地址/group/mypkg.git@v0.1.0        # 指定 tag
pip install git+https://内网git地址/group/mypkg.git@dev#egg=mypkg # 指定分支
```

要求：仓库根目录有 `pyproject.toml`/`setup.py`（与前面一致）。适合源码在 git、懒得发布产物的场景。

---

## 9. 方法七：私有 PyPI 索引（团队规范分发）

目标：让同事直接 `pip install mypkg`（不用给路径）。两种常见做法：

### 9.1 文件共享 + pip 指向目录/URL（最简）

```bash
# 把 dist/*.tar.gz 放到共享盘或内网静态目录
pip install \\共享盘\packages\mypkg-0.1.0.tar.gz
pip install https://内网域名/packages/mypkg-0.1.0.tar.gz
```

### 9.2 起一个 pypiserver（轻量私有源）

```bash
python -m pip install pypiserver
mkdir packages
pypi-server -p 8080 ./packages &
# 上传
python -m twine upload -r local --repository-url http://127.0.0.1:8080 dist/*.tar.gz
# 同事安装
pip install -i http://127.0.0.1:8080/simple mypkg
```

### 9.3 公司级：Nexus / devpi / Artifactory

大同小异：配好仓库后 `twine upload`，`pip install -i <内网源> 包名`。企业内网常见 Nexus。

---

## 10. 常见坑与排查

| 症状 | 原因 / 解法 |
|---|---|
| `ERROR: 找不到 setup.py 或 pyproject.toml` | 包里没有构建描述文件；或 tar.gz 结构不对（多包了一层目录）。确认解压后**根目录**就有 pyproject.toml |
| `ERROR: Invalid requirement` | 包名非法（空格、中文、大写混用）；小写字母+数字+`-_`，不能以数字开头 |
| 装上了但 `import mypkg` 报错 | 包目录没被识别：检查 `[tool.setuptools.packages.find] where=["src"]` 是否写对；或 package 名与目录名不一致 |
| 命令行命令不存在 | 忘了 `[project.scripts]`，或装完没重开终端 |
| 版本号报错 `Invalid version` | 版本号必须 PEP 440 合法：`0.1.0`、`0.1.0rc1` 可以，`v0.1`、`1.0-1` 不行 |
| wheel 装到别的机器报「不是受支持的平台上此 wheel」 | 平台标签不匹配，换 sdist（tar.gz）装，或在该平台重新构建 |
| 打包后少了数据文件/配置文件 | 加 `[tool.setuptools.package-data]`（wheel 用）+ `MANIFEST.in`（sdist 用） |
| `pip install -e .` 后代码改动不生效 | editable 是软链/映射，确认装的确实是 editable（`pip show` 里 Location 指向项目目录） |
| 权限报错（系统 Python 目录只读） | 用虚拟环境，或 `pip install --user` |
| 想覆盖同版本重装报 `already satisfied` | `pip install --force-reinstall ...` |

---

## 11. 一个最小完整示例（可直接复制运行）

在任意空目录执行：

```bash
mkdir mypkg && cd mypkg
mkdir -p src/mypkg
```

`pyproject.toml`：

```toml
[build-system]
requires = ["setuptools>=61"]
build-backend = "setuptools.build_meta"

[project]
name = "mypkg"
version = "0.1.0"
description = "minimal example"
requires-python = ">=3.8"

[project.scripts]
mypkg = "mypkg.cli:main"

[tool.setuptools.packages.find]
where = ["src"]
```

`src/mypkg/__init__.py`：

```python
__version__ = "0.1.0"
```

`src/mypkg/core.py`：

```python
def hello(name: str = "world") -> str:
    return f"hello, {name}"
```

`src/mypkg/cli.py`：

```python
def main() -> None:
    from .core import hello
    print(hello())
```

然后：

```bash
python -m pip install build
python -m build                                # 产出 dist/mypkg-0.1.0.tar.gz 与 .whl
pip install dist/mypkg-0.1.0.tar.gz            # 装（等价于 IVCLibs 的用法）
mypkg                                          # 输出 hello, world
python -c "from mypkg.core import hello; print(hello('张三'))"
```

---

## 12. 速查命令表

| 目的 | 命令 |
|---|---|
| 装构建工具 | `python -m pip install build twine` |
| 构建全部产物 | `python -m build` |
| 只构建 wheel | `python -m pip wheel . -w dist` |
| 装本地目录 | `pip install .` |
| 装 sdist | `pip install dist/xxx.tar.gz` |
| 装 wheel | `pip install dist/xxx.whl` |
| 开发模式 | `pip install -e .` |
| 从 git 装 | `pip install git+https://xxx.git@分支` |
| 上传到私有源 | `python -m twine upload -r local --repository-url <源地址> dist/*.tar.gz` |
| 查安装信息 | `pip show 包名` |
| 看装到哪了 | `python -c "import 包名; print(包名.__file__)"` |
| 强制重装 | `pip install --force-reinstall dist/xxx.tar.gz` |
| 卸载 | `pip uninstall 包名` |

---

## 一句话总结

> **做包 = 搭一个带 `pyproject.toml` 的标准目录 + 用 `python -m build` 产出 tar.gz/whl；pip 安装 = 给它任意一个「内部是标准包结构」的路径/文件/URL。** 方法七种，本质一个：让目标对象长成 Python 发行包的样子。



