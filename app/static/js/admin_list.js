$(function(){
	window.API_HOST = (function(){
  		return {
      		'127.0.0.1:5000':'127.0.0.1:5000'
    		}[window.location.host] || window.location.host
	})();
	console.log(window.location.host);
	if(window.API_HOST=='localhost'){
		window.API_HOST='127.0.0.1:5000'
	}
	var url = '//'+window.API_HOST + '/sudo/admins';
	alert(url)
	console.log(url);
	tabData();
	
	//点击查询获取数据
	$('#search').on('click',function(){
		tabData();
	})
	//渲染表格数据
	function tabData(){
		$('#tt').datagrid({
				loader:fn,
				url:'http://127.0.0.1/sudo/admins',
				singleSelect: true,
				loadMsg: '数据加载中.....',
				nowrap:false,
				frozenColumns:[[
					{field:'id',title:'用户编号',align:'center'},
					{field:'name',title:'用户名称',align:'center'},
				]],
				columns:[[
					{field:'email',title:'邮箱账号',align:'center'},
					{field:'latest',title:'注册日期',align:'center'},
					{field:'cz',align:'center',width:'100px',title:'操作',

					formatter: function (vales ,row, index ) {
							var bh=row.id;

							var a = '<a class="dis" id="'+bh+'"></a> <a class="amend" data_id="'+bh+'">修改</a>';
							return a;
						}
					}
				]],

				onLoadSuccess:function(data){
					var script=document.createElement('script');
					script.src='../../static/js/structure.js';
					document.body.appendChild(script);
					for(var i in data.rows){
						if(data.rows[i].active==true){
							$($('.dis')[i]).text('启用');
						}else{
							$($('.dis')[i]).text('禁用');
							
						}
					}
					$('.dis').on('click',function(){
						if($(this).text()=="禁用"){
							$(this).text("启用");
						}else{
							$(this).text("禁用");
						}
						var aid=$(this).attr('id'),
							aObj={};
						if($(this).text()=='启用'){
							aObj.active=1;
						}else{
							aObj.active=0;
						}
						$.ajax({
							url:'https://127.0.0.1/sudo/admins/'+aid,
							data: JSON.stringify(aObj),
							type:'post',
                            dataType: 'json',
            			 	contentType:'application/json',
            			 	success:function(e){
            			 		console.log(e)
            			 	},
            			 	error:function(){
            			 		alert("失败");
            			 	}
							
						})
					})	
					$('.amend').on('click',function(){
						var aid=$(this).attr('data_id');
						location.href='./admin_edit.html?aid='+aid;
					})
				}
		})
	}
	function fn(param,success,error){
		var account=$('#account').val(),
			tele=$('#tele').val();
		console.log(account)
		var obj={"account":account, "tele":tele};

		console.log(obj);

		var url1 = url,
    　　 ajax1 = $.ajax(
      　　 　　 {
         　　　　     url : url1,
         			type:'get',
         			data: obj,
         			success:function(e){

            			 		console.log(e)
            			 	}
        　　　　}
 　　  　　 );

　　　　$.when(ajax1).done(function(e){
			var data=e.admins;
//		    document.getElementById("adminName").innerText = e.login_name['login_name'];
			console.log(data);
			success(data);
			qk();


　　　　}).fail(function(){
　　
   　　　　 alert("fail");

　　　　});
}
function qk(){

	$('#account').val(),

	$('#tele').val();
}
	
})
