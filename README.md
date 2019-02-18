# yuehu
 这个是我自己博客的后端源码，有兴趣的可以参考一下，自己动手建立属于自己的博客，欢迎前来交流。
 博客地址[点击这里](https://www.python-dog.com/) 博客采用前后端分离方式实现，服务器都是腾讯、阿里打折促销时候买的，不在同一个地区，所以可能会有些慢。
 
## 1.为什么叫yuehu?
"温故而知新，不亦说乎，有朋自远方来，不亦说乎。"
编写博客温习旧的知识，和喜欢相同技术的朋友讨论也是很快乐的事情。

## 2. docker化项目（都是些常用命令，方便使用）

### docker build

docker build -t yuehu:1.0 -f Dockerfile ./

### local

docker run --name yuehu -it --link mysql:mysql --link redis:redis --link redis_session:redis_session -e DJANGO_LOCAL_SETTING=local -e GITHUB_CLINT_ID=$GITHUB_CLINT_ID -e GITHUB_CLINT_SECRET=$GITHUB_CLINT_SECRET -e WEIBO_CLINT_ID=$WEIBO_CLINT_ID -e WEIBO_CLINT_SECRET=$WEIBO_CLINT_SECRET -v $PWD:/src -p 8000:8000 yuehu:1.0 sh run_local.sh

### docker run
docker run --name yuehu -d --link mysql:mysql --link redis:redis -e DJANGO_LOCAL_SETTING=docker -e GITHUB_CLINT_ID=$GITHUB_CLINT_ID -e GITHUB_CLINT_SECRET=$GITHUB_CLINT_SECRET -e WEIBO_CLINT_ID=$WEIBO_CLINT_ID -e WEIBO_CLINT_SECRET=$WEIBO_CLINT_SECRET -v $PWD:/src -p 8000:8000 yuehu:1.0 sh run_docker.sh

## 3. jenkins
test branch is develop

## 4. 项目改造
（想要在自己数据库存储Emoji表情可以这么做）
1.数据库字符编码由utf8mb4改为utf8mb4 以支持真正的utf8字符集
tip:全环境都要更改
（想要项目普通缓存与session分开存储可以这么做，配置中有）
2.session 和 项目cache 分开存储 分成两个redis（19.01.11)
tip:只有正式环境和本地改造 暂时测试可以不这么分
 
 
## 5. 查看消息执行结果
docker run --name yuehu_flower -it --link redis:redis -e DJANGO_LOCAL_SETTING=local -v $PWD:/src -p 5555:5555 yuehu:1.0 sh

pip install flower -i https://pypi.tuna.tsinghua.edu.cn/simple/

celery -A celery_yuehu flower --port=5555 --host=0.0.0.0
