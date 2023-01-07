# 一个从C to LLVM的编译器实现

## 部署环境

- python 3.10

- Ubuntu desktop aarch64 (on Parallels Desktop 18)

- pip requirements (latest):

```shell
antlr4-tools
antlr4-python3-runtime==4.11
llvmlite
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


