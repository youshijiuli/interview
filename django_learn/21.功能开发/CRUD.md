# CRUD操作

## 基本的增删改查操作

#### 1. 查：

```python
def object_list(request):
  object_list = models.Student.objects.all()
  return render(request,'object_list.html',{'object_list':object_list})
```



#### 2. 增





## 模态对话框的增删改查

也就是点击增加的时候，弹出对话框，矿体内容就是一个表单，编辑也是如此；删除就弹出对话框，显示是否删除，下面两个按钮。













## 动态特效

详情查看：[Bootstrap-sweetalert项目](https://github.com/lipis/bootstrap-sweetalert)。

#### 删除操作

见桌面插件`plugins`

一半情况下，可能就会是路由跳转，下面介绍一种方式：

需要使用两个文件：

```
swal.js
wasl.css
```



```html
<td>
	<a href="{% url 'edit_book' book.id %}" class="btn btn-warning">编辑</a>
	<a href="{% url 'del_book' book_id=book.id %}" class="btn btn-danger">删除</a>
	<button class="btn btn-danger ajax_sub" xx="{{ book.pk }}">ajax删除</button>
	<a href="{% url 'del_book' book.id %}" class="btn btn-danger">删除</a>
</td>

    <script>
        console.log('hahhahahah')
    $(".ajax_del").click(function () {
        console.log(111111)
            var book_id = $(this).attr('xx');  //获取xx属性对应的值
            var ths = $(this); // 保存一下这个this
            swal({
                title: "are you sure？",
                text: "开弓没有回头箭!",
                type: "warning",
                showCancelButton: true,
                confirmButtonClass: "btn-danger",
                confirmButtonText: "确认删除",
                cancelButtonText: "容我三思",
                closeOnConfirm: false
            }, function (isConfirm) {


                console.log(isConfirm,'.....')


                if (isConfirm) {
                    // 确认删除才发送网络请求
                    $.ajax({
                    type:'get',
                    url:'/ajax_del_book/' + `${book_id}` + '/',  // http://127.0.0.1:8000/ajax_del_book/1/
                    success:function (res){
                        console.log(res,'--------')
                        if (res.status === 1){
                            swal("删除成功!", "该条记录已被删除", "success");
                            ths.parent().parent().remove();
                        }else {
                            swal("删除失败", "删除动作有有误!", "error");
                        }

                    },

                })
                    swal("删除成功!", "该条记录已被删除", "success");
                } else {
                    {#用户三思，就关闭弹窗#}
                    swal("删除失败", "删除动作有有误!", "error");
                }
            })

        });


    </script>
```



`views.py`

```python
def ajax_del_book(request, *args, **kwargs):
    print(args)
    print(kwargs)
    """
    ()
    {'bid': 6}
    """
    dic = {'status': 0, 'msg': '删除失败'}

    bid = kwargs.get('bid')

    try:
        book_obj = models.Book.objects.get(pk=bid)
        book_obj.delete()
        dic['status'] = 1
        dic['msg'] = '删除成功'
    except Exception as error:
        dic['detail'] = error

    return JsonResponse(dic)

```

