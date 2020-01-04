$(function(){
	//截取id
	var locat=location.href,
		s=locat.indexOf("?");
		t=locat.substring(s+1);
		arr=t.split("=");
		aid=arr[1];
	$.ajax({
		url:'http://127.0.0.1/sudo/article/'+aid,
		type:'get',
        success:function(e){
        	console.log(e);
        	var datas=e.article;

        	//姓名
        	var name=datas.title;
        	$('#title').val(name);
        	//邮箱
        	var email=datas.content;
        	$('#content').val(email);

        	var id=datas.id;
        	xg(id);

        },
        error:function(){
        	alert("失败");
        }
	})
	//点击修改
function xg(ids){
	var obj={};
	$('#ktzh').on('click',function(){
		var name=$('#name').val(),
			email=$('#email').val(),
			phone=$('#phone').val(),
			wechat=$('#wechat').val();

		//公共

		if(name!==''){
			obj.name=name;
		}else{
			if(obj.name){
				delete obj.name;
			}
		}
		if(email!==''){
			obj.email=email;
		}else{
			if(obj.email){
				delete obj.email;
			}
		}
		if(phone!==''){
			obj.phone=phone;
		}else{
			if(obj.phone){
				delete obj.phone;
			}
		}
		if(wechat!==''){
			obj.wechat=wechat;
		}else{
			if(obj.wechat){
				delete obj.wechat;
			}
		}



		console.log(obj);
		ajaxData(obj,ids)
	})
	}

	function ajaxData(obj,aid){
		$.ajax({
			url:'http://127.0.0.1/sudo/articles/'+aid,
			data: JSON.stringify(obj),
			type:'post',
            dataType: 'json',
            contentType:'application/json',
			success:function(e){
				console.log(e);
				location.href='./article_list.html';
			},
			error:function(){
				alert('获取数据失败');
			}
		})
	}

})