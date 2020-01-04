$(function(){
	$('#roles').on('change',function(){
		formK();
	})
	//切换角色,表单数据变为空
	function formK(){
		$('#firstName').val('');
		$('#email').val('');
		$('#perId').val('');
		$('#remarks').val('');
	}
	var obj={};
	$('#ktzh').on('click',function(){
		var type=$('#roles').val(),
			name=$('#firstName').val(),
			email=$('#email').val(),
			password=$('#pas').val();
		password=hex_md5(password);

		if(name!==''){
			obj.name=name;
		}else{
			if(obj.name){
				delete obj.name; 
			}
		}
		if(password!==''){
			obj.password=password;
		}else{
			if(obj.password){
				delete obj.password; 
			}
		}
		if(email!==''){
			obj.email=email;
		}else{
			if(obj.email){
				delete obj.email; 
			}
		}
		console.log(obj);
		//验证邮箱
		var reg=/^([0-9A-Za-z\-_\.]+)@([0-9a-z]+\.[a-z]{2,3}(\.[a-z]{2})?)$/g;		
		if(email==''){
			$('.emailTs').css('display','block');
			return false;
		}else{
			if(reg.test(email)==false){
				$('.emailTs').css('display','block');
				return false;
			}else{
				$('.emailTs').css('display','none');
				ajaxData(obj);
		}
		}
		
	})
	function ajaxData(obj){
		$.ajax({
			url:'http://127.0.0.1/sudo/admins',
			data: JSON.stringify(obj),
			type:'post',
            dataType: 'json',
            contentType:'application/json',
			success:function(e){
				location.href='./admin_list.html';
			},
			error:function(){
				alert('获取数据失败');
			}
		})
	}
})