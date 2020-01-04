$(function(){
    //ajax登陆请求验证码图片
	$(window).on('load',function(){
		ajaxImg();
	})
	$('#getImg ,#getImg1').on('click',function(){
		ajaxImg();
	})
	function ajaxImg(){

	    u = "http://127.0.0.1/user/v_code";
		$.ajax({
			url: u,
			success:function(e){
                alert(e)
				var src=e;
				$('#getImg ,#getImg1').find('img').attr('src',src);
			},
			error:function(){
				alert("");
			}
		})
	}
	// 登录按钮切换
	$('#PwdLogin').on('click', function(){
	    PwdLogin()
	})
    function PwdLogin() {
        var login = document.getElementsByClassName("login_con");
        login[0].classList.remove("hidden");
        login[0].classList.add("show");
        login[1].classList.remove("show");
        login[1].classList.add("hidden");
        var tags = document.getElementsByClassName("top_tag");
        tags[0].classList.add("active");
        tags[1].classList.remove("active");
        var ad = document.getElementById("AdImg");

        // ad.style.height = "558px";
        // ad.style.backgroundImage='url(https://static.zcool.cn/v1.1.43/passport4.0/images/login-ground.jpg)';
    }

     var divset = document.getElementsByClassName("register");

     for (var i = 0; i<divset.length;i++) {
       divset[i].style.display="none";
       }
    //注册按钮
    $('#QrcodeLogin').on('click',function(){
		QrcodeLogin();
	})

    function QrcodeLogin() {

        divset = document.getElementsByClassName("register");
        for (var i = 0; i<divset.length;i++) {
          divset[i].style.display="";
        };
        var login = document.getElementsByClassName("login_con");
        login[0].classList.remove("show");
        login[0].classList.add("hidden");
        login[1].classList.remove("hidden");
        login[1].classList.add("show");
        var tags = document.getElementsByClassName("top_tag");
        tags[1].classList.add("active");
        tags[0].classList.remove("active");
        var ad = document.getElementById("AdImg");
        // ad.style.height = "558px";
        // ad.style.height = "407px";
    }

    var obj={};
    $('#user_login').on('click',function(){
        var username=$('#user_name').val(),
        password=$("#user_pwd").val(),
        vcode=$('#auth_code').val(),
        password=hex_md5(password);
        obj.username=username;
        obj.password=password;
        obj.vcode=vcode;
        $.ajax({
            url:"http://127.0.0.1/user/passwd_login",
            data: JSON.stringify(obj),
            type:"post",
            dataType: 'json',
            contentType:'application/json',
            success:function(e){
                if(e.message=='登陆成功'){
						location.href='./shouye.html';
                    }
            },
            error:function(jqXHR,textStatus,errorThrown){
					alert(errorThrown);
			}
        })
    })
    $('#register').on('click',function(){
        var username=$('#username').val(),
        password=$("#userpwd").val(),
        vcode=$('#authcode').val(),
        password=hex_md5(password);
        obj.username=username;
        obj.password=password;
        obj.vcode=vcode;
        $.ajax({
            url:"http://127.0.0.1/user/register",
            data: JSON.stringify(obj),
            type:"post",
            dataType: 'json',
            contentType:'application/json',
            success:function(e){
                if(e.message=='注册成功'){
						location.href='./index.html';
                }
            },error:function(jqXHR,textStatus,errorThrown){
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




















// inputs[1].onmouseout = function () {

//     if (inputs[1].value == 0) {
//         tips[1].classList.add('show');
//         tips[1].classList.remove('hidden');

//     } else {
//         tips[1].classList.add('hidden');
//         tips[1].classList.remove('show');
//     }
// }
// inputs[2].onmouseout = function () {

//     if (inputs[2].value == 0) {
//         tips[2].classList.add('show');
//         tips[2].classList.remove('hidden');

//     } else {
//         tips[2].classList.add('hidden');
//         tips[2].classList.remove('show');
//     }
// }
