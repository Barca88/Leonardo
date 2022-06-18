class Parameters {
	constructor() {
		this._domain = "";
		this._subdomain = "";
		this._difficulty = 0;
		this._reps = 0;
		this._precs = [];
		this.header = ""
	}
	get domain() {
		return this._domain;
	}
	set domain(v) {
		this._domain = v;
	}
	get subdomain() {
		return this._subdomain;
	}
	set subdomain(v) {
		this._subdomain = v;
	}
	get difficulty() {
		return this._difficulty;
	}
	set difficulty(v) {
		this._difficulty = v;
	}
	get reps() {
		return this._reps;
	}
	set reps(v) {
		this._reps = v;
	}
	get precs() {
		return this._precs;
	}
	set precs(v) {
		this._precs = v;
	}
	get header() {
		return this._header;
	}
	set header(v){
		this._header = v;
	}
}

class Answer {
	constructor() {
		this._correction = -1;
		this._mandatory = false;
		this._content = "";
	}
	get correction() {
		return this._correction;
	}
	set correction(v) {
		this._correction = v;
	}
	get mandatory() {
		return this._mandatory;
	}
	set mandatory(v) {
		this._mandatory = v;
	}
	get content() {
		return this._content;
	}
	set content(v) {
		this._content = v;
	}
}

class Solution {
	constructor() {
		this._refs = [];
		this._content = "";
	}
	get refs() {
		return this._refs;
	}
	set refs(v) {
		this._refs = v;
	}
	get content() {
		return this._content;
	}
	set content(v) {
		this._content = v;
	}
}

function getCheckedVal(id) {
	return $(id + " > .iradio_flat-green.checked") //parent > child
			.children()
				.first()
					.val();
}

function getPrecedences() {
	return $("#tags_1_tagsinput > span.tag")
			.map( function() {
				return $( this ).children()
					.first().text().trim();
			})
			.get();
}

function buildParams() {
	var params = new Parameters();
	params.domain = $("#domain_in").val();
	params.subdomain = $("#subdomain_in").val();
	params.difficulty = getCheckedVal("#difficulty_in");
	params.reps = $("#heard").val();
	params.precs = getPrecedences();
	params.header = $("#editor-header").html();

	return params;
}

function buildAnswer(num) {
	var answer = new Answer();
	answer.correction = (parseInt($("#correction_a"+num).val())/100).toString();
	answer.mandatory = getCheckedVal("#mandatory_a"+num);
	answer.content = $("#editor-answer"+num).html();

	return answer;
}

function buildSolution() {
	var sol = new Solution();
	var refs = [];
	$(".reference_field").map(
		function() {
			refs.push($( this ).val());
		}
	);
	sol.refs = refs;
	sol.content = $("#editor-solution").html();

	return sol;
}

function buildJSON(p, a, s) {
	var answers = [];
	for (var i = 0; i < a.length; i++) {
		var obj = {
			"answer": a[i].content,
			"correction": a[i].correction,
			"mandatory": a[i].mandatory
		}
		answers.push(obj);
	}
	//var num = db.questions.find( {}, { number: 1 } ).sort( { number: -1 } ).limit(1);
	var json = {
		"domain": p.domain,
		"subdomain": p.subdomain,
		"header": p.header,
		"body": answers,
		"solution": s.content,
		"references": s.refs,
		"degree": p.difficulty,
		"repetitions": p.reps,
		"number": "0", //NEED TO GET FROM DATABASE THE NUMBER FROM LAST INSERTED -> num
		"precedence": p.precs,
		"insertionDate": new Date().toISOString(),
		"state": "0"
	}

	return JSON.stringify(json);
}

function inputErrors(p, la, s) {
	var errors = [];

	if (p.domain == "") errors.push("[Parâmetros] Domínio não selecionado.");
	if (p.subdomain == "") errors.push("[Parâmetros] Subdmínio não selecionado.");
	if (p.header == "" || p.header == "<br>") errors.push("[Parâmetros] O conteúdo da questão não pode ser vazio.");
	if (p.difficulty === undefined) errors.push("[Parâmetros] Grau de dificuldade não selecionado.");

	var i = 1, mandatory = 0;
	for (var j = 0; j < la.length; j++) {
		var a = la[j];
		if (a.content == "" || a.content == "<br>") errors.push("[Resposta "+i+"] O conteúdo não pode ser vazio.");
		if (a.correction == "") errors.push("[Resposta "+i+"] O grau de correção deverá ser um valor entre 0 e 100.");
		if (a.mandatory == "true") mandatory++;
		i++;
	}
	if (mandatory > 3) errors.push("[Respostas] O máximo de respostas obrigatórias é 3.");

	if (s.content == "" || s.content == "<br>") errors.push("[Solução] O conteúdo não pode ser vazio.");
	for (var i = 0; i < s.refs.length; i++) {
		if (s.refs[i] == "") errors.push("[Solução] Referências não podem ser vazias.")
	}

	return errors;
}

function checkHandler() {
	var btn = $( this );
	if (btn.hasClass("checked") == false){
		var fst = btn.parent().children().first();
		var snd = btn.parent().children().last();
		var bro = btn.prev();
		if (bro.length == 0) {
			fst.addClass("checked");
			snd.removeClass("checked");
		}
		else {
			snd.addClass("checked");
			fst.removeClass("checked");
		}
	}
}

function ask4Confirmation(num) {
	$($('p.delete_answer_btn').get(num-4))
		.addClass("invisible")

	var check = $("<i>").addClass("dialog_yes fa fa-check")
						.attr("onclick", "deleteAnswer("+num+")");
	var cancel = $("<i>").addClass("dialog_no fa fa-times")
						 .attr("onclick", "rollbackAnswer("+num+")");

	$('<div>').addClass("confirmation_dialog")
			.html($("<span>").html("Apagar resposta? ")
					.add(check)
					.add(cancel))
			.insertBefore($("p.answer_num").get(num-1));
}

function deleteAnswer(num) {
	answers--;

	$($("p.answer_num")
		.get(num-1))
		.parent()
		.next()
		.addBack()
		.remove();
}

function addRef() {
	var ref = $($(".refs_div").get(0));
	var el = ref.clone().on("click", event => deleteRef(event));
	el.insertBefore($("#addRefBtn"));
}

function deleteRef(event) {
	$(event.target).addClass("invisible");

	var check = $("<i>").addClass("dialog_yes fa fa-check")
						.on("click", () => {
							$(event.target).parent().remove();
						});
	var cancel = $("<i>").addClass("dialog_no fa fa-times")
						 .on("click", ev => {
						 	$(ev.target).parent().remove();
							$(event.target).removeClass("invisible");
						});

	$('<div>').addClass("confirmation_dialog")
			.html($("<span>").html("Apagar resposta? ")
					.add(check)
					.add(cancel))
			.insertAfter($(event.target).prev());

}

$(".delete_ref").on("click", event => deleteRef(event));

function rollbackAnswer(num) {
	$($('div.confirmation_dialog').get(num-4))
		.remove()
	$($('p.delete_answer_btn').get(num-4))
		.removeClass("invisible")
}

function fieldModifier(n) {
	$('<p>').addClass("delete_answer_btn")
			.html($('<i>').addClass("fa fa-trash")
						  .attr("title", "Apagar resposta")
						  .attr("onclick", "ask4Confirmation("+n+")"))
			.insertBefore($("p.answer_num").get(n-1));
	$($("p.answer_num")
		.get(n-1)).html("Resposta " + n);
	$("#correction_a0")
		.attr("id", "correction_a" + n);
	$("#mandatory_a0")
		.attr("id", "mandatory_a" + n);
	$("#mandatory_a" + n)
		.children().on("click", checkHandler);
	$("#mandatory_a" + n)
		.children().hover(function() {
			$( this ).addClass("hover");
		}, function() {
			$( this ).removeClass("hover");
		});
	$("#editor-answer0")
		.attr("id", "editor-answer" + n);
	$("#pictureBtn_a0")
		.attr("id", "pictureBtn_a" + n);
	jQuery("[data-target = '#pictureBtn_a0']")
		.attr("data-target", "#pictureBtn_a" + n);
	jQuery("[data-target = '#editor-answer0']")
		.attr("data-target", "#editor-answer" + n);
}

$('#domain_in').on('change', function() {
	var selected = $(this).val();
	$("#subdomain_in option").each(
		function(item){
			var element =  $(this);
			if (element.data("tag") != selected)
				element.hide();
			else
				element.show();
		}
	);
	$("#subdomain_in").val($("#subdomain_in option:visible:first").val());

});

$("#submitSubsubdomain").click( () => {
	var $domainSelect = $("#domainChoice").find(":selected");
	var scholarity    = $domainSelect.data('scholarity');
	var studyCycle    = $domainSelect.data('study-cycle');
	var dom           = $("#domainChoice").val();
	var sub_dom       = $("#subdomainChoice").val();
	var new_subsubdom = $("#newSubsubdom_input").val();
	var usersElem     = $("#tags_1_tagsinput .tag");

	if (dom == "" || sub_dom == "" || new_subsubdom == "") {
		if (dom == ""){
			$("<p>").addClass("error_msg")
					.html("*Domínio não selecionado")
					.insertAfter($(".text-warning").get(0));
		}
		if (sub_dom == ""){
			$("<p>").addClass("error_msg")
					.html("*Designação do novo subdomínio não definida")
					.insertAfter($(".subdomain-warning"));
		}
		if (new_subsubdom == ""){
			$("<p>").addClass("error_msg")
					.html("*Designação do novo subsubdomínio não definida")
					.insertAfter($("#newSubsubdom_input"));
		}
	}
	else {
		var users = [];
		for (var i = 0; i < usersElem.length; i++){
			users.push($(usersElem.get(i)).children().first().text().trim());
		}
		var json = {
			"domain": {
				"study_cycle": studyCycle,
				"scholarity" : scholarity,
				"description": dom
			},
			"subdomain": sub_dom,
			"subsubdomain": new_subsubdom,
			"users": users
		};
		$.ajax({
			type: 'POST',
			url: "/questions/subsubdomains",
			data: JSON.stringify(JSON.stringify(json)),
			dataType: 'json',
			contentType: 'application/json; charset=utf-8'
		}).done(function() {
			console.log("New subsubdomain info successfully sent!");
		});

		$("<div>").addClass("loader")
			.insertBefore($("#addSubsubdomain_modal > div:nth-child(1) > div:nth-child(1) > div:nth-child(3)")
			.children().first());

		window.setTimeout(function(){
			$(".loader").remove();
			window.location.href = '/questions/subsubdomains/add';
		}, 500);
	}
});

$("#submitSubdomain").click( () => {
	var $domainSelect = $("#domainChoice").find(":selected");
	var scholarity    = $domainSelect.data('scholarity');
	var studyCycle    = $domainSelect.data('study-cycle');
	var dom           = $("#domainChoice").val();
	var new_sub       = $("#newSubdom_input").val();
	var usersElem     = $("#tags_1_tagsinput .tag");

	if (dom == "" || new_sub == "") {
		if (dom == ""){
			$("<p>").addClass("error_msg")
					.html("*Domínio não selecionado")
					.insertAfter($(".text-warning").get(0));
		}
		if (new_sub == ""){
			$("<p>").addClass("error_msg")
					.html("*Designação do novo subdomínio não definida")
					.insertAfter($("#newSubdom_input"));
		}
	}
	else {
		var users = [];
		for (var i = 0; i < usersElem.length; i++){
			users.push($(usersElem.get(i)).children().first().text().trim());
		}
		var json = {
			"domain": {
				"study_cycle": studyCycle,
				"scholarity" : scholarity,
				"description": dom
			},
			"study_cycle": studyCycle,
			"scholarity" : scholarity,
			"subdomain"  : new_sub,
			"users"      : users
		};
		$.ajax({
			type: 'POST',
			url: "/questions/subdomains",
			data: JSON.stringify(JSON.stringify(json)),
			dataType: 'json',
			contentType: 'application/json; charset=utf-8'
		}).done(function() {
			console.log("New subdomain info successfully sent!");
		})

		$("<div>").addClass("loader")
			.insertBefore($("#addSubdomain_modal > div:nth-child(1) > div:nth-child(1) > div:nth-child(3)")
			.children().first());

		window.setTimeout(function(){
			$(".loader").remove();
			window.location.href = '/questions/subdomains/add';
		}, 500);
	}
});

$("#submitDomain").click( () => {
  var studyCycle  = $("#study-cycle").val();
  var scholarity  = $("#scholarity").val();
	var description = $("#description").val();
	var usersElem   = $("#tags_1_tagsinput .tag");

  if (description == "" || scholarity == "" || studyCycle == "") {
    var errorField = '';
    var errorId    = '';

    if (description == "") {
      errorField = 'Designação';
      errorId    = '#description';
		} else if (scholarity == "") {
      errorField = 'Escolaridade';
      errorId    = '#scholarity';
    } else {
      errorField = 'Ciclo de estudos';
      errorId    = '#study_cycle';
    }

    $("<p>").addClass("error_msg")
        .html(`*${errorField} do novo domínio por definir.`)
        .insertAfter($(errorId));

		if (usersElem.length == 0) {
			$($(".errorsList").get(0)).append(
				$("<p>").addClass("error_msg")
						.html("*O novo domínio requer um ou mais responsáveis"));
		}
	}
	else {
		var users                 = [];
    var lowPerformanceFactor  = $('#addDomain_modal').find('input[name="low_performance_factor"]').val();
    var highPerformanceFactor = $('#addDomain_modal').find('input[name="high_performance_factor"]').val();
    var lowSkillFactor        = $('#addDomain_modal').find('input[name="low_skill_factor"]').val();
    var highSkillFactor       = $('#addDomain_modal').find('input[name="high_skill_factor"]').val();
    var backlogFactor         = $('#addDomain_modal').find('input[name="backlog_factor"]').val();
    var questionsFactor       = $('#addDomain_modal').find('input[name="questions_factor"]').val();
    var questionsNumber       = $('#addDomain_modal').find('input[name="min_questions_number"]').val();
    var defaultUserLevel      = $('#addDomain_modal').find('input[name="default_user_level"]').val();

		for (var i = 0; i < usersElem.length; i++){
			users.push($(usersElem.get(i)).children().first().text().trim());
		}
		var json = {
      'study_cycle'            : studyCycle,
      'scholarity'             : scholarity,
			'description'            : description,
			'users'                  : users,
      'low_performance_factor' : lowPerformanceFactor,
      'high_performance_factor': highPerformanceFactor,
      'low_skill_factor'       : lowSkillFactor,
      'high_skill_factor'      : highSkillFactor,
      'backlog_factor'         : backlogFactor,
      'questions_factor'       : questionsFactor,
      'min_questions_number'   : questionsNumber,
      'default_user_level'     : defaultUserLevel
    };

		$.ajax({
			type: 'POST',
			url: '/questions/domains',
			data: JSON.stringify(JSON.stringify(json)),
			dataType: 'json',
			contentType: 'application/json; charset=utf-8'
		}).done(function() {
			console.log('New domain info successfully sent!');
		});

		$('<div>').addClass('loader')
			.insertBefore($('#addDomain_modal > div:nth-child(1) > div:nth-child(1) > div:nth-child(3)')
			.children().first());

		window.setTimeout(function(){
			$('.loader').remove();
			window.location.href = '/questions/domains/add';
		}, 500);
	}
});

var log = [];

// ================ LOGS ====================

$('.side-menu a').click( event => {
	var menu_opt = $(event.target).text();
	var url = window.location.pathname;
});

// ===========================================

var answers = 3;

$("#addAnswerBtn").on("click", () => {
	answers++;

	$("<div>").addClass("row")
			  .html($("#nextAnswer").html())
			  .insertBefore("#nextAnswer");

	$("<div>").addClass("ln_solid")
			  .insertBefore("#nextAnswer");

	fieldModifier(answers);
});

$("#submitBtn").on("click", () => {
	var params = buildParams();
	var list_answers = [];
	for (var i = 1; i <= answers; i++) {
		var ans = buildAnswer(i);
		list_answers[i-1] = ans;
	}
	var solution = buildSolution();

	var errors = inputErrors(params, list_answers, solution);
	if (errors.length == 0) {
		if ($("span.input_invalid").hasClass("invisible") == false)
			$("span.input_invalid").addClass("invisible");
		$("span.invisible.input_valid").removeClass("invisible");
		var json = buildJSON(params, list_answers, solution);
		$.ajax({
			type: 'POST',
			url: "/questions/add",
			data: JSON.stringify(json),
			dataType: 'json',
			contentType: 'application/json; charset=utf-8'
		}).done(function() {
			console.log("Question added successfully");
		})
	}
	else {
		for (var i = 0; i < errors.length; i++)
			console.log(errors[i]);
		var data = " Questão inválida: " + errors.length + " erros precisam de ser corrigidos.";
		var icon = $("<i>").addClass("fa fa-eye");
		var el = $("span.input_invalid");
		if (el.hasClass("invisible"))
			el.removeClass("invisible");
		el.html("").append(icon).append(data);
	}
});

function hideError() {
  $("p.error_msg").remove();
}

function dateFormat(date){
	isodate = new Date(date);
    var dd = isodate.getDate();
    if (dd.toString().length == 1)
      dd = "0"+dd;
    var mm = isodate.getMonth()+1;
    if (mm.toString().length == 1)
      mm = "0"+mm;
    var yyyy = isodate.getFullYear();
    return dd+"-"+mm+"-"+yyyy;
}
