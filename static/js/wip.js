
/******************************************************************************************************
* Date: 2015-8-6
* Author: alphp1e0
* Description: 记录当前状态的类，用于记录当前选择哪些project、host、vul、comment，对于当前状态的更新需要同步更新页面标题
******************************************************************************************************/
function Current(){
	this.project = null;
	this.host = null;
	this.vul = null;
	this.comment = null;
}

Current.prototype.init = function(){
	this.project = null;
	this.host = null;
	this.vul = null;
	this.comment = null;

	$("#wip-title-project").text("[project]");
	$("#wip-title-host").text("[host]");
	$("#wip-title-vul").text("[vul]");
	$("#wip-title-comment").text("[comment]");
}
Current.prototype.initProject = function(){
	this.project = null;
	this.host = null;
	this.vul = null;
	this.comment = null;

	$("#wip-title-project").text("[project]");
	$("#wip-title-host").text("[host]");
	$("#wip-title-vul").text("[vul]");
	$("#wip-title-comment").text("[comment]");
}
Current.prototype.initHost = function(){
	this.host = null;
	this.vul = null;
	this.comment = null;

	$("#wip-title-host").text("[host]");
	$("#wip-title-vul").text("[vul]");
	$("#wip-title-comment").text("[comment]");
}
Current.prototype.initVul = function(){
	this.vul = null;

	$("#wip-title-vul").text("[vul]");
}
Current.prototype.initComment = function(){
	this.comment = null;

	$("#wip-title-comment").text("[comment]");
}
Current.prototype.setProject = function(project){
	this.project = project;
	if(!project) {
		$("#wip-title-project").text("[project]");
	} else {
		$("#wip-title-project").text("["+project.name+"]");
	}
	this.setHost(null);
	this.setVul(null);
	this.setComment(null);
}
Current.prototype.getProject = function(){
	return this.project;
}
Current.prototype.setHost = function(host){
	this.host = host;
	if(!host){
		$("#wip-title-host").text("[host]");
	} else {
		$("#wip-title-host").text("["+host.title+"]");
	}
	this.setVul(null);
	this.setComment(null);
}
Current.prototype.getHost = function(){
	return this.host;
}
Current.prototype.setVul = function(vul){
	this.vul = vul;
	if(!vul) {
		$("#wip-title-vul").text("[vul]");
	} else {
		$("#wip-title-vul").text("["+vul.name+"]");
	}	
}
Current.prototype.getVul = function(){
	return this.vul;
}
Current.prototype.setComment = function(comment){
	this.comment = comment;
	if(!comment) {
		$("#wip-title-comment").text("[comment]");
	} else {
		$("#wip-title-comment").text("["+comment.name+"]");
	}	
}
Current.prototype.getComment = function(){
	return this.comment;
}
Current.prototype.record = function(){}
Current.prototype.changed = function(){}

/******************************************************************************************************
* Date: 2015-8-6
* Description: 初始化工作，绑定事件
******************************************************************************************************/
var current = new Current();

$(document).ready(function() {
    listProject();
    //绑定与project相关操作的事件
    $("#wip-button-project-add").click(addProject);
    $("#wip-button-project-delete").click(deleteProject);
    $("#wip-button-project-modify").click(modifyProject);
    $("#wip-button-project-refresh").click(refreshProject);

    //绑定与host相关操作的事件
    $("#wip-tab-button-detail").click(function(){listHost();});
    $("#wip-button-host-add").click(addHost);
    $("#wip-button-host-delete").click(deleteHost);
    $("#wip-button-host-modify").click(modifyHost);
    $("#wip-button-host-refresh").click(refreshHost);
    $("#wip-button-host-ipsort").click(function(){listHost("ip");});
    $("#wip-button-host-urlsort").click(function(){listHost("url");});

    //绑定与vul、comment相关操作的事件
    $("#wip-button-host-list").click(listHostDetail);
    $("#wip-button-vul-list").click(function(){listVul();});
    $("#wip-button-comment-list").click(function(){listComment();});
    $("#wip-button-vul-refresh").click(refreshHost);

    $("#wip-button-vul-add").click(addVul);
    $("#wip-button-vul-delete").click(deleteVul);
    $("#wip-button-vul-modify").click(modifyVul);

    $("#wip-button-comment-add").click(addComment);
    $("#wip-button-comment-delete").click(deleteComment);
    $("#wip-button-comment-modify").click(modifyComment);

    $("#wip-button-attachment-add").click(addAttachment);

    //绑定与auto task相关操作的事件
    $("#wip-tab-button-autotask").click(configTasks);
    $("#wip-autotask-button-show-taskresult").click(listTaskResult);
});

/******************************************************************************************************
* Date: 2015-8-6
* Author: alphp1e0
* Description: project相关操作，增、删、改操作，显示项目列表、显示项目详情
******************************************************************************************************/

function addProject(){
	 $("#wip-modal-project").modal("show");
	 var options = {
    	type:"POST",
    	url:"addproject",
    	beforeSubmit:function(){
    		//参数校验
    	},
    	success:function(){   		
    		alert("提交成功!");
    		$("#wip-modal-project").modal("hide");
    		listProject();
    	},
    	error:function(xhr, status, error){
    	 	alert("提交失败，失败原因："+xhr.responseText);
    	}
    };
    //$('#wip-modal-form-project').submit(function(){$(this).ajaxSubmit(options);return false;});  
    $("#wip-modal-form-project").ajaxForm(options);
}

function deleteProject(){
	if(!current.getProject()) {
		alert("请先选择project!");
		return
	}
	if(confirm("是否删除当前项目？") == false){
		return
	}
	$.get("/deleteproject?id="+current.getProject().id, function(data,status){
		listProject();
		$("#wip-project-detail").empty();
		current.setProject(null);
	});	
}

function modifyProject(){
	if(!current.getProject()) {
		alert("请先选择project!");
		return;
	}
	$("#wip-modal-project").modal("show");
	$("#wip-modal-form-project-id").val(current.getProject().id);
	$("#wip-modal-form-project-name").val(current.getProject().name);
	$("#wip-modal-form-project-url").val(current.getProject().url);
	$("#wip-modal-form-project-ip").val(current.getProject().ip);
	$("#wip-modal-form-project-whois").val(current.getProject().whois);
	$("#wip-modal-form-project-description").val(current.getProject().description);

	
	var options = {
    	type:"POST",
    	url:"modifyproject",
    	beforeSubmit:function(formData, jqForm, opt){
    		//参数校验
    	},
    	success:function(){    		
    		alert("提交成功!");
    		$("#wip-modal-project").modal("hide");
    		listProject();
    	},
    	error:function(xhr, status, error){
    	 	alert("提交失败，失败原因："+xhr.responseText);
    	}
    };

    $("#wip-modal-form-project").ajaxForm(options);
}

function listProject(){
	function addProjectItem(id, name){
		var item = $("<a></a>").addClass("list-group-item").attr("id","wip-project-id-"+id).attr("href","#").text(name);
		item.click(clickProject);
		$("#wip-project-list").append(item);
	}

	current.initProject();
	$("#wip-project-list").empty()
	$.getJSON("/listproject", function(result){
		$.each(result, function(i, value){
			addProjectItem(value.id, value.name);
		});
	});
}

function clickProject(){
	function addProjectDetailItem(name, value){
		$("#wip-project-detail").append($("<div></div>").addClass("list-group-item").append($("<b></b>").text(name+":"), $("<br />"), value));
	}

	var id = $(this).attr('id').substring(15);
	$(this).addClass("active");
	if(current.getProject() && (current.getProject().id != id)){
		$("#wip-project-id-"+current.getProject().id).removeClass("active");
	}

	$("#wip-project-detail").empty();
	$.getJSON("/getprojectdetail?id="+id, function(result){
		current.setProject(result[0]);
		addProjectDetailItem("项目名称", result[0].name);
		addProjectDetailItem("URL地址", result[0].url);
		addProjectDetailItem("IP地址", result[0].ip);
		addProjectDetailItem("Whois信息", result[0].whois);
		addProjectDetailItem("创建时间", result[0].ctime);
		addProjectDetailItem("描述信息", result[0].description);
	});
}

function refreshProject(){
	current.initProject();
	listProject();
	$("#wip-project-detail").empty();
}

/******************************************************************************************************
* Date: 2015-8-13
* Author: alphp1e0
* Description: host相关的操作，增、删、该，显示host列表、显示host详情
******************************************************************************************************/

function addHost(){
	 $("#wip-modal-host").modal("show");
	 var options = {
    	type:"POST",
    	url:"addhost",
    	beforeSerialize:function(form, opt){
    	},
    	beforeSubmit:function(formData, jqForm, opt){
    		//参数校验
    		if (!current.getProject()) {
    			alert("请先选择project!");
    			$("#wip-modal-host").modal("hide");
    			return false;
    		}
    		var project_id = current.getProject().id;
    		formData.push({'name':'projectid', 'value':project_id});
    	},
    	success:function(){   		
    		alert("提交成功!");
    		$("#wip-modal-host").modal("hide");
    		listHost();
    	},
    	error:function(xhr, status, error){
    	 	alert("提交失败，失败原因："+xhr.responseText);
    	}
    };

    $("#wip-modal-form-host").ajaxForm(options);
}

function deleteHost(){
	if(!current.getHost()) {
		alert("请先选择Host!");
		return
	}
	if(confirm("是否删除当前Host？") == false){
		return
	}
	$.get("/deletehost?id="+current.getHost().id, function(data,status){
		listHost();
		$("#wip-vul-comment-list").empty();
		current.setHost(null);
	});	
}

function modifyHost(){
	if(!current.getHost()) {
		alert("请先选择Host!");
		return;
	}
	$("#wip-modal-host").modal("show");
	$("#wip-modal-form-host-id").val(current.getHost().id);
	$("#wip-modal-form-host-url").val(current.getHost().url);
	$("#wip-modal-form-host-ip").val(current.getHost().ip);
	$("#wip-modal-form-host-title").val(current.getHost().title);
	$("#wip-modal-form-host-level").val(current.getHost().level);
	$("#wip-modal-form-host-os").val(current.getHost().os);
	$("#wip-modal-form-host-server_info").val(current.getHost().server_info);
	$("#wip-modal-form-host-middleware").val(current.getHost().middleware);
	$("#wip-modal-form-host-description").val(current.getHost().description);
	
	var options = {
    	type:"POST",
    	url:"modifyhost",
    	beforeSubmit:function(formData, jqForm, opt){
    	},
    	success:function(){    		
    		alert("提交成功!");
    		$("#wip-modal-host").modal("hide");
    		listHost();
    	},
    	error:function(xhr, status, error){
    	 	alert("提交失败，失败原因："+xhr.responseText);
    	}
    };

    $("#wip-modal-form-host").ajaxForm(options);
}

function listHost(orderby="level"){
	if(!current.getProject()) {
		//alert("请先选择Project!");
		return;
	}
	//如果没有重新选择project，则不刷新host list
	if(current.getHost() && orderby == "level"){
		if(current.getHost().project_id == current.getProject().id) {
			return
		}
	}
	function addHostItem(id, url, ip){
		var b = $("<b></b>").text(ip+" | ")
		var i = $("<i></i>").text(url)
		var item = $("<a></a>").addClass("list-group-item").attr("id","wip-host-id-"+id).attr("href","#").append(b,i);
		item.click(clickHost);
		$("#wip-host-list").append(item);
	}

	current.initHost();
	$("#wip-host-list").empty();
	$("#wip-vul-comment-list").empty();
	var url = "/listhost?projectid=" + current.getProject().id + "&orderby=" + orderby;
	$.getJSON(url, function(result){
		$.each(result, function(i, value){
			addHostItem(value.id, value.url, value.ip);
		});
	});
}

function listHostDetail(){
	var host = current.getHost()
	if(!host) {
		alert("请先选择Host!");
		return
	}

	function addHostDetailItem(name, value, type=0){
		if(type==0){
			$("#wip-vul-comment-list").append($("<div></div>").addClass("list-group-item").append($("<b></b>").text(name+":\t"), $("<br />"), value));
		} else {
			var typeList = ["http","https","ftp"];
			var url = typeList[type-1]+"://"+value;
			var a = $("<a></a>").attr("href", url).attr("target","_blank").text(url);
			$("#wip-vul-comment-list").append($("<div></div>").addClass("list-group-item").append($("<b></b>").text(name+":\t"), $("<br />"), a));
		}		
	}

	$("#wip-vul-comment-list").empty();
	$("#wip-vul-comment-detail").empty();
	levelList = ["关键","重要","一般","提示"];

	addHostDetailItem("Title", host.title);
	addHostDetailItem("URL地址", host.url, host.protocol);
	addHostDetailItem("IP地址", host.ip, host.protocol);
	addHostDetailItem("等级", levelList[host.level-1]);
	addHostDetailItem("OS信息", host.os);
	addHostDetailItem("Server信息", host.server_info);
	addHostDetailItem("中间件", host.middleware);
	addHostDetailItem("描述", host.description);
}

function clickHost(){
	if(!current.getProject()) {
		alert("请先选择project!");
		return
	}
	function addHostDetailItem(name, value, type=0){
		if(type==0){
			$("#wip-vul-comment-list").append($("<div></div>").addClass("list-group-item").append($("<b></b>").text(name+":\t"), $("<br />"), value));
		} else {
			var typeList = ["http","https","ftp"];
			var url = typeList[type-1]+"://"+value;
			var a = $("<a></a>").attr("href", url).attr("target","_blank").text(url);
			$("#wip-vul-comment-list").append($("<div></div>").addClass("list-group-item").append($("<b></b>").text(name+":\t"), $("<br />"), a));
		}		
	}

	var id = $(this).attr('id').substring(12);
	$(this).addClass("active");
	if(current.getHost() && (current.getHost().id != id)){
		$("#wip-host-id-"+current.getHost().id).removeClass("active");
	}

	$("#wip-vul-comment-list").empty();
	$("#wip-vul-comment-detail").empty();
	levelList = ["关键","重要","一般","提示"];
	$.getJSON("/gethostdetail?id="+id, function(result){
		current.setHost(result[0]);
		addHostDetailItem("Title", result[0].title);
		addHostDetailItem("URL地址", result[0].url, result[0].protocol);
		addHostDetailItem("IP地址", result[0].ip, result[0].protocol);
		addHostDetailItem("等级", levelList[result[0].level-1]);
		addHostDetailItem("OS信息", result[0].os);
		addHostDetailItem("Server信息", result[0].server_info);
		addHostDetailItem("中间件", result[0].middleware);
		addHostDetailItem("描述", result[0].description);
	});
}

function refreshHost(){
	current.initHost();
	listHost();
	$("#wip-vul-comment-list").empty();
}

/******************************************************************************************************
* Date: 2015-8-13
* Author: alphp1e0
* Description: 漏洞相关操作，增、删、该，显示漏洞列表，显示漏洞详情
******************************************************************************************************/
function addVul(){
	 $("#wip-modal-vul").modal("show");
	 var options = {
    	type:"POST",
    	url:"addvul",
    	beforeSerialize:function(form, opt){
    	},
    	beforeSubmit:function(formData, jqForm, opt){
    		//参数校验
    		if (!current.getHost()) {
    			alert("请先选择host!");
    			$("#wip-modal-vul").modal("hide");
    			return false;
    		}
    		var host_id = current.getHost().id;
    		formData.push({'name':'hostid', 'value':host_id});
    	},
    	success:function(){   		
    		alert("提交成功!");
    		$("#wip-modal-vul").modal("hide");
    		listVul();
    	},
    	error:function(xhr, status, error){
    	 	alert("提交失败，失败原因："+xhr.responseText);
    	}
    };

    $("#wip-modal-form-vul").ajaxForm(options);
}

function deleteVul(){
	if(!current.getVul()) {
		alert("请先选择漏洞!");
		return
	}
	if(confirm("是否删除当前漏洞？") == false){
		return
	}
	$.get("/deletevul?id="+current.getVul().id, function(data,status){
		listVul();
		$("#wip-vul-comment-list").empty();
		current.setVul(null);
	});	
}

function modifyVul(){
	if(!current.getVul()) {
		alert("请先选择漏洞!");
		return
	}
	$("#wip-modal-vul").modal("show");
	$("#wip-modal-form-vul-id").val(current.getVul().id);
	$("#wip-modal-form-vul-name").val(current.getVul().name);
	$("#wip-modal-form-vul-url").val(current.getVul().url);
	$("#wip-modal-form-vul-info").val(current.getVul().info);
	$("#wip-modal-form-vul-type").val(current.getVul().type);
	$("#wip-modal-form-vul-level").val(current.getVul().level);
	$("#wip-modal-form-vul-description").val(current.getVul().description);
	
	var options = {
    	type:"POST",
    	url:"modifyvul",
    	beforeSubmit:function(formData, jqForm, opt){
    	},
    	success:function(){    		
    		alert("提交成功!");
    		$("#wip-modal-vul").modal("hide");
    		listVul();
    	},
    	error:function(xhr, status, error){
    	 	alert("提交失败，失败原因："+xhr.responseText);
    	}
    };

    $("#wip-modal-form-vul").ajaxForm(options);
}

function listVul(orderby="level"){
	if(!current.getHost()) {
		alert("请先选择Host!");
		return;
	}

	function addVulItem(id, name){
		var item = $("<a></a>").addClass("list-group-item").attr("id","wip-vul-id-"+id).attr("href","#").text(name);
		item.click(clickVul);
		$("#wip-vul-comment-list").append(item);
	}

	current.initVul();
	$("#wip-vul-comment-list").empty();
	$("#wip-vul-comment-detail").empty();
	var url = "/listvul?hostid=" + current.getHost().id + "&orderby=" + orderby;
	$.getJSON(url, function(result){
		$.each(result, function(i, value){
			addVulItem(value.id, value.name);
		});
	});
}

function clickVul(){
	if(!current.getHost()) {
		alert("请先选择project!");
		return
	}
	function addVulDetailItem(name, value){
		$("#wip-vul-comment-detail").append($("<div></div>").addClass("list-group-item").append($("<b></b>").text(name+":\t"), $("<br />"), value));
	}

	var id = $(this).attr('id').substring(11);
	$(this).addClass("active");
	if(current.getVul() && (current.getVul().id != id)){
		$("#wip-vul-id-"+current.getVul().id).removeClass("active");
	}

	$("#wip-vul-comment-detail").empty();
	levelList = ["关键","重要","一般","提示"];
	typeList = ["溢出漏洞","注入漏洞","XSS","CSRF","路径遍历","上传","逻辑漏洞","弱口令","信息泄露","配置错误","认证/会话管理","点击劫持","跨域漏洞","其他"]
	$.getJSON("/getvuldetail?id="+id, function(result){
		current.setVul(result[0]);
		addVulDetailItem("名称", result[0].name);
		addVulDetailItem("等级", levelList[result[0].level-1]);
		addVulDetailItem("URL地址", result[0].url);
		addVulDetailItem("详情", result[0].info);
		addVulDetailItem("类型", typeList[result[0].type-1]);		
		addVulDetailItem("描述", result[0].description);
	});
}

function refreshVul(){
	current.initVul();
	current.initComment();
	listVul();
	$("#wip-vul-comment-detail").empty();
}

/******************************************************************************************************
* Date: 2015-8-13
* Author: alphp1e0
* Description: 备注相关操作，增、删、改，显示备注列表、显示备注详情
******************************************************************************************************/

function addComment(){
    $("#wip-modal-comment").modal("show");
    var options = {
        type:"POST",
        url:"addcomment",
        beforeSerialize:function(form, opt){
        },
        beforeSubmit:function(formData, jqForm, opt){
            //参数校验
            if (!current.getHost()) {
                alert("请先选择host!");
                $("#wip-modal-comment").modal("hide");
                return false;
            }
            var host_id = current.getHost().id;
            formData.push({'name':'hostid', 'value':host_id});
        },
        success:function(){             
            alert("提交成功!");
            $("#wip-modal-comment").modal("hide");
            listComment();
        },
        error:function(xhr, status, error){
            alert("提交失败，失败原因："+xhr.responseText);
        }
    };

    $("#wip-modal-form-comment").ajaxForm(options);
}

function deleteComment(){
    if(!current.getComment()) {
        alert("请先选择注释!");
        return
    }
    if(confirm("是否删除当前Comment？") == false){
        return
    }
    $.get("/deletecomment?id="+current.getComment().id, function(data,status){
        listComment();
    	$("#wip-vul-comment-list").empty();
    	current.setComment(null);
    });    
}

function modifyComment(){
    if(!current.getComment()) {
        alert("请先选择注释!");
        return
    }
    $("#wip-modal-comment").modal("show");
    $("#wip-modal-form-comment-id").val(current.getComment().id);
    $("#wip-modal-form-comment-name").val(current.getComment().name);
    $("#wip-modal-form-comment-url").val(current.getComment().url);
    $("#wip-modal-form-comment-info").val(current.getComment().info);        
    $("#wip-modal-form-comment-level").val(current.getComment().level);
    $("#wip-modal-form-comment-type").val(current.getComment().attachment);
    $("#wip-modal-form-comment-description").val(current.getComment().description);
        
    var options = {
        type:"POST",
        url:"modifycomment",
        beforeSubmit:function(formData, jqForm, opt){
        },
        success:function(){             
            alert("提交成功!");
            $("#wip-modal-comment").modal("hide");
            listComment();
        },
        error:function(xhr, status, error){
            alert("提交失败，失败原因："+xhr.responseText);
        }
    };

    $("#wip-modal-form-comment").ajaxForm(options);
}

function listComment(orderby="level"){
    if(!current.getHost()) {
        alert("请先选择Host!");
        return;
    }

    function addCommentItem(id, name){
        var item = $("<a></a>").addClass("list-group-item").attr("id","wip-comment-id-"+id).attr("href","#").text(name);
        item.click(clickComment);
        $("#wip-vul-comment-list").append(item);
    }

    current.initComment();
    $("#wip-vul-comment-list").empty();
    $("#wip-vul-comment-detail").empty();
    var url = "/listcomment?hostid=" + current.getHost().id + "&orderby=" + orderby;
    $.getJSON(url, function(result){
        $.each(result, function(i, value){
            addCommentItem(value.id, value.name);
        });
    });
}

function clickComment(){
    if(!current.getHost()) {
        alert("请先选择project!");
        return
    }
    function addCommentDetailItem(name, value){
        $("#wip-vul-comment-detail").append($("<div></div>").addClass("list-group-item").append($("<b></b>").text(name+":\t"), $("<br />"), value));
    }

    var id = $(this).attr('id').substring(15);
    $(this).addClass("active");
    if(current.getComment() && (current.getComment().id != id)){
        $("#wip-comment-id-"+current.getComment().id).removeClass("active");
    }

    $("#wip-vul-comment-detail").empty();
    levelList = ["关键","重要","一般","提示"];
    typeList = ["溢出漏洞","注入漏洞","XSS","CSRF","路径遍历","上传","逻辑漏洞","弱口令","信息泄露","配置错误","认证/会话管理","点击劫持","跨域漏洞","其他"]
    $.getJSON("/getcommentdetail?id="+id, function(result){
        current.setComment(result[0]);
        addCommentDetailItem("名称", result[0].name);
        addCommentDetailItem("等级", levelList[result[0].level-1]);
        addCommentDetailItem("URL地址", result[0].url);
        addCommentDetailItem("详情", result[0].info);                
        addCommentDetailItem("描述", result[0].description);
        attachmentItem = $("<a></a>").addClass("list-group-item").append($("<b></b>").text("附件"+":\t"), $("<br />"), result[0].attachment)
        attachmentItem.attr("href","static/attachment/"+result[0].attachment).attr("target","_blank");
        $("#wip-vul-comment-detail").append(attachmentItem);
    });
}

function refreshComment(){
    current.initComment();
    listComment();
    $("#wip-vul-comment-list").empty();
}

function addAttachment(){
	$("#wip-modal-attachment").modal("show");
    var options = {
        type:"POST",
        url:"addattachment",
        beforeSerialize:function(form, opt){
        },
        beforeSubmit:function(formData, jqForm, opt){
            //参数校验
            if (!current.getHost()) {
                alert("请先选择host!");
                $("#wip-modal-attachment").modal("hide");
                return false;
            }
            var host_id = current.getHost().id;
            formData.push({'name':'hostid', 'value':host_id});
        },
        success:function(){             
            alert("提交成功!");
            $("#wip-modal-attachment").modal("hide");
        },
        error:function(xhr, status, error){
            alert("提交失败，失败原因："+xhr.responseText);
        }
    };

    $("#wip-modal-form-attachment").ajaxForm(options);
}

/******************************************************************************************************
* Date: 2015-8-17
* Author: alphp1e0
* Description: 备注相关操作，增、删、改，显示备注列表、显示备注详情
******************************************************************************************************/

function configTasks(){
	configZonetransTask();
	configGooglehackingTask();
	configDnsbruteTask();
	configSubnetscanTask();
	//getTaskStatus();
	listTaskResult();
}

function configZonetransTask(){}

function configGooglehackingTask(){}

function configDnsbruteTask(){
    var options = {
        type:"POST",
        url:"adddict",
        beforeSerialize:function(form, opt){
        },
        beforeSubmit:function(formData, jqForm, opt){
            //参数校验
        },
        success:function(){             
            alert("上传成功!");
        },
        error:function(xhr, status, error){
            alert("上传失败!");
        }
    };
    $("#wip-form-autotask-dnsbrute-dictadd").ajaxForm(options);	

	$("#wip-form-autotask-dnsbrute-dictselect").empty()
	$.getJSON("/getdictlist", function(result){
        $.each(result, function(i, value){
            $("#wip-form-autotask-dnsbrute-dictselect").append($("<option></option>").val(value).text(value));
        });
    });
    var options = {
        type:"POST",
        url:"startdnsbrute",
        beforeSerialize:function(form, opt){
        },
        beforeSubmit:function(formData, jqForm, opt){
            //参数校验
            if (!current.getProject()) {
    			alert("请先选择project!");
    			return false;
    		}
    		var project_id = current.getProject().id;
    		formData.push({'name':'projectid', 'value':project_id});
        },
        success:function(){             
            alert("提交成功!");
        },
        error:function(xhr, status, error){
            alert("提交失败，失败原因："+xhr.responseText);
        }
    };
    $("#wip-form-autotask-dnsbrute-start").ajaxForm(options);
}

function configSubnetscanTask(){}

function listTaskResult(){
	if(!current.getProject()){
		$("#wip-autotask-task-result-list").empty()
		return false;
	}
	function addTaskItem(id, url, ip, level, source){
		levelList = ["关键","重要","一般","提示"];
		allDiv = $("<div></div>").addClass("list-group-item").attr("id","wip-autotask-task-reuslt"+id);
		sourceSpan = $("<span></span>").text("来源："+source+" | "+"等级："+levelList[level-1]);
		urlA = $("<a></a>").text(" | URL: "+url).attr("href","http://"+url).attr("target","url_"+id);
		ipA = $("<a></a>").text(" | IP: "+ip).attr("href","http://"+ip).attr("target","ip_"+id);
		allDiv.append(sourceSpan,urlA,ipA);
		$("#wip-autotask-task-result-list").append(allDiv);
	}

	$("#wip-autotask-task-result-list").empty()
	$.getJSON("/gettaskresult?projectid="+current.getProject().id, function(result){
        $.each(result, function(i, value){
            addTaskItem(value.id, value.url, value.ip, value.level, value.source);
        });
    });
}

