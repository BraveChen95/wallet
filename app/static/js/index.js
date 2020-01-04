$(function(){
	//后台点击登录把密码加密
	var obj={};
	$('#dls').on('click',function(){
		//获取form值 并把密码加密
		var userName=$('#userName').val(),
	    	password=$('#psw').val(),

       		password=hex_md5(password);
			// $('#psw').val(password);
			obj.username=userName;
			obj.password=password;

			//传送数据
			$.ajax({
				url: window.location.protocol + '//'+ window.location.host + "/sudo/",
				data: JSON.stringify(obj),
				type:"post",
                dataType: 'json',
                contentType:'application/json',
				success:function(e){
					if(e.message=='登陆成功'){

						location.href='./user_list.html';
					}
				},
				error:function(jqXHR,textStatus,errorThrown){
					alert(errorThrown);
				}
			})
	})
	//前台点击登录把密码加密
	$('#dl').on('click',function(){
		var password=$('#psw').val();
        password=hex_md5(password);
		$('#psw').val(password);

	})	
	//错误提示框消失
	setTimeout(function(){
		$('#ts').hide();
	},1500);

})