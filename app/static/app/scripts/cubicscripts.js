$(document).ready(function () {
    ///////////////////////New website scripts///////////////////////////


    //contact row links
    $("#contact-strip .col1").click(function () {
        window.open("mailto:support@cubic3d.co.ke");
    });
    $("#contact-strip .col3").click(function () {
        window.open("https://www.instagram.com/cubic3d_ke/");
    });
    $("#contact-strip .col4").click(function () {
        window.open("https://twitter.com/Cubic3D_Ke");
    });

    //material page table or grid selector
    $(window).resize(function () {
        if ($("#materialstrip .row").css('display') === 'block') {
            $("#comptable").hide();
        }
        else {
            $("#comptable").show();
        }
    });
    //material table border styling on hover
    $("#comptable tr").hover(function () {
        $("td:nth-child(2)", this).toggleClass('borderstyling');
    });

    //form placeholders
    $("#id_email").attr('placeholder', 'someone@example.com');
    $("#id_password1").attr('placeholder', 'Password');
    $("#id_password2").attr('placeholder', 'Retype password');
    $("#id_first_name").attr('placeholder', 'First name');
    $("#id_last_name").attr('placeholder', 'Last name');
    $("#id_mobile").attr('placeholder', 'Mobile number');
    $("#id_new_password1").attr('placeholder', 'New password');
    $("#id_new_password2").attr('placeholder', 'Retype new password');
    $("#id_bill_to").attr('placeholder', 'Alternative billing name (optional)');
    $("#id_delivery_fee").attr('placeholder', 'Price for delivery (optional)');
    $("#id_price").attr('placeholder', 'Final Price');
    $("#id_rejectmessage").attr('placeholder',
        'Explanation as to why the print request has been rejected (optional) (If left blank no email will be sent)');
    $("#id_quantity").attr('placeholder', 'Quantity');

    //signupform fill username with email
    $("#signup #id_email").change(function () {
        $("#signup #id_username").val($("#signup #id_email").val());
    });

    //Change profile fill username with email
    $("#edit_profile input").addClass("form-control");

    //Login form placeholder
    $("#login #id_username").attr('placeholder', 'Email');
    $("#id_password").attr('placeholder', 'Password');

    //upload and quote-upload forms placeholders
    $("#id_description").attr('placeholder', 'Descriptive name for your part');

    //Tie decoy file-picker with actual hidden filepicker
    $("#file-icon svg").click(function () {
        $("#id_thing").trigger("click");
    });

    $("#id_thing").change(function (e) {
        var fileName = e.target.files[0].name;
        $("#decoy_filename").val(fileName);
    });

    //Make visible specific upload tips at a time
    var duration = 400;
    $("#file-icon").mouseenter(function () {
        if ($(".uploadhelp .STL-info").css("display") === "none") {
            $(".uploadhelp div").hide();
            $(".uploadhelp .STL-info").show(duration, "swing");
        }
    });
    //$("#file-icon").mouseout(function () {
    //    $(".uploadhelp .STL-info").hide(400);
    //});
    $("#id_purpose").focusin(function () {
        $(".uploadhelp div").hide(duration, "swing");
        $(".uploadhelp .purpose-info").show(duration);
    });
    $("#id_material").focusin(function () {
        $(".uploadhelp div").hide(duration);
        $(".uploadhelp .material-info").show(duration);
    });
    $("#id_color_combo").focusin(function () {
        $(".uploadhelp div").hide(duration);
        $(".uploadhelp .color-info").show(duration);
    });
    $("#id_color").focusin(function () {
        $(".uploadhelp div").hide(duration);
    });

    // Make visible text area fields when related option is selected.
    $("#further_select").change(function (event) {
        if ($(this).is(":checked")) {
            $("#furthertext").show();
        }
        else {
            $("#furthertext").hide();
        }
    });

    $("#id_color").change(function (event) {
        if ($(this).val() === "Combo") {
            $("#combo_info").show();
        }
        else {
            $("#combo_info").hide();
        }
    });
    //Add .stl file filter to file field
    $("#id_thing").attr('accept', '.stl');

    // Auto update the colors field with the colors of the selected material.
    var url = $("#upload_form").attr("data-colors-url"); //Excecute on initial load
    var material = $("#id_material").val();

    $.ajax({
        url: url,
        data: { 'material': material },
        success: function (data) {
            $("#id_color").html(data);
        }
    });
    $("#id_material").change(function () {
        var url = $("#upload_form").attr("data-colors-url");
        var material = $(this).val();

        $.ajax({
            url: url,
            data: { 'material': material },
            success: function (data) {
                $("#id_color").html(data);
            }
        });
    });

    //call the Loading modal on submition of Request
    $("#upload_form").on('submit', function (event) {
        $('#uploadmodal').modal('show');
        //$("#uploadmodal").on('shown.bs.modal', function () {
        //    $("#uploadmodal").css("display", "flex");
        //});
    });

    //review tooltips
    $("#viewer-help-icon").mouseenter(function () {
        $("#id_stlviewer").css("opacity", 0.1);
        //$("#viewer-tooltip").delay(500).show(400);

    });
    $("#viewer-help-icon").mouseleave(function () {
        //$("#viewer-tooltip").hide(400);
        $("#id_stlviewer").css("opacity", 1);
    });
    //review iframe reload on window resize
    $(window).resize(function () {
        var iframe = $("#id_stlviewer");
        if (iframe.length) {
            $("#id_stlviewer")[0].contentWindow.location.reload(true);
        }        
    });
    //thanks page strip min height
    $("#thanks_info").css('min-height', $(window).height() - $("#thanks_title").height() - $("nav").height() - $("footer").height());

    //gallery image modal
    $("#gallery_strip img").click(function () {
        var image = $(this);
        var imagesrc = $(this).attr("src");
        $("#gallery_carousel img").parent().removeClass("active");
        $("#gallery_carousel li").removeClass("active");
        selectorstring = decodeURI('#gallery_carousel img[src="' + imagesrc + '"]');
        $(selectorstring).parent().addClass('active');
        $("#gallery_carousel li[data-slide-to='0']").addClass("active");
        $("#gallery_modal").modal('show');
    });
    //gallery enable swiping for carousel
    if ($(".carousel").length) {
        $(".carousel").bcSwipe({ threshold: 50 });
    }
    //home-page SEO display according to screen size:
    if ($("#mobile_welcome").css('display') === 'block') {
        $(".SEO.carousel-caption").hide();
    }
    else {
        $(".SEO.carousel-caption").show();
    }
    $(window).resize(function () {
        if ($("#mobile_welcome").css('display') === 'block') {
            $(".SEO.carousel-caption").hide();
        }
        else {
            $(".SEO.carousel-caption").show();
        }
    });

    //navbar images height setting
    var set_nav_image = function () {
        $(".navbar-image").height($("#navbar-container").height() + $("#overview").height() + 30);
    };
    set_nav_image();
    $(window).resize(set_nav_image);

    //Enable tooltips
    $('[data-toggle="tooltip"]').tooltip();

    //display correct form fields in reject or accept page depending on the clicked button
    $("#sendconfirm").click(function (event) {
        $(this).addClass("selected");
        $('.acceptance').show();
        $("#id_price").prop('required', true);
        $('.rejection').hide();
        $('#sendreject').removeClass("selected");
        $('#emailsubmit').attr("value","Send invoice");
    });
    $("#sendreject").click(function (event) {
        $(this).addClass("selected");
        $('.rejection').show();
        $('.acceptance').hide();
        $("#id_price").prop('required', false);
        $('#sendconfirm').removeClass("selected");
        $('#emailsubmit').attr("value", "Delete request");
    });
    $("#id_rejectmessage").bind('input',function () {
        $('#emailsubmit').attr("value", "Reject request");
    });
    $("#id_add_to_group:checkbox").change(function () {
        if (this.checked) {
            $('#emailsubmit').attr("value", "Add to group");
            $('#id_bill_to').parent().hide();
            $('#id_delivery_fee').parent().hide();
        }
        else {
            $('#emailsubmit').attr("value", "Send invoice");
            $('#id_bill_to').parent().show();
            $('#id_delivery_fee').parent().show();
        }
    });
    //Load the estimated price of the model in the Admin "accept_or_reject" page
    var $estimatedprice = $("#our_price_estimate");
    var request_id = $estimatedprice.data("pr")
    var url = $estimatedprice.data("url")
    $.ajax({
        url: url,
        data: { 'request_id': request_id },
        success: function (data) {
            $("#our_price_estimate > strong").text(data.price);
        }
    });
});
