

{% set index=namespace(value=1) %}

<p style="text-align: center;"><img src="https://asc360-prod.frappe.cloud/files/logo.png" width="100"></p>
<h1 style="text-align: center;">Welcome to ASC360</h1>
<h3 style="text-align: center;>Important ADVENTURE SAFETY Information</h3>
<div style="width:60%; ">
    <p style="line-height:30px;"><b>Hi {{doc.customer_name}}</b></p>
    <p >Namaste from ASC360 team! You have elected to opt for the India’s premier adventure safety, medical and travel safety services. 
We are excited for your adventure in India. But first, please make note of these important details about your coverage.
We've attached all of your important documents in this email.</p><p></p>
    <p style="line-height:30px;">Please double check all your travel details. If something is not quite right, kindly let us know.</p>
    <p style="line-height:30px;">Have an amazing adventure!.</p>
    <p style="line-height:30px;">Below are your plan details.</p>
    <br>
    <h2 style="text-align: center;"> Your Adventure Insurance Policy Details</h2>
<table style="table-layout: fixed; width: 80%;">
    <tr>
        <td>Tour Operator</td>
        <td>Policy Number</td>
    </tr>
<tr>
    <td>{{doc.tour_operator_name}}</td>
    <td><b>{{doc.name}}</b></td>
</tr>
<tr>
    <td>Type of Plan</td>
    <td>Start Date</td>
</tr>
<tr>
    <td>Individual</td>
    <td>{{frappe.utils.get_datetime(doc.start_date).strftime("%d-%m-%Y")}}</td>
</tr>
<tr>
    <td>Service</td>
    <td>End Date</td>
</tr>
<tr>
    <td>Adventure Insurance, Medical Evacuation</td>
    <td>{{frappe.utils.get_datetime(doc.end_date).strftime("%d-%m-%Y")}}</td>
</tr>
<tr>
    <td>Term</td>
    <td>Amount Charged</td>
</tr>
<tr>
    <td>{{doc.period_of_issuance}} Days</td>
    <td>Rs. {{'{0:.2f}'.format(doc.amount)}}/-</td>
</tr>
<tr></tr>
</table>
<br>
<center style="width:100%;min-width:380px"> 
<!--<table>	-->
<!--<tr style="border: 5px solid black;">-->
<!--    <td width="50%"><b>Benefits</b></td>-->
<!--    <td width="50%"><b>Sum Insured</b></td>-->
<!--</tr>-->
<!-- <br>-->
<!-- <img src="https://asc360-prod.frappe.cloud/files/Screenshot%20from%202022-07-08%2017-02-53.png" style="width:60%">-->
<!-- <br>-->

<!--<div style="height:20px;width:20px;border:2px solid black"></div>-->
<!--{% set benefits= frappe.get_doc("Item", doc.policy).benefit_details %}-->

<!--{% for benefit in benefits %}-->
<!--{% if index.value%2==0 %}-->
<!--         <tr>-->
<!--            <td width="50%">{{benefit.benefit}}</td>-->
<!--            <td width="50%">{{benefit.amount}}</td>-->
<!--            {% set index.value=index.value+1 %}-->
<!--        </tr>-->
<!--        {% else %}-->
<!--         <tr>-->
<!--            <td width="50%">{{benefit.benefit}}</td>-->
<!--            <td width="50%">{{benefit.amount}}</td>-->
<!--            {% set index.value=index.value+1 %}-->
<!--        </tr>-->
<!--        {% endif %}-->
<!--{% endfor %}-->
<!--</table>	-->
</center>
<br>

<p style="line-height: 2px;">This plan is valid for single adventure trip.</p>
<p style="line-height: 2px;">Any claim due to or arising out of pre-existing diseases/ailments whether declared or undeclared is NOT covered under the policy.</p>
<p style="line-height: 2px;">Claims Procedure: In the event of an accident, immediately contact the Help Line number stating the necessary details.</p>
<p style="line-height: 2px;">Claims Assistance & Evacuation assistance ASC360: +91-7303800101 or Email: info@asc360.com</p>
<p style="line-height: 2px;">Wishing you a safe and exciting adventure !</p>
<p></p>
<p>Thanks and regards</p>
<p><b>Team ASC360</b></p>
<p>www.asc360.com </p>
<p>Making outdoors safe n secure!</p>

</div>