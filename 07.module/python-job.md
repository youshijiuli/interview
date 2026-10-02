## Python基础知识

### Python里面search()和match()的区别  
match()函数只检测RE是不是在string的开始位置匹配, search()会扫描整个string查找匹配  

### 用Python匹配HTML tag的时候，`<.*>`和`<.*?>`有什么区别  
贪婪和非贪婪 *号是一个量词 量词后面加? 号表示 非贪婪,也就是尽可能少的匹配
