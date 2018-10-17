## Python 与大数据：Airflow、 Jupyter Notebook 与 Hadoop 3、Spark、Presto


最近几年里，Python 已成为数据科学、机器学习和深度学习领域的一门流行的编程语言。只需再配上查询语言 SQL 即可完成大多数工作。SQL 很棒，用英语即可发出指令，且只需指示想要什么，而无需关心具体如何查询。这使得底层的查询引擎可以不改变 SQL 查询就能对其进行优化。Python 也很棒，它有大量高质量的库，本身也易于使用。

作业编排是执行日常任务并使其自动化的行为。在过去，这通常是通过 CRON 作业完成的。而在最近几年，越来越多的企业开始使用 Apache Airflow 和 Spotify 的 Luigi 等创建更强大的系统。这些工具可以监控作业、记录结果并在发生故障时重新运行作业。如果您有兴趣，我曾写过一篇博客文章，其中包括 Airflow 的背景故事，题为《使用 Airflow 构建数据管道》。

作为数据探索和可视化工具的 Notebooks 在过去几年中也在数据领域变得非常流行。像 Jupyter Notebook 和 Apache Zeppelin 这样的工具旨在满足这一需求。Notebooks 不仅向您显示分析结果，还显示产生这些结果的代码和查询。这有利于发现疏忽并可帮助分析师重现彼此的工作。

Airflow 和 Jupyter Notebook 可以很好地协同工作，您可以使用 Airflow 自动将新数据输入数据库，然后数据科学家可以使用 Jupyter Notebook 进行分析。

在这篇博文中，我将安装一个单节点的 Hadoop，让 Jupyter Notebook 运行并展示如何创建一个 Airflow 作业，它可以获取天气数据源，将其存储在 HDFS 上，再转换为 ORC 格式，最后导出到 Microsoft Excel 格式的电子表格中。

我正在使用的机器有一个主频为 3.40 GHz 的 Intel Core i5-4670K CPU、12 GB 的 RAM 和 200 GB 的 SSD。我将使用全新安装的 Ubuntu 16.04.2 LTS，并根据我的博客文章《Hadoop 3：单节点安装指南》 中的说明构建安装单节点 Hadoop。

### 安装依赖项

接下来将安装 Ubuntu 上的依赖项。 git 包将用于从 GitHub 获取天气数据集，其余三个包是 Python 本身、Python 包安装程序和 Python 环境隔离工具包。




    $ sudo apt install \
        git \
        python \
        python-pip \
        virtualenv

Airflow 将依靠 RabbitMQ 的帮助来跟踪其作业。下面安装 Erlang，这是编写 RabbitMQ 的语言。

    $ echo "deb http://binaries.erlang-solutions.com/debian xenial contrib" | \
        sudo tee /etc/apt/sources.list.d/erlang.list
    $ wget -O - http://binaries.erlang-solutions.com/debian/erlang_solutions.asc | \
        sudo apt-key add -
    $ sudo apt update
    $ sudo apt install esl-erlang

