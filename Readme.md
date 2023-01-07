# 一个从C to LLVM的编译器实现

## 部署环境

- python 3.10

- Linux codespaces-1df23a 5.4.0-1098-azure #104~18.04.2-Ubuntu SMP Tue Nov 29 12:13:35 UTC 2022 x86_64 x86_64 x86_64 GNU/Linux

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


