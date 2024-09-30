<!--
****************
** Guidelines **
****************

**Chosen Approach:**

The **Quick Start Guide Focused README** is the most promising for optimizing the time to first workflow. It allows developers to get hands-on experience quickly, which is essential for engagement and understanding.

* * *

**Outline for the README:**

1.  **Title and Badges**
    *   Julep Logo or Title
    *   Build status, npm version, license badges
2.  **Introduction**
    *   _Briefly explain what Julep is and its purpose._
    *   Emphasize how it simplifies building persistent AI agents with workflows.
3.  **Features**
    *   _Highlight key features with a focus on "tasks" (AI workflows)._
    *   Mention support for persistent sessions, tool integration, and document management.
4.  **Installation**
    *   _Provide npm installation command:_
        
        bash
        
        Copy code
        
        `npm install julep`
        
5.  **Quick Start Guide**
    *   **Step 1: Import Julep**
        *   _Show how to import Julep into a project._
            
            javascript
            
            Copy code
            
            `const Julep = require('julep');`
            
    *   **Step 2: Initialize the Agent**
        *   _Guide on creating a new agent with basic settings._
            
            javascript
            
            Copy code
            
            `const agent = new Julep.Agent({  name: 'MyAgent',  model: 'gpt-4-turbo', });`
            
    *   **Step 3: Chat with the Agent**
        *   _Provide a simple example of a chat with the agent._
            
            javascript
            
            Copy code
            
            `const response = await client.sessions.chat({  session_id: session.id,  message: 'Hello, how are you?' });`   
            
    *   **Step 4: Create a multi-step Task**
        *   _Provide a simple example of a task definition._
            
            javascript
            
            Copy code
            
            `const task = {  name: 'GreetingTask',  main: [    {      prompt: 'Say hello to the user.',    },  ], }; agent.addTask(task);`
            
    *   **Step 5: Execute the Task**
        *   _Show how to run the task and handle the output._
            
            javascript
            
            Copy code
            
            `agent.executeTask('GreetingTask').then((output) => {  console.log(output); });`
            
6.  **Understanding Tasks**
    *   _Explain what tasks are and how they function within Julep._
    *   Describe different types of workflow steps.
        *   Prompt, Tool Call, Evaluate, etc.
    *   _Note:_ Link to detailed documentation for each step type.
7.  **Advanced Features**
    *   _Briefly mention other capabilities:_
        *   Adding tools to agents.
        *   Managing sessions and users.
        *   Document integration and search.
8.  **API Reference**
    *   _Link to full API documentation._
    *   Mention key endpoints for agents, tasks, and executions.
9.  **Examples and Tutorials**
    *   _Provide links to example projects or further tutorials._
    *   Encourage users to explore and build upon provided examples.
10.  **Contributing**
    *   _Instructions for contributing to the project._
    *   Link to contribution guidelines and code of conduct.
11.  **Support and Community**
    *   _Information on how to get help._
    *   Links to community forums, chat groups, or issue trackers.
12.  **License**
    *   _State the project's license._
    *   Provide a link to the LICENSE file.
13.  **Acknowledgements**
    *   _Credit to contributors and used resources._

* * *

**Notes:**

*   **Code Examples:** Ensure all code snippets are easy to understand and copy-paste ready.
*   **Simplicity:** Keep explanations concise to maintain focus on getting started quickly.
*   **Links:** Include hyperlinks to detailed documentation sections for users who want to delve deeper.
*   **Visuals:** Consider adding diagrams or images to illustrate concepts if possible.
*   **Tone:** Maintain an encouraging and helpful tone throughout the README
-->

<sup>[English](README.md) | 中文</sup>

<div align="center">
    <img src="https://socialify.git.ci/julep-ai/julep/image?description=1&descriptionEditable=快速构建AI工作流和代理&font=Source%20Code%20Pro&logo=https%3A%2F%2Fraw.githubusercontent.com%2Fjulep-ai%2Fjulep%2Fdev%2F.github%2Fjulep-logo.svg&owner=1&pattern=Solid&stargazers=1&theme=Auto" alt="julep" width="640" height="320" />
</div>

<p align="center">
  <br />
  <a href="https://docs.julep.ai" rel="dofollow"><strong>探索文档</strong></a>
  ·
  <a href="https://discord.com/invite/JTSBGRZrzj" rel="dofollow">Discord</a>
  ·
  <a href="https://x.com/julep_ai" rel="dofollow">𝕏</a>
  ·
  <a href="https://www.linkedin.com/company/julep-ai" rel="dofollow">领英</a>
</p>


<p align="center">
    <a href="https://www.npmjs.com/package/@julep/sdk"><img src="https://img.shields.io/npm/v/%40julep%2Fsdk?style=social&amp;logo=npm&amp;link=https%3A%2F%2Fwww.npmjs.com%2Fpackage%2F%40julep%2Fsdk" alt="NPM 版本"></a>
    <span>&nbsp;</span>
    <a href="https://pypi.org/project/julep"><img src="https://img.shields.io/pypi/v/julep?style=social&amp;logo=python&amp;label=PyPI&amp;link=https%3A%2F%2Fpypi.org%2Fproject%2Fjulep" alt="PyPI - 版本"></a>
    <span>&nbsp;</span>
    <a href="https://hub.docker.com/u/julepai"><img src="https://img.shields.io/docker/v/julepai/agents-api?sort=semver&amp;style=social&amp;logo=docker&amp;link=https%3A%2F%2Fhub.docker.com%2Fu%2Fjulepai" alt="Docker 镜像版本"></a>
    <span>&nbsp;</span>
    <a href="https://choosealicense.com/licenses/apache/"><img src="https://img.shields.io/github/license/julep-ai/julep" alt="GitHub 许可证"></a>
</p>


*****

## 🎉🚀 **激动人心的消息：Julep 1.0 Alpha 版发布！** 🚀🎉

我们很高兴地宣布 Julep 1.0 的 alpha 版本发布！🥳

🌟 **新特性：**
- 增强的工作流功能
- 改进的代理持久性
- 扩展的工具集成
- 简化的 API

🧪 试用它并帮助塑造 AI 工作流的未来！

> [!NOTE]
> 在测试阶段，您可以通过 [Discord](https://discord.com/invite/JTSBGRZrzj) 获取 API 密钥。

> [!TIP]
> 🐛 发现了 bug？有建议？我们很乐意听取您的意见！
>   加入我们的 [Discord](https://discord.com/invite/JTSBGRZrzj) 或提交 [issue](https://github.com/julep-ai/julep/issues)。

请继续关注我们即将发布的稳定版本的更多更新！📢

## 简介

Julep 是一个开源平台，用于创建具有可定制工作流的持久 AI 代理。它提供了开发、管理和部署 AI 驱动应用程序的工具，注重灵活性和易用性。

使用 Julep，您可以：
- 快速开发能够在多次交互中保持上下文和状态的 AI 代理
- 设计和执行针对您的 AI 代理定制的复杂工作流
- 无缝集成各种工具和 API 到您的 AI 工作流中
- 轻松管理持久会话和用户交互

无论您是在开发聊天机器人、自动化任务，还是构建复杂的 AI 助手，Julep 都能为您提供所需的灵活性和功能，帮助您快速高效地将想法转化为现实。

<details>
<summary>这里有一个简单的 Python 示例：</summary>

<pre><code class="language-python">
from julep import Julep, AsyncJulep

# 🔑 初始化 Julep 客户端
#     或者使用 AsyncJulep 进行异步操作
client = Julep(api_key="your_api_key")

##################
## 🤖 代理 🤖 ##
##################

# 创建一个研究代理
agent = client.agents.create(
    name="研究代理",
    model="claude-3.5-sonnet",
    about="您是一个设计用于处理研究查询的研究代理。",
)

# 🔍 为代理添加工具
client.agents.tools.create(
    agent_id=agent.id,
    name="web_search",  # 应该是有效的 Python 变量名
    description="使用此工具进行研究查询。",
    integration={
        "provider": "brave",
        "method": "search",
        "setup": {
            "api_key": "your_brave_api_key",
        },
    },
)

#################
## 💬 聊天 💬 ##
#################

# 与代理开始交互式聊天会话
session = client.sessions.create(
    agent_id=agent.id,
    context_overflow="adaptive",  # 🧠 Julep 将在需要时动态计算上下文窗口
)

# 🔄 聊天循环
while (user_input := input("您：")) != "退出":
    response = client.sessions.chat(
        session_id=session.id,
        message=user_input,
    )

    print("代理：", response.choices[0].message.content)


#################
## 📋 任务 📋 ##
#################

# 为代理创建一个周期性研究任务
task = client.tasks.create(
    agent_id=agent.id,
    name="研究任务",
    description="每24小时研究给定的主题。",
    #
    # 🛠️ 任务特定工具
    tools=[
        {
            "name": "send_email",
            "description": "向用户发送包含结果的电子邮件。",
            "api_call": {
                "method": "post",
                "url": "https://api.sendgrid.com/v3/mail/send",
                "headers": {"Authorization": "Bearer YOUR_SENDGRID_API_KEY"},
            },
        }
    ],
    #
    # 🔢 任务主要步骤
    main=[
        #
        # 步骤 1：研究主题
        {
            # `_`（下划线）变量指向上一步的输出
            # 这里，它指向用户输入的主题
            "prompt": "查找主题 '{{_.topic}}' 并总结结果。",
            "tools": [{"ref": {"name": "web_search"}}],  # 🔍 使用代理的网络搜索工具
            "unwrap": True,
        },
        #
        # 步骤 2：发送包含研究结果的电子邮件
        {
            "tool": "send_email",
            "arguments": {
                "subject": "研究结果",
                "body": "'以下是今天的研究结果：' + _.content",
                "to": "inputs[0].email",  # 引用用户输入的电子邮件
            },
        },
        #
        # 步骤 3：等待 24 小时后重复
        {"sleep": "24 * 60 * 60"},
    ],
)

# 🚀 启动周期性任务
client.executions.create(task_id=task.id, input={"topic": "Python"})

# 🔁 这将每 24 小时运行一次任务，
#    研究 "Python" 主题，并
#    将结果发送到用户的电子邮件
</code></pre>
</details>

## 特性

Julep 简化了构建具有可定制工作流的持久 AI 代理的过程。主要特性包括：

- **持久 AI 代理**：创建和管理能够在多次交互中保持上下文的 AI 代理。
- **可定制工作流**：使用任务（Tasks）设计复杂的多步骤 AI 工作流。
- **工具集成**：无缝集成各种工具和 API 到您的 AI 工作流中。
- **文档管理**：高效管理和搜索代理的文档。
- **会话管理**：处理持久会话以实现连续交互。
- **灵活执行**：支持工作流中的并行处理、条件逻辑和错误处理。

## 安装

要开始使用 Julep，请使用 [npm](https://www.npmjs.com/package/@julep/sdk) 或 [pip](https://pypi.org/project/julep/) 安装：

```bash
npm install @julep/sdk
```

或

```bash
pip install julep
```

> [!TIP]
> 在测试阶段，您可以通过 [Discord](https://discord.com/invite/JTSBGRZrzj) 获取 API 密钥。

## 快速入门指南

### 步骤 1：导入 Julep

首先，将 Julep SDK 导入到您的项目中：

```javascript
const Julep = require('@julep/sdk');
```

或

```python
from julep import AsyncJulep
```

### 步骤 2：初始化代理

使用基本设置创建一个新代理：

```javascript
const julep = new Julep({ apiKey: 'your-api-key' });

const agent = await julep.agents.create({
  name: '研究助手',
  model: 'gpt-4-turbo',
  about: "您是一个创意讲故事代理，能够根据想法创作引人入胜的故事并生成漫画面板。",
});
```

或

```python
client = AsyncJulep(api_key="your_api_key")

agent = await client.agents.create(
    name="讲故事代理",
    model="gpt-4-turbo",
    about="您是一个创意讲故事代理，能够根据想法创作引人入胜的故事并生成漫画面板。",
)
```

### 步骤 3：与代理聊天

与代理开始交互式聊天会话：

```javascript
const session = await julep.sessions.create({
  agentId: agent.id,
}); 

// 向代理发送消息
const response = await julep.sessions.chat({
  sessionId: session.id,
  message: '你好，能给我讲个故事吗？',
});

console.log(response);
```

或

```python
session = await client.sessions.create(agent_id=agent.id)

# 向代理发送消息
response = await client.sessions.chat(
    session_id=session.id,
    message="你好，能给我讲个故事吗？",
)

print(response)
```

### 步骤 4：创建多步骤任务

让我们定义一个多步骤任务，根据输入的想法创建故事并生成分镜漫画：

```python
# 🛠️ 为代理添加图像生成工具（DALL·E）
await client.agents.tools.create(
    agent_id=agent.id,
    name="image_generator",
    description="使用此工具根据描述生成图像。",
    integration={
        "provider": "dalle",
        "method": "generate_image",
        "setup": {
            "api_key": "your_dalle_api_key",
        },
    },
)

# 📋 任务
# 创建一个任务，接受一个想法并创建故事和 4 格漫画
task = await client.tasks.create(
    agent_id=agent.id,
    name="故事和漫画创作器",
    description="根据一个想法创作故事并生成 4 格漫画来说明故事。",
    main=[
        # 步骤 1：生成故事并将其概括为 4 个面板
        {
            "prompt": [
                {
                    "role": "system",
                    "content": "您是 {{agent.name}}。{{agent.about}}"
                },
                {
                    "role": "user",
                    "content": (
                        "基于想法 '{{_.idea}}'，写一个适合 4 格漫画的短故事。"
                        "提供故事和一个编号列表，包含 4 个简短描述，每个描述对应一个面板，说明故事中的关键时刻。"
                    ),
                },
            ],
            "unwrap": True,
        },
        # 步骤 2：提取面板描述和故事
        {
            "evaluate": {
                "story": "_.split('1. ')[0].strip()",
                "panels": "re.findall(r'\\d+\\.\\s*(.*?)(?=\\d+\\.\\s*|$)', _)",
            }
        },
        # 步骤 3：使用图像生成器工具为每个面板生成图像
        {
            "foreach": {
                "in": "_.panels",
                "do": {
                    "tool": "image_generator",
                    "arguments": {
                        "description": "_",
                    },
                },
            },
        },
        # 步骤 4：为故事生成一个吸引人的标题
        {
            "prompt": [
                {
                    "role": "system",
                    "content": "您是 {{agent.name}}。{{agent.about}}"
                },
                {
                    "role": "user",
                    "content": "根据以下故事，生成一个吸引人的标题。\n\n故事：{{outputs[1].story}}",
                },
            ],
            "unwrap": True,
        },
        # 步骤 5：返回故事、生成的图像和标题
        {
            "return": {
                "title": "outputs[3]",
                "story": "outputs[1].story",
                "comic_panels": "[output.image.url for output in outputs[2]]",
            }
        },
    ],
)
```

> [!TIP]
> Node.js 版本的代码类似。

### 步骤 5：执行任务

```python
# 🚀 执行任务，输入一个想法
execution = await client.executions.create(
    task_id=task.id,
    input={"idea": "一只学会飞翔的猫"}
)

# 🎉 观看故事和漫画面板的生成过程
await client.executions.stream(execution_id=execution.id)
```

这个例子展示了如何创建一个带有自定义工具的代理，定义一个复杂的多步骤任务，并执行它以生成创意输出。

<!-- TODO: 在 README 中添加展示任务执行过程的 gif -->

> [!TIP]
> 您可以在[这里](example.ts)找到另一个 Node.js 示例，或在[这里](example.py)找到 Python 示例。

## 理解任务

任务是 Julep 工作流系统的核心。它们允许您定义复杂的多步骤 AI 工作流，供您的代理执行。以下是任务组件的简要概述：

- **名称和描述**：每个任务都有唯一的名称和描述，便于识别。
- **主要步骤**：任务的核心，定义了要执行的操作序列。
- **工具**：可选的集成，在任务执行期间扩展代理的能力。

### 工作流步骤类型

Julep 中的任务可以包含各种类型的步骤：

1. **提示**：向 AI 模型发送消息并接收响应。
   ```python
   {"prompt": "分析以下数据：{{data}}"}
   ```

2. **工具调用**：执行集成的工具或 API。
   ```python
   {"tool": "web_search", "arguments": {"query": "最新 AI 发展"}}
   ```

3. **评估**：执行计算或操作数据。
   ```python
   {"evaluate": {"average_score": "sum(scores) / len(scores)"}}
   ```

4. **条件逻辑**：基于条件执行步骤。
   ```python
   {"if": "score > 0.8", "then": [...], "else": [...]}
   ```

5. **循环**：遍历数据或重复步骤。
   ```python
   {"foreach": {"in": "data_list", "do": [...]}}
   ```

| 步骤类型 | 描述 | 输入 |
|---------|------|------|
| **提示** | 向 AI 模型发送消息并接收响应。 | 提示文本或模板 |
| **工具调用** | 执行集成的工具或 API。 | 工具名称和参数 |
| **评估** | 执行计算或操作数据。 | 要评估的表达式或变量 |
| **等待输入** | 暂停工作流直到收到输入。 | 任何所需的用户或系统输入 |
| **日志** | 记录指定的值或消息。 | 要记录的消息或值 |
| **嵌入** | 将文本嵌入到特定格式或系统中。 | 要嵌入的文本或内容 |
| **搜索** | 基于查询执行文档搜索。 | 搜索查询 |
| **获取** | 从键值存储中检索值。 | 键标识符 |
| **设置** | 在键值存储中为键分配值。 | 要分配的键和值 |
| **并行** | 并行运行多个步骤。 | 要同时执行的步骤列表 |
| **遍历** | 遍历集合并为每个项目执行步骤。 | 要遍历的集合或列表 |
| **映射归约** | 对集合进行映射并基于表达式归约结果。 | 要映射和归约的集合和表达式 |
| **如果-否则** | 基于条件执行步骤。 | 要评估的条件 |
| **开关** | 基于多个条件执行步骤，类似于 switch-case 语句。 | 多个条件和相应的步骤 |
| **生成** | 运行子工作流并等待其完成。 | 子工作流标识符和输入数据 |
| **错误** | 通过指定错误消息来处理错误。 | 错误消息或处理指令 |
| **睡眠** | 暂停工作流指定的持续时间。 | 持续时间（秒、分钟等） |
| **返回** | 从工作流返回值。 | 要返回的值 |

有关每种步骤类型的详细信息和高级用法，请参阅我们的[任务文档](https://docs.julep.ai/tasks)。

## 高级功能

Julep 提供了一系列高级功能来增强您的 AI 工作流：

### 为代理添加工具

通过集成外部工具和 API 来扩展代理的能力：

```python
client.agents.tools.create(
    agent_id=agent.id,
    name="web_search",
    description="搜索网络以获取信息。",
    integration={
        "provider": "google",
        "method": "search",
        "setup": {"api_key": "your_google_api_key"},
    },
)
```

### 管理会话和用户

Julep 为持久交互提供了强大的会话管理：

```python
session = client.sessions.create(
    agent_id=agent.id,
    user_id="user123",
    context_overflow="adaptive"
)

# 在同一会话中继续对话
response = client.sessions.chat(
    session_id=session.id,
    message="继续我们之前的对话。"
)
```

### 文档集成和搜索

轻松管理和搜索代理的文档：

```python
# 上传文档
document = client.documents.create(
    file="path/to/document.pdf",
    metadata={"category": "research_paper"}
)

# 搜索文档
results = client.documents.search(
    query="AI 进展",
    filter={"category": "research_paper"}
)
```

有关更多高级功能和详细用法，请参阅我们的[高级功能文档](https://docs.julep.ai/advanced-features)。

## API 参考

探索我们全面的 API 文档，了解更多关于代理、任务和执行的信息：

- [代理 API](https://docs.julep.ai/api/agents)
- [任务 API](https://docs.julep.ai/api/tasks)
- [执行 API](https://docs.julep.ai/api/executions)

## 示例和教程

发现示例项目和教程，帮助您入门并基于提供的示例进行构建：

- [示例项目](https://github.com/julep-ai/julep/tree/main/examples)
- [教程](https://docs.julep.ai/tutorials)

## 贡献

我们欢迎对项目的贡献！了解如何贡献以及我们的行为准则：

- [贡献指南](https://github.com/julep-ai/julep/blob/main/CONTRIBUTING.md)
- [行为准则](https://github.com/julep-ai/julep/blob/main/CODE_OF_CONDUCT.md)

## 支持和社区

加入我们的社区，获取帮助、提问和分享您的想法：

- [Discord](https://discord.com/invite/JTSBGRZrzj)
- [GitHub 讨论](https://github.com/julep-ai/julep/discussions)
- [Twitter](https://twitter.com/julep_ai)

## 许可证

本项目采用 [Apache License 2.0](https://github.com/julep-ai/julep/blob/main/LICENSE) 许可。

## 致谢

们要感谢所有贡献者和开源社区为他们宝贵的资源和贡献。