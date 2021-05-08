$(document).ready(function () {
    //Button events for filament diameter
    $(".dia_button").click(function () {
        var dia = this.value;
        if (!$(this).hasClass('disabled')) {
            $(".diameter_select").addClass("hidden");
            //$(".material_select").removeClass("hidden");
            $(".material_select").show(function () {
                $(this).css("opacity", 1);
                $(this).css("transform", "translate(0, 0)");
            });
        }
        $("#id_diameter").val(dia);
    })


    //button event for filament material
    $(".matl_button").click(function () {
        var matl = this.innerHTML;
        $("#id_material").val(matl);
        $("#filterform").submit();
    })

    //Ajax request to add to the cart
    $(".add_cart_btn").click(function () {
        var button = $(this);
        var productID = $(this).val();
        $.ajax({
            url: '/ajax/addCart',
            data: { 'product_id': productID },
            dataType: 'json',
            success: function (data) {
                if (data.added) {
                    $('#cart_icon span').html(data.numOfItems);

                    $('#cart-animator').animate({ opacity: '1', width: '150px', height: '150px' }).delay(1000);
                    $('#cart-animator').animate({ opacity: '0px', width: '0px', height: '0px' });

                }
                else {
                    button.siblings(".stock-info").html("Not enough stock");
                    button.siblings(".stock-info").fadeIn(1000).delay(1000).fadeOut(1000);
                }
            }
        })
    })


    //Ajax request to increase item quantity
    $(".increase_qty").click(function () {
        var button = $(this)
        var productID = $(this).parent().data("id");
        $.ajax({
            url: '/ajax/addCart',
            data: { 'product_id': productID },
            dataType: 'json',
            success: function (data) {
                if (data.added) {
                    location.reload();
                }
                else {
                    button.parent().siblings(".stock_message").html("Not enough stock");
                    button.parent().siblings(".stock_message").fadeIn(1000).fadeOut(1000);
                }
            }
        })
    })
    //Ajax request to reduce item quantity
    $(".decrease_qty").click(function () {
        var productID = $(this).parent().data("id");
        $.ajax({
            url: '/ajax/removeCart',
            data: { 'product_id': productID },
            dataType: 'json',
            success: function (data) {
                location.reload();
            }
        })
    })

    //Ajax request to update the delivery cost
    $("#id_region").change(function () {
        var region_id = $(this).val();
        $.ajax({
            url: '/ajax/updateDelivery',
            data: { 'region_id': region_id },
            dataType: 'json',
            success: function (data) {
                $('#delivery_cost > span').html(data.cost);
                var total = parseInt($('.subtotal span').html()) + parseInt(data.cost);
                $('#checkout_total strong').html(total);
            }
        })
    })

    //Place order btn
    $('.order-btn-wrapper button').click(function () {
        $('#checkout-form').submit();
    })

    //button event to confirm release stock of pre-orders
    $("#releaseConfirm").click(function () {
        $.ajax({
            url: '/myadmin/release-stock',
            success: function (data) {
                location.reload();
            }
        })
    })
    //ajax request to set paid field of order
    $(".set-paid button").click(function () {
        var OID = $(this).data("id");
        $.ajax({
            url: '/ajax/setPaid',
            data: {'order_id': OID},
            dataType: 'json',
            success: function () {
                location.reload();
            }
        })
    })

    //ajax request to set delivered field of order
    $(".set-delievered button").click(function () {
        var OID = $(this).data("id");
        $.ajax({
            url: '/ajax/setDelivered',
            data: { 'order_id': OID },
            dataType: 'json',
            success: function () {
                location.reload();
            }
        })
    })


    //make the body of the page be at least the height of the viewport
    function minbody() {
        bHeight = $("body").height();
        bcHeight = $(".body-content").height();
        wHeight = $(window).height();
        fHeight = $(".footer-container").height();
        nHeight = $(".navbar").height();

        if (bHeight < wHeight) {
            $(".body-content").css("height", (bcHeight + wHeight - bHeight));
        }
        else if (bHeight > wHeight && (bHeight - fHeight) < wHeight) {
            $(".body-content").css("height", bcHeight + fHeight - (bHeight - wHeight));
        }
    }
    //minbody();


    //update the cart using ajax request
    $.ajax({
        url: '/ajax/updateCart',
        dataType: 'json',
        success: function (data) {
            $('#cart_icon span').html(data.numOfItems);
        }
    })

    //scroll fade in effect
    function scrollfade() {
        var pageTop = $(document).scrollTop();
        var pageBottom = pageTop + $(window).height();
        var tags = $(".scroll_fade_in");

        for (var i = 0; i < tags.length; i++) {
            var tag = tags[i];

            if ($(tag).position().top < pageBottom) {
                $(tag).addClass("visible");
            }
            else {
                $(tag).removeClass("visible");
            }
        }
    }
    scrollfade();
    $(document).on("scroll", function () {
        scrollfade();
    })

    //Click event for changing default delivery address for authenticated users
    $("#change_default").click(function () {
        $(".auth_checkout").hide("fast", "swing");
        $(".checkout_form").show("fast", "swing");
    });


    //display alternate contact fields on checout page if needed
    $("#alt_contact").change(function () {
        $(".alt").toggle("fast", "swing");
    });

    //enable tooltips
    $('[data-toggle="tooltip"]').tooltip();
})