
var current = {};
current.project = null
current.host = null
current.port = null
current.vul = null
current.comment = null

$(document).ready(function() {
    var options = {
    	type:"POST",
    	beforeSubmit:function(){
    		//参数校验
    	},
    	success:function(){
    		alert("提交成功!");
    		$('#wip-add-project').modal('hide');
    	},
    	error:function(err){
    	 	alert("提交失败!");
    	}
    };
    //$('#wip-add-project-form').submit(function(){$(this).ajaxSubmit(options);return false;});  
    $("#wip-add-project-form").ajaxForm(options);

    listProject();
});


function clickProject(){
	alert($(this).attr('id'));
}

function listProject(){
	function createItem(id, name){
		var item = $("<a></a>").addClass("list-group-item").attr("id","wip-project-id-"+id).attr("href","#");
		item.append($("<span></span>").text(name));
		item.click(clickProject);
		return item;
	}

	$.getJSON("/listproject", function(result){
		$.each(result, function(i, field){
			$("#wip-list-project").append(createItem(i, field));
		});
	});
}

