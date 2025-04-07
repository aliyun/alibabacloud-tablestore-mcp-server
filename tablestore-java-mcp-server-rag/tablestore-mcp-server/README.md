# tablestore-mcp-server

A Tablestore Java MCP Server.

> [模型上下文协议（Model Context Protocol，MCP）](https://modelcontextprotocol.io/introduction)是一个开放协议，支持大型语言模型（LLM）应用程序与外部数据源及工具之间的无缝集成。
> 无论是开发AI驱动的集成开发环境（IDE）、增强聊天界面功能，还是创建定制化AI工作流，MCP均提供了一种标准化方案，
> 可将LLMs与其所需的关键背景信息高效连接。

这篇文章介绍如何基于Tablestore(表格存储)构建一个MCP服务，使用其向量和标量的混合检索，提供检索相关的 tool 能力。
# 本地运行


## 下载源码

1. 使用 `git clone` 将代码下载到本地。
2. 进入到该项目 java 源码的根目录

## 编译代码

代码需要 `jdk17` 版本以上进行构建，使用了 `mvn` 进行包和环境管理。

```bash
   # 确保 jdk17 环境
   ./mvnw package -DskipTests -s settings.xml
```

## 3.3 配置环境变量

代码里所有的配置是通过环境变量来实现的，出完整的变量见下方表格。 主要依赖的数据库 [Tablestore(表格存储)](https://www.aliyun.com/product/ots) 支持按量付费，使用该工具，表和索引都会自动创建，仅需要在控制台上申请一个实例即可。

| 变量名                          |                              必填                              |         含义         |                                                      默认值                                                       |
|------------------------------|:------------------------------------------------------------:|:------------------:|:--------------------------------------------------------------------------------------------------------------:|
| TABLESTORE_INSTANCE_NAME     | <span style="color:red; font-weight:bold;">**是(yes)**</span> |        实例名         |                                                       -                                                        |
| TABLESTORE_ENDPOINT          | <span style="color:red; font-weight:bold;">**是(yes)**</span> |       实例访问地址       |                                                       -                                                        |
| TABLESTORE_ACCESS_KEY_ID     | <span style="color:red; font-weight:bold;">**是(yes)**</span> |       秘钥 ID        |                                                       -                                                        |
| TABLESTORE_ACCESS_KEY_SECRET | <span style="color:red; font-weight:bold;">**是(yes)**</span> |     秘钥 SECRET      |                                                       -                                                        |


## Embedding
为了方便，这里不使用云服务的Embedding能力，而使用了内置的本地Embedding模型，这些模型都是可以应用生产的模型，示例代码仅支持了 [DeepJavaLibrary](https://djl.ai/) 上自带的Embedding模型，基本上都来自 Hugging Face，使用十分简单。

想用其它Embedding模型可以运行 `com.alicloud.openservices.tablestore.sample.service.EmbeddingService.listModels()` 方法查看支持的模型。

## 运行 MCP 服务

```bash
   export TABLESTORE_ACCESS_KEY_ID=xx
   export TABLESTORE_ACCESS_KEY_SECRET=xx
   export TABLESTORE_ENDPOINT=xxx
   export TABLESTORE_INSTANCE_NAME=xxx
   
   java -jar target/tablestore-java-mcp-server-1.0-SNAPSHOT.jar
```
