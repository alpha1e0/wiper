
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

function addDB() {
    var db = $("#wip-form-input-setup-db-dbadd").val();
    $("#wip-form-setup-db-select").append($("<option></option>").val(db).text(db));
}

function showDBSetup() {
	hideAllSetup();
	$("#wip-setup-db").show();
	inactiveAllSetupButton();
	$("#wip-button-setup-db").parent().addClass("active");

    $("#wip-form-setup-db-select").empty();
	$.getJSON("/dbsetup", function(result){
        $.each(result.all, function(i, value){
            $("#wip-form-setup-db-select").append($("<option></option").val(value).text(value));
        });
        $("#wip-form-setup-db-select option[val='wiper.db']").attr("selected", true);
    });

    $("#wip-form-button-setup-db-dbadd").unbind("click");
    $("#wip-form-button-setup-db-dbadd").click(addDB);

	var options = {
        type:"post",
        url:"dbsetup",
        beforeSerialize:function(form, opt){
        },
        beforeSubmit:function(formData, jqForm, opt){
            //参数校验
        },
        success:function(){         
            alert("提交成功!");
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
    $("#wip-form-setup-dict").ajaxForm(options);
}

function showElseSetup() {
	hideAllSetup();
	$("#wip-setup-else").show();
	inactiveAllSetupButton();
	$("#wip-button-setup-else").parent().addClass("active");

    var options = {
        type:"POST",
        url:"nmapsetup",
        beforeSerialize:function(form, opt){
        },
        beforeSubmit:function(formData, jqForm, opt){
            //参数校验
        },
        success:function(){             
            alert("设置成功!");
        },
        error:function(xhr, status, error){
            alert("设置失败!");
        }
    };
    $("#wip-form-setup-else-nmap").ajaxForm(options);
}