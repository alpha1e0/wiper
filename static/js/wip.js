
/**************************************
* Date: 2015-8-6
* Description: the class Current record the current data
*
**************************************/
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

	$("#wip-title-project").text("project");
	$("#wip-title-host").text("host");
	$("#wip-title-vul").text("vul");
	$("#wip-title-comment").text("comment");
}
Current.prototype.initProject = function(){
	this.project = null;
	this.host = null;
	this.vul = null;
	this.comment = null;

	$("#wip-title-project").text("project");
	$("#wip-title-host").text("host");
	$("#wip-title-vul").text("vul");
	$("#wip-title-comment").text("comment");
}
Current.prototype.initHost = function(){
	this.host = null;
	this.vul = null;
	this.comment = null;

	$("#wip-title-host").text("host");
	$("#wip-title-vul").text("vul");
	$("#wip-title-comment").text("comment");
}
Current.prototype.initVul = function(){
	this.vul = null;

	$("#wip-title-vul").text("vul");
}
Current.prototype.initComment = function(){
	this.comment = null;

	$("#wip-title-comment").text("comment");
}
Current.prototype.setProject = function(project){
	this.project = project;
	if(!project) {
		$("#wip-title-project").text("project");
		this.setHost(null);
		this.setVul(null);
		this.setComment(null);
	} else {
		$("#wip-title-project").text(project.name);
	}	
}
Current.prototype.getProject = function(){
	return this.project;
}
Current.prototype.setHost = function(host){
	this.host = host;
	if(!host){
		$("#wip-title-host").text("host");
		this.setVul(null);
		this.setComment(null);
	} else {
		$("#wip-title-host").text(host.ip+'|'+host.url);
	}	
}
Current.prototype.getHost = function(){
	return this.host;
}
Current.prototype.setVul = function(vul){
	this.vul = vul;
	if(!vul) {
		$("#wip-title-vul").text("vul");
	} else {
		$("#wip-title-vul").text(vul.name);
	}	
}
Current.prototype.getVul = function(){
	return this.vul;
}
Current.prototype.setComment = function(comment){
	this.comment = comment;
	if(!comment) {
		$("#wip-title-comment").text("comment");
	} else {
		$("#wip-title-comment").text(comment.name);
	}	
}
Current.prototype.getComment = function(){
	return this.comment;
}

/**************************************
* Date: 2015-8-6
* Description: init the program
*
**************************************/
var current = new Current();

$(document).ready(function() {

    listProject();

//    bindAddProjectEvent();
    $("#wip-project-button-add").click(addProject);
    $("#wip-project-button-delete").click(deleteProject);
    $("#wip-project-button-modify").click(modifyProject);

    $("#wip-host-button-add").click(addHost);
});

/**************************************
* Date: 2015-8-6
* Description: manage the project table
**************************************/

function addProject(){
//	 data-toggle="modal" data-target="#wip-project"
	 $("#wip-project-modal").modal("show");
	 var options = {
    	type:"POST",
    	url:"addproject",
    	beforeSubmit:function(){
    		//参数校验
    	},
    	success:function(){   		
    		alert("提交成功!");
    		$("#wip-project-modal").modal("hide");
    		listProject();
    	},
    	error:function(err){
    	 	alert("提交失败!");
    	}
    };
    //$('#wip-project-modal-form').submit(function(){$(this).ajaxSubmit(options);return false;});  
    $("#wip-project-modal-form").ajaxForm(options);
}

function deleteProject(){
	if(confirm("是否删除当前项目？") == false){
		return
	}
	if(!current.getProject()) {
		alert("请先选择project!");
		return
	}
	$.get("/deleteproject?id="+current.getProject().id, function(data,status){
		if(status!="success") {
			alert("删除失败！");
		}
	});
	listProject();
	$("#wip-project-detail").empty();
	current.setProject(null);
}

function modifyProject(){
	$("#wip-project-modal").modal("show");
	$("#wip-project-modal-form-id").val(current.getProject().id);
	$("#wip-project-modal-form-name").val(current.getProject().name);
	$("#wip-project-modal-form-url").val(current.getProject().url);
	$("#wip-project-modal-form-ip").val(current.getProject().ip);
	$("#wip-project-modal-form-whois").val(current.getProject().whois);
	$("#wip-project-modal-form-disp").val(current.getProject().description);

	
	var options = {
    	type:"POST",
    	url:"modifyproject",
    	beforeSubmit:function(formData, jqForm, opt){
//    		var project = {};
//    		project.id = formData[0].value;
//    		project.name = formData[1].value;
//    		project.ip = formData[2].value;
//    		project.url = formData[3].value;
//    		project.whois = formData[4].value;
//    		project.description = formData[5].value;

//    		current.setProject(project);
    	},
    	success:function(){    		
    		alert("提交成功!");
    		$("#wip-project-modal").modal("hide");
    		listProject();
    	},
    	error:function(err){
    	 	alert("提交失败!");
    	}
    };

    $("#wip-project-modal-form").ajaxForm(options);
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
		$.each(result, function(id, name){
			addProjectItem(id, name);
		});
	});
}

function clickProject(){
	function addProjectDetailItem(name, value){
		$("#wip-project-detail").append($("<a></a>").addClass("list-group-item").attr("href","#").append($("<b></b>").text(name+":\t"), $("<br />"), value));
	}

	var id = $(this).attr('id').substring(15);
	$(this).addClass("active");
	if(current.getProject() && (current.getProject().id != id)){
		$("#wip-project-id-"+current.getProject().id).removeClass("active");
	}

	$("#wip-project-detail").empty();
	$.getJSON("/getprojectdetail?id="+id, function(result){
		current.setProject(result);
		addProjectDetailItem("项目名称", result.name);
		addProjectDetailItem("URL地址", result.url);
		addProjectDetailItem("IP地址", result.ip);
		addProjectDetailItem("Whois信息", result.whois);
		addProjectDetailItem("创建时间", result.ctime);
		addProjectDetailItem("描述信息", result.description);
	});
}

/**************************************
* Date: 2015-8-13
* Description: manage the host table
**************************************/

function addHost(){
	 $("#wip-host-modal").modal("show");
	 var options = {
    	type:"POST",
    	url:"addhost",
    	beforeSerialize:function(form, opt){
    	},
    	beforeSubmit:function(formData, jqForm, opt){
    		//参数校验
    		if (!current.getProject()) {
    			alert("请先选择project!");
    			$("#wip-host-modal").modal("hide");
    			return false;
    		}
    		var project_id = current.getProject().id;
    		formData[8] = {'name':'project_id', 'value':project_id}
    	},
    	success:function(){   		
    		alert("提交成功!");
    		$("#wip-host-modal").modal("hide");
    		listProject();
    	},
    	error:function(err){
    	 	alert("提交失败!");
    	}
    };

    $("#wip-host-modal-form").ajaxForm(options);
}

function deleteHost(){
	if(confirm("是否删除当前Host？") == false){
		return
	}
	if(!current.getHost()) {
		alert("请先选择Host!");
		return
	}
	$.get("/deletehost?id="+current.getHost().id, function(data,status){
		if(status!="success") {
			alert("删除失败！");
		}
	});
	listHost();
	$("#wip-vul-comment-list").empty();
	current.setHost(null);
}

function modifyHost(){
	$("#wip-host-modal").modal("show");
	$("#wip-host-modal-form-id").val(current.getHost().id);
	$("#wip-host-modal-form-url").val(current.getHost().url);
	$("#wip-host-modal-form-ip").val(current.getHost().ip);
	$("#wip-host-modal-form-level").val(current.getHost().level);
	$("#wip-host-modal-form-os").val(current.getHost().os);
	$("#wip-host-modal-form-server_info").val(current.getHost().server_info);
	$("#wip-host-modal-form-middleware").val(current.getHost().middleware);
	$("#wip-host-modal-form-description").val(current.getHost().description);
	
	var options = {
    	type:"POST",
    	url:"modifyhost",
    	beforeSubmit:function(formData, jqForm, opt){
    	},
    	success:function(){    		
    		alert("提交成功!");
    		$("#wip-host-modal").modal("hide");
    		listHost();
    	},
    	error:function(err){
    	 	alert("提交失败!");
    	}
    };

    $("#wip-host-modal-form").ajaxForm(options);
}

function listHost(){
	function addHostItem(id, url, ip){
		var b = $("<b></b>").text(ip)
		var i = $("<i></i>").text(url)
		var item = $("<a></a>").addClass("list-group-item").attr("id","wip-host-id-"+id).attr("href","#").append(b,i);
		item.click(clickHost);
		$("#wip-host-list").append(item);
	}

	current.initHost();
	$("#wip-host-list").empty()
	$.getJSON("/listhost", function(result){
		$.each(result, function(i, value){
			addHostItem(value.id, value.url, value.ip);
		});
	});
}

function clickHost(){
	function addHostDetailItem(name, value){
		$("#wip-vul-comment-list").append($("<a></a>").addClass("list-group-item").attr("href","#").append($("<b></b>").text(name+":\t"), $("<br />"), value));
	}

	var id = $(this).attr('id').substring(12);
	$(this).addClass("active");
	if(current.getHost() && (current.getHost().id != id)){
		$("#wip-host-id-"+current.getHost().id).removeClass("active");
	}

	$("#wip-vul-comment-list").empty();
	$.getJSON("/gethostdetail?id="+id, function(result){
		current.setHost(result);
		addHostDetailItem("URL地址", result.url);
		addHostDetailItem("IP地址", result.ip);
		addHostDetailItem("等级", result.level);
		addHostDetailItem("OS信息", result.os);
		addHostDetailItem("Server信息", result.server_info);
		addHostDetailItem("中间件", result.middleware);
		addHostDetailItem("描述", result.description);
	});
}

/**************************************
* Date: 2015-8-13
* Description: manage the vul table
**************************************/