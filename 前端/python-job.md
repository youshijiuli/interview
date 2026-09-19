## 前端知识之 jQuery、Ajax、JsonP等

### rgba()和opacity的透明效果有什么不同？  
答案： rgba()和opacity都能实现透明效果，但最大的不同是opacity作用于元素，以及元素内的所有内容的透明度，  
而rgba()只作用于元素的颜色或其背景色。（设置rgba透明的元素的子元素不会继承透明效果！）  

### px和em的区别？  
px和em都是长度单位，区别是，px的值是固定的，指定是多少就是多少，计算比较容易。em得值不是固定的，并且em会继承父级元素的字体大小。  
浏览器的默认字体高都是16px。所以未经调整的浏览器都符合: 1em=16px。那么12px=0.75em, 10px=0.625em。  

### javascript：获取所有的checkbox？  
```javascript
var domList = document.getElementsByTagName(‘input’)    
// checkbox属于input，所以通过getElementsByTagName即标签名获取所有的input数组，包含文本框text，单选按钮radio，复选框checkbox等等  
var checkBoxList = [];  // 定义一个存储checkbox的空数组  
var len = domList.length;　　//缓存到局部变量  // 第一步获取的数组的长度  
while (len--) {　　//使用while的效率会比for循环更高   // 开始循环判断  
　　if (domList[len].type == ‘checkbox’) {   // 如果类型为checkbox即为题目所需的复选框  
  　　checkBoxList.push(domList[len]);          // 就把那个元素加入到上面定义的数组中  
　　}    
}  
```

用js实现随机选取10–100之间的10个且不重复的数字，存入一个数组。  
```javascript
var randoms=[];  
while (true)  
{  
    var isExists = false;  
    // 获取一个10–100范围的数  
    var random = parseInt(10 + (90 - 10) * (Math.random()))  
    // 判断当前随机数是否已经存在  
    for (var i = 0; i < randoms.length; i++) {  
        if (random === randoms[i]) {  
            isExists = true;  
            break;  
        }  
    }  
    // 如果不存在，则添加进去  
    if (!isExists)  
        randoms.push(random);  
    // 如果有10位随机数了，就跳出  
    if (randoms.length === 10)  
        break;  
}  
```

### window.onload与\$(document).ready()异同  
原生JS的`window.onload`与Jquery的`$(document).ready(function(){})`有什么不同？如何用原生JS实现Jq的ready方法？  
`window.onload()`方法是必须等到页面内包括图片的所有元素加载完毕后才能执行。  
`$(document).ready()`是DOM结构绘制完毕后就执行，不必等到加载完毕。`$(document).ready(function(){})`能够简写成`$(function(){})`。  

### JS作用域  
1. JS以函数作为作用域  
2. 函数的作用域在未调用之前就已经创建  
3. 函数的作用域存在作用域链，并且也是在未调用之前创建  
4. 函数内局部变量提前声明  

### 以下代码的输出是什么?  
```javascript
function t1(age){  
    console.log(age);  
    var age = 27;  
    console.log(age);  
    function age(){};  
    console.log(age);  
}  
t1(3)  
// 答案 function age() 27 27  
```

### 你为什么要使用jquery？  
因为jQuery是轻量级的框架，它有强大的选择器，出色的DOM操作的封装，有可靠的事件处理机制(jQuery在处理事件绑定的时候相当的可靠)，完善的ajax(它的ajax封装的非常的好，不需要考虑复杂浏览器的兼容性和XMLHttpRequest对象的创建和使用的问题。) 出色的浏览器的兼容性。而且支持链式操作，隐式迭代。行为层和结构层的分离，还支持丰富的插件，jquery的文档也非常的丰富。  

### 讲一下jquery有哪些选择器？  
jQuery中的选择器大致分为:基本选择器，层次选择器，过滤选择器，表单选择器  

### 你是如何使用jquery中的ajax的？  
如果是一些常规的ajax程序的话，使用`load()`,`$.get()`,`$.post()`,就可以搞定了，一般我会使用的是`$.post()` 方法。如果需要设定beforeSend(提交前回调函数),error(失败后处理),success(成功后处理)及complete(请求完成后处理)回调函数等，这个时候我会使用\$.ajax()  

### `jquery中$.get()`提交和`$.post()`提交有区别吗？  
`$.get()` 方法使用GET方法来进行异步请求的。`$.post()` 方法使用POST方法来进行异步请求的。  
get请求会将参数跟在URL后进行传递，而POST请求则是作为HTTP消息的实体内容发送给Web服务器的，这种传递是对用户不可见的。  
get方式传输的数据大小不能超过2KB 而POST要大的多  
GET 方式请求的数据会被浏览器缓存起来，因此有安全问题。  

### 在jquery中你是如何去操作样式的？  
addClass() 来追加样式 ，removeClass() 来删除样式，toggle() 来切换样式, css直接设置样式  
style设置单个样式  

### 你在jquery中使用过哪些插入节点的方法，它们的区别是什么？  
append(),appendTo(),prepend(),prependTo(),after(),insertAfter()，before(),insertBefore() 大致可以分为 内部追加和外部追加append() 表式向每个元素内部追加内容。appendTo()表示 讲所有的元素追加到指定的元素中。例\$(A)appendTo(B) 是将A追加到B中下面的方法解释类似。  

你使用过包裹节点的方法吗，包裹节点有方法有什么好处？  
wrapAll(),wrap(), wrapInner()需要在文档中插入额外的结构化标记的时候可以使用这些包裹的方法应为它不会帛画原始文档的语义  

### jquery中如何来获取或和设置属性？  
jQuery中可以用attr()方法来获取和设置元素属性removeAttr() 方法来删除元素属性  

### 如何来设置和获取HTML 和文本的值？  
html()方法 类似于innerHTML属性 可以用来读取或者设置某个元素中的HTML内容  
注意：html() 可以用于xhtml文档 不能用于xml文档text() 类似于innerText属性 可以用来读取或设置某个元素中文本内容。val() 可以用来设置和获取元素的值  

### jquery中有哪些方法可以遍历节点  
children() 取得匹配元素的子元素集合,只考虑子元素不考虑后代元素 next() 取得匹配元素后面紧邻的同辈元素  
prev() 取得匹配元素前面紧邻的同辈元素  
siblings() 取得匹配元素前后的所有同辈元素  
closest() 取得最近的匹配元素  
find() 取得匹配元素中的元素集合 包括子代和后代  

### radio单选组的第二个元素为当前选中值，该怎么去取？  
```javascript
$('input[name=items]').get(1).checked = true;  
```

### 你知道jQuery中的事件冒泡吗，它是怎么执行的，何如来停止冒泡事件  
知道,事件冒泡是从里面的往外面开始触发。在jQuery中提供了stopPropagation()方法可以停止冒泡。  

### 在jquery中你有没有编写过插件，插件有什么好处？它应该注意那些？  
a) 插件的好处：对已有的一系列方法或函数的封装，以便在其他地方重新利用，方便后期维护和提高开发效率插件的分类：封装对象方法插件 、封装全局函数插件、选择器插件  
b) 注意的地方：  
1. 插件的文件名推荐命名为`jquery.[插件名].js`，以免和其他的javaScript库插件混淆  
2. 所有的对象方法都应当附加到`jQuery.fn`对象上，而所有的全局函数都应当附加到jQuery对象本身上  
3. 插件应该返回一个jQuery对象，以保证插件的可链式操作  
4. 避免在插件内部使用\$作为jQuery对象的别名,而应使用完整的jQuery来表示，这样可以避免冲突或使用闭包来避免  
5. 所有的方法或函数插件，都应当一分好结尾，否则压缩的时候可能出现问题。在插件头部加上分号，这样可以避免他人的不规范代码给插件带来影响  
6. 在插件中通过`$.extent({})`封装全局函数,选择器插件，扩展已有的object对象通过`$.fn.extend({})`封装对象方法插件  

## Ajax相关  

### Ajax相关知识点  
Iframe伪造Ajax请求  
FormData对象以及Ajax文件上传  
Iframe文件上传  
JSONP实现AJax跨域  

### XMLHttpRequest对象发送请求  
Ajax和XMLHttpRequest  
从上面的解释中可以知道：ajax是一种技术方案，但并不是一种新技术。它依赖的是现有的CSS/HTML/Javascript，而其中最核心的依赖是浏览器提供的XMLHttpRequest对象，是这个对象使得浏览器可以发出HTTP请求与接收HTTP响应。  
所以我用一句话来总结两者的关系：我们使用XMLHttpRequest对象来发送一个Ajax请求。  

### 什么是JSONP？  
由于同源策略的限制，XmlHttpRequest只允许请求当前源（域名、协议、端口）的资源，为了实现跨域请求，可以通过在页面动态创建script标签，通过通过src属性实现跨域请求，然后在服务端输出JSON数据并执行回调函数，从而解决了跨域的数据数据传输。  

### ajax与jsonp跨域请求的异同再做一些补充说明：  
1、ajax和jsonp这两种技术在调用方式上“看起来”很像，目的也一样，都是请求一个url，然后把服务器返回的数据进行处理，因此jquery和ext等框架都把jsonp作为ajax的一种形式进行了封装；  
2、但ajax和jsonp其实本质上是不同的东西。ajax的核心是通过XmlHttpRequest获取非本页内容，而jsonp的核心则是动态添加`<script>`标签来调用服务器提供的js脚本。  
3、所以说，其实ajax与jsonp的区别不在于是否跨域，ajax通过服务端代理一样可以实现跨域，jsonp本身也不排斥同域的数据的获取。  
4、还有就是，jsonp是一种方式或者说非强制性协议，如同ajax一样，它也不一定非要用json格式来传递数据，如果你愿意，字符串都行，只不过这样不利于用jsonp提供公开服务。  
总而言之，jsonp不是ajax的一个特例，哪怕jquery等巨头把jsonp封装进了ajax，也不能改变着一点！  

### 浅谈session实现原理(阿里面试题)  
现在一般采用使用服务器端产生的Session结合浏览器的Cookie来识别用户和存储数据,  
一般来说包括以下4个步骤：  
1. 服务器端的产生Session ID（一般可以使用UUID模块）  
2. 服务器端和客户端存储Session ID  
3. 从HTTP Header中提取Session ID(发送的是一个COOKIC值)  
4. 根据Session ID从服务器端的Hash中获取请求者身份信息  

### cookie机制和session机制的区别  
cookie保存在客户端，而session保存在服务器端  
cookie上的数据需要来回传输到服务器上,session会消耗服务器的性能  
安全性要求不是很高的用户数据一般采用cookies,敏感数据使用session
