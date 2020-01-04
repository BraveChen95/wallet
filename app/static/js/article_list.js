$(function(){
	tabData();
	//点击查询获取表单数据
	$('#search').on('click',function(){
		tabData();
	})
	//渲染表格数据
	function tabData(){
		$('#tt').datagrid({
				loader:fn,
				url:'http://127.0.0.1/sudo/article',
				singleSelect: true,
				loadMsg: '数据加载中.....',
				frozenColumns:[[
					{field:'id',title:'项目编号',align:'center'},
					{field:'title',title:'项目名称',align:'center'},
				]],
				columns:[[
					{field:'content',title:'内容',align:'center'},
					{field:'use_id',title:'以获取用户id',align:'center'},
					{field:'hongbao_money',title:'红包剩余金额',align:'center'},
					{field:'hongbao_number',title:'红包剩余数量',align:'center'},
					{field:'status',title:'状态',align:'center'},
					{field:'use_id',title:'以领红包用户id',align:'center'},
					{field:'register_time',title:'提交时间',align:'center'},
					{field:'audit',align:'center',title:'审核',width:'100px',
						formatter: function (vales ,row, index ) {
							var bh=row.id;
							var a = '<a class="pass" data_id="'+bh+'"> </a><a class="reject" data_id="'+bh+'"></a>';
							return a;
						}
					}
				]],
				onLoadSuccess:function(data){
					var script=document.createElement('script');
					script.src='../../static/js/structure.js';
					document.body.appendChild(script);
					console.log(data.rows);
					for(var i in data.rows){
						if(data.rows[i].status=='待审核'){
							$($('.pass')[i]).text('通过');
							$($('.reject')[i]).text('驳回');
						}else if(data.rows[i].status=='已驳回'){
							$($('.pass')[i]).text('已驳回');
						}else if(data.rows[i].status=='已通过'){
							$($('.pass')[i]).text('已通过');
						}
					}
					//阻止冒泡
					function stopBubble(e){
　　                    if(e&&e.stopPropagation){//非IE
　　                          e.stopPropagation();
　　                    }
　　                    else{//IE
　　                         window.event.cancelBubble=true;
　　                    }
　　                }
					var aObj={};
					//点击通过
					$('.pass').on('click',function(e){
						stopBubble(e);
						if($(this).text()=='通过'){
							aObj.status='Confirmed';
						}else if($(this).text()=='已通过'){
							$(this).siblings().remove();
							return false;
						}else if($(this).text()=='已驳回'){
							return false;
						}
						var uid=$(this).attr('data_id');
						ajaxD(uid,aObj);
						$(this).text("已通过");
					})
					//点击驳回
					$('.reject').on('click',function(e){
						stopBubble(e);
						if($(this).text()=='驳回'){
							aObj.status='Rejected';
						}else if($(this).text()=='已通过'){
							return false;
						}else if($(this).text()=='已驳回'){
							$(this).siblings().remove();
							return false;
						}
						var uid=$(this).attr('data_id');
						ajaxD(uid,aObj);
						$(this).text("已驳回");
					})
					function ajaxD(aid,aObj){
						$.ajax({
							url:'http://127.0.0.1/sudo/article/'+aid,
							data: JSON.stringify(aObj),
							type:'post',
                            dataType: 'json',
            			 	contentType:'application/json',
            			 	success:function(e){
            			 		console.log(e)
            			 		location.href = './article_list.html'
            			 	},
            			 	error:function(){
            			 		alert("失败");
            			 	}
						})
					}
				},
				onClickRow: function (rowIndex, rowData) {
					/*console.log(rowData.id)*/
					location.href='./article_edit.html?aid='+rowData.id;
				}
		})
	}
	function fn(param,success,error){
		var itemlNum=$('#itemlNum').val(),
			itemName=$('#itemName').val(),
			principal=$('#principal').val(),
			industry=$('#industry option:selected').text(),
			stage=$('#stage option:selected').text(),
			tele=$('#tele').val(),
			startT=$('#startT').val(),
			endT=$('#endT').val();
		var obj={};
		if(itemlNum!==''){
			obj.id=itemlNum;
		}
		if(itemName!==''){
			obj.name=itemName;
		}
		if(principal!==''){
			obj.contact_name=principal;
		}
		if(tele!==''){
			obj.contact_phone=tele;
		}
		if(startT!==''){
			obj.starttime=startT;
		}
		if(endT!==''){
			obj.endtime=endT;
		}
		if(industry!=='请选择'){
			obj.industry=industry;
		}
		if(stage!=='请选择'){
			obj.phase=stage;
		}
		var url1 = 'http://127.0.0.1/sudo/article',
    　　　　ajax1 = $.ajax(
      　　 　　 {
         　　　　   url : url1,
         			type:'get',
         			data: obj
        　　　　}
 　　  　　 );

　　　　$.when(ajax1).done(function(e){
			var data=e.article;
			console.log(e);
			for(var i in data){
				if(data[i].status=='NewStatus.Submitted'){
					data[i].status='待审核';
				}else if(data[i].status=='NewStatus.Rejected'){
					data[i].status='已驳回';
				}else{
					data[i].status='已通过';
				}
			}
   　　　　 success(data);
   			qk();

　　　　}).fail(function(){
　　
   　　　　 alert("fail");

　　　　});
	}
function qk(){
	$('#itemlNum').val(''),
	$('#itemName').val('');
	$('#principal').val('');
	$('#tele').val('');
	$('#startT').val('');
	$('#endT').val('');
}
})

