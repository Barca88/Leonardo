function click_box() {
	if ($("input[name='remember_me']").is(":checked"))
		$("input[name='remember_me']").prop("checked", false);
	else
		$("input[name='remember_me']").prop("checked", true);
}

function hideError() {
  $("p.error_msg").remove();
}

$("#username_login").attr("onfocus", "hideError()");
$("#pwd_login").attr("onfocus", "hideError()");

function verifyInput(type) {
	var empty = [];

	var form = $("form[name="+type+"_input]");
	var user = $(document).form.username.value;
	var pass = $(document).form.password.value;

	if (user == "")
		empty.push("user");
	if (pass == "")
		empty.push("pass");

	if (type == "signup") {
		// add credential & name & repeat password match
		var email = $(document).form.email.value;
		var name = $(document).form.name.value;

		if (email == "")
			empty.push("email");
		if (name == "")
			empty.push("name");
	}

	if (empty.length > 0) {
		// display "Empty fields not allowed"
		for (var i = 0; i < empty.length; i++) {
			$("#"+empty[i]+"_empty").css("display: block");
		}
		return false;
	}

	return true;
}
