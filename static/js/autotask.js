
function initTaskPage(){
    $("#wip-button-autotask-subdomainscan").unbind("click");
    $("#wip-button-autotask-subnetscan").unbind("click");
    $("#wip-button-autotask-servicerecognize").unbind("click");
    $("#wip-button-autotask-vulscan").unbind("click");

    $("#wip-button-autotask-subdomainscan").click(showSubDomainScanTask);
    $("#wip-button-autotask-subnetscan").click(showSubNetScanTask);
    $("#wip-button-autotask-servicerecognize").click(showServiceRecognizeTask);
    $("#wip-button-autotask-vulscan").click(showVulScanTask);

    showSubDomainScanTask();
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

$("#wip-tab-button-autotask").click(initTaskPage);

//------------------------sub domain task-----------------------
function showSubDomainScanTask(){
    hideAllTask();
    $("#wip-autotask-subdomainscan").show();
    inactiveAllButton();
    $("#wip-button-autotask-subdomainscan").parent().addClass("active");

    if (current.getHost()) {
        var domain = current.getHost().url;
    } else if (current.getProject()) {
        var domain = current.getProject().url;
    } else {
        var domain = "";
    }
    $("#wip-form-autotask-subdomainscan-domain").val(domain);
    $("#wip-form-autotask-subdomainscan-dictselect").empty()
    $.getJSON("/subdomainscan", function(result){
        $.each(result, function(i, value){
            $("#wip-form-autotask-subdomainscan-dictselect").append($("<option></option>").val(value).text(value));
        });
    });

    var options = {
        type:"POST",
        url:"subdomainscan",
        beforeSerialize:function(form, opt){
        },
        beforeSubmit:function(formData, jqForm, opt){
            //参数校验
            if (!current.getProject()) {
                alert("请先选择project!");
                return false;
            }
            var project_id = current.getProject().id;
            formData.push({'name':'project_id', 'value':project_id});
        },
        success:function(){         
            alert("提交任务成功!");
        },
        error:function(xhr, status, error){
            alert("提交失败，失败原因："+xhr.responseText);
        }
    };
    $("#wip-form-autotask-subdomainscan").ajaxForm(options);
}

//------------------------sub net task-----------------------
function delIP(){
    $("#wip-form-autotask-subnetscan-ipselect option:selected").remove();
}

function addIP(pip=null,pcount=null){
    if (pip==null) {
        var ip = $("#wip-form-input-autotask-subnetscan-ipadd").val();
        var count = 1;
    } else {
        var ip = pip;
        var count = pcount;
    }
    var re = /^((2[0-4]\d|25[0-5]|[01]?\d?\d)\.){3}(2[0-4]\d|25[0-5]|[01]?\d\d?)$/g
    if (!re.test(ip)) {
        return
    }
    var selectItem = $("<option></option>").val(ip).text(ip+" 数目:"+count);
    $("#wip-form-autotask-subnetscan-ipselect").append(selectItem);
}

function saveTmpHost() {
    var id = $(this).parent().parent().attr("id").substring(15);
    $.get("/savetmphost?id="+id, function(){
        $("#wip-tmphost-id-"+id).remove();
    });
}

function deleteTmpHost() {
    var id = $(this).parent().parent().attr("id").substring(15);
    $.get("/deletetmphost?id="+id, function(){
        $("#wip-tmphost-id-"+id).remove();
    });
}

function renderTmpHostList(hosts) {
    for (var i=0; i<hosts.length; i++) {
        var title = $("<td></td>").text(hosts[i].title);
        if (hosts[i].protocol=='http' || hosts[i].protocol=='https') {
            var ipstr = hosts[i].protocol + "://" + hosts[i].ip + ":" + hosts[i].port;
            var iplink = $("<a></a>").attr("href", ipstr).text(ipstr).attr("target","_blank");
            var ip = $("<td></td>").append(iplink);
        } else {
            var ip = $("<td></td>").text(hosts[i].protocol + "://" + hosts[i].ip + ":" + hosts[i].port);
        }
        var protocol = $("<td></td>").text(hosts[i].protocol);
        var saveButton = $("<a></a>").text("保存").click(saveTmpHost).attr("href","#");
        var deleteButton = $("<a></a>").text("删除").click(deleteTmpHost).attr("href","#");
        var operation = $("<td></td>").append(saveButton, " | ", deleteButton);

        var tr = $("<tr></tr>").attr("id","wip-tmphost-id-"+hosts[i].id).append(title, ip, protocol, operation);
        $("#wip-table-autotask-subnetscan-tmphostlist").append(tr);
    }
}

function showSubNetScanTask() {
    if (!current.getProject()) {
        alert("请先选择project!");
        return false;
    }
    hideAllTask();
    $("#wip-autotask-subnetscan").show();
    inactiveAllButton();
    $("#wip-button-autotask-subnetscan").parent().addClass("active");

    $("#wip-form-button-autotask-subnetscan-ipdel").unbind("click");
    $("#wip-form-button-autotask-subnetscan-ipdel").click(delIP);
    $("#wip-form-button-autotask-subnetscan-ipadd").unbind("click");
    $("#wip-form-button-autotask-subnetscan-ipadd").click(function(){addIP(null)});

    $.getJSON("/subnetscan?project_id="+current.getProject().id, function(result){
        $("#wip-form-autotask-subnetscan-ipselect").empty();
        $.each(result['iplist'], function(i, value){
            addIP(value[0],value[1]);
        });
        renderTmpHostList(result['hosts']);
    });

    var options = {
        type:"POST",
        url:"subnetscan",
        beforeSerialize:function(form, opt){
        },
        beforeSubmit:function(formData, jqForm, opt){
            //参数校验
            if (!current.getProject()) {
                alert("请先选择project!");
                return false;
            }
            var project_id = current.getProject().id;
            formData.push({'name':'project_id', 'value':project_id});
        },
        success:function(){         
            alert("提交任务成功!");
        },
        error:function(xhr, status, error){
            alert("提交失败，失败原因："+xhr.responseText);
        }
    };
    $("#wip-form-autotask-subnetscan").ajaxForm(options);
}

//------------------------sub service recognize task-----------------------
function showServiceRecognizeTask(){
    hideAllTask();
    $("#wip-autotask-servicerecognize").show();
    inactiveAllButton();
    $("#wip-button-autotask-servicerecognize").parent().addClass("active");
}

//------------------------sub vul scan task-----------------------
function showVulScanTask(){
    hideAllTask();
    $("#wip-autotask-vulscan").show();
    inactiveAllButton();
    $("#wip-button-autotask-vulscan").parent().addClass("active");
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