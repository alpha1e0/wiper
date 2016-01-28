
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
    this.porderby = null;
    this.horderby = null;
}

Current.prototype.init = function(){
    this.project = null;
    this.host = null;
    this.vul = null;
    this.comment = null;
    this.porderby = "level";
    this.horderby = "level";

    $("#wip-title-project").text("null");
    $("#wip-title-host").text("null");
    $("#wip-title-vul").text("null");
    $("#wip-title-comment").text("null");
}
Current.prototype.initProject = function(){
    this.project = null;
    this.host = null;
    this.vul = null;
    this.comment = null;

    $("#wip-title-project").text("null");
    $("#wip-title-host").text("null");
    $("#wip-title-vul").text("null");
    $("#wip-title-comment").text("null");
}
Current.prototype.initHost = function(){
    this.host = null;
    this.vul = null;
    this.comment = null;

    $("#wip-title-host").text("null");
    $("#wip-title-vul").text("null");
    $("#wip-title-comment").text("null");
}
Current.prototype.initVul = function(){
    this.vul = null;

    $("#wip-title-vul").text("null");
}
Current.prototype.initComment = function(){
    this.comment = null;

    $("#wip-title-comment").text("null");
}
Current.prototype.setProject = function(project){
    this.project = project;
    if(!project) {
        $("#wip-title-project").text("null");
    } else {
        $("#wip-title-project").text(project.name);
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
        $("#wip-title-host").text("null");
    } else {
        $("#wip-title-host").text(host.title);
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
        $("#wip-title-vul").text("null");
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
        $("#wip-title-comment").text("null");
    } else {
        $("#wip-title-comment").text(comment.name);
    }   
}
Current.prototype.getComment = function(){
    return this.comment;
}

/******************************************************************************************************
* Date: 2015-8-6
* Description: 初始化工作，绑定事件
******************************************************************************************************/
var current = new Current();
current.init();

var LEVELLIST = ["undefined","关键","重要","一般","提示"];
var LEVELCLASSLIST = ["list-group-item-info","list-group-item-danger","list-group-item-warning","list-group-item-info","list-group-item-success"];
var VULTYPELIST = ["undefined","溢出漏洞","注入漏洞","XSS","CSRF","路径遍历","上传","逻辑漏洞","弱口令","信息泄露","配置错误","认证/会话管理","点击劫持","跨域漏洞","其他"];

$(document).ready(function() {
    listProject();
    //绑定与project相关操作的事件
    $("#wip-button-project-levelsort").click(function(){listProject("level");});
    $("#wip-button-project-namesort").click(function(){listProject("name");});
    $("#wip-button-project-timesort").click(function(){listProject("ctime");});

    $("#wip-button-project-add").click(addProject);
    $("#wip-button-project-refresh").click(refreshProject);
    $("#wip-button-project-import").click(importProject);

    //绑定与host相关操作的事件
    $("#wip-button-host-levelsort").click(function(){listHost("level");});
    $("#wip-button-host-ipsort").click(function(){listHost("ip");});
    $("#wip-button-host-urlsort").click(function(){listHost("url");});

    $("#wip-tab-button-detail").click(function(){listHost();});
    $("#wip-button-host-add").click(addHost);
    $("#wip-button-host-refresh").click(refreshHost);

    //绑定与vul、comment相关操作的事件
    $("#wip-button-host-detail").click(listHostDetail);
    $("#wip-button-vul-list").click(function(){listVul();});
    $("#wip-button-comment-list").click(function(){listComment();});

});


function adjustListColumnHeight(listdom, restHeight) {
    var maxheight = document.documentElement.clientHeight - restHeight;
    maxheight = maxheight + "px";
    //listdom.css({"max-height":maxheight;});
    listdom.css("max-height",maxheight);
}

/******************************************************************************************************
* Date: 2015-8-6
* Author: alphp1e0
* Description: project相关操作，增、删、改操作，显示项目列表、显示项目详情
******************************************************************************************************/


function renderProjectListColumn(data){
    if(!data) return;
    function genRow(project){
        var row = $("<a></a>").addClass("list-group-item").attr("id","wip-project-id-"+project.id).attr("href","#").text(project.name);
        row.click(clickProject);
        row.addClass(LEVELCLASSLIST[project.level]);
        return row;
    }

    clearProjectListColumn();
    var listGroup = $("<div></div").attr("id","wip-project-list").addClass("content-list");
    adjustListColumnHeight(listGroup,200);
    for(var i=0;i<data.length;i++){
        listGroup.append(genRow(data[i]));
    }
    $("#wip-project-list-column").append(listGroup);
}

function clearProjectListColumn(){
    $("#wip-project-list-column").empty();
}

function renderProjectDetailColumn(data){
    if(!data) return;
    function genRow(name, value){
        var row = $("<pre></pre>").addClass("list-group-item").append($("<b class='text-primary'></b>").text(name+":"), $("<br />"), $("<span></span>").text(value));
        return row;
    }

    clearProjectDetailColumn();
    var listGroup = $("<div></div").attr("id","wip-project-detail-list").addClass("content-list");
    adjustListColumnHeight(listGroup,250);
    listGroup.append(genRow("项目名称", data.name));
    listGroup.append(genRow("URL地址", data.url));
    listGroup.append(genRow("IP地址", data.ip));
    listGroup.append(genRow("等级", LEVELLIST[data.level]));
    listGroup.append(genRow("Whois信息", data.whois));
    listGroup.append(genRow("创建时间", data.ctime));
    listGroup.append(genRow("描述信息", data.description));

    var modifyButton = $('<button id="wip-button-project-modify" type="button" class="btn btn-success" title="修改项目"><span class="glyphicon glyphicon-pencil" aria-hidden="true"></span></button>')
    modifyButton.click(modifyProject);
    var deleteButton = $('<button id="wip-button-project-delete" type="button" class="btn btn-warning" title="删除项目"><span class="glyphicon glyphicon-minus" aria-hidden="true"></span></button>')
    deleteButton.click(deleteProject);
    var exportButton = $('<button id="wip-button-project-export" type="button" class="btn btn-success" title="导出项目">导出项目</button>');
    exportButton.click(exportProject);
    var operationGroup = $("<div></div").attr("id","wip-project-detail-operation").append(modifyButton," ",deleteButton," ",exportButton);

    $("#wip-project-detail-column").append(listGroup, $("<br />"), operationGroup);
}

function clearProjectDetailColumn(){
    $("#wip-project-detail-column").empty();
}

function listProject(){
    var orderby = arguments[0] ? arguments[0]:"level";
    current.initProject();
    current.porderby = orderby;
    $.getJSON("/listproject?orderby="+orderby, function(result){
        renderProjectListColumn(result);
    });
    clearProjectDetailColumn();
}

function clickProject(){
    var id = $(this).attr('id').substring(15);
    $(this).addClass("active");
    if(current.getProject() && (current.getProject().id != id)){
        $("#wip-project-id-"+current.getProject().id).removeClass("active");
    }

    $.getJSON("/getprojectdetail?id="+id, function(result){
        current.setProject(result);
        renderProjectDetailColumn(result);
    });
}

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
            listProject(current.porderby);
        },
        error:function(xhr, status, error){
            alert("提交失败，失败原因："+xhr.responseText);
        }
    }
    $("#wip-modal-form-project").ajaxForm(options);
    //$('#wip-modal-form-project').submit(function(){$(this).ajaxSubmit(options);return false;});  
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
        $("#wip-project-detail").empty();
        current.setProject(null);
        listProject(current.porderby);
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
    //$("input:radio").attr("checked",false);
    $("input[name='level']").get(current.getProject().level-1).checked=true;

    
    var options = {
        type:"POST",
        url:"modifyproject",
        beforeSubmit:function(formData, jqForm, opt){
            //参数校验
        },
        success:function(){         
            alert("提交成功!");
            $("#wip-modal-project").modal("hide");
            listProject(current.porderby);
        },
        error:function(xhr, status, error){
            alert("提交失败，失败原因："+xhr.responseText);
        }
    };

    $("#wip-modal-form-project").ajaxForm(options);
}

function refreshProject(){
    current.initProject();
    listProject(current.porderby);
}

function importProject(){
    $("#wip-modal-project-import").modal("show");
    var options = {
        type:"POST",
        url:"importproject",
        beforeSerialize:function(form, opt){
        },
        beforeSubmit:function(formData, jqForm, opt){
            //参数校验
        },
        success:function(){             
            alert("提交成功!");
            $("#wip-modal-project-import").modal("hide");
            listProject();
        },
        error:function(xhr, status, error){
            alert("提交失败，失败原因："+xhr.responseText);
        }
    };

    $("#wip-modal-form-project-import").ajaxForm(options);
}

function exportProject(){
    if(!current.getProject()) {
        alert("请先选择project!");
        return;
    }
    $.get("/exportproject?id="+current.getProject().id,function(){
        alert("导出成功，请到‘/static/tmp/’目录下下载");
    });
}

/******************************************************************************************************
* Date: 2015-8-13
* Author: alphp1e0
* Description: host相关的操作，增、删、该，显示host列表、显示host详情
******************************************************************************************************/

function renderHostListColumn(data){
    if(!data) return;
    function genRow(host){
        var b = $("<b></b>").text(host.ip+" | ");
        if (host.protocol=="http" || host.protocol=="https") {
            if (host.url!=null) {
                var i = $("<i></i>").text(host.url);
            } else {
                var i = $("<i></i>").text(host.protocol);
            }       
        } else {
            var i = $("<i></i>").text(host.protocol)
        }
        var item = $("<a></a>").addClass("list-group-item").attr("id","wip-host-id-"+host.id).attr("href","#").append(b,i);
        item.click(clickHost);
        item.addClass(LEVELCLASSLIST[host.level]);
        return item;
    }
    clearHostListColumn();
    var listGroup = $("<div></div").attr("id","wip-host-list").addClass("content-list");
    adjustListColumnHeight(listGroup,200);
    for(var i=0; i<data.length; i++){
        listGroup.append(genRow(data[i]));
    }
    $("#wip-host-list-column").append(listGroup);
}

function clearHostListColumn(){
    $("#wip-host-list-column").empty();
}

function renderHostDetailColumn(data){
    if (!data) return;
    //type:protocol type ["undefined","http","https","ftp","ssh","telnet","vnc","rdp","mysql","sqlserver","oracle"]
    function genRow(name, value){
        var protocol = arguments[2] ? arguments[2]:null;
        var port = arguments[3] ? arguments[3]:null;
        if (protocol==null) {
            var row = $("<pre></pre>").addClass("list-group-item").append($("<b class='text-primary'></b>").text(name+":\t"), $("<br />"), value);
        } else {            
            var uri = protocol + "://" + value + ":" + port;
            var a = $("<a></a>").attr("href", uri).attr("target","_blank").text(uri);
            var row = $("<pre></pre>").addClass("list-group-item").append($("<b class='text-primary'></b>").text(name+":\t"), $("<br />"), a);
        }
        return row;
    }

    clearHostDetailColumn();
    var listGroup = $("<div></div").attr("id","wip-host-detail-list").addClass("content-list");
    adjustListColumnHeight(listGroup,250);
    listGroup.append(genRow("Title", data.title));
    if(data.protocol=="http" || data.protocol=="https") {
        listGroup.append(genRow("URL地址", data.url, data.protocol, data.port));
        listGroup.append(genRow("IP地址", data.ip, data.protocol, data.port));
    } else {
        listGroup.append(genRow("IP地址", data.ip, data.protocol, data.port));
        listGroup.append(genRow("端口", data.port));
        listGroup.append(genRow("协议", data.protocol));
    }
    listGroup.append(genRow("等级", LEVELLIST[data.level]));
    listGroup.append(genRow("OS信息", data.os));
    listGroup.append(genRow("Server信息", data.server_info));
    listGroup.append(genRow("中间件", data.middleware));
    listGroup.append(genRow("描述", data.description));

    var modifyButton = $('<button id="wip-button-host-modify" type="button" class="btn btn-success" title="修改Host"><span class="glyphicon glyphicon-pencil" aria-hidden="true"></span></button>')
    modifyButton.click(modifyHost);
    var deleteButton = $('<button id="wip-button-host-delete" type="button" class="btn btn-warning" title="删除Host"><span class="glyphicon glyphicon-minus" aria-hidden="true"></span></button>')
    deleteButton.click(deleteHost);
    var operationGroup = $("<div></div").attr("id","wip-host-detail-operation").append(modifyButton," ",deleteButton);

    $("#wip-host-detail-column").append(listGroup, $("<br />"), operationGroup);
}

function clearHostDetailColumn(){
    $("#wip-host-detail-column").empty();
}

function listHost(){
    var orderby = arguments[0] ? arguments[0]:"level";
    current.horderby = orderby;
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
    
    current.initHost();
    clearHostDetailColumn();
    clearVulDetailColumn();
    var url = "/listhost?projectid=" + current.getProject().id + "&orderby=" + orderby;
    $.getJSON(url, function(result){
        renderHostListColumn(result);
    });
}

function listHostDetail(){
    var host = current.getHost()
    if(!host) {
        alert("请先选择Host!");
        return
    }

    renderHostDetailColumn(host);
}

function clickHost(){
    if(!current.getProject()) {
        alert("请先选择project!");
        return
    }
    
    var id = $(this).attr('id').substring(12);
    $(this).addClass("active");
    if(current.getHost() && (current.getHost().id != id)){
        $("#wip-host-id-"+current.getHost().id).removeClass("active");
    }
    
    $.getJSON("/gethostdetail?id="+id, function(result){
        current.setHost(result);
        renderHostDetailColumn(result);
    });
}

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
            formData.push({'name':'project_id', 'value':project_id});
        },
        success:function(){         
            alert("提交成功!");
            $("#wip-modal-host").modal("hide");
            listHost(current.horderby);
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
        $("#wip-vul-comment-list").empty();
        current.setHost(null);
        listHost(current.horderby);
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
    $("#wip-modal-form-host-port").val(current.getHost().port);
    $("#wip-modal-form-host-protocol option:selected").removeAttr("selected");
    $("#wip-modal-form-host-protocol option[value="+current.getHost().protocol+"]").attr("selected",true);
    $("#wip-modal-form-host-title").val(current.getHost().title);
    $("#wip-modal-form-host-os").val(current.getHost().os);
    $("#wip-modal-form-host-server_info").val(current.getHost().server_info);
    $("#wip-modal-form-host-middleware").val(current.getHost().middleware);
    $("#wip-modal-form-host-description").val(current.getHost().description);
    //$("input:radio").attr("checked",false);
    $("input[name='level']").get(current.getHost().level+3).checked=true;
    
    var options = {
        type:"POST",
        url:"modifyhost",
        beforeSubmit:function(formData, jqForm, opt){
        },
        success:function(){         
            alert("提交成功!");
            $("#wip-modal-host").modal("hide");
            listHost(current.horderby);
        },
        error:function(xhr, status, error){
            alert("提交失败，失败原因："+xhr.responseText);
        }
    };

    $("#wip-modal-form-host").ajaxForm(options);
}

function refreshHost(){
    current.initHost();
    //clearHostListColumn();
    //clearHostDetailColumn();
    listHost(current.horderby);
}

/******************************************************************************************************
* Date: 2015-8-13
* Author: alphp1e0
* Description: 漏洞相关操作，增、删、该，显示漏洞列表，显示漏洞详情
******************************************************************************************************/

function renderVulListColumn(data){
    if(!data) return;
    function genRow(vul){
        var row = $("<a></a>").addClass("list-group-item").attr("id","wip-vul-id-"+vul.id).attr("href","#").text(vul.name);
        row.click(clickVul);
        row.addClass(LEVELCLASSLIST[vul.level]);
        return row;
    }

    clearVulListColumn();
    clearVulDetailColumn();

    var addButton = $('<button id="wip-button-vul-add" type="button" class="btn btn-success" title="添加漏洞"><span class="glyphicon glyphicon-plus" aria-hidden="true"></span></button>')
    addButton.click(addVul);
    var refreshButton = $('<button id="wip-button-vul-refresh" type="button" class="btn btn-success" title="刷新漏洞列表"><span class="glyphicon glyphicon-repeat" aria-hidden="true"></span></button>')
    refreshButton.click(refreshVul);
    var operationGroup = $("<div></div").attr("id","wip-vul-list-operation").append(refreshButton," ",addButton,$("<hr class='thin'/>"));

    var listGroup = $("<div></div").attr("id","wip-vul-list").addClass("content-list");
    adjustListColumnHeight(listGroup,250);
    for(var i=0; i<data.length; i++){
        listGroup.append(genRow(data[i]));
    }

    $("#wip-host-detail-column").append(operationGroup, listGroup);
}

function clearVulListColumn(){
    $("#wip-host-detail-column").empty();
}

function renderVulDetailColumn(data){
    if(!data) return;
    function genRow(name, value){
        var type = arguments[2] ? arguments[2]:0;
        if(type==0){
            var row = $("<pre></pre>").addClass("list-group-item").append($("<b class='text-primary'></b>").text(name+":\t"), $("<br />"), value);
        }else{
            if(!value){
                var uri=""
            }else{
                var uri = value;
            }
            var a = $("<a></a>").attr("href", type+"://"+uri).attr("target","_blank").text(uri);
            var row = $("<pre></pre>").addClass("list-group-item").append($("<b class='text-primary'></b>").text(name+":\t"), $("<br />"), a);
        }
        return row;
    }

    clearVulDetailColumn();
    var listGroup = $("<div></div").attr("id","wip-vul-detail-list").addClass("content-list");
    adjustListColumnHeight(listGroup,250);
    listGroup.append(genRow("名称", data.name));
    listGroup.append(genRow("等级", LEVELLIST[data.level]));
    listGroup.append(genRow("URL地址", data.url, current.getHost().protocol));
    listGroup.append(genRow("详情", data.info));
    listGroup.append(genRow("类型", VULTYPELIST[data.type]));
    listGroup.append(genRow("描述", data.description));

    var modifyButton = $('<button id="wip-button-vul-modify" type="button" class="btn btn-success" title="修改漏洞"><span class="glyphicon glyphicon-pencil" aria-hidden="true"></span></button>')
    modifyButton.click(modifyVul);
    var deleteButton = $('<button id="wip-button-vul-delete" type="button" class="btn btn-warning" title="删除漏洞"><span class="glyphicon glyphicon-minus" aria-hidden="true"></span></button>')
    deleteButton.click(deleteVul);
    var operationGroup = $("<div></div").attr("id","wip-vul-detail-operation").append(modifyButton," ",deleteButton);

    $("#wip-vul-detail-column").append(listGroup, $("<br />"), operationGroup);
}

function clearVulDetailColumn(){
    $("#wip-vul-detail-column").empty();
}

function listVul(){
    var orderby = arguments[0] ? arguments[0]:"level";
    if(!current.getHost()) {
        alert("请先选择Host!");
        return;
    }

    current.initVul();
    var url = "/listvul?hostid=" + current.getHost().id + "&orderby=" + orderby;
    $.getJSON(url, function(result){
        renderVulListColumn(result);
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
    
    current.initVul();
    $.getJSON("/getvuldetail?id="+id, function(result){
        current.setVul(result);
        renderVulDetailColumn(result);
    });
}

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
            formData.push({'name':'host_id', 'value':host_id});
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
        $("#wip-vul-comment-list").empty();
        current.setVul(null);
        listVul();
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
    $("#wip-modal-form-vul-description").val(current.getVul().description);
    $("input[name='level']").get(current.getVul().level+7).checked=true;
    $("#wip-modal-form-vul-type option:selected").removeAttr("selected");
    $("#wip-modal-form-vul-type option[value="+current.getVul().type+"]").attr("selected",true);
    
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



function refreshVul(){
    current.initVul();
    //current.initComment();
    listVul();
}

/******************************************************************************************************
* Date: 2015-8-13
* Author: alphp1e0
* Description: 备注相关操作，增、删、改，显示备注列表、显示备注详情
******************************************************************************************************/

function renderCommentListColumn(data){
    if(!data) return;
    function genRow(comment){
        var row = $("<a></a>").addClass("list-group-item").attr("id","wip-comment-id-"+comment.id).attr("href","#").text(comment.name);
        row.click(clickComment);
        row.addClass(LEVELCLASSLIST[comment.level]);
        return row;
    }

    clearCommentListColumn();
    clearCommentDetailColumn();

    var addButton = $('<button id="wip-button-comment-add" type="button" class="btn btn-success" title="添加备注"><span class="glyphicon glyphicon-plus" aria-hidden="true"></span></button>')
    addButton.click(addComment);
    var refreshButton = $('<button id="wip-button-comment-refresh" type="button" class="btn btn-success" title="刷新备注列表"><span class="glyphicon glyphicon-repeat" aria-hidden="true"></span></button>')
    refreshButton.click(refreshComment);
    var attachButton = $('<button id="wip-button-attachment-add" type="button" class="btn btn-success">添加附件</button>');
    attachButton.click(addAttachment);
    var operationGroup = $("<div></div").attr("id","wip-comment-list-operation").append(refreshButton, " ", addButton, " ", attachButton, $("<hr class='thin'/>"));

    var listGroup = $("<div></div").attr("id","wip-comment-list").addClass("content-list");
    adjustListColumnHeight(listGroup,250);
    for(var i=0; i<data.length; i++){
        listGroup.append(genRow(data[i]));
    }

    $("#wip-host-detail-column").append(operationGroup, listGroup);
}

function clearCommentListColumn(){
    $("#wip-host-detail-column").empty();
}

function renderCommentDetailColumn(data){
    if(!data) return;
    function genRow(name, value){
        var type = arguments[2] ? arguments[2]:0;
        if(type==0){
            var row = $("<pre></pre>").addClass("list-group-item").append($("<b class='text-primary'></b>").text(name+":\t"), $("<br />"), value);
        }else{
            if(!value){
                var uri=""
            }else{
                var uri = value;
            }
            var a = $("<a></a>").attr("href", type+"://"+uri).attr("target","_blank").text(uri);
            var row = $("<pre></pre>").addClass("list-group-item").append($("<b class='text-primary'></b>").text(name+":\t"), $("<br />"), a);
        }
        return row;
    }

    clearCommentDetailColumn();
    var listGroup = $("<div></div").attr("id","wip-comment-detail-list").addClass("content-list");
    adjustListColumnHeight(listGroup,250);
    listGroup.append(genRow("名称", data.name));
    listGroup.append(genRow("等级", LEVELLIST[data.level]));
    listGroup.append(genRow("URL地址", data.url, current.getHost().protocol));
    listGroup.append(genRow("详情", data.info));
    listGroup.append(genRow("描述", data.description));
    var link = $("<a></a>").attr("href", "static/attachment/"+data.attachment).attr("target","_blank").text(data.attachment);
    var attachmentItem = $("<div></div>").addClass("list-group-item").append($("<b class='text-primary'></b>").text("附件"+":\t"), $("<br />"), link);
    listGroup.append(attachmentItem);

    var modifyButton = $('<button id="wip-button-comment-modify" type="button" class="btn btn-success" title="修改备注"><span class="glyphicon glyphicon-pencil" aria-hidden="true"></span></button>')
    modifyButton.click(modifyComment);
    var deleteButton = $('<button id="wip-button-comment-delete" type="button" class="btn btn-warning" title="删除备注"><span class="glyphicon glyphicon-minus" aria-hidden="true"></span></button>')
    deleteButton.click(deleteComment);
    var operationGroup = $("<div></div").attr("id","wip-comment-detail-operation").append(modifyButton," ",deleteButton);

    $("#wip-vul-detail-column").append(listGroup, $("<br />"), operationGroup);
}

function clearCommentDetailColumn(){
    $("#wip-vul-detail-column").empty();
}

function listComment(){
    var orderby = arguments[0] ? arguments[0]:"level";
    if(!current.getHost()) {
        alert("请先选择Host!");
        return;
    }

    current.initComment();
    var url = "/listcomment?hostid=" + current.getHost().id + "&orderby=" + orderby;
    $.getJSON(url, function(result){
        renderCommentListColumn(result);
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

    $.getJSON("/getcommentdetail?id="+id, function(result){
        current.setComment(result);
        renderCommentDetailColumn(result);
    });
}

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
            formData.push({'name':'host_id', 'value':host_id});
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
        $("#wip-vul-comment-list").empty();
        current.setComment(null);
        listComment();
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
    $("#wip-modal-form-comment-type").val(current.getComment().attachment);
    $("#wip-modal-form-comment-description").val(current.getComment().description);
    $("input[name='level']").get(current.getComment().level+11).checked=true;
        
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

function refreshComment(){
    current.initComment();
    listComment();
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
            listComment();
        },
        error:function(xhr, status, error){
            alert("提交失败，失败原因："+xhr.responseText);
        }
    };

    $("#wip-modal-form-attachment").ajaxForm(options);
}



