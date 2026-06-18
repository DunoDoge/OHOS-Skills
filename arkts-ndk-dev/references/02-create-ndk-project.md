<!-- 上游 URL: https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/create-with-ndk -->
<!-- 抓取时间: 2026-06-18 -->

# 创建 NDK 工程

## 通过 DevEco Studio 创建

使用 DevEco Studio 创建包含 C/C++ 代码的 HarmonyOS 工程步骤如下：

1. 打开 DevEco Studio，选择 **Create Project**
2. 在模板选择页面，选择 **Native C++** 模板
3. 配置工程信息（项目名称、包名、保存路径等）
4. 点击 **Finish** 完成创建

## 工程目录结构

创建完成后，C++ 代码位于 `entry/src/main/cpp` 目录下。典型的 NDK 工程目录结构如下：

```
entry/
└── src/
    └── main/
        ├── cpp/                    # C/C++ 代码目录
        │   ├── CMakeLists.txt      # CMake 构建配置文件
        │   ├── hello.cpp           # C++ 源文件
        │   └── types/              # Node-API 接口声明
        │       └── libhello/
        │           ├── index.d.ts   # ArkTS 接口声明文件
        │           └── index.js     # 接口注册文件
        ├── ets/                    # ArkTS 代码目录
        └── resources/              # 资源文件目录
```

> **说明**：关于 C++ 项目的完整目录结构说明，请参考 [C++工程目录结构](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/cpp-project-structure) 文档。
