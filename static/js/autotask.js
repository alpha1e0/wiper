
function initTaskPage(){
    $("#wip-button-autotask-subdomainscan").unbind("click");
    $("#wip-button-autotask-subnetscan").unbind("click");
    $("#wip-button-autotask-servicerecognize").unbind("click");
    $("#wip-button-autotask-vulscan").unbind("click");
    $("#wip-button-autotask-search").unbind("click");

    $("#wip-button-autotask-subdomainscan").click(showSubDomainScanTask);
    $("#wip-button-autotask-subnetscan").click(showSubNetScanTask);
    $("#wip-button-autotask-servicerecognize").click(showServiceRecognizeTask);
    $("#wip-button-autotask-vulscan").click(showVulScanTask);
    $("#wip-button-autotask-search").click(showSearchTask);

    showSubDomainScanTask();
}

function hideAllTask(){
    $("#wip-autotask-subdomainscan").hide();
    $("#wip-autotask-subnetscan").hide();
    $("#wip-autotask-servicerecognize").hide();
    $("#wip-autotask-vulscan").hide();
    $("#wip-autotask-search").hide();
}

function inactiveAllTaskButton(){
    $("#wip-button-autotask-subdomainscan").parent().removeClass("active");
    $("#wip-button-autotask-subnetscan").parent().removeClass("active");
    $("#wip-button-autotask-servicerecognize").parent().removeClass("active");
    $("#wip-button-autotask-vulscan").parent().removeClass("active");
    $("#wip-button-autotask-search").parent().removeClass("active");
}

$("#wip-tab-button-autotask").click(initTaskPage);

//------------------------sub domain task-----------------------
function showSubDomainScanTask(){
    hideAllTask();
    $("#wip-autotask-subdomainscan").show();
    inactiveAllTaskButton();
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

function addIP(){
    var pip = arguments[0] ? arguments[0]:null;
    var pcount = arguments[0] ? arguments[0]:null;
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
    inactiveAllTaskButton();
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
    inactiveAllTaskButton();
    $("#wip-button-autotask-servicerecognize").parent().addClass("active");

    if (current.getHost()) {
        var domain = current.getHost().url;
    } else {
        var domain = "";
    }
    $("#wip-form-autotask-servicerecognize-domain").val(domain);

    var options = {
        type:"post",
        url:"servicerecognize",
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
    $("#wip-form-autotask-servicerecognize").ajaxForm(options);
}

//------------------------sub vul scan task-----------------------
function showVulScanTask(){
    hideAllTask();
    $("#wip-autotask-vulscan").show();
    inactiveAllTaskButton();
    $("#wip-button-autotask-vulscan").parent().addClass("active");
}

//------------------------common search-----------------------
function doSearch(){
    var packetstorm = "https://packetstormsecurity.com/search/?q=";
    var exploitdb = "https://www.exploit-db.com/search/?action=search&description=";

    var keywords = encodeURIComponent($("#wip-form-autotask-search").val());
    window.open(packetstorm+keywords);
    window.open(exploitdb+keywords);
}

function showSearchTask(){
    hideAllTask();
    $("#wip-autotask-search").show();
    inactiveAllTaskButton();
    $("#wip-button-autotask-search").parent().addClass("active");

    $("#wip-form-button-autotask-search").unbind("click");
    $("#wip-form-button-autotask-search").click(doSearch);
}
