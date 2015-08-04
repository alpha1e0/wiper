
var current = {};
current.project = null
current.host = null
current.port = null
current.vul = null
current.comment = null

$(document).ready(function() {
    listProject();

//    bindAddProjectEvent();
    $("#wip-project-button-add").click(addProject);
    $("#wip-project-button-delete").click(deleteProject);
    $("#wip-project-button-modify").click(modifyProject);
});

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
	$.get("/deleteproject?projectid="+current.project, function(data,status){
		if(status!="success") {
			alert("删除失败！");
		}
	});
	listProject();
	$("#wip-project-detail").empty();
	current.project = null;
}

function modifyProject(){
	$("#wip-project-modal").modal("show");
	$.getJSON("/getprojectdetail?projectid="+current.project, function(result){
		$("#wip-project-modal-form-id").val(current.project);
		$("#wip-project-modal-form-name").val(result[0]);
		$("#wip-project-modal-form-url").val(result[1]);
		$("#wip-project-modal-form-ip").val(result[2]);
		$("#wip-project-modal-form-whois").val(result[3]);
		$("#wip-project-modal-form-disp").val(result[5]);
	});
	
	var options = {
    	type:"POST",
    	url:"modifyproject",
    	beforeSubmit:function(){

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

function createModifyProjectDialog(){
	$("#wip-project-modal").modal("show");

	$.getJSON("/getprojectdetail?projectid="+current.project, function(result){
		$("#wip-project-modal-form-name").val(result[0]);
		$("#wip-project-modal-form-url").val(result[1]);
		$("#wip-project-modal-form-ip").val(result[2]);
		$("#wip-project-modal-form-whois").val(result[3]);
		$("#wip-project-modal-form-desp").val(result[4]);
	});

//	$("#wip-project-modal-title").text("添加项目");
//	$("#wip-project-modal-name").val(result[0]);
//	$("#wip-project-modal-url").val(result[1]);
//	$("#wip-project-modal-ip").val(result[2]);
//	$("#wip-project-modal-whois").val(result[3]);
//	$("#wip-project-modal-desp").val(result[4]);
}

function clickProject(){

	var id = $(this).attr('id').substring(15);
	$(this).addClass("active");
	$("#wip-project-id-"+current.project).removeClass("active");
	current.project = id;

	$("#wip-project-detail").empty();
	var nameList = ['Name','URL','IP','Whois','CreateTime','Description']
	$.getJSON("/getprojectdetail?projectid="+id, function(result){
		$.each(result, function(i, value){
			$("#wip-project-detail").append($("<a></a>").addClass("list-group-item").attr("href","#").append($("<b></b>").text(nameList[i]+":\t"), $("<br />"), value));
		});
	});
}

function listProject(){
	function createItem(id, name){
		var item = $("<a></a>").addClass("list-group-item").attr("id","wip-project-id-"+id).attr("href","#").text(name);
		item.click(clickProject);
		return item;
	}

	$("#wip-list-project").empty()
	$.getJSON("/listproject", function(result){
		$.each(result, function(name, value){
			$("#wip-list-project").append(createItem(name, value));
		});
	});
}

