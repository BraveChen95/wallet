$(function(){

	    u = "http://219.143.144.250/user/newshow";
		$.ajax({
			url: u,
			success:function(e){
                console.log(e["article"])

                var markerArr = e["article"];
                alert(markerArr)
        var changeIcon1 = new BMap.Icon("../../static/images/red_packet.jpg",new BMap.Size(128,128));//自定义图标
        // 百度地图API功能
        var map = new BMap.Map("allmap");
        var point = new BMap.Point(117.232475,31.826542);
        map.centerAndZoom(point,14);
        var geolocation = new BMap.Geolocation();


        var point = new Array(); //存放标注点经纬信息的数组
        var marker = new Array(); //存放标注点对象的数组
        var info = new Array(); //存放提示信息窗口对象的数组
        // var searchInfoWindow =new Array();//存放检索信息窗口对象的数组

        for (var i = 0; i < markerArr.length; i++) {
            var p0 = markerArr[i].point.split(",")[0]; //
            var p1 = markerArr[i].point.split(",")[1]; //按照原数组的point格式将地图点坐标的经纬度分别提出来
            point[i] = new window.BMap.Point(p0, p1); //循环生成新的地图点
            marker[i] = new window.BMap.Marker(point[i],{icon:changeIcon1}); //按照地图点坐标生成标记

            map.addOverlay(marker[i]);
            marker[i].setAnimation(BMAP_ANIMATION_BOUNCE); //跳动的动画
    　　　　　　　　　　　　　　//显示marker的title，marker多的话可以注释掉
            var label = new window.BMap.Label(markerArr[i].title, { offset: new window.BMap.Size(20, -10) });
            marker[i].setLabel(label);
            // 创建信息窗口对象
            info[i] = "<p style=’font-size:12px;lineheight:1.8em;’>" + "</br>地址：" + markerArr[i].address + "</br> 电话：" + markerArr[i].tel + "</br></p>";

            var obj ={}
            marker[i].addEventListener("click",
                (function(k){
                    // js 闭包
                    return function(){
                        obj.point=markerArr[k].point
                        $.ajax({
                            url:"http://219.143.144.250/user/newshow",
                            data: JSON.stringify(obj),
                            type:"post",
                            dataType: 'json',
                            contentType:'application/json',
                            success:function(e){
                                location.href="./new_show.html"
                            },error:function(jqXHR,textStatus,errorThrown){
                                alert(errorThrown);
                        }
                        })
                        //window.location.href='./qq.html';
                        //将被点击marker置为中心
                        //map.centerAndZoom(point[k], 18);
                        //在marker上打开检索信息窗口
                        //searchInfoWindow[k].open(marker[k]);
                    }
                })(i)
            );
        }

        geolocation.getCurrentPosition(function(r){console.log(r.point)
            if(this.getStatus() == BMAP_STATUS_SUCCESS){
                var mk = new BMap.Marker(r.point);
                map.addOverlay(mk);//标出所在地
                map.panTo(r.point);//地图中心移动
                //alert('您的位置：'+r.point.lng+','+r.point.lat);
                var point = new BMap.Point(r.point.lng,r.point.lat);//用所定位的经纬度查找所在地省市街道等信息
                var gc = new BMap.Geocoder();
                gc.getLocation(point, function(rs){
                   var addComp = rs.addressComponents; console.log(rs.address);//地址信息
                   alert(rs.address);//弹出所在地址

                });
            }else {
                alert('failed'+this.getStatus());
            }
        },{enableHighAccuracy: true})




			},
			error:function(){
				alert("请求失败");
			}
		})







})



