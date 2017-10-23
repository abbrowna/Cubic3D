def accepthtml(printrequest):
    mail="""
            <!DOCTYPE html>
            <html lang="en" xmlns="http://www.w3.org/1999/xhtml">
            <head>
                <meta charset="utf-8" />
                <title></title>
            </head>
            <body style="margin:0; padding:0;">
                <table border="1" cellpadding="0" bgcolor="#ffffff">
                    <tr>
                        <td>
                            <table align="center" border="1" cellpadding="0" cellspacing="0" width="600" style="border-collapse: collapse;">
                                <tr>
                                    <td align="center" bgcolor="#333333" style="padding: 40px 0 30px 0;">
                                        <h1 style="color:White;font-family:BankGothic Md BT">CUBIC3D</h1>
                                    </td>
                                </tr>
                                <tr>
                                    <td style="padding:40px 30px 40px 30px">
                                        <table bgcolor="#333333" border="1" cellpadding="0" width="100%" style="border-radius:20px;padding-top:20px;padding-bottom:20px;">
                                            <tr>
                                                <td align="left" bgcolor="#ffffff" style="padding-top:20px;padding-left:10px;padding-right:10px">
                                                    <h2 style="border-bottom-width:2px; border-bottom-color:#333333; border-bottom-style:solid;">Good News!</h2>
                                                    <p>
                                                        We took a look at your print request of <strong>{}</strong> and determined that it is viable.
                                                        We are now writting to you to confirm that you still want this part printed and with the following options:
                                                    </p>
                                                    <ul>
                                                        <li>Purpose:{}</li>
                                                        <li>Material:{}</li>
                                                        <li>Color:{}</li>                                           
                                                    </ul>
                                                    <p>If that looks alright just a few more things then we can make it final</p>
                                                </td>
                                            </tr>
                                            <tr>
                                                <td align="left" bgcolor="#ff8000" style="padding-top:20px;padding-left:10px;padding-right:10px">
                                                    <h2 style="border-bottom-width:2px; border-bottom-color:#333333; border-bottom-style:solid;">Payment and exchange Info</h2>
                                                    <ul>
                                                        <li>After final assesment of your request, your item will cost a total of <strong>KSH {}</strong> to print</li>
                                                        <li>
                                                            Payment is expected during the physical handing over of the already printed part. You are hence expected to be prepared in order
                                                            to recieve your part
                                                        </li>
                                                        <li>
                                                            The available payment option is through MPESA n.o <strong>0728274309</strong><br />
                                                            It is vital that the names reflected in your CUBIC account will be the same as in the MPESA transaction details. You can confirm your account details
                                                            <a style="color:white;"href="http://www.cubic.co.ke/myaccount">here</a>.
                                                        </li>
                                                        <li>
                                                            Also note that additional fees will be incured for clients outside of the Juja Locale for the purpose of courier delivery or other delivery means.
                                                        </li>
                                                        <li>
                                                            When your part is printed, we will give you a call using the number provided in your account details to organise for the exchange.
                                                        </li>
                                                    </ul>
                                                </td>
                                            </tr>
                                            <tr>
                                                <td align="left" bgcolor="#ffffff" style="padding-top:20px;padding-left:10px;padding-right:10px">
                                                    <h2 style="border-bottom-width:2px; border-bottom-color:#333333; border-bottom-style:solid;">Print confirmation</h2>
                                                    <p>
                                                        If you agree to the above price and conditions,<br />
                                                        Clicking on the button below will confirm your print request and make it final. We will place it in our printing queue and produce your part as soon as possible
                                                    </p>
                                                    <a style="font-family:'BankGothic Md BT';border-radius:6px;background-color:#333333;color:#e6e6e6; padding:15px 15px 15px 15px;" href="http://www.cubic3d.co.ke/confirm/{}">Confirm Print</a>
                                                    <p>
                                                        If you have however changed your mind, simply ignore this email and your print request will be deleted within 48 hours.
                                                    </p>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                </table>
            </body>
            </html>
    """.format (printrequest.description,printrequest.purpose,printrequest.material,printrequest.color,printrequest.thing_price(),printrequest.id)
    return mail

def rejecthtml(printrequest,message):
    mail="""
        <!DOCTYPE html>
        <html lang="en" xmlns="http://www.w3.org/1999/xhtml">
        <head>
            <meta charset="utf-8" />
            <title></title>
        </head>
        <body style="margin:0; padding:0;">
            <table border="1" cellpadding="0" bgcolor="#ffffff">
                <tr>
                    <td>
                        <table align="center" border="1" cellpadding="0" cellspacing="0" width="600" style="border-collapse: collapse;">
                            <tr>
                                <td align="center" bgcolor="#333333" style="padding: 40px 0 30px 0;">
                                    <h1 style="color:White;font-family:BankGothic Md BT">CUBIC3D</h1>
                                </td>
                            </tr>
                            <tr>
                                <td style="padding:40px 30px 40px 30px">
                                    <table bgcolor="#333333" border="1" cellpadding="0" width="100%" style="border-radius:20px;padding-top:20px;padding-bottom:20px;">
                                        <tr>
                                            <td align="left" bgcolor="#ffffff" style="padding-top:20px;padding-left:10px;padding-right:10px">
                                                <h2 style="border-bottom-width:2px; border-bottom-color:#333333; border-bottom-style:solid;">Print request error</h2>
                                                <p>
                                                    We took a look at your print request of <strong>{}</strong> and encountered some problems.
                                                    Dont Give up though, the below section details the reason we can't print your part and the possible solutions.
                                                </p>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td align="left" bgcolor="#ff8000" style="padding-top:20px;padding-bottom:20px;padding-left:10px;padding-right:10px">
                                                <h2 style="border-bottom-width:2px; border-bottom-color:#333333; border-bottom-style:solid;">Info</h2>                                        
                                                <p>After assesment of your request, we found the follwing issues.</p>
                                                <strong>
                                                    {}
                                                </strong>
                                                <p>
                                                    Please make a new print request taking the above into consideration. Here is a link to get you there quickly
                                                </p>
                                                <a style="font-family:'BankGothic Md BT';border-radius:6px;background-color:#333333;color:#e6e6e6; padding:15px 15px 15px 15px;" href="http://www.cubic3d.co.ke/gettingstarted/login">Request a print</a>
                                            </td>
                                        </tr>
                                    </table>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>
        </body>
        </html>
    """ .format(printrequest.description,message)
    return mail
