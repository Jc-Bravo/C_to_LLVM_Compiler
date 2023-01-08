# 一个从C to LLVM的编译器实现

## 部署环境

- python 3.10

- Ubuntu 18.04 (x86_64 & arm)
    
可以在`generator/generator.py`中 Class Visitor中，通过`self.ARCH = 'x86_64' # or 'arm64'`来控制生成对应为arm还是x86结构的代码，默认为x86

### install 

```shell
pip install antlr4-tools
pip install antlr4-python3-runtime==4.11
pip install llvmlite
```

- apt requirements:

```shell
antlr4==4.11
```


## 运行

进入main.py的同级目录下

生成中间代码：

`python3 main.py example/example.c`

运行：

`lli example/example.ll`



