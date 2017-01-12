# July

七月，一个用`python3`中的`Django`框架实现的简单小博客，没事自己拿来玩，欢迎指导！

[Demo](https://blog.ansheng.me/)

## Create a new post

``` bash
[root@July ~]# virtualenv July
[root@July July]# source bin/activate
(July) [root@July July]# git clone https://github.com/anshengme/July.git
(July) [root@July July]# cd July/
(July) [root@July July]# pip install -r requirements.txt
(July) [root@July July]# python manage.py makemigrations
(July) [root@July July]# python manage.py migrate
(July) [root@July July]# python manage.py runserver
```

![blog](https://github.com/anshengme/July/raw/master/doc/blog.png)

