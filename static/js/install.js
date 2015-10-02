

var options = {
	type:"POST",
	url:"install",
	beforeSubmit:function(){
		//参数校验
	},
	success:function(){
		$("#wip-setup-column").empty();
		var prompt = "安装成功,5秒钟后将跳转到主页。如果不能成功跳转，请点击后面链接：";
		var link = $("<a></a>").attr("href","/").text("主页");
		$("#wip-setup-column").append(prompt,link);
		
		setTimeout(function(){
			window.location.href = "/";
		}, 5000)
	},
	error:function(xhr, status, error){
	 	alert("安装失败，失败原因："+xhr.responseText);
	}
}
$("#wip-setup-form").ajaxForm(options);