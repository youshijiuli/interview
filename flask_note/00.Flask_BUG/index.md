# flask报错

在运行项目的时候有很多报错：这个文件就是收集到的报错信息以及解决



1. 由于版本原因，无法从`werkzeug`中导入`url_quote`，修改如下所示：

```python
# from werkzeug.urls import url_quote
from urllib.parse import quote as url_quote
```



2. 也是模块导入问题，解决方案如下：

```python
# from flask._compat import text_type
from flask_script._compat import text_type
```



3. 模块导入问题

> from werkzeug.urls import url_parse
> ImportError: cannot import name 'url_parse' from 'werkzeug.urls' 



解决方案：降低版本：`pip install Werkzeug==2.2.2`



4. 模块导入问题

>  from werkzeug import secure_filename, FileStorage
> ImportError: cannot import name 'secure_filename' from 'werkzeug'

解决方案：

```python
# from werkzeug import secure_filename, FileStorage
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
```

