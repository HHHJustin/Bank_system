操作

* 進入 postgre 切換成管理員帳號
$ sudo su postgre 
* 創建database
$ createdb db名稱
* 使用database
$ psql db名稱
* 創建Table
$ create table Table名稱(欄位名稱 資料型態...);
* delete database
$ dropdb db名稱
* delelte table
$ drop table <table_name>

# 可利用 .sql儲存Table初始話模板 再利用 \i xxx.sql引入