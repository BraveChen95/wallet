$(function(){
	//截取id
	var locat=location.href,
		s=locat.indexOf("?"); 
		t=locat.substring(s+1);
		arr=t.split("=");
		aid=arr[1];
	$.ajax({
		url:'http://127.0.0.1/sudo/admins/'+aid,
		type:'get',
        success:function(e){
        	console.log(e);
        	var datas=e.admin;

        	//姓名
        	var name=datas.name;
        	$('#name').val(name);
        	//邮箱
        	var email=datas.email;
        	$('#email').val(email);
        	//手机号
        	var phone=datas.phone;
        	$('#phone').val(phone);
        	//微信号
        	var wechat=datas.wechat;
        	$('#wechat').val(wechat);
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
			url:'http://127.0.0.1/sudo/admins/'+aid,
			data: JSON.stringify(obj),
			type:'post',
            dataType: 'json',
            contentType:'application/json',
			success:function(e){
				console.log(e);
				location.href='./admin_list.html';
			},
			error:function(){
				alert('获取数据失败');
			}
		})
	} 

})