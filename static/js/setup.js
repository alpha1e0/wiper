
function initSetupPage(){
    $("#wip-button-setup-db").unbind("click");
    $("#wip-button-setup-dict").unbind("click");
    $("#wip-button-setup-else").unbind("click");

    $("#wip-button-setup-db").click(showDBSetup);
    $("#wip-button-setup-dict").click(showDictSetup);
    $("#wip-button-setup-else").click(showElseSetup);

    showDBSetup();
}

function hideAllSetup(){
	$("#wip-setup-db").hide();
    $("#wip-setup-dict").hide();
    $("#wip-setup-else").hide();
}

function inactiveAllSetupButton(){
    $("#wip-button-setup-db").parent().removeClass("active");
    $("#wip-button-setup-dict").parent().removeClass("active");
    $("#wip-button-setup-else").parent().removeClass("active");
}

$("#wip-tab-button-setup").click(initSetupPage);

//------------------------db setup-----------------------

function showDBSetup() {
	hideAllSetup();
	$("#wip-setup-db").show();
	inactiveAllSetupButton();
	$("#wip-button-setup-db").parent().addClass("active");

	$.getJSON("/dbsetup", function(result){
        $.each(result, function(i, value){
            $("#wip-form-setup-db-select").append($("<option></option").val(value).text(value));
        });
        renderTmpHostList(result['hosts']);
    });

	var options = {
        type:"post",
        url:"dbsetup",
        beforeSerialize:function(form, opt){
        },
        beforeSubmit:function(formData, jqForm, opt){
            //参数校验
        },
        success:function(){         
            alert("提交任务成功!");
        },
        error:function(xhr, status, error){
            alert("提交失败，失败原因："+xhr.responseText);
        }
    };
    $("#wip-form-setup-db").ajaxForm(options);
}

function showDictSetup() {
	hideAllSetup();
	$("#wip-setup-dict").show();
	inactiveAllSetupButton();
	$("#wip-button-setup-dict").parent().addClass("active");
}

function showElseSetup() {
	hideAllSetup();
	$("#wip-setup-else").show();
	inactiveAllSetupButton();
	$("#wip-button-setup-else").parent().addClass("active");
}