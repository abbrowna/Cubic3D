$(document).ready(function () {
    if ($("#id_material").val() == "PLA") {
        $("#id_color option").remove();
        $("#id_color").append('<option value="GRN" selected="selected">Green</option>');
        $("#id_color").append('<option value="BLK">Black</option>');
        $("#id_color").append('<option value="COMBO"> green-black combo</option>');
    }
    $("#file_picker input").remove();
    $("#file_picker").append('<input type="file" name="thing" accept=".stl" required id="id_thing">');

    $("#id_material").change(function (event) {
        if ($(this).val() == "PETG") {
            $("#id_color option").remove();
            $("#id_color").append('<option value="WHT" selected="selected">White</option>');
        }
        else if ($(this).val() == "PLA") {
            $("#id_color option").remove();
            $("#id_color").append('<option value="GRN" selected="selected">Green</option>');
            $("#id_color").append('<option value="BLK">Black</option>');
            $("#id_color").append('<option value="COMBO"> green-black combo</option>');
        }
    });

    $("#id_color").change(function (event) {
        if ($(this).val() == "COMBO") {
            $("#combo_info").show();
        }
        else {
            $("#combo_info").hide();
        }
    });

    $(".iframe").css('height', $(window).height() + 'px');
    $(".iframe").css('width', $(".container").width() + 'px');

    $("#scaleselect").change(function (event) {
        if ($(this).is(":checked")) {
            $("#scalingtext").show();
        }
        else {
            $("#scalingtext").hide();
        }
    });
    $("#further_select").change(function (event) {
        if ($(this).is(":checked")) {
            $("#furthertext").show();
        }
        else {
            $("#furthertext").hide();
        }
    });

    $(":input[type!='file']").addClass("form-control");
    $(":input[type='checkbox']").removeClass("form-control");
    $("select").addClass("form-control");
    $("textarea").addClass("form-control");

    //display correct form in reject or accept page depending on the clicked button
    $("#sendconfirm").click(function (event) {
        $('#rejectmessagefield').hide();
        $('#finalpricefield').show();
        $('#id_rejectmessage').val("N/A");
        $('#viablebool').val(true);
        $('#emailsubmit').show();
    });
    $("#sendreject").click(function (event) {
        $('#rejectmessagefield').show();
        $('#finalpricefield').hide();
        $('#viablebool').val(false);
        $('#emailsubmit').show();
    });

    //signupform placeholders
    $("#id_email").attr('placeholder', 'someone@example.com');
    $("#id_password1").attr('placeholder', 'More than 8 characters');
    $("#id_password2").attr('placeholder', 'Retype password');

    //loginform placeholders
    $("#id_username").attr('placeholder', 'Username');
    $("#id_password").attr('placeholder', 'Password');

    //signup form logo
    $(".logocol").css('height', $(".signuprow").height() + 'px');
    //review and info viewer
    $("#viewrow").css('height', $("#review").height() + 'px');
});