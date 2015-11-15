
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

function inactiveAllButton(){
    $("#wip-button-setup-db").parent().removeClass("active");
    $("#wip-button-setup-dict").parent().removeClass("active");
    $("#wip-button-setup-else").parent().removeClass("active");
}

$("#wip-tab-button-setup").click(initSetupPage);

//------------------------db setup-----------------------

function showDBSetup() {
	hideAllSetup();
	$("#wip-setup-db").show();
	inactiveAllButton();
	$("#wip-button-setup-db").parent().addClass("active");
}

function showDictSetup() {
	hideAllSetup();
	$("#wip-setup-dict").show();
	inactiveAllButton();
	$("#wip-button-setup-dict").parent().addClass("active");
}

function showElseSetup() {
	hideAllSetup();
	$("#wip-setup-else").show();
	inactiveAllButton();
	$("#wip-button-setup-else").parent().addClass("active");
}