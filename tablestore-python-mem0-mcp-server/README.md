# tablestore-mcp-server

A based Tablestore Mem0 Python MCP Server.

> [模型上下文协议（Model Context Protocol，MCP）](https://modelcontextprotocol.io/introduction)是一个开放协议，支持大型语言模型（LLM）应用程序与外部数据源及工具之间的无缝集成。
> 无论是开发AI驱动的集成开发环境（IDE）、增强聊天界面功能，还是创建定制化AI工作流，MCP均提供了一种标准化方案，
> 可将LLMs与其所需的关键背景信息高效连接。

这篇文章介绍如何使用基于Tablestore(表格存储)的Mem0 MCP服务。

> 注意：1）本项目基于mem0的openmemory进行开发，删除了其中我们用不到的本地数据库及数据管理相关代码，只保留了mcp相关部分。
> 2）项目内部基于的mem0使用了本地开发代码，为了支持阿里云表格存储服务，这部分代码已提交[pull request](https://github.com/mem0ai/mem0/pull/3151)，待合并后将会更新为官方远程版本。

# 1. 本地运行

## 1.1 下载源码

1. 使用 `git clone` 将代码下载到本地。
2. 进入 python 源码的根目录：`cd tablestore-mcp-server/tablestore-python-mem0-mcp-server`

## 1.2 准备环境

代码需要 `python3.10` 版本以上进行构建，使用了  [`uv`](https://docs.astral.sh/uv) 进行包和环境管理。

安装 uv：

```bash
  # 方式1：使用现有 python3 安装 uv
  pip3 install uv
  # 方式2：源码安装 uv:
  curl -LsSf https://astral.sh/uv/install.sh | sh
```

准备 Python 环境：
> 如果本地有 `python3.10` 版本以上环境，无需执行这一小步。

因为我们项目至少需要 `python3.10` 版本，这里使用 `python3.12` 进行示例。

```bash
  # 查看当前有哪些 python 环境
  uv python list
  # 如果没有python 3.12.x 相关版本，请安装 python3.12 版本. 内部会从 github 下载 uv 官方维护的 python 包。 
  uv python install 3.12
```

创建虚拟环境:

```bash
  # 使用 python 3.12 版本当做虚拟环境
  uv venv --python 3.12
```

## 1.3 配置环境变量

代码里所有的配置是通过环境变量来实现的，出完整的变量见下方表格。 主要依赖的数据库 [Tablestore(表格存储)](https://www.aliyun.com/product/ots) 支持按量付费，使用该工具，表和索引都会自动创建，仅需要在控制台上申请一个实例即可。

| 变量名                                  |                              必填                              |         含义          |         默认值          |
|--------------------------------------|:------------------------------------------------------------:|:-------------------:|:--------------------:|
| SERVER_HOST                          |                             _否_                              |  MCP server 的 host  |       0.0.0.0        |
| SERVER_PORT                          |                             _否_                              |  MCP server 的 port  |         8765         |
| TABLESTORE_INSTANCE_NAME             | <span style="color:red; font-weight:bold;">**是(yes)**</span> |         实例名         |          -           |
| TABLESTORE_ENDPOINT                  | <span style="color:red; font-weight:bold;">**是(yes)**</span> |       实例访问地址        |          -           |
| TABLESTORE_ACCESS_KEY_ID             | <span style="color:red; font-weight:bold;">**是(yes)**</span> |        秘钥 ID        |          -           |
| TABLESTORE_ACCESS_KEY_SECRET         | <span style="color:red; font-weight:bold;">**是(yes)**</span> |      秘钥 SECRET      |          -           |
| TABLESTORE_STS_TOKEN                 |                             _否_                              |      STS Token      |         None         |
| TABLESTORE_VECTOR_DIMENSION          |                             _否_                              |        向量维度         |         1536         |
| OPENAI_API_KEY                       | <span style="color:red; font-weight:bold;">**是(yes)**</span> |     大模型的API_KEY     |          -           |
| OPENAI_BASE_URL                      | <span style="color:red; font-weight:bold;">**是(yes)**</span> |    大模型的BASE_URL     |          -           |
| LLM_MODEL                            |                             _否_                              |      大语言模型的名字       |      qwen-plus       |
| EMBEDDER_MODEL                       |                             _否_                              |       编码模型的名字       |  text-embedding-v4   |
| TOOL_ADD_MEMORIES_DESCRIPTION        |                             _否_                              |  添加记忆的MCP TOOL描述文字  |    参考settings.py     |
| TOOL_SEARCH_MEMORIES_DESCRIPTION     |                             _否_                              |  检索记忆的MCP TOOL描述文字  |    参考settings.py     |
| TOOL_LIST_MEMORIES_DESCRIPTION       |                             _否_                              | 显示所有记忆的MCP TOOL描述文字 |    参考settings.py     |
| TOOL_DELETE_ALL_MEMORIES_DESCRIPTION |                             _否_                              | 删除所有记忆的MCP TOOL描述文字 |    参考settings.py     |
| MCP_STDIO_USER_ID                    |                             _否_                              |   stdio模式下使用的用户id   |  stdio_default_user  |
| MCP_STDIO_CLIENT_NAME                |                             _否_                              |   stdio模式下使用的客户端名   | stdio_default_client |

其中，需要注意LLM_MODEL（大语言模型的名字）的设置，该字段将决定mem0能否顺利运行

因大模型的返回具有不确定性，若模型选择不当，可能导致程序内部，部分结果无法正确解析，出现报错，目前测试qwen-max-0125也可以正常运行

## 1.4 运行 MCP 服务

本MCP服务器，支持两种启动方式，分别是sse模式和stdio模式，本文档，将基于Cline进行运行演示

### 1.4.1 sse模式

sse模式，支持用户通过url进行访问，所以可以在服务器运行时，通过修改mcp客户端绑定的url，实现修改客户端名和用户名，指定mcp tool操作的范围

#### 启动方式：

首先，配置相关环境变量，并启动mcp服务

```bash
   # 加速下载 Hugging 的 Embedding Model
   export OPENAI_API_KEY=xx
   export OPENAI_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
    
   export TABLESTORE_ACCESS_KEY_ID=xx
   export TABLESTORE_ACCESS_KEY_SECRET=xx
   export TABLESTORE_ENDPOINT=xxx
   export TABLESTORE_INSTANCE_NAME=xxx
   
    uv run tablestore-mcp-server --transport=sse
```

随后，在Cline中配置如下信息：

<img src="./docs/img/sse_mcp配置信息.png" alt="sse_mcp配置信息" width="500">

其中，url可以根据个人需要进行修改，格式如下：

`http://localhost:8765/mcp/{client_name}/sse/{user_id}`

若不需要自动触发工具，可以在配置中去掉`autoApprove`字段

#### 运行效果：

触发add_memories工具

<img src="./docs/img/sse触发add操作语句.png" alt="sse触发add操作语句" width="500">

mcp服务器返回以下信息

<img src="./docs/img/sse触发add后服务器返回.png" alt="sse触发add后服务器返回" width="500">

此时，表格存储实例内容如下：

<img src="./docs/img/sse后表格存储实例.png" alt="sse后表格存储实例" width="1000">

<img src="./docs/img/sse触发add后实例中记忆详细信息.png" alt="sse触发add后实例中记忆详细信息" width="500">

可以看到记忆对应正确的客户端名和用户名

### 1.4.2 stdio模式

#### 启动方式：

在Cline中，配置如下信息：

<img src="./docs/img/stdio_mcp配置信息.png" alt="stdio_mcp配置信息" width="500">

#### 运行效果

<img src="./docs/img/stdio触发add.png" alt="stdio触发add" width="500">

此时，表格存储实例内容如下：

<img src="./docs/img/stdio触发add后实例中记忆详细信息.png" alt="stdio触发add后实例中记忆详细信息" width="500">

可以看到存储了stdio模式下，默认的客户端名和用户名

# 2 跨应用与模型访问

由于，mem0将用户相关记忆存储于表格存储实例中，我们可以实现跨应用模型访问相同记忆

## 2.1 简单访问之前插入信息

前述过程中，我们使用Cline作为mcp客户端，同时使用qwen-coder-plus作为语言生成模型

<img src="./docs/img/cline使用的mcp语言模型.png" alt="cline使用的mcp语言模型" width="500">

现在改用cherry studio，同时将qwen-max作为语言生成模型

<img src="./docs/img/跨应用访问示例.png" alt="跨应用访问示例" width="500">

## 2.2 复杂应用场景

首先在Cline中，使用qwen-coder-plus作为语言生成模型，添加一些用户偏好

<img src="./docs/img/复杂应用场景偏好添加.png" alt="复杂应用场景偏好添加" width="500">

随后，在cherry studio中，利用qwen-max进行周末外出游玩计划制定

<img src="./docs/img/复杂应用场景游玩计划制定.png" alt="复杂应用场景游玩计划制定" width="500">

可以看到成功跨应用访问了用户相关记忆，制定了一份依赖于用户的，个性化的游玩方案

依赖此能力，我们可以灵活地使用各种模型及应用对相同的信息进行处理，无需局限于同一应用及模型，用户可以在阿里云表格存储中持久化的存储个人相关的记忆信息，更加个性化的使用大模型

# 3 拓展应用场景
MCP 的 Tool 的能力和场景是 Tool 的描述来提供的，因此我们可以定义一些特殊的能力，可以发挥你的想象力。

仅需要修改如下配置即可, 如何写可以参考 [settings.py](src/tablestore_openmemory_mcp/settings.py)

```shell
  export TOOL_ADD_MEMORIES_DESCRIPTION="你的自定义的描述"
  export TOOL_SEARCH_MEMORIES_DESCRIPTION="你的自定义的描述"
  export TOOL_LIST_MEMORIES_DESCRIPTION="你的自定义的描述"
  export TOOL_DELETE_ALL_MEMORIES_DESCRIPTION="你的自定义的描述"
```