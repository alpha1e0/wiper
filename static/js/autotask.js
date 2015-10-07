
function initTaskPage(){
    $("#wip-button-autotask-subdomainscan").unbind("click");
    $("#wip-button-autotask-subnetscan").unbind("click");
    $("#wip-button-autotask-servicerecognize").unbind("click");
    $("#wip-button-autotask-vulscan").unbind("click");

    $("#wip-button-autotask-subdomainscan").click(subDomainScanTask);
    $("#wip-button-autotask-subnetscan").click(subNetScanTask);
    $("#wip-button-autotask-servicerecognize").click(serviceRecognizeTask);
    $("#wip-button-autotask-vulscan").click(vulScanTask);

    subDomainScanTask();
}

function hideAllTask(){
    $("#wip-autotask-subdomainscan").hide();
    $("#wip-autotask-subnetscan").hide();
    $("#wip-autotask-servicerecognize").hide();
    $("#wip-autotask-vulscan").hide();
}

function inactiveAllButton(){
    $("#wip-button-autotask-subdomainscan").parent().removeClass("active");
    $("#wip-button-autotask-subnetscan").parent().removeClass("active");
    $("#wip-button-autotask-servicerecognize").parent().removeClass("active");
    $("#wip-button-autotask-vulscan").parent().removeClass("active");
}

function subDomainScanTask(){
//    if(!current.getProject()) {
//        alert("请先选择Project!");
//        return;
//    }
    hideAllTask();
    $("#wip-autotask-subdomainscan").show();
    inactiveAllButton();
    $("#wip-button-autotask-subdomainscan").parent().addClass("active");

    if(current.getHost()){
        var domain = current.getHost().url;
    }else if(current.getProject()){
        var domain = current.getProject().url;
    }else{
        var domain = "";
    }
    $("#wip-form-autotask-subdomainscan-domain").val(domain);

    $("#wip-form-autotask-subdomainscan-dictselect").empty()
    $.getJSON("/getdictlist", function(result){
        $.each(result, function(i, value){
            $("#wip-form-autotask-subdomainscan-dictselect").append($("<option></option>").val(value).text(value));
        });
    });
}

function subNetScanTask(){
//    if(!current.getProject()) {
//        alert("请先选择Project!");
//        return;
//    }
    hideAllTask();
    $("#wip-autotask-subnetscan").show();
    inactiveAllButton();
    $("#wip-button-autotask-subnetscan").parent().addClass("active");
}

function serviceRecognizeTask(){
    hideAllTask();
    $("#wip-autotask-servicerecognize").show();
    inactiveAllButton();
    $("#wip-button-autotask-servicerecognize").parent().addClass("active");
}

function vulScanTask(){
    hideAllTask();
    $("#wip-autotask-vulscan").show();
    inactiveAllButton();
    $("#wip-button-autotask-vulscan").parent().addClass("active");
}


$("#wip-tab-button-autotask").click(initTaskPage);

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
    $("#wip-form-domainseek-dnsbrute-dictadd").ajaxForm(options);	

	$("#wip-form-domainseek-dnsbrute-dictselect").empty()
	$.getJSON("/getdictlist", function(result){
        $.each(result, function(i, value){
            $("#wip-form-domainseek-dnsbrute-dictselect").append($("<option></option>").val(value).text(value));
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
    $("#wip-form-domainseek-dnsbrute-start").ajaxForm(options);
}

function configSubnetscanTask(){}

function listTaskResult(){
	if(!current.getProject()){
		$("#wip-domainseek-task-result-list").empty()
		return false;
	}
	function addTaskItem(id, url, ip, level, source){
		
		allDiv = $("<div></div>").addClass("list-group-item").attr("id","wip-domainseek-task-reuslt"+id);
		sourceSpan = $("<span></span>").text("来源："+source+" | "+"等级："+LEVELLIST[level]);
		urlA = $("<a></a>").text(" | URL: "+url).attr("href","http://"+url).attr("target","url_"+id);
		ipA = $("<a></a>").text(" | IP: "+ip).attr("href","http://"+ip).attr("target","ip_"+id);
		allDiv.append(sourceSpan,urlA,ipA);
		$("#wip-domainseek-task-result-list").append(allDiv);
	}

	$("#wip-domainseek-task-result-list").empty()
	$.getJSON("/gettaskresult?projectid="+current.getProject().id, function(result){
        $.each(result, function(i, value){
            addTaskItem(value.id, value.url, value.ip, value.level, value.source);
        });
    });
}