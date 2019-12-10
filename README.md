# 使用遗传算法解决TSP问题
本文完成主要完成了三个算法
* 一个算法`./mywork/`来自一篇论文[3],我对其中算法的实现做了改进,发现其中提出的CX2算法存在漏洞,所以导致目前项目停滞;
* 一个算法`./simple_baseline/`,是我对网上的一篇文章[4]进行完善,效率不高;
* 第三个算法就是geatpy库带的算法`./tsp_test/`。

## mywork
### 运行

`python TSP_origin.py --filename data/a280.tsp --answer_filename ./data/a280.opt.tour --show_figure --pop_size 100  --elite_size 20  --generations 10000 --mutation_rate 0.01`

### 种群表示

* `City` 城市对象，由(x,y)坐标表示
* `Fitness`适应度对象，封装了一条路线的适应度和长度等方法

* `population` 个体，一条路线，表示方法：[(x1,y1),(x2,y2),...]
* `pop` 种群，若干条路线

### 进化过程

* `popRanked` 种群内个体按适应度排序后的结果[(个体序号1，适应度1)，...]
* `selectedResults` 种群进行选择后的序号表示[个体序号1，个体序号2，...]
* `matingpool` [个体1，个体2，...]
* 



### Bug记录

* 致命的错误：算法本省原理不能解决所有情况，当出现：P1=[4 1 2 3 0],P2=[3 4 0 1 2]这种情况，运行：

  O1 = (3,x,x,x,x)

  O2 = (4,x,x,x,x)

  接下来算法无法对其进行应对，因此程序生成的子染色体有大量相同节点，后续计算完全错误！归纳出这种情况是：O1,O2均出现P2，P1对应节点，且两节点不相同，则无法继续向下进行交叉运算，因此，这里提出一个简单的**解决方法**：将O1，O2添加上对方节点，于是变成：

  O1 = (3,4,x,x,x)

  ### O2 = (4,3,x,x,x),算法构成了一个环，则继续向下计算即可
## geatpy
参考官方tsp源码

[1]. Wikipedia https://zh.wikipedia.org/wiki/遗传算法

[2]. Wikipedia https://zh.wikipedia.org/wiki/旅行推销员问题

[3].https://github.com/mehdirazarajani/Genetic-Algorithm-for-Traveling-Salesman-Problem-with-Modified-Cycle-Crossover-Operator-Report 

[4].https://towardsdatascience.com/evolution-of-a-salesman-a-complete-genetic-algorithm-tutorial-for-python-6fe5d2b3ca35
