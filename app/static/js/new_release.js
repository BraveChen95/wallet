
//px转换为rem
(function(doc, win) {
    var docEl = doc.documentElement,
        resizeEvt = 'orientationchange' in window ? 'orientationchange' : 'resize',
        recalc = function() {
            var clientWidth = docEl.clientWidth;
            if (!clientWidth) return;
            if (clientWidth >= 640) {
                docEl.style.fontSize = '100px';
            } else {
                docEl.style.fontSize = 100 * (clientWidth / 640) + 'px';
            }
        };

    if (!doc.addEventListener) return;
    win.addEventListener(resizeEvt, recalc, false);
    doc.addEventListener('DOMContentLoaded', recalc, false);
})(document, window);

    function imgChange(obj1, obj2) {
        //获取点击的文本框
        var imgCount=($(".z_addImg").length + 1);
        if (imgCount<=5){
        var file = document.getElementById("file");
        //存放图片的父级元素
        var imgContainer = document.getElementsByClassName(obj1)[0];
        //获取的图片文件
        var fileList = file.files;
        //文本框的父级元素
        var input = document.getElementsByClassName(obj2)[0];
        var imgArr = [];
        var name = []
        //遍历获取到得图片文件
        for (var i = 0; i < fileList.length; i++) {


            var imgUrl = window.URL.createObjectURL(file.files[i]);

            imgArr.push(imgUrl);
            var img = document.createElement("img");
            img.setAttribute("name", file.files[i]["name"]);
            img.setAttribute("src", imgArr[i]);

            var imgAdd = document.createElement("div");

            name.unshift(file.files[i]["name"]);
            imgAdd.setAttribute("class", "z_addImg");
            imgAdd.appendChild(img);
            imgContainer.appendChild(imgAdd);
            console.log(name)
        };
        imgRemove();
        }
        else{
            alert('不能超过5张')
        }
    };

    function imgRemove() {
        var imgList = document.getElementsByClassName("z_addImg");
        var mask = document.getElementsByClassName("z_mask")[0];
        var cancel = document.getElementsByClassName("z_cancel")[0];
        var sure = document.getElementsByClassName("z_sure")[0];
        console.log(imgList)
        for (var j = 0; j < imgList.length; j++) {
            imgList[j].index = j;
            imgList[j].onclick = function() {
                var t = this;
                mask.style.display = "block";
                cancel.onclick = function() {
                    mask.style.display = "none";
                };
                sure.onclick = function() {
                    mask.style.display = "none";
                    t.remove();
                };

            }
        };
    };

$(function(){
    var picture=[]
    var obj = {}
    $("#upload").on("click", function(){
        var title=$("#biaoti").val(),
        article=$(".textarea").val();
        $("div[class=z_addImg] img").each(function() {
        var src=$(this).attr("name");
        picture.push(src)
        });
        obj.title=title;
        obj.article=article;
        obj.picture=picture;
        $.ajax({
            url:"http://127.0.0.1:5000/user",
            data: JSON.stringify(obj),
            type:"post",
            dataType: 'json',
            contentType:'application/json',
            success:function(e){
                location.href='./new_release.html';
            },
             error:function(jqXHR,textStatus,errorThrown){
					alert(errorThrown);
			}

        })
    })
})
