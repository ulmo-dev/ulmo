
<html>
<head>
<title>Rivergages.com - Data Mining</title>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
<link href="/WaterControl/watercontrol.css" rel="stylesheet" type="text/css">
<script language="JavaScript" type="text/JavaScript">
<!--
function validate() {
 if (document.frm_mining.fld_station.value == "") {
	alert("You must provide a Station ID.") 
	return false; }
 if (document.frm_mining.fld_parameter.value == "") {
	alert("You must provide a Parameter Code.") 
	return false; }
document.frm_mining.submit()
}

function validateDate(fld) {
    if (fld.value!='') {
	//var RegExPattern = /^(?=\d)(?:(?:(?:(?:(?:0?[13578]|1[02])(\/|-|\.)31)\1|(?:(?:0?[1,3-9]|1[0-2])(\/|-|\.)(?:29|30)\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})|(?:0?2(\/|-|\.)29\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))|(?:(?:0?[1-9])|(?:1[0-2]))(\/|-|\.)(?:0?[1-9]|1\d|2[0-8])\4(?:(?:1[6-9]|[2-9]\d)?\d{2}))($|\ (?=\d)))?(((0?[1-9]|1[012])(:[0-5]\d){0,2}(\ [AP]M))|([01]\d|2[0-3])(:[0-5]\d){1,2})?$/;
	var RegExPattern = /^(?=\d)(?:(?:(?:(?:(?:0?[13578]|1[02])(\/)31)\1|(?:(?:0?[1,3-9]|1[0-2])(\/)(?:29|30)\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})|(?:0?2(\/)29\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))|(?:(?:0?[1-9])|(?:1[0-2]))(\/)(?:0?[1-9]|1\d|2[0-8])\4(?:(?:1[6-9]|[2-9]\d)?\d{2}))($|\ (?=\d)))?(((0?[1-9]|1[012])(:[0-5]\d){0,2}(\ [AP]M))|([01]\d|2[0-3])(:[0-5]\d){1,2})?$/;
    //var errorMessage = 'Please enter valid date as month, day, and four digit year.\nYou may use a slash, hyphen or period to separate the values.\nThe date must be a real date. 2-30-2000 would not be accepted.\nFormat mm/dd/yyyy.';
	var errorMessage = 'Please choose a valid date for both the From and To Dates as month, day, and four digit year.\nThe dates must be a real dates. 2/30/2000 would not be accepted.';

    if ((fld.value.match(RegExPattern)) && (fld.value!='')) {
		//return true;
        //alert('Date is OK'); 
    } else {
        alert(errorMessage);
        if (fld == document.frm_mining.fld_fromdate) {
		document.frm_mining.fld_fromdate.focus();
		return false;
		}
		if (fld == document.frm_mining.fld_todate) {
		document.frm_mining.fld_todate.focus();
		return false;
		}
    }
	} 
}

//-->
</script>
</head>
<script language="JavaScript">
function MM_openBrWindow(theURL,winName,features) { //v2.0
window.open(theURL,winName,features);
}
function MM_goToURL() { //v3.0
var i, args=MM_goToURL.arguments; document.MM_returnValue = false;
for (i=0; i<(args.length-1); i+=2) eval(args[i]+".location='"+args[i+1]+"'");
}
</script>
<body bgcolor="#E6E6E6">
<table width="670" align="center">
<tr>
<td> 
<!-- Do Nothing -->

<!-- Fireworks MX Dreamweaver MX target. Created Wed Jul 09 17:23:02 GMT-0500 (Central Daylight Time) 2003-->
<script language="JavaScript">
<!--
function MM_findObj(n, d) { //v4.01
var p,i,x; if(!d) d=document; if((p=n.indexOf("?"))>0&&parent.frames.length) {
d=parent.frames[n.substring(p+1)].document; n=n.substring(0,p);}
if(!(x=d[n])&&d.all) x=d.all[n]; for (i=0;!x&&i<d.forms.length;i++) x=d.forms[i][n];
for(i=0;!x&&d.layers&&i<d.layers.length;i++) x=MM_findObj(n,d.layers[i].document);
if(!x && d.getElementById) x=d.getElementById(n); return x;
}
function MM_swapImage() { //v3.0
var i,j=0,x,a=MM_swapImage.arguments; document.MM_sr=new Array; for(i=0;i<(a.length-2);i+=3)
if ((x=MM_findObj(a[i]))!=null){document.MM_sr[j++]=x; if(!x.oSrc) x.oSrc=x.src; x.src=a[i+2];}
}
function MM_swapImgRestore() { //v3.0
var i,x,a=document.MM_sr; for(i=0;a&&i<a.length&&(x=a[i])&&x.oSrc;i++) x.src=x.oSrc;
}
function MM_preloadImages() { //v3.0
var d=document; if(d.images){ if(!d.MM_p) d.MM_p=new Array();
var i,j=d.MM_p.length,a=MM_preloadImages.arguments; for(i=0; i<a.length; i++)
if (a[i].indexOf("#")!=0){ d.MM_p[j]=new Image; d.MM_p[j++].src=a[i];}}
}
function mmLoadMenus() {
if (window.mm_menu_0709172118_0) return;
window.mm_menu_0709172118_0 = new Menu("root",126,18,"Arial, Helvetica, sans-serif",12,"#267dff","#ff0000","#ffffff","#ffffff","left","middle",3,0,1000,-5,7,true,true,true,0,true,true);
mm_menu_0709172118_0.addMenuItem("St.&nbsp;Paul&nbsp;District","window.open('/WaterControl/Districts/MVP/districtdefault.cfm', '_blank');");
mm_menu_0709172118_0.addMenuItem("Rock&nbsp;Island&nbsp;District","window.open('/WaterControl/Districts/MVR/districtdefault.cfm', '_blank');");
mm_menu_0709172118_0.addMenuItem("Kansas&nbsp;City&nbsp;District","window.open('/WaterControl/Districts/NWK/districtdefault.cfm', '_blank');");
mm_menu_0709172118_0.addMenuItem("St.&nbsp;Louis&nbsp;District","window.open('/WaterControl/Districts/MVS/districtdefault.cfm', '_blank');");
mm_menu_0709172118_0.addMenuItem("Memphis&nbsp;District","window.open('/WaterControl/Districts/MVM/districtdefault.cfm', '_blank');");
mm_menu_0709172118_0.addMenuItem("Little&nbsp;Rock&nbsp;District","window.open('/WaterControl/Districts/SWL/districtdefault.cfm', '_blank');");
mm_menu_0709172118_0.addMenuItem("Vicksburg&nbsp;District","window.open('/WaterControl/Districts/MVK/districtdefault.cfm', '_blank');");
mm_menu_0709172118_0.addMenuItem("New&nbsp;Orleans&nbsp;District","window.open('/WaterControl/Districts/MVN/districtdefault.cfm', '_blank');");
mm_menu_0709172118_0.fontWeight="bold";
mm_menu_0709172118_0.hideOnMouseOut=true;
mm_menu_0709172118_0.menuBorder=1;
mm_menu_0709172118_0.menuLiteBgColor='#ffffff';
mm_menu_0709172118_0.menuBorderBgColor='#555555';
mm_menu_0709172118_0.bgColor='#555555';
mm_menu_0709172118_0.writeMenus();
} // mmLoadMenus()
//-->
</script>
<script language="JavaScript1.2" src="/WaterControl/images/banner/mm_menu.js"></script>
</head>
<body bgcolor="#ffffff" onLoad="MM_preloadImages('/WaterControl/images/banner/HomeBtn_f2.gif','/WaterControl/images/banner/SearchBtn_f2.gif','/WaterControl/images/banner/RelatedWebsitesBtn_f2.gif','/WaterControl/images/banner/DataMiningBtn_f2.gif','/WaterControl/images/banner/GlossaryBtn_f2.gif','/WaterControl/images/banner/WhoWeAreBtn_f2.gif','/WaterControl/images/banner/ReportsBtn_f2.gif','/WaterControl/images/banner/ContactUsBtn_f2.gif');">
<script language="JavaScript1.2">mmLoadMenus();</script>
<script language="JavaScript">
function map_clicked() {
document.frm_menu.fld_district.value = district;
mapbased = confirm("If You Wish To View The Map Based Version\nOf Rivergages.com, Click OK. Otherwise Click Cancel.");
if (mapbased == false && document.frm_menu.fld_district.value != '') {
document.frm_menu.submit();
}
else {
MM_openBrWindow('https://rsgis.crrel.usace.army.mil/cv_dev/corpsview_dev.cvmain.display?district=' + districtabbr,'','')
}
}
function check_value() {
if (document.frm_menu.fld_district.value != '') {
document.frm_menu.submit();
}
}
function check_value2() {
if (document.frm_specific2.fld_basin.value != '') {
document.frm_specific2.submit()
}
}
function set_district() {
document.frm_menu.fld_district.value = district;
check_value();
}
</script>
<SCRIPT language="JavaScript">
var MouseOverCol = "#FF0000";
var MouseNotOverCol = "#267DFF";
function ToColorJS(NewColor)
{
window.event.srcElement.style.color = NewColor;
}
</SCRIPT>
<script language="JavaScript" type="text/JavaScript">
<!--
function MM_goToURL() { //v3.0
var i, args=MM_goToURL.arguments; document.MM_returnValue = false;
for (i=0; i<(args.length-1); i+=2) eval(args[i]+".location='"+args[i+1]+"'");
}
//-->
</script>
<table border="0" cellpadding="0" cellspacing="0" width="670">
<!-- fwtable fwsrc="banner670.png" fwbase="banner670.gif" fwstyle="Dreamweaver" fwdocid = "742308039" fwnested="0" -->
<tr>
<td><img src="/WaterControl/images/banner/spacer.gif" width="1" height="1" border="0" alt=""></td>
<td><img src="/WaterControl/images/banner/spacer.gif" width="49" height="1" border="0" alt=""></td>
<td><img src="/WaterControl/images/banner/spacer.gif" width="1" height="1" border="0" alt=""></td>
<td><img src="/WaterControl/images/banner/spacer.gif" width="104" height="1" border="0" alt=""></td>
<td><img src="/WaterControl/images/banner/spacer.gif" width="1" height="1" border="0" alt=""></td>
<td><img src="/WaterControl/images/banner/spacer.gif" width="114" height="1" border="0" alt=""></td>
<td><img src="/WaterControl/images/banner/spacer.gif" width="1" height="1" border="0" alt=""></td>
<td><img src="/WaterControl/images/banner/spacer.gif" width="82" height="1" border="0" alt=""></td>
<td><img src="/WaterControl/images/banner/spacer.gif" width="1" height="1" border="0" alt=""></td>
<td><img src="/WaterControl/images/banner/spacer.gif" width="67" height="1" border="0" alt=""></td>
<td><img src="/WaterControl/images/banner/spacer.gif" width="1" height="1" border="0" alt=""></td>
<td><img src="/WaterControl/images/banner/spacer.gif" width="67" height="1" border="0" alt=""></td>
<td><img src="/WaterControl/images/banner/spacer.gif" width="1" height="1" border="0" alt=""></td>
<td><img src="/WaterControl/images/banner/spacer.gif" width="88" height="1" border="0" alt=""></td>
<td><img src="/WaterControl/images/banner/spacer.gif" width="19" height="1" border="0" alt=""></td>
<td><img src="/WaterControl/images/banner/spacer.gif" width="72" height="1" border="0" alt=""></td>
<td><img src="/WaterControl/images/banner/spacer.gif" width="1" height="1" border="0" alt=""></td>
<td><img src="/WaterControl/images/banner/spacer.gif" width="1" height="1" border="0" alt=""></td>
</tr>
<tr>
<td colspan="17"><img name="banner032204_r1_c1" src="/WaterControl/images/banner/MainBanner.gif" width="670" height="67" border="0" alt=""></td>
<td><img src="/WaterControl/images/banner/spacer.gif" width="1" height="67" border="0" alt=""></td>
</tr>
<tr>
<td rowspan="3"><img name="banner032204_r2_c1" src="/WaterControl/images/banner/banner032204_r2_c1.gif" width="1" height="18" border="0" alt=""></td>
<td rowspan="3"><a href="/WaterControl/new/layout.cfm" onMouseOut="MM_swapImgRestore();" onMouseOver="MM_swapImage('HomeBtn','','/WaterControl/images/banner/HomeBtn_f2.gif',1);"><img name="HomeBtn" src="/WaterControl/images/banner/HomeBtn.gif" width="49" height="18" border="0" alt="Home"></a></td>
<td rowspan="3"><img name="banner032204_r2_c3" src="/WaterControl/images/banner/banner032204_r2_c3.gif" width="1" height="18" border="0" alt=""></td>
<td rowspan="3"><a href="/WaterControl/search2.cfm" onMouseOut="MM_swapImgRestore();" onMouseOver="MM_swapImage('SearchBtn','','/WaterControl/images/banner/SearchBtn_f2.gif',1);"><img name="SearchBtn" src="/WaterControl/images/banner/SearchBtn.gif" width="104" height="18" border="0" alt="Search This Site"></a></td>
<td rowspan="3"><img name="banner032204_r2_c5" src="/WaterControl/images/banner/banner032204_r2_c5.gif" width="1" height="18" border="0" alt=""></td>
<td rowspan="3"><a href="/WaterControl/relatedsites2.cfm" onMouseOut="MM_swapImgRestore();" onMouseOver="MM_swapImage('RelatedWebsitesBtn','','/WaterControl/images/banner/RelatedWebsitesBtn_f2.gif',1);"><img name="RelatedWebsitesBtn" src="/WaterControl/images/banner/RelatedWebsitesBtn.gif" width="114" height="18" border="0" alt="Related Websites"></a></td>
<td rowspan="3"><img name="banner032204_r2_c7" src="/WaterControl/images/banner/banner032204_r2_c7.gif" width="1" height="18" border="0" alt=""></td>
<td rowspan="3"><a href="/WaterControl/datamining2.cfm" onMouseOut="MM_swapImgRestore();" onMouseOver="MM_swapImage('DataMiningBtn','','/WaterControl/images/banner/DataMiningBtn_f2.gif',1);"><img name="DataMiningBtn" src="/WaterControl/images/banner/DataMiningBtn.gif" width="82" height="18" border="0" alt="Data Mining"></a></td>
<td rowspan="3"><img name="banner032204_r2_c9" src="/WaterControl/images/banner/banner032204_r2_c9.gif" width="1" height="18" border="0" alt=""></td>
<td rowspan="3"><a href="/WaterControl/glossary2.cfm" onMouseOut="MM_swapImgRestore();" onMouseOver="MM_swapImage('GlossaryBtn','','/WaterControl/images/banner/GlossaryBtn_f2.gif',1);"><img name="GlossaryBtn" src="/WaterControl/images/banner/GlossaryBtn.gif" width="67" height="18" border="0" alt="Glossary"></a></td>
<td rowspan="3"><img name="banner032204_r2_c11" src="/WaterControl/images/banner/banner032204_r2_c11.gif" width="1" height="18" border="0" alt=""></td>
<td rowspan="3"><a href="/WaterControl/reports2.cfm" onMouseOut="MM_swapImgRestore();" onMouseOver="MM_swapImage('ReportsBtn','','/WaterControl/images/banner/ReportsBtn_f2.gif',1);"><img name="ReportsBtn" src="/WaterControl/images/banner/ReportsBtn.gif" width="67" height="18" border="0" alt="Reports"></a></td>
<td rowspan="3"><img name="banner032204_r2_c13" src="/WaterControl/images/banner/banner032204_r2_c13.gif" width="1" height="18" border="0" alt=""></td>
<td rowspan="3"><a href="#" onMouseOut="MM_swapImgRestore();MM_startTimeout();" onMouseOver="MM_showMenu(window.mm_menu_0709172118_0,0,18,null,'WhoWeAreBtn');MM_swapImage('WhoWeAreBtn','','/WaterControl/images/banner/WhoWeAreBtn_f2.gif',1);"><img name="WhoWeAreBtn" src="/WaterControl/images/banner/WhoWeAreBtn.gif" width="88" height="18" border="0" alt="Who We Are"></a></td>
<td colspan="3"><img name="banner032204_r2_c15" src="/WaterControl/images/banner/banner032204_r2_c15.gif" width="92" height="1" border="0" alt=""></td>
<td><img src="/WaterControl/images/banner/spacer.gif" width="1" height="1" border="0" alt=""></td>
</tr>
<tr>
<td rowspan="2"><img name="banner032204_r3_c15" src="/WaterControl/images/banner/banner032204_r3_c15.gif" width="19" height="17" border="0" alt=""></td>
<td><a href="mailto:CEMVRRiverGages@usace.army.mil" onMouseOut="MM_swapImgRestore();" onMouseOver="MM_swapImage('ContactUsBtn','','/WaterControl/images/banner/ContactUsBtn_f2.gif',1);"><img name="ContactUsBtn" src="/WaterControl/images/banner/ContactUsBtn.gif" width="72" height="16" border="0" alt="Contact Us"></a></td>
<td rowspan="2"><img name="banner032204_r3_c17" src="/WaterControl/images/banner/banner032204_r3_c17.gif" width="1" height="17" border="0" alt=""></td>
<td><img src="/WaterControl/images/banner/spacer.gif" width="1" height="16" border="0" alt=""></td>
</tr>
<tr>
<td><img name="banner032204_r4_c16" src="/WaterControl/images/banner/banner032204_r4_c16.gif" width="72" height="1" border="0" alt=""></td>
<td><img src="/WaterControl/images/banner/spacer.gif" width="1" height="1" border="0" alt=""></td>
</tr>
<td colspan="17"><table width="670">
<tr valign="top">
<td width="213" align="left">
<form method="post" name="frm_menu" id="frm_menu">
<strong><font color="#FF0000" size="2" face="Arial, Helvetica, sans-serif">Water
Levels By:</font></strong><br>
<select name="fld_district" id="fld_district" onChange="check_value();">
<option value="" selected>Choose An Option</option>
<option value="">District</option>

<option value="18" >&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Lakes and Rivers Division</option>

<option value="0" >&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;St. Paul District</option>

<option value="14" >&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Sacramento District</option>

<option value="15" >&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Tulsa District</option>

<option value="17" >&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Huntington District</option>

<option value="6" >&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Rock Island District</option>

<option value="16" >&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Pittsburgh District</option>

<option value="8" >&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Omaha District</option>

<option value="19" >&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Buffalo District</option>

<option value="9" >&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Kansas City District</option>

<option value="2" >&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;St. Louis District</option>

<option value="13" >&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Louisville District</option>

<option value="20" >&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Portland District</option>

<option value="3" >&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Memphis District</option>

<option value="11" >&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Little Rock District</option>

<option value="12" >&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Nashville District</option>

<option value="21" >&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Seattle District</option>

<option value="4" >&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Vicksburg District</option>

<option value="5" >&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;New Orleans District</option>

<option value="Basin" >Basin</option>
<option value="Stream" >Stream</option>
<option value="State" >State</option>
<option value="City" >City</option>
</select>
</form>
</td>
<td width="349" align="left">
<form name="frm_specific2" action="/WaterControl/new/layout.cfm" method="POST">

</form>
</td>
<td width="349" align="left"><form action="" method="post" name="frm_nws" id="frm_nws">
<div align="right" style="cursor:hand" onMouseOver="ToColorJS(MouseOverCol)" onMouseOut="ToColorJS(MouseNotOverCol)" onClick="MM_goToURL('parent','/docs/ldm/index.cfm');return document.MM_returnValue"><strong><font color="#267DFF" size="2" face="Arial, Helvetica, sans-serif">National Weather <br>
  Service Products</font></strong> </div>
</form></td>
</tr>
</table></td>
</tr>
</table>
</td>
</tr>
<tr valign="top">
<td>
<form method="post" name="frm_mining" id="frm_mining">
<table width="640" border="5" align="center" bordercolor="#0066CC" bgcolor="#FFFFFF"><tr bgcolor=#FFFFFF class="style11">
<td bgcolor="#FFFFFF"> <div align="center"><b> Data Mining</b></div></td>
<tr bgcolor=#000055>
  <td bgcolor="#000055" class="style11"><div align="center"><font size="2"><font color="#FFFFFF">Choose
    A Station<br>
    <select name="fld_station" id="fld_station" onChange="MM_goToURL('parent','/WaterControl/datamining2.cfm?sid=' + document.frm_mining.fld_station.value);return document.MM_returnValue">
      <option value="" selected >-----</option>
      
        <option value="AGNI4" > East Fork Des Moines River near Algona, IA</option>
      
        <option value="DEMI4" > Raccoon River at Fleur Dr. in Des Moines, IA</option>
      
        <option value="03335500" > Wabash River at Lafayette </option>
      
        <option value="SF128" >(Old) St. Francis River At Marked Tree, AR</option>
      
        <option value="85652" >17th Street Canal 1 - ICS Lake-side (85652)</option>
      
        <option value="85653" >17th Street Canal 2 - ICS Canal-side (85653)</option>
      
        <option value="85654" >17th Street Canal 3 - Geneva St. (85654)</option>
      
        <option value="85655" >17th Street Canal 4 - Georgia Ct. (85655)</option>
      
        <option value="85656" >17th Street Canal 5 - Cherry St. (85656)</option>
      
        <option value="85657" >17th Street Canal 6 -  I-10 (85657)</option>
      
        <option value="85658" >17th Street Canal 7 - Lemon St. (85658)</option>
      
        <option value="85659" >17th Street Canal 8 - PS6 (85659)</option>
      
        <option value="ACCM2" >Accident, MD (ACDM)</option>
      
        <option value="ALXW2" >Alexander, WV (ALXW)</option>
      
        <option value="ALZO1" >Alexandria near Caldwell, OH (ALXE3)</option>
      
        <option value="76240" >Algiers Lock - GIWW (76240)</option>
      
        <option value="KNZP1" >Allegheny Reservoir, PA (KINP)</option>
      
        <option value="ELRP1" >Allegheny River at Eldred, PA (ELRP)</option>
      
        <option value="FRKP1" >Allegheny River at Franklin, PA (FRKP)</option>
      
        <option value="SHRP1" >Allegheny River at L/D-2, Sharpsburg, PA (Upper) (SHRP)</option>
      
        <option value="ACMP1" >Allegheny River at L/D-3, CW Bill Young, PA (Upper) (ACMP)</option>
      
        <option value="NATP1" >Allegheny River at L/D-4, Natrona, PA (Upper) (NATP)</option>
      
        <option value="FREP1" >Allegheny River at L/D-5, Freeport, PA (Upper) (FREP)</option>
      
        <option value="CLNP1" >Allegheny River at L/D-6, Clinton, PA (Upper) (CLNP)</option>
      
        <option value="KTTP1" >Allegheny River at L/D-7, Kittanning, PA (Upper) (KTTP)</option>
      
        <option value="MOSP1" >Allegheny River at L/D-8, Mosgrove, PA (Upper) (MOSP)</option>
      
        <option value="RMRP1" >Allegheny River at L/D-9, Rimer, PA (Upper) (NEVP)</option>
      
        <option value="OLNN6" >Allegheny River at Olean, NY (OLNN)</option>
      
        <option value="PARP1" >Allegheny River at Parker, PA (PKLP)</option>
      
        <option value="PALP1" >Allegheny River at Port Allegany, PA (PALP)</option>
      
        <option value="WRRP1" >Allegheny River at Warren, PA  (WRRP)</option>
      
        <option value="WHKP1" >Allegheny River at West Hickory, PA (WHKP)</option>
      
        <option value="AACO1" >Alliance, OH (WTP) (ALIO)</option>
      
        <option value="AFRO1" >Alum Creek (Below Dam) at Africa, OH (ACSOF)</option>
      
        <option value="ACRO1" >Alum Creek at Alum Creek Reservoir near Kilbourne, OH (ACSE3)</option>
      
        <option value="CLMO1" >Alum Creek at Columbus, OH (CLAF3)</option>
      
        <option value="KLBO1" >Alum Creek near Kilbourne, OH (KLAD3)</option>
      
        <option value="85040" >Amite River near Denham Springs (85040) </option>
      
        <option value="AMDO1" >Amsterdam, OH (AMDO)</option>
      
        <option value="ADEO1" >Andover, OH (ANDO)</option>
      
        <option value="APRI2" >Apple River near Hanover, IL</option>
      
        <option value="APP" >Applegate Reservoir</option>
      
        <option value="APRO" >Applegate River near Applegate</option>
      
        <option value="ARWO" >Applegate River near Wilderville</option>
      
        <option value="APPO" >Applegate at Copper</option>
      
        <option value="NOGA4" >Arkansas Post Canal at Lock 1 (Norrell)</option>
      
        <option value="ACGA4" >Arkansas Post Canal at Lock 2</option>
      
        <option value="NAGA4" >Arkansas River at D02 (Mills)</option>
      
        <option value="DARA4" >Arkansas River at Dardanelle</option>
      
        <option value="SWNA4" >Arkansas River at LD03 (Joe Hardin)</option>
      
        <option value="LADA4" >Arkansas River at LD04 (Sanders)</option>
      
        <option value="LNDA4" >Arkansas River at LD05 (Maynard)</option>
      
        <option value="DTLA4" >Arkansas River at LD06 (Terry)</option>
      
        <option value="MYLA4" >Arkansas River at LD07 (Murray)</option>
      
        <option value="TODA4" >Arkansas River at LD08 (Toad Suck Ferry)</option>
      
        <option value="MOLA4" >Arkansas River at LD09 (Ormond)</option>
      
        <option value="DRDA4" >Arkansas River at LD10 (Dardanelle)</option>
      
        <option value="OZGA4" >Arkansas River at LD12 (Ozark)</option>
      
        <option value="BARA4" >Arkansas River at LD13 (Trimble)</option>
      
        <option value="LITA4" >Arkansas River at Little Rock</option>
      
        <option value="MORA4" >Arkansas River at Morrilton</option>
      
        <option value="PFAA4" >Arkansas River at Pendleton</option>
      
        <option value="PBFA4" >Arkansas River at Pine Bluff</option>
      
        <option value="CE5E9948" >Ascalmore Tippo Structure (landside)</option>
      
        <option value="CZ5E9948" >Ascalmore-Tippo Structure (riverside)</option>
      
        <option value="88600" >Atchafalaya Bay at Eugene Island (88600)</option>
      
        <option value="03120" >Atchafalaya River at Butte La Rose (03120)</option>
      
        <option value="03075" >Atchafalaya River at Krotz Springs (03075)</option>
      
        <option value="03060" >Atchafalaya River at Melville (03060)</option>
      
        <option value="03045" >Atchafalaya River at Simmesport (03045)</option>
      
        <option value="SMML1" >Atchafalaya River at Simmesport (USGS)</option>
      
        <option value="03045Q" >Atchafalaya River at Simmesport - Discharge (03045Q)</option>
      
        <option value="ATW" >Atwell Mills Weather</option>
      
        <option value="AVLP1" >Avella, PA (AVLP)</option>
      
        <option value="03820" >Avoca Island Cutoff south of Morgan City (03820)</option>
      
        <option value="FLSN1" >B Nemaha River at Falls City, NE</option>
      
        <option value="DBCN8" >Baldhill Creek near Dazey, ND - USGS Station No. 05057200</option>
      
        <option value="BLDN8" >Baldhill Dam Pool above Valley City, ND</option>
      
        <option value="BLDDD" >Baldhill Dam and Reservoir</option>
      
        <option value="BLMO" >Balm Fork above Lake</option>
      
        <option value="07380251" >Barataria Bay North of Grand Isle (USGS)</option>
      
        <option value="73802516" >Barataria Pass at Grand Isle (USGS)</option>
      
        <option value="82875" >Barataria Waterway at Lafitte (82875)</option>
      
        <option value="ROMW3" >Bark River near Rome, WI</option>
      
        <option value="BRNP1" >Barnes, PA (BRNP)</option>
      
        <option value="BRRK2" >Barren River Lake</option>
      
        <option value="03314500" >Barren River at Bowling Green</option>
      
        <option value="03313000" >Barren River near Finney</option>
      
        <option value="CE487DEA" >Bayou Bartholomew @ Beekman, LA</option>
      
        <option value="CE455860" >Bayou Bartholomew @ Star City, AR</option>
      
        <option value="CE456328" >Bayou Bartholomew @ Wilmot, AR</option>
      
        <option value="76024" >Bayou Bienvenue Floodgate - West (76024)</option>
      
        <option value="76025" >Bayou Bienvenue Floodgate East - MRGO (76025)</option>
      
        <option value="52840" >Bayou Black at Gibson (52840)</option>
      
        <option value="52880" >Bayou Black at Greenwood (52880)</option>
      
        <option value="CE494458" >Bayou Bodcau @ Bayou Bodcau Dam (riverside), LA</option>
      
        <option value="CE40D766" >Bayou Bodcau Lake Nr. Shreveport (landside), LA</option>
      
        <option value="76360" >Bayou Boeuf Lock - East (76360)</option>
      
        <option value="76400" >Bayou Boeuf Lock - West (76400)</option>
      
        <option value="52800" >Bayou Boeuf at Amelia (52800)</option>
      
        <option value="82725" >Bayou Boeuf at Kraemer (82725)</option>
      
        <option value="CE5EDA42" >Bayou Cocodrie @ Deer Park Monterey, LA</option>
      
        <option value="CZ5ED490" >Bayou Cocodrie @ Wild Cow Bayou Structure (Lower)</option>
      
        <option value="CE5ED490" >Bayou Cocodrie @ Wild Cow Bayou Structure (Upper)</option>
      
        <option value="58400" >Bayou Courtableau above Drainage Structure (58400)</option>
      
        <option value="CE7F2700" >Bayou Darrow Drainage Structure (landside), LA</option>
      
        <option value="CE48FBFE" >Bayou Darrow Drainage Structure (riverside)</option>
      
        <option value="BD111" >Bayou DeView At Morton, AR</option>
      
        <option value="82700" >Bayou Des Allemands at Des Allemands (82700)</option>
      
        <option value="BDGL1" >Bayou Des Glaises Diversion Channel at Moreauville (USGS) </option>
      
        <option value="76005" >Bayou Dupre Floodgate - Bayou side (76005 - West)</option>
      
        <option value="76010" >Bayou Dupre Floodgate - MRGO side (76010 - East)</option>
      
        <option value="03210" >Bayou La Rompe at Lake Long (03210)</option>
      
        <option value="DD394496" >Bayou LaFourche @ Alto, LA</option>
      
        <option value="CE49A7AA" >Bayou Lafourche @ Crew Lake, LA</option>
      
        <option value="40900" >Bayou Latenache Above Pointe Coupee Drainage Str (40900)</option>
      
        <option value="43500" >Bayou Latenache Below Pointe Coupee Drainage Str (43500)</option>
      
        <option value="CE493C1A" >Bayou Macon @ Como, LA</option>
      
        <option value="CE5EE10A" >Bayou Macon @ Eudora, AR</option>
      
        <option value="76305" >Bayou Petit Caillou at Cocodrie (76305) </option>
      
        <option value="82740" >Bayou Segnette at Lapalco Blvd (82740)</option>
      
        <option value="85634" >Bayou St John at Lake Pontchartrain (85634) </option>
      
        <option value="64700" >Bayou Teche at East Calumet Floodgate (64700)</option>
      
        <option value="64650" >Bayou Teche at West Calumet Floodgate (64650)</option>
      
        <option value="85780" >Bayou Terre Aux Boeufs at Delacroix, La. (85780)</option>
      
        <option value="85663" >Bayou Trepagnier Control Structure -North (85663)</option>
      
        <option value="BEHO1" >Beach City Lake at Beach City, OH (BCSC5)</option>
      
        <option value="MCK" >Bear Creek</option>
      
        <option value="BARQ" >Bear Creek Dam Outflow</option>
      
        <option value="BECR" >Bear Creek Reservoir</option>
      
        <option value="BARP" >Bear Creek Reservoir Pool</option>
      
        <option value="BCRM7" >Bear Creek at Hannibal, MO</option>
      
        <option value="OMBA4" >Bear Creek at Omaha</option>
      
        <option value="MBRI2" >Bear Creek near Marcelline, IL</option>
      
        <option value="BRM" >Beartrap Meadow Weather</option>
      
        <option value="BRBM7" >Beaver Creek at Bradleyville</option>
      
        <option value="MTCK2" >Beaver Creek at Monticello,KY</option>
      
        <option value="NHRI4" >Beaver Creek at New Hartford, IA</option>
      
        <option value="GRMI4" >Beaver Creek near Grimes, IA </option>
      
        <option value="WWDI4" >Beaver Creek near Woodward, IA</option>
      
        <option value="BEAP1P" >Beaver River @ Beaver Falls</option>
      
        <option value="BEAP1" >Beaver River at Beaver Falls, PA (BEAP)</option>
      
        <option value="WPMP1" >Beaver River at Wampum, PA (WAMP)</option>
      
        <option value="BEAW3" >Beaverdam River at Beaver Dam, WI</option>
      
        <option value="BFOW2" >Beech Fork Dam Outflow near Lavalette, WV (BBFOF)</option>
      
        <option value="BFLW2" >Beech Fork Dam near Huntington, WV (BBFL4)</option>
      
        <option value="03300400" >Beech Fork at Maud</option>
      
        <option value="BNRA4" >Bennetts River at Vidette</option>
      
        <option value="BRWO1" >Berlin Lake Outflow, OH (BROO)</option>
      
        <option value="BRLO1" >Berlin Lake, OH (BERO)</option>
      
        <option value="BEPO1" >Berlin Lake, OH (Route 224) (BERX)</option>
      
        <option value="CE2F6048" >Big Bayou @ Dermott, AR</option>
      
        <option value="CE7DF49C" >Big Bayou @ Lake Village, AR</option>
      
        <option value="CE3C23D2" >Big Bayou Meto @ Stuttgart, AR</option>
      
        <option value="LADI4" >Big Bear Creek near Ladora, IA</option>
      
        <option value="CE50207C" >Big Black River @ Bentonia</option>
      
        <option value="CE501B34" >Big Black River @ Bovina, MS</option>
      
        <option value="176EB63E" >Big Black River @ West, MS</option>
      
        <option value="BARN1" >Big Blue River at Barneston, NE</option>
      
        <option value="MRYK1" >Big Blue River at Marysville, KS</option>
      
        <option value="CRTN1" >Big Blue River near Crete, NE</option>
      
        <option value="MNTK1" >Big Blue River near Manhattan, KS</option>
      
        <option value="PINI2" >Big Bureau Creek at Princeton,IL </option>
      
        <option value="MLBO" >Big Butte Creek near McLeod</option>
      
        <option value="CE5EC7E6" >Big Colewa Bayou @ Oak Grove, LA</option>
      
        <option value="BCM10" >Big Creek At Millington, TN</option>
      
        <option value="PLKI4" >Big Creek Lake near Polk City, IA </option>
      
        <option value="BIGI4" >Big Creek Ponding Area near Polk City, IA</option>
      
        <option value="MBCA4" >Big Creek at Elizabeth</option>
      
        <option value="BCM12" >Big Creek at Rosemark, TN</option>
      
        <option value="MPZI4" >Big Creek near Mt. Pleasant, IA</option>
      
        <option value="BIFM5" >Big Fork River at Big Fork, MN - USGS Station No. 05132000</option>
      
        <option value="BL116" >Big Lake (Downstream of Ditch 81 Control Structure) Near Manila, AR</option>
      
        <option value="BL115" >Big Lake (Upstream Of Ditch 81 Control Structure) Near Manila, AR</option>
      
        <option value="BL113" >Big Lake Inlet (Downstream Of North End Control Structure) Near Manila, AR</option>
      
        <option value="RENDLKPL" >Big Muddy River at Rend Lake (Pool)</option>
      
        <option value="DVRA4" >Big Piney Creek at Hwy 164 near Dover, AR</option>
      
        <option value="03340900" >Big Raccoon Creek at Ferndale at CM Harden Lake TW</option>
      
        <option value="03340800" >Big Raccoon Creek near Fincastle</option>
      
        <option value="ROCW2" >Big Sandy Creek at Rockville,WV (RVLW)</option>
      
        <option value="SDYM5" >Big Sandy Lake near McGregor MN</option>
      
        <option value="FLRK2" >Big Sandy River at Fullers Station near Louisa, KY (FSSM3)</option>
      
        <option value="PRCK2" >Big Sandy River near Price, KY (PRIP3)</option>
      
        <option value="SOOW" >Big Soos Creek Near Auburn, WA </option>
      
        <option value="CE488D6E" >Big Sunflower River @ Anguilla, Ms</option>
      
        <option value="CE3EB344" >Big Sunflower River @ Clarksdale, MS</option>
      
        <option value="CE4890CA" >Big Sunflower River @ Holly Bluff, MS</option>
      
        <option value="CE507ED2" >Big Sunflower River @ Little Callio Landing, MS</option>
      
        <option value="CE6A12C4" >Big Sunflower River @ Lombardy, MS</option>
      
        <option value="DDA21764" >Big Sunflower River @ Sunflower, MS</option>
      
        <option value="CSCO1" >Big Walnut Creek at Central College near Gould Park, OH (CNCE3)</option>
      
        <option value="REEO1" >Big Walnut Creek at Rees, OH (REWF3)</option>
      
        <option value="03357500" >Big Walnut Creek nr Reelsville</option>
      
        <option value="IRCW2" >Birch River, WV (BIRL7)</option>
      
        <option value="CE5EA200" >Black Bayou @ Black Bayou (Charleston), MS</option>
      
        <option value="CE5EACD2" >Black Bayou @ Greenville, MS (highway 82)</option>
      
        <option value="CE486E9C" >Black Bayou @ Hollandale, MS (Hwy 12)</option>
      
        <option value="CHRN6" >Black Creek at Churchville</option>
      
        <option value="LDVO1" >Black Fork River at Loudonville, OH (LOBC4)</option>
      
        <option value="MEPO1" >Black Fork River at Melco near Perrysville, OH (MELC4)</option>
      
        <option value="CHAO1" >Black Fork River below Charles Mill Dam near Mifflin, OH (CMBOF)</option>
      
        <option value="HUDI4" >Black Hawk Creek at Hudson, IA</option>
      
        <option value="BLR" >Black Rascal Diversion</option>
      
        <option value="CE41ADDE" >Black River @ Acme, LA</option>
      
        <option value="CZ48F52C" >Black River @ Jonesville Lock & Dam (lower)</option>
      
        <option value="CE48F52C" >Black River @ Jonesville Lock & Dam (upper)</option>
      
        <option value="JSIM7" >Black River East Fork near Lesterville</option>
      
        <option value="BRFW3" >Black River at Black River Falls, WI - USGS Station No. 053813595</option>
      
        <option value="BKRA4" >Black River at Black Rock</option>
      
        <option value="CLRM7" >Black River at Clearwater Dam - HW</option>
      
        <option value="CLTM7" >Black River at Clearwater Dam - TW</option>
      
        <option value="EFGA4" >Black River at Elgin Ferry</option>
      
        <option value="POCA4" >Black River at Pocahontas</option>
      
        <option value="PPBM7" >Black River at Poplar Bluff</option>
      
        <option value="ANNM7" >Black River near Annapolis</option>
      
        <option value="CRGA4" >Black River near Corning</option>
      
        <option value="GALW3" >Black River near Galesville, WI - USGS Station No. 05382000</option>
      
        <option value="FKFK1" >Black Vermillion River near Frankfort, KS</option>
      
        <option value="BB111" >Blackfish Bayou Near Hughes, AR (West)</option>
      
        <option value="JOSP1" >Blacklick Creek at Josephine, PA (JOSP)</option>
      
        <option value="BLVM7" >Blackwater River at Blue Lick, MO</option>
      
        <option value="BWRW2" >Blackwater River at Davis, WV (DVSW)</option>
      
        <option value="YTVK2" >Blaine Creek below Yatesville Lake near Louisa, KY (YBCOF)</option>
      
        <option value="BLNK2" >Blaine Creek near Blaine, KY (BLAM3)</option>
      
        <option value="BNDV2" >Bland, VA (BLAQ6)</option>
      
        <option value="BLCT1" >Bledsoe Creek near Gallatin, TN</option>
      
        <option value="BMFO1" >Bloomfield, OH (BLMO)</option>
      
        <option value="KCCM7" >Blue River at Bannister Road, MO</option>
      
        <option value="BSZM7" >Blue Springs Lake near Blue Springs, MO</option>
      
        <option value="SC04" >Bluestem Lake (Salt Creek Dam site #04)</option>
      
        <option value="BLLW2" >Bluestone Lake near Hinton, WV (BLNO7)</option>
      
        <option value="PIPW2" >Bluestone River near Pipestem, WV (PIBO6)</option>
      
        <option value="CE3EC5D4" >Bobo Bayou @ Bobo, MS</option>
      
        <option value="CE69E54E" >Boeuf River @ Alto, LA</option>
      
        <option value="CE509D20" >Boeuf River @ Eudora, AR</option>
      
        <option value="CE490752" >Boeuf River @ Fort Necessity, LA</option>
      
        <option value="17CB545A" >Bogue Chitto River @ Bush, LA</option>
      
        <option value="17CB72B6" >Bogue Chitto River @ Franklinton, LA</option>
      
        <option value="1773E2BA" >Bogue Chitto River @ Tylertown, MS</option>
      
        <option value="CVEL1" >Bogue Falaya River at Boston St. at Covington</option>
      
        <option value="DE1667E0" >Bogue Phalia @ Leland, MS</option>
      
        <option value="WHRM5" >Boix de Sioux River and White Rock Dam near White Rock, SD - USGS St No.05050000</option>
      
        <option value="BIVO1" >Bolivar Lake near Bolivar, OH (BOSC6)</option>
      
        <option value="GLDI4" >Boone River near Goldfield, IA </option>
      
        <option value="WBCI4" >Boone River near Webster City, IA </option>
      
        <option value="BRLQ" >Borel Canal </option>
      
        <option value="BRLP" >Borel Canal Pool</option>
      
        <option value="BOHA" >Bowman-Haley Reservoir</option>
      
        <option value="SC18" >Branched Oak Lake (Salt Creek Dam site #18)</option>
      
        <option value="03295890" >Brashears Creek at Taylorsville</option>
      
        <option value="YVLP1" >Brokenstraw Creek at Youngsville, PA (YVLP)</option>
      
        <option value="BKVI3" >Brookville Lake</option>
      
        <option value="TBCM7" >Bryant Creek near Tecumseh</option>
      
        <option value="BKNW2" >Buckhannon River at Buckhannon, WV (BKNW)</option>
      
        <option value="BUCK2" >Buckhorn Lake</option>
      
        <option value="49235" >Buffalo Cove at Round Island nr Charenton (49235) </option>
      
        <option value="PRAI4" >Buffalo Creek South of Prairieburg, IA</option>
      
        <option value="BRIW2" >Buffalo Creek at Barrackville, WV (BRRW)</option>
      
        <option value="SJOA4" >Buffalo River near St. Joe</option>
      
        <option value="BBCM7" >Bull Creek at Branson</option>
      
        <option value="BNR" >Bunning Ranch Weather</option>
      
        <option value="BURQ" >Burns Creek Dam Outflow</option>
      
        <option value="BURP" >Burns Creek Reservoir</option>
      
        <option value="BRNW2" >Burnsville Dam near Burnsville, WV (BUSJ7)</option>
      
        <option value="GJTI4" >Buttrick Creek near Grand Junction, IA</option>
      
        <option value="CJBO1" >C.J. Brown Dam and Resevoir</option>
      
        <option value="CR114" >Cache River At Brasfield, AR</option>
      
        <option value="CR113" >Cache River At Patterson, AR</option>
      
        <option value="CR115" >Cache River at Little Dixie, AR</option>
      
        <option value="CE7F42E6" selected>Caddo Lake Dam, LA</option>
      
        <option value="DDBFA012" >Caddo River @ Caddo Gap, AR</option>
      
        <option value="CE40AF24" >Caddo River @ Degray Dam, AR</option>
      
        <option value="CDOO1" >Cadiz, OH (CADD7)</option>
      
        <option value="CAZO1" >Cadiz, OH (CDZO)</option>
      
        <option value="85765" >Caernarvon Canal Sector Gate - Northwest/Protected Side (85765)</option>
      
        <option value="85760" >Caernarvon Canal Sector Gate - Southeast/Flood Side (85760)</option>
      
        <option value="CCLO1" >Caesar Creek Lake</option>
      
        <option value="03235000" >Caesar Creek nr Wellman</option>
      
        <option value="CAGI3" >Cagles Mill Lake</option>
      
        <option value="07381349" >Caillou Lake (Sister Lake) SW of Dulac, LA (USGS)</option>
      
        <option value="73650" >Calcasieu River & Pass Near Cameron (73650)</option>
      
        <option value="73472" >Calcasieu River Salt Water Barrier at Lake Charles (E) (73472)</option>
      
        <option value="73473" >Calcasieu River Salt Water Barrier at Lake Charles (W) (73473)</option>
      
        <option value="73550" >Calcasieu River and Pass at Lake Charles (73550)</option>
      
        <option value="CMNW2" >Cameron, WV (CAMW)</option>
      
        <option value="CNVW2" >Canaan Valley, WV (CANW)</option>
      
        <option value="CE498146" >Canal 43 @ Arkansas City, AR</option>
      
        <option value="CE5056EC" >Canal 43N @ Dumas, AR</option>
      
        <option value="CE498F94" >Canal 81 @ Arkansas City, AR.</option>
      
        <option value="DSVN6" >Canaseraga Creek at Dansville, NY</option>
      
        <option value="CFST1" >Caney Fork River at Gordonsville, TN</option>
      
        <option value="CFLK2" >Carr Creek Lake</option>
      
        <option value="03277450" >Carr Fork near Sassafras</option>
      
        <option value="GNTM2" >Casselman River at Grantsville, MD (GTVM)</option>
      
        <option value="MAKP1" >Casselman River at Markleton, PA (MAKP)</option>
      
        <option value="CE3ED6A2" >Cassidy Bayou @ Marks, MS</option>
      
        <option value="CE43EB20" >Cassidy Bayou @ Webb, MS</option>
      
        <option value="CE5EEFD8" >Catahoula Lake @ Center of the Lake</option>
      
        <option value="CZ491AF6" >Catahoula Lake Control Structure (Riverside), LA</option>
      
        <option value="CE491AF6" >Catahoula Lake Control Structure (lakeside), LA</option>
      
        <option value="70675" >Catfish Point Control Structure - North (70675)</option>
      
        <option value="70750" >Catfish Point Control Structure - South (70750)</option>
      
        <option value="NALN6" >Cattaraugus, NY (NALN)</option>
      
        <option value="CRLK2" >Cave Run Lake</option>
      
        <option value="CHLI3" >Cecil M Harden Lake CHLI3</option>
      
        <option value="BSSI4" >Cedar Creek near Bussey, IA </option>
      
        <option value="OKMI4" >Cedar Creek near Oakland Mills, IA</option>
      
        <option value="PLOI4" >Cedar River at Blairs Ferry Road at Palo, IA</option>
      
        <option value="CEDI4" >Cedar River at Cedar Falls, IA</option>
      
        <option value="CIDI4" >Cedar River at Cedar Rapids, IA</option>
      
        <option value="CCYI4" >Cedar River at Charles City, IA</option>
      
        <option value="JANI4" >Cedar River at Janesville, IA</option>
      
        <option value="LANM5" >Cedar River at Lansing,MN</option>
      
        <option value="OSGI4" >Cedar River at Osage, IA</option>
      
        <option value="VINI4" >Cedar River at Vinton, IA</option>
      
        <option value="ALOI4" >Cedar River at Waterloo, IA</option>
      
        <option value="WVLI4" >Cedar River at Waverly,IA</option>
      
        <option value="ASNM5" >Cedar River near Austin,MN</option>
      
        <option value="CNEI4" >Cedar River near Conesville, IA</option>
      
        <option value="CTLP1" >Central City, PA (STP) (CTLP)</option>
      
        <option value="64450" >Charenton Drainage Canal at Baldwin (64450)</option>
      
        <option value="CHOO1" >Charles Mill Lake near Mansfield, OH (CMBC4)</option>
      
        <option value="CARP1" >Chartiers Creek at Carnegie, PA (CARP)</option>
      
        <option value="WAHP1" >Chartiers Creek at Washington, PA (WSHP)</option>
      
        <option value="CHFI" >Chatfield Reservoir</option>
      
        <option value="ABRW2" >Cheat River at Albright, WV (ALBW)</option>
      
        <option value="LLPW2" >Cheat River at Lake Lynn Outflow, WV (PMAW)</option>
      
        <option value="PSNW2" >Cheat River near Parsons, WV (PSNW)</option>
      
        <option value="ROLW2" >Cheat River near Rowlesburg, WV (ROWW)</option>
      
        <option value="85750" >Chef Menteur Pass nr Lake Borgne (85750)</option>
      
        <option value="CHCR" >Cherry Creek Reservoir</option>
      
        <option value="CH01" >Chicago River Lock and Dam</option>
      
        <option value="LEMI2" >Chicago Sanitary & Ship Canal near Lemont, IL</option>
      
        <option value="GNDL1" >Chicot Pass near Myette Point near Charenton (03540) </option>
      
        <option value="03465" >Chicot Pass near West Fork (03465)</option>
      
        <option value="WTSDD" >Chippewa Diversion Dam</option>
      
        <option value="WTSM5" >Chippewa River Diversion Dam near Watson, MN</option>
      
        <option value="DURW3" >Chippewa River at Durand, WI - USGS Station No. 05369500</option>
      
        <option value="MLNM5" >Chippewa River near Milan, MN - USGS Station No. 05304500</option>
      
        <option value="COKP1" >Clarion River at Cooksburg, PA (COKP)</option>
      
        <option value="JHNP1" >Clarion River at Johnsonburg, PA (JHNP)</option>
      
        <option value="RDYP1" >Clarion River at Ridgway, PA (RDYP)</option>
      
        <option value="CLLV2" >Claytor Dam near Radford, VA (CLNQ7)</option>
      
        <option value="CRAI4" >Clear Creek near Coralville, IA</option>
      
        <option value="OXJI4" >Clear Creek near Oxford, IA</option>
      
        <option value="CLFW2" >Clear Fork at Clear Fork, WV (CLCO5)</option>
      
        <option value="SXTK2" >Clear Fork at Saxton, KY</option>
      
        <option value="PHLO1" >Clear Fork below Pleasant Hill Dam near Perrysville, OH (PHCOF)</option>
      
        <option value="CFKT1" >Clear Fork near Robbins, TN</option>
      
        <option value="CLKO1" >Clendening Lake near Tippecanoe, OH (CLBD6)</option>
      
        <option value="CLIK1" >Clinton Lake near Lawrence, KS</option>
      
        <option value="TORW2" >Coal River at Tornado, WV (TORM5)</option>
      
        <option value="COLD" >Cold Brook Reservoir</option>
      
        <option value="CE40794C" >Coldwater River @ Arkabutla Dam, MS (Intake)</option>
      
        <option value="CE7F5190" >Coldwater River @ Arkabutla Dam, MS (Outlet)</option>
      
        <option value="CE7F87F8" >Coldwater River @ Coldwater, MS</option>
      
        <option value="CE3C1648" >Coldwater River @ Darling, MS</option>
      
        <option value="CE5E84EC" >Coldwater River @ Lewisburg, MS</option>
      
        <option value="CE7F892A" >Coldwater River @ Marks, MS</option>
      
        <option value="170085FE" >Coldwater River @ Olive Branch, MS</option>
      
        <option value="CE416612" >Coldwater River @ Sarah, MS</option>
      
        <option value="MCGT1" >Collins River near McMinnville, TN</option>
      
        <option value="CMDP1" >Conemaugh River Lake Outflow, PA (CNOP)</option>
      
        <option value="CNMP1" >Conemaugh River Lake, PA (CONP)</option>
      
        <option value="SWDP1" >Conemaugh River at Seward, PA (SWDP)</option>
      
        <option value="SC12" >Conestoga Lake (Salt Creek Dam site #12)</option>
      
        <option value="RSSP1" >Conewango Creek at Russell, PA (RSSP)</option>
      
        <option value="CE69F638" >Connerly Bayou @ Connerly Bayou Dam, AR</option>
      
        <option value="BTRP1" >Connoquenessing Creek near Butler, PA (BTLP)</option>
      
        <option value="CRVI4" >Coralville Lake Reservoir</option>
      
        <option value="CRYP1" >Corry, PA (CORP)</option>
      
        <option value="CGV" >Cosgrove Creek</option>
      
        <option value="GLLA4" >Cossatot River at Gillham Dam - HW</option>
      
        <option value="GLTA4" >Cossatot River at Gillham Dam - TW</option>
      
        <option value="DEQA4" >Cossatot River near DeQueen</option>
      
        <option value="COUP1" >Coudersport, PA (CSPP)</option>
      
        <option value="COYQ" >Coyote Dam Outflow</option>
      
        <option value="CCRO1" >Crab Creek at Youngstown, OH (CRBO)</option>
      
        <option value="CRBW2" >Crab Orchard near Beckley, WV (BECN6)</option>
      
        <option value="CRNW2" >Cranberry River near Richwood, WV (CRCL8)</option>
      
        <option value="CNLM5" >Crane Lake at Crane Lake, MN</option>
      
        <option value="CNRV2" >Cranesnest River near Clintwood, VA (CLCQ4)</option>
      
        <option value="CCLK2" >Cranks Creek at Cranks Creek Dam, KY</option>
      
        <option value="MILW3" >Crawfish River at Milford, WI</option>
      
        <option value="CSSP1" >Cresson, PA (RAWS) (CRSP)</option>
      
        <option value="03830" >Crewboat Channel at Wax Lake Outlet nr Calumet (03830)</option>
      
        <option value="CCDP1" >Crooked Creek Lake Outflow, PA (CROP)</option>
      
        <option value="CRCP1" >Crooked Creek Lake, PA (CRCP)</option>
      
        <option value="IDAP1" >Crooked Creek at Idaho, PA (IDAP)</option>
      
        <option value="YEGA4" >Crooked Creek at Yellville</option>
      
        <option value="85661" >Cross Bayou Canal near Hwy 61 - North of Drainage Control Str (85661)</option>
      
        <option value="85660" >Cross Bayou Canal near Hwy 61 - South of Drainage Control Str (85660)</option>
      
        <option value="CRS" >Cross Creek</option>
      
        <option value="CRWI4" >Crow Creek at Bettendorf, IA</option>
      
        <option value="BERA1" >Cullman Gage for Duck River near Berlin, AL</option>
      
        <option value="BBVK2" >Cumberland River at Barbourville, KY</option>
      
        <option value="BARK2" >Cumberland River at Barkley Dam, KY</option>
      
        <option value="BRKK2" >Cumberland River at Burkesville, KY</option>
      
        <option value="CTHT1" >Cumberland River at Carthage, TN</option>
      
        <option value="CLAT1" >Cumberland River at Celina, TN</option>
      
        <option value="CHET1" >Cumberland River at Cheatham Dam, TN</option>
      
        <option value="CKVT1" >Cumberland River at Clarksville, TN</option>
      
        <option value="CFAK2" >Cumberland River at Cumberland Falls, KY</option>
      
        <option value="DOVT1" >Cumberland River at Dover, TN</option>
      
        <option value="HNTT1" >Cumberland River at Hunters Point, TN</option>
      
        <option value="OHIT1" >Cumberland River at Old Hickory Dam TW, TN</option>
      
        <option value="PENT1" >Cumberland River at Penitentiary Branch, TN</option>
      
        <option value="PVLK2" >Cumberland River at Pine St Br at Pineville, KY</option>
      
        <option value="RWNK2" >Cumberland River at Rowena, KY</option>
      
        <option value="NAST1" >Cumberland River at Shelby St Bridge at Nashville, TN</option>
      
        <option value="WLBK2" >Cumberland River at Williamsburg, KY</option>
      
        <option value="LYLK2" >Cumberland River near Harlan, KY</option>
      
        <option value="PA11" >Cunningham Lake (Papio Dam site #11)</option>
      
        <option value="DNZM7" >Current River at Doniphan</option>
      
        <option value="VNBM7" >Current River at Van Buren</option>
      
        <option value="0DD17" >DD17 Pumping Station Inlet Near Half Moon, AR</option>
      
        <option value="DVPV2" >Davenport, VA (DAVQ4)</option>
      
        <option value="CE3DE436" >Deep Bayou @ Grady, AR</option>
      
        <option value="PCBO1" >Deer Creek (below Dam) near Pancoastburg, OH (DCSOF)</option>
      
        <option value="DCRO1" >Deer Creek Reservoir near Pancoastburg, OH (DCSG2)</option>
      
        <option value="MSTO1" >Deer Creek at Mt. Sterling, OH (MTSF2)</option>
      
        <option value="WMSO1" >Deer Creek at Williamsport, OH (WMTH2)</option>
      
        <option value="TOLI4" >Deer Creek near Toledo, IA</option>
      
        <option value="DCWO1" >Delaware Lake near Delaware, OH (DDOD2)</option>
      
        <option value="MSCK1" >Delaware River near Muscotah, KS</option>
      
        <option value="DESN8" >Des Lacs River near Foxholm, ND - USGS Station No. 05116500</option>
      
        <option value="DESI4" >Des Moines River Below Raccoon River at Des Moines, IA</option>
      
        <option value="DMOI4" >Des Moines River at 2nd Ave Des Moines, IA</option>
      
        <option value="BONI4" >Des Moines River at Bonaparte,IA</option>
      
        <option value="CHLI4" >Des Moines River at Chilicothe,IA</option>
      
        <option value="FRMI4" >Des Moines River at Farmington,IA</option>
      
        <option value="FODI4" >Des Moines River at Fort Dodge, IA </option>
      
        <option value="GRNI4" >Des Moines River at Granger,IA</option>
      
        <option value="KEQI4" >Des Moines River at Keosauqua, IA </option>
      
        <option value="OTMI4" >Des Moines River at Ottumwa, IA </option>
      
        <option value="SFLM7" >Des Moines River at St. Francisville, MO </option>
      
        <option value="RRDI4" >Des Moines River downstream of Lake Red Rock Reservoir</option>
      
        <option value="SDTI4" >Des Moines River downstream of Saylorville Lake Reservoir</option>
      
        <option value="EDYI4" >Des Moines River near Eddyville, IA </option>
      
        <option value="STRI4" >Des Moines River near Stratford, IA</option>
      
        <option value="SWNI4" >Des Moines River near Swan, IA</option>
      
        <option value="TRCI4" >Des Moines River near Tracy, IA </option>
      
        <option value="RVRI2" >Des Plaines River at Riverside, IL </option>
      
        <option value="JRSI2" >Des Plaines River at Ruby Street Bridge at Joliet, IL</option>
      
        <option value="RUSI2" >Des Plaines River at Russell, IL</option>
      
        <option value="DSPI2" >Des Plaines River near Des Plaines, IL</option>
      
        <option value="GUNI2" >Des Plaines River near Gurnee, IL</option>
      
        <option value="DWYK2" >Dewey Lake near Van Lear, KY (DWJO3)</option>
      
        <option value="DLFO1" >Dillon Lake near Zanesville, OH (DILF4)</option>
      
        <option value="SFODS" >Ditch 60 Gage Near Marked Tree, AR (West)</option>
      
        <option value="BL110" >Ditch 81 Ext. (Upstream of Big Lake Northend CS--Above Trash Rack (BL110))</option>
      
        <option value="BL111" >Ditch 81 Ext. (Upstream of Big Lake Northend CS-BL111), Near Manila, AR</option>
      
        <option value="BL112" >Ditch 81 Ext.(Downstream of Big Lake Northend Control Structure) Near Manila, AR</option>
      
        <option value="CE4971C2" >Ditch Bayou Dam Nr. Lake Village, AR (Lake Chicot)</option>
      
        <option value="03285000" >Dix River near Danville</option>
      
        <option value="DOBM5" >Dobbins Creek at Austin,MN</option>
      
        <option value="POTN6" >Dodge Creek at Portville, NY (PTVN)</option>
      
        <option value="DNGP1" >Donegal, PA (DGLP)</option>
      
        <option value="DVRO1" >Dover Lake at Dover, OH (DOTC6)</option>
      
        <option value="03314000" >Drakes Creek near Alvaton</option>
      
        <option value="LCV" >Dry Creek near Lemoncove</option>
      
        <option value="HENW2" >Dry Fork River at Hendricks, WV (DFKW)</option>
      
        <option value="BRSW2" >Dry Fork at Beartown (Bradshaw), WV (BRAP5)</option>
      
        <option value="SORI2" >Du Page River at Shorewood, IL </option>
      
        <option value="DCK" >Duck Creek</option>
      
        <option value="DUC" >Duck Creek Diversion</option>
      
        <option value="DKII4" >Duck Creek at DC Golf Course at Davenport, IA</option>
      
        <option value="SNPP1" >Dunkard Creek at Shannopin, PA. (SPNP)</option>
      
        <option value="WLTA4" >Dutch Creek at Waltreak</option>
      
        <option value="PHAO1" >Eagle Creek at Phalanx Station, OH (EGLO)</option>
      
        <option value="GHDP1" >East Branch Clarion River Lake Outflow, PA (EBOP)</option>
      
        <option value="EBRP1" >East Branch Clarion River Lake, PA (EBRP)</option>
      
        <option value="BOLI2" >East Branch Du Page River at Bolingbrook, IL</option>
      
        <option value="BCHW3" >East Branch Pecatonica River near Blanchardville, WI</option>
      
        <option value="88800" >East Cote Blanche Bay at Luke's Landing (88800)</option>
      
        <option value="DAKI4" >East Fork Des Moines River at Dakota City, IA </option>
      
        <option value="03247041" >East Fork Little Miami River at Harsha Lake TW</option>
      
        <option value="03247500" >East Fork Little Miami River at Perintown</option>
      
        <option value="JAGT1" >East Fork Obey River near Jamestown, TN</option>
      
        <option value="LAST1" >East Fork Stones River near Lascassas, TN</option>
      
        <option value="03276000" >East Fork Whitewater River at Brookville </option>
      
        <option value="ELSW2" >East Fork of Twelvepole (Below Dam) near East Lynn, WV (ELTOF)</option>
      
        <option value="DUNW2" >East Fork of Twelvepole Creek near Dunlow, WV (DUNM4)</option>
      
        <option value="ELYW2" >East Lynn Lake near East Lynn, WV (ELTM4)</option>
      
        <option value="EPLO1" >East Palestine, OH (EAPO)</option>
      
        <option value="ERHW2" >East Rainelle, WV (RANN7)</option>
      
        <option value="SVPDD" >Eau Galle Dam and Reservoir</option>
      
        <option value="SVPW3" >Eau Galle Dam at Spring Valley, WI</option>
      
        <option value="SPRW3" >Eau Galle Tailwater at Spring Valley, WI - USGS Station No. 05370000</option>
      
        <option value="EBEP1" >Ebensburg, PA (STP) (EBNP)</option>
      
        <option value="NWBI2" >Edwards River near New Boston,IL </option>
      
        <option value="ORII2" >Edwards River near Orion, IL</option>
      
        <option value="03360000" >Eel  River at Bowling Green</option>
      
        <option value="03328500" >Eel River near Logansport(Adamsboro)</option>
      
        <option value="EPGM7" >Eleven Point River near Bardley</option>
      
        <option value="RVSA4" >Eleven Point River near Ravenden Springs</option>
      
        <option value="ELKO" >Elk Creek near Trail</option>
      
        <option value="QUSW2" >Elk River at Queen Shoals, WV (QSEL6)</option>
      
        <option value="SUTW2" >Elk River at Sutton Lake, WV (SUEK7)</option>
      
        <option value="WEBW2" >Elk River below Webster Springs, WV (WBEK8)</option>
      
        <option value="CLYW2" >Elk River near Clay, WV (CYEL6)</option>
      
        <option value="FRMW2" >Elk River near Frametown, WV (FREK7)</option>
      
        <option value="SUSW2" >Elk River near Sutton Lake (Tailwater), WV (SUEOF)</option>
      
        <option value="PENI2" >Elkhorn Creek near Penrose, IL</option>
      
        <option value="KECI4" >English Creek near Knoxville, IA </option>
      
        <option value="KALI4" >English River at Kalona, IA</option>
      
        <option value="CE02442C" >FWRS LAKE 30</option>
      
        <option value="CE02575A" >FWRS LAKE 38</option>
      
        <option value="CE0262C0" >FWRS LAKE 47</option>
      
        <option value="CE0271B6" >FWRS LAKE 52</option>
      
        <option value="FMDI2" >Farm Creek at Farmdale, IL</option>
      
        <option value="FTLK2" >Fishtrap Lake near Shelbiana, KY (FRLP4)</option>
      
        <option value="HRMM5" >Five Mile Creek near Herman, MN</option>
      
        <option value="FTGV2" >Flat Gap near Pound, VA (FLGQ4)</option>
      
        <option value="16876222" >Flat River @ Shed Road</option>
      
        <option value="FLW" >Flowers Mountain Weather</option>
      
        <option value="FDCI2" >Fondulac Creek near East Peoria, IL</option>
      
        <option value="CE7F4C34" >Fool River Pumping Plant (landside)</option>
      
        <option value="CZ7F4C34" >Fool River Pumping Plant (riverside)</option>
      
        <option value="FTH" >Foothill Ditch</option>
      
        <option value="FNSP1" >Fort Necessity, PA (FNCP)</option>
      
        <option value="APLA4" >Fourche LaFave River at Aplin</option>
      
        <option value="HUSA4" >Fourche LaFave River at Houston</option>
      
        <option value="NMBA4" >Fourche LaFave River at Nimrod Dam - TW</option>
      
        <option value="NMLA4" >Fourche LaFave River at Nimrod Dam -HW</option>
      
        <option value="GRVA4" >Fourche LaFave River near Gravelly</option>
      
        <option value="DFMI4" >Fourmile Creek at Des Moines, IA</option>
      
        <option value="ALGI2" >Fox River at Algonquin, IL</option>
      
        <option value="DAYI2" >Fox River at Dayton, IL </option>
      
        <option value="MNGI2" >Fox River at Montgomery, IL</option>
      
        <option value="NMSW3" >Fox River near New Munster, WI</option>
      
        <option value="WYLM7" >Fox River near Wayland,MO </option>
      
        <option value="FRKN6" >Franklinville, NY (FRKN)</option>
      
        <option value="FDMP1" >Freedom, PA  (Cranberry STP) (FDMP)</option>
      
        <option value="CBSP1" >French Creek at Cambridge Springs, PA (CBSP)</option>
      
        <option value="MEDP1" >French Creek at Meadville, PA (MEDP)</option>
      
        <option value="UTCP1" >French Creek at Utica, PA (UTIP)</option>
      
        <option value="WTTP1" >French Creek near Wattsburg, PA (WTTP)</option>
      
        <option value="76592" >Freshwater Canal at Freshwater Bayou Lock - North (76592)</option>
      
        <option value="76593" >Freshwater Canal at Freshwater Bayou Lock - South (76593)</option>
      
        <option value="RDYA4" >Frog Bayou at Rudy</option>
      
        <option value="76560" >GIWW at Bayou Sale Ridge (76560)</option>
      
        <option value="76320" >GIWW at Houma (76320)</option>
      
        <option value="76260" >GIWW at West Closure Complex (76260)</option>
      
        <option value="GSML1" >GIWW at mile 103 South of Morgan City (USGS/COE)</option>
      
        <option value="76040" >GIWW near Paris Road Bridge (76040)</option>
      
        <option value="BUNW3" >Galena River at Buncombe, WI </option>
      
        <option value="GAIO1" >Galion, OH (GALC3)</option>
      
        <option value="GRVO1" >Garrettsville, OH (WTP) (GARO)</option>
      
        <option value="GRYW2" >Gary, WV (GRYP5)</option>
      
        <option value="JRMM7" >Gasconade River at Jerome, MO</option>
      
        <option value="RIFM7" >Gasconade River near Rich Fountain, MO</option>
      
        <option value="BVAW2" >Gauley River above Belva, WV (BEGM6)</option>
      
        <option value="COGW2" >Gauley River at Camden on Gauley, WV (CMDL7)</option>
      
        <option value="SUMW2" >Gauley River below Summersville Lake (Tailwater), WV (SUGOF)</option>
      
        <option value="CRAW2" >Gauley River near Craigsville, WV (CVGL7)</option>
      
        <option value="AVON6" >Genesee River at Avon, NY</option>
      
        <option value="BLBN6" >Genesee River at Ballantyne Bridge near Mortimer, NY</option>
      
        <option value="JONN6" >Genesee River at Jones Bridge near Mt. Morris, NY</option>
      
        <option value="PRTN6" >Genesee River at Portageville, NY</option>
      
        <option value="WELN6" >Genesee River at Wellsville, NY</option>
      
        <option value="GNF" >Giant Forest Weather</option>
      
        <option value="GLOO2" >Glover Creek near Glover</option>
      
        <option value="82250" >Golden Meadow Floodgate (North) (82250)</option>
      
        <option value="82260" >Golden Meadow Floodgate (South) (82260)</option>
      
        <option value="WR122" >Graham Burke Pumping Station (Little Island Bayou Inlet) Near Mellwood, AR</option>
      
        <option value="WR123" >Graham Burke Pumping Station (Little Island Bayou Outlet) Near Mellwood, AR</option>
      
        <option value="BTNW3" >Grant River near Burton,WI</option>
      
        <option value="GRAK2" >Grayson Lake near Grayson, KY (GRLL3)</option>
      
        <option value="GRYP1" >Graysville, PA (GRVP)</option>
      
        <option value="03271601" >Great Miami River Below Miamisburg</option>
      
        <option value="03270500" >Great Miami River at Dayton</option>
      
        <option value="03274000" >Great Miami River at Hamilton</option>
      
        <option value="03271500" >Great Miami River at Miamisburg</option>
      
        <option value="03272100" >Great Miami River at Middletown</option>
      
        <option value="GRLK2" >Green River Lake, KY</option>
      
        <option value="GPUW" >Green River Near Palmer, WA</option>
      
        <option value="03306500" >Green River at Greensburg</option>
      
        <option value="03319885" >Green River at Livermore </option>
      
        <option value="03320000" >Green River at Lock 2 at Calhoun </option>
      
        <option value="03315500" >Green River at Lock 4 at Woodbury</option>
      
        <option value="03311500" >Green River at Lock 6 at Brownsville </option>
      
        <option value="03308500" >Green River at Munfordville</option>
      
        <option value="03316645" >Green River at Rockport </option>
      
        <option value="HAHW" >Green River downstream of Howard Hanson Dam </option>
      
        <option value="AUBW" >Green River near Auburn, WA</option>
      
        <option value="03306000" >Green River near Campbellsville</option>
      
        <option value="GENI2" >Green River near Geneseo, IL </option>
      
        <option value="ALDW2" >Greenbrier River at Alderson, WV (ALDO7)</option>
      
        <option value="BUCW2" >Greenbrier River at Buckeye, WV (BUGM8)</option>
      
        <option value="HLLW2" >Greenbrier River at Hilldale near Talcott, WV (HDGO7)</option>
      
        <option value="GRVP1" >Greenville, PA (WTP) (GVLP)</option>
      
        <option value="GLLM5" >Gull Lake Dam near Brainerd, MN</option>
      
        <option value="GLKM5" >Gull Lake Elevation near Brainerd, MN</option>
      
        <option value="BRAW2" >Guyandotte River at Branchland (BHLM4)</option>
      
        <option value="RDBW2" >Guyandotte River below R. D. Bailey Dam near Hanover, WV (RDBOF)</option>
      
        <option value="BAIW2" >Guyandotte River near Baileysville, WV (BAGO5)</option>
      
        <option value="LOGW2" >Guyandotte River near Logan, WV (LGNN5)</option>
      
        <option value="MNAW2" >Guyandotte River near Man, WV (MANO5)</option>
      
        <option value="GUYP1" >Guys Mills, PA (GMLP)</option>
      
        <option value="TKZM7" >H.S. TRUMAN DAM AND RESERVOIR AT WARSAW MO</option>
      
        <option value="CE7F5F42" >Ha Ha Bayou Drainage Structure (landside)</option>
      
        <option value="CZ7F5F42" >Ha Ha Bayou Drainage Structure (riverside)</option>
      
        <option value="BELT1" >Harpeth River at Bellevue, TN</option>
      
        <option value="FRAT1" >Harpeth River at Franklin, TN</option>
      
        <option value="KINT1" >Harpeth River near Kingston Springs, TN</option>
      
        <option value="HRTW2" >Harts, WV (HARM4)</option>
      
        <option value="76220" >Harvey Canal Sector Gates (North/Protected Side) nr Lapalco Blvd (76220)</option>
      
        <option value="76230" >Harvey Canal at Boomtown Casino (76230)</option>
      
        <option value="76200" >Harvey Lock at GIWW (76200)</option>
      
        <option value="HA113" >Hatchie River At Pocahontas, TN (Northwest)</option>
      
        <option value="HA116" >Hatchie River At Rialto, TN</option>
      
        <option value="HABRN" >Hatchie River at Brownsville, TN</option>
      
        <option value="OQUI2" >Henderson River near Oquawka,IL </option>
      
        <option value="JHCI2" >Hickory Creek at Joliet, IL</option>
      
        <option value="MILDD" >Highway 40 Bridge</option>
      
        <option value="ODADD" >Highway 75 Dam</option>
      
        <option value="ODAM5" >Highway 75 Dam near Odessa, MN</option>
      
        <option value="HSPO1" >Hillsboro, OH (HILI1)</option>
      
        <option value="03252300" >Hinkston Creek nr Carlise</option>
      
        <option value="HCK" >Hockett Meadow Weather</option>
      
        <option value="ATHO1" >Hocking River at Athens, OH (ADHH4)</option>
      
        <option value="ENTO1" >Hocking River at Enterprise, OH (ENTG4)</option>
      
        <option value="SC17" >Holmes Lake (Salt Creek Dam site #17)</option>
      
        <option value="HOSP1" >Holsopple, PA (HOLP)</option>
      
        <option value="HOMDD" >Homme Dam</option>
      
        <option value="HOMN8" >Homme Dam Pool near Park River, ND</option>
      
        <option value="HNYN6" >Honeoye Creek at Honeoye Falls, NY</option>
      
        <option value="HAH" >Howard Hanson Dam </option>
      
        <option value="HDDW2" >Hundred, WV (HNDW)</option>
      
        <option value="HTNW2" >Hutton's Knob, WV (HUTW)</option>
      
        <option value="76030" >IHNC Surge Barrier East / Flood Side (76030)</option>
      
        <option value="76032" >IHNC Surge Barrier West / Protected Side  (76032)</option>
      
        <option value="76880" >IWW at Calcasieu Lock - East (76880)</option>
      
        <option value="76960" >IWW at Calcasieu Lock -West (76960)</option>
      
        <option value="76720" >IWW at Leland Bowman Lock - East (76720)</option>
      
        <option value="76800" >IWW at Leland Bowman Lock - West (76800)</option>
      
        <option value="STVA4" >Illinois Bayou near Scottsville</option>
      
        <option value="BEAI2" >Illinois River at Beardstown,IL </option>
      
        <option value="IL03" >Illinois River at Brandon Road Lock and Dam</option>
      
        <option value="JOLI2" >Illinois River at Brandon Road Lock and Dam (MET Station)</option>
      
        <option value="IL04" >Illinois River at Dresden Island Lock and Dam</option>
      
        <option value="DRSI2" >Illinois River at Dresden Island Lock and Dam (MET Station)</option>
      
        <option value="IL02" >Illinois River at Lockport Lock and Dam</option>
      
        <option value="LOKI2" >Illinois River at Lockport Lock and Dam (MET Station)</option>
      
        <option value="IL05" >Illinois River at Marseilles Lock and Dam </option>
      
        <option value="MMOI2" >Illinois River at Marseilles Lock and Dam (MET Station)</option>
      
        <option value="MRSI2" >Illinois River at Marseilles,IL</option>
      
        <option value="IL08" >Illinois River at New LaGrange Lock and Dam</option>
      
        <option value="NLGI2" >Illinois River at New LaGrange Lock and Dam (MET Station)</option>
      
        <option value="IL01" >Illinois River at O'Brien Lock and Dam</option>
      
        <option value="OBII2" >Illinois River at O'Brien Lock and Dam (MET Station)</option>
      
        <option value="OTWI2" >Illinois River at Ottawa, IL</option>
      
        <option value="OTTI2" >Illinois River at Ottawa,IL</option>
      
        <option value="IL07" >Illinois River at Peoria Lock and Dam</option>
      
        <option value="PRAI2" >Illinois River at Peoria Lock and Dam (MET Station)</option>
      
        <option value="PIAI2" >Illinois River at Peoria,IL </option>
      
        <option value="SPVI2" >Illinois River at Spring Valley,IL</option>
      
        <option value="IL06" >Illinois River at Starved Rock Lock and Dam</option>
      
        <option value="SRDI2" >Illinois River at Starved Rock Lock and Dam (MET Station)</option>
      
        <option value="VALI2" >Illinois River at Valley City, IL</option>
      
        <option value="COPI2" >Illinois River near Copperas Creek,IL </option>
      
        <option value="HAVI2" >Illinois River near Havana,IL </option>
      
        <option value="HNYI2" >Illinois River near Henry,IL </option>
      
        <option value="KNGI2" >Illinois River near Kingston Mines,IL </option>
      
        <option value="LSLI2" >Illinois River near La Salle,IL </option>
      
        <option value="MORI2" >Illinois River near Morris,IL </option>
      
        <option value="MGOI4" >Indian Creek near Mingo, IA</option>
      
        <option value="WYGI2" >Indian Creek near Wyoming, IL</option>
      
        <option value="ATLO1" >Indian Fork at Atwood Dam near New Cumberland, OH (ATIC6)</option>
      
        <option value="INVP" >Indian Valley Reservoir Pool</option>
      
        <option value="INIP1" >Indiana, PA (WTP) (IDIP)</option>
      
        <option value="76160" >Inner Harbor Navigation Canal (IHNC Lock) New Orleans (76160)</option>
      
        <option value="CJTI4" >Iowa River at Columbus Junction, IA</option>
      
        <option value="TMAI4" >Iowa River at County Highway E49 near Tama, IA</option>
      
        <option value="IOWI4" >Iowa River at Iowa City, IA</option>
      
        <option value="MROI4" >Iowa River at Marengo, IA</option>
      
        <option value="MIWI4" >Iowa River at Marshalltown, IA</option>
      
        <option value="OKVI4" >Iowa River at Oakville, IA</option>
      
        <option value="STBI4" >Iowa River at Steamboat Rock, IA</option>
      
        <option value="WAPI4" >Iowa River at Wapello, IA</option>
      
        <option value="CTWI4" >Iowa River directly downstream of Coralville Lake Reservoir</option>
      
        <option value="BPLI4" >Iowa River near Belle Plaine, IA</option>
      
        <option value="LNTI4" >Iowa River near Lone Tree, IA</option>
      
        <option value="ROWI4" >Iowa River near Rowan, IA</option>
      
        <option value="TAMI4" >Iowa River near Tama, IA</option>
      
        <option value="IRQI2" >Iroquois River at Iroquois, IL</option>
      
        <option value="CHBI2" >Iroquois River near Chebanse, IL</option>
      
        <option value="ISBW" >Isabella Lake Weather</option>
      
        <option value="HUNI3" >J Edward Roush Lake</option>
      
        <option value="EMCM7" >Jacks Fork at Eminence</option>
      
        <option value="GLNM7" >James River at Galena</option>
      
        <option value="JENP1" >Jeannette, PA (JNNP)</option>
      
        <option value="JECK1" >Jeffery Energy Center on Kansas River near Belvue, KS</option>
      
        <option value="JNCT1" >Jennings Creek near Whitleyville, TN</option>
      
        <option value="JOBW2" >Job's Knob near Clearco, WV (JOKM7)</option>
      
        <option value="HYSV2" >John W. Flannagan Lake near Haysi, VA (JFPQ4)</option>
      
        <option value="VLRK2" >John's Creek below Dewey Lake near Van Lear, KY (DWJOF)</option>
      
        <option value="MTGK2" >John's Creek near Meta, KY (METO4)</option>
      
        <option value="DNKP1" >Jollytown, PA (DNKP)</option>
      
        <option value="CHAW2" >Kanawha River at Charleston (Old Lock 6), WV (CLKL5)</option>
      
        <option value="CRRW2" >Kanawha River at Charleston (SS) Railroad Bridge, WV (CHKL5)</option>
      
        <option value="KANW2" >Kanawha River at Kanawha Falls, WV (KFKM6)</option>
      
        <option value="LONW2" >Kanawha River at London L&D, WV (LONW2)</option>
      
        <option value="MMTW2" >Kanawha River at Marmet L&D near Belle, WV (MMKL5)</option>
      
        <option value="WINW2" >Kanawha River at Winfield L&D, WV (WMFK5)</option>
      
        <option value="DAVI3" >Kankakee River at Davis, IN</option>
      
        <option value="DBRI3" >Kankakee River at Dunns Bridge, IN</option>
      
        <option value="MOMI2" >Kankakee River at Momence, IL </option>
      
        <option value="SLBI3" >Kankakee River at Shelby, IN </option>
      
        <option value="KTSI3" >Kankakee River near Kouts, IN</option>
      
        <option value="WLMI2" >Kankakee River near Wilmington, IL </option>
      
        <option value="KCKK1" >Kansas River at 23rd St. in Kansas City, KS</option>
      
        <option value="DSOK1" >Kansas River at DeSoto, KS</option>
      
        <option value="FTRK1" >Kansas River at Fort Riley, KS</option>
      
        <option value="LCPK1" >Kansas River at Lecompton, KS</option>
      
        <option value="MHKK1" >Kansas River at Manhattan, KS</option>
      
        <option value="MAPK1" >Kansas River at Maple Hill, KS</option>
      
        <option value="STMK1" >Kansas River at Saint Marys, KS</option>
      
        <option value="TPAK1" >Kansas River at Topeka, KS</option>
      
        <option value="WMGK1" >Kansas River at Wamego, KS</option>
      
        <option value="BVUK1" >Kansas River near Belvue, KS</option>
      
        <option value="TRR" >Kaweaha River at Three Rivers</option>
      
        <option value="MK2" >Kaweaha River below McKay Pt Diversion</option>
      
        <option value="03615" >Keelboat Pass below Lake Chicot (03615)</option>
      
        <option value="03284000" >Kentucky River at Lock 10 near Winchester</option>
      
        <option value="03282000" >Kentucky River at Lock 14 at Heidelberg</option>
      
        <option value="03290500" >Kentucky River at Lock 2 at Lockport</option>
      
        <option value="03290080" >Kentucky River at Lock 3 at Gest </option>
      
        <option value="03287500" >Kentucky River at Lock 4 at Frankfort</option>
      
        <option value="03287250" >Kentucky River at Lock 5 near Tyrone </option>
      
        <option value="03287000" >Kentucky River at Lock 6 near Salvisa</option>
      
        <option value="03286500" >Kentucky River at Lock 7 near High Bridge </option>
      
        <option value="KRN" >Kern River @ Kernville</option>
      
        <option value="ISBQ" >Kern River bl Isabella Dam</option>
      
        <option value="WAYI2" >Kickapoo Creek at Waynesville,IL</option>
      
        <option value="STEW3" >Kickapoo River at Steuben, WI - USGS Station No. 05410490</option>
      
        <option value="KILO1" >Killbuck Creek at Killbuck, OH (KIKC5)</option>
      
        <option value="BRYA4" >Kings River near Berryville</option>
      
        <option value="GUFP1" >Kinzua Creek at Guffey, PA (GUFP)</option>
      
        <option value="KIZP1" >Kinzua Dam Outflow, PA (KZOP)</option>
      
        <option value="BVDI2" >Kishwaukee River at Belvidere, IL</option>
      
        <option value="PRYI2" >Kishwaukee River near Perryville, IL</option>
      
        <option value="VGFP1" >Kiskiminetas River at Vandergrift, PA (VGFP)</option>
      
        <option value="KNUM5" >Knutson Dam near Cass Lake, MN</option>
      
        <option value="KNUDD" >Knutson Dam-Cass Lake</option>
      
        <option value="MVEO1" >Kokosing River at Mount Vernon, OH (MTVD4)</option>
      
        <option value="KOPW2" >Kopperston, WV (KOPN5)</option>
      
        <option value="LA111" >L'Anguille River At Palestine, AR</option>
      
        <option value="LA112" >L'Anguille River Near Marianna, AR (Northeast)</option>
      
        <option value="RIPI2" >LaMoine River at Ripley, IL </option>
      
        <option value="CLMI2" >LaMoine River near Colmar, IL </option>
      
        <option value="LQRDD" >Lac Qui Parle Reservoir</option>
      
        <option value="MILM5" >Lac Qui Parle Reservoir at Hwy 40 Bridge west of Milan, MN</option>
      
        <option value="LQRM5" >Lac Qui Parle Reservoir near Watson, MN</option>
      
        <option value="LQPM5" >Lac Qui Parle River near Lac Qui Parle, MN</option>
      
        <option value="82730" >Lake Cataouatche Pumping Station, LA (Headwater) (82730)</option>
      
        <option value="CE7F79AE" >Lake Chicot Pumping Plant (landside), AR</option>
      
        <option value="CE504B48" >Lake Chicot Pumping Plant (riverside), AR</option>
      
        <option value="DARN8" >Lake Darling near Foxholm, ND - USGS Station No. 05115500</option>
      
        <option value="MCHO1" >Lake Fork below Mohicanville Dam near Mohicanville, OH (MOLOF)</option>
      
        <option value="CLFI2" >Lake Fork near Cornland, IL</option>
      
        <option value="ISBP" >Lake Isabella Pool</option>
      
        <option value="GPOM5" >Lake Kabetogama at Gold Portage, MN - USGS Station No. 05129290</option>
      
        <option value="NVLW3" >Lake Koshkonong near Newville, WI</option>
      
        <option value="NWTO1" >Lake Milton, OH (MLTO)</option>
      
        <option value="52750" >Lake Palourde near Morgan City (52750)</option>
      
        <option value="85555" >Lake Pontchartrain at Bonnet Carre Spillway (85555)</option>
      
        <option value="85550" >Lake Pontchartrain at Frenier (85550)</option>
      
        <option value="85670" >Lake Pontchartrain at Lakefront Airport (85670)</option>
      
        <option value="85575" >Lake Pontchartrain at Mandeville (85575)</option>
      
        <option value="85625" >Lake Pontchartrain at West End (85625)</option>
      
        <option value="PELI4" >Lake Red Rock Reservoir</option>
      
        <option value="TRMW" >Lake Terminus Weather</option>
      
        <option value="TRADD" >Lake Traverse Reservoir</option>
      
        <option value="TRAM5" >Lake Traverse at Reservation Dam near Wheaton, MN</option>
      
        <option value="WNBM5" >Lake Winnibigoshish Dam near Bena, MN</option>
      
        <option value="SSIM5" >Lake Woods at Spring Steel Island near Warroad, MN - USGS Station No. 05140521</option>
      
        <option value="CE7F3AA4" >Larto Lake @ Larto Lake</option>
      
        <option value="URSP1" >Laurel Hill Creek at Ursina, PA (URSP)</option>
      
        <option value="CBNK2" >Laurel River near Corbin, KY</option>
      
        <option value="VBRA4" >Lee Creek at Lee Creek Reservoir</option>
      
        <option value="FEDM5" >Leech Lake Dam near Federal Dam, MN</option>
      
        <option value="LLRM5" >Leech Lake River above Mud Lake Dam near Ball Club, MN</option>
      
        <option value="LEEM5" >Leech Lake at Sugar Point near Federal Dam, MN - USGS Station No. 05205900</option>
      
        <option value="LAXO1" >Leesville Lake Auxillary near Leesville, OH (LAXD6)</option>
      
        <option value="LELO1" >Leesville Lake near Leesville, OH (LEMD6)</option>
      
        <option value="RPLW2" >Left Fork of Holly River at Replete, WV (REPK7)</option>
      
        <option value="LMN" >Lemoncove Ditch</option>
      
        <option value="LESW" >Lester Stream Gage</option>
      
        <option value="LECW" >Lester Weather Station</option>
      
        <option value="BIGV2" >Levisa Fork at Big Rock, VA (BRLP4)</option>
      
        <option value="PTVK2" >Levisa Fork at Paintsville, KY (PTLN3)</option>
      
        <option value="PKYK2" >Levisa Fork at Pikeville, KY (PKVP3)</option>
      
        <option value="PSTK2" >Levisa Fork at Prestonsburg, KY (PRLO3)</option>
      
        <option value="MILK2" >Levisa Fork below Fishtrap Dam near Millard near Shelbiana, KY (FRLOF)</option>
      
        <option value="03253500" >Licking River at Catawba</option>
      
        <option value="03249500" >Licking River at Cave Run Lake Tail water</option>
      
        <option value="03249505" >Licking River at Farmers</option>
      
        <option value="03251500" >Licking River at McKinneyburg</option>
      
        <option value="DLLO1" >Licking River below Dillon Dam (Tailwater) near Dillon Falls, OH (DILOF)</option>
      
        <option value="NEAO1" >Licking River near Newark, OH (NKLE4)</option>
      
        <option value="03250500" >Licking River nr Blue Lick Springs</option>
      
        <option value="03248300" >Licking River nr Salyersville</option>
      
        <option value="LIGP1" >Ligonier, PA (LIGP)</option>
      
        <option value="LISO1" >Lisbon, OH (LSBO)</option>
      
        <option value="LTHO1" >Lithopolis, OH (LITF3)</option>
      
        <option value="49365" >Little Alabama Bayou at Sherbourne (49365)</option>
      
        <option value="APLO" >Little Applegate near Applegate</option>
      
        <option value="49725" >Little Bayou Sorrel At Junction with GIWW (49725) </option>
      
        <option value="FRBN1" >Little Blue River near Fairbury, NE</option>
      
        <option value="LKCM7" >Little Blue near Lake City, MO</option>
      
        <option value="IONI4" >Little Cedar River near Ionia, IA</option>
      
        <option value="ECMP1" >Little Conemaugh River at East Conemaugh, PA (ECMP)</option>
      
        <option value="LFKM5" >Little Fork River at Little Fork, MN - USGS Station No. 05131500</option>
      
        <option value="FRG" >Little John Creek</option>
      
        <option value="BURW2" >Little Kanawha River at Burnsville, WV (BRNJ7)</option>
      
        <option value="ELZW2" >Little Kanawha River at Elizabeth (Palestine), WV (ELLI6)</option>
      
        <option value="GRTW2" >Little Kanawha River at Grantsville, WV (GRVJ6)</option>
      
        <option value="BULW2" >Little Kanawha River below Burnsville, WV (BUSOF)</option>
      
        <option value="GLEW2" >Little Kanawha River near Glenville, WV (GLVJ7)</option>
      
        <option value="WLDW2" >Little Kanawha River near Wildcat near Falls Mill, WV (WLKK7)</option>
      
        <option value="MCRP1" >Little Mahoning Creek at McCormick, PA (MCRP)</option>
      
        <option value="03245500" >Little Miami River at Milford</option>
      
        <option value="03242050" >Little Miami River at Spring Valley</option>
      
        <option value="CE419844" >Little Missouri River @ Boughton, AR</option>
      
        <option value="DE3FC0AA" >Little Missouri River @ Langley, AR</option>
      
        <option value="CE50583E" >Little Missouri River @ Murfreesboro, AR</option>
      
        <option value="CE40B280" >Little Missouri River @ Narrows Dam, AR</option>
      
        <option value="LMRA4" >Little Piney Creek near Lamar</option>
      
        <option value="SRGA4" >Little Red River Middle Fork at Shirley</option>
      
        <option value="CIGA4" >Little Red River South Fork at Clinton</option>
      
        <option value="GRRA4" >Little Red River at Greers Ferry Dam - HW & TW</option>
      
        <option value="GREDO" >Little Red River at Greers Ferry Dam - WQ</option>
      
        <option value="JUDA4" >Little Red River at Judsonia</option>
      
        <option value="PAGA4" >Little Red River near Pangburn</option>
      
        <option value="17BA8564" >Little River @ Rochelle, LA</option>
      
        <option value="LD111" >Little River Diversion Channel Near Delta, MO</option>
      
        <option value="LD112" >Little River Diversion Channel Near Dutchtown, MO</option>
      
        <option value="AHDA4" >Little River at Millwood Dam - HW</option>
      
        <option value="MWTA4" >Little River at Millwood Dam - TW</option>
      
        <option value="CDZK2" >Little River near Cadiz, KY</option>
      
        <option value="GRYV2" >Little River near Graysontown, VA (GRYR7)</option>
      
        <option value="HRGA4" >Little River near Horatio</option>
      
        <option value="03324000" >Little River near Huntington</option>
      
        <option value="IDBO2" >Little River near Idabel</option>
      
        <option value="GYNK2" >Little Sandy River at Grayson, KY (GRAL3)</option>
      
        <option value="LEOK2" >Little Sandy River at Leon, KY (LEOL3)</option>
      
        <option value="GYLK2" >Little Sandy River below Grayson Dam near Grayson, KY (GRLOF)</option>
      
        <option value="TPLO1" >Little Stillwater Creek below Tappan Dam at Tappan near Deerfield, OH (TALOF)</option>
      
        <option value="CE48B626" >Little Sunflower Control Structure (landside)</option>
      
        <option value="CE4962B4" >Little Sunflower Control Structure (riverside)</option>
      
        <option value="CE4089C8" >Little Tallahatchie River @ Batesville, MS</option>
      
        <option value="CE5E8A3E" >Little Tallahatchie River @ Belmont Bridge, MS</option>
      
        <option value="172856DE" >Little Tallahatchie River @ Etta, MS</option>
      
        <option value="CE4168C0" >Little Tallahatchie River @ Sardis Dam, MS (Intake)</option>
      
        <option value="CE487338" >Little Tallahatchie River @ Sardis Dam, MS (Outlet)</option>
      
        <option value="FLZI4" >Lizard Creek near Fort Dodge, IA </option>
      
        <option value="ELLM7" >Logan Creek at Ellington</option>
      
        <option value="LOOO1" >London (Madison County), OH (LONF2)</option>
      
        <option value="85626" >London Ave Canal 1 - ICS Lake-side (85626)</option>
      
        <option value="85627" >London Ave Canal 2 - ICS Canal-side (85627)</option>
      
        <option value="85628" >London Ave Canal 3 - Leon C Simon Dr (85628)</option>
      
        <option value="85629" >London Ave Canal 4 - Prentiss Ave. (85629)</option>
      
        <option value="85630" >London Ave Canal 5 - Filmore Ave. (85630)</option>
      
        <option value="85631" >London Ave Canal 6 - Mirabeau Ave (85631)</option>
      
        <option value="85632" >London Ave Canal 7 - Harrison Ave. (85632)</option>
      
        <option value="85633" >London Ave Canal 8 - PS3 (85633)</option>
      
        <option value="CE5EC934" >Long Branch Drainage Structure (landside)</option>
      
        <option value="CE4883BC" >Long Branch Drainage Structure (riverside)</option>
      
        <option value="DNRA4" >Long Creek at Denver</option>
      
        <option value="LNZM7" >Longview Lake at Kansas City, MO</option>
      
        <option value="LE111" >Loosahatchie River Near Brunswick, TN (North)</option>
      
        <option value="LE110" >Loosahatchie River Near Frayser, TN</option>
      
        <option value="LE113" >Loosahatchie River Near Somerville, TN</option>
      
        <option value="LOS" >Lost Creek Reservoir</option>
      
        <option value="03780" >Lower Atchafalaya River at Morgan City (03780)</option>
      
        <option value="MRGL1" >Lower Atchafalaya River at Morgan City (USGS)  </option>
      
        <option value="HIAO" >Lower Hinton Creek near Heppner</option>
      
        <option value="LSAF" >Lower St Anthony Falls at Minneapolis, MN</option>
      
        <option value="KINP1" >Loyalhanna Creek at Kingston, PA (KNGP)</option>
      
        <option value="LATP1" >Loyalhanna Creek at Latrobe, PA (LATP)</option>
      
        <option value="LHDP1" >Loyalhanna Lake Outflow, PA (LYOP)</option>
      
        <option value="LYLP1" >Loyalhanna Lake, PA (LOYP)</option>
      
        <option value="CORK2" >Lynn Camp Creek near Corbin, KY</option>
      
        <option value="CNGI2" >Mackinaw River near Congerville,IL </option>
      
        <option value="GNVI2" >Mackinaw River near Green Valley, IL </option>
      
        <option value="CE497F10" >Macon Lake Nr. Macon Lake, AR</option>
      
        <option value="03267900" >Mad River at Eagle City</option>
      
        <option value="MGLO1" >Magnolia Levee, OH (MASC6)</option>
      
        <option value="MGN" >Magoon Weather</option>
      
        <option value="MHDP1" >Mahoning Creek Lake Outflow, PA (MNOP)</option>
      
        <option value="MHGP1" >Mahoning Creek Lake, PA (MAHP)</option>
      
        <option value="PXSP1" >Mahoning Creek at Punxsutawney, PA (PNXP)</option>
      
        <option value="ALLO1" >Mahoning River at Alliance, OH (ALLO)</option>
      
        <option value="LEAO1" >Mahoning River at Leavittsburg, OH (LEVO)</option>
      
        <option value="LLWO1" >Mahoning River at Lowellville, OH (LWLO)</option>
      
        <option value="PRIO1" >Mahoning River at Pricetown, OH (PRIO)</option>
      
        <option value="YGWO1" >Mahoning River at Youngstown, OH (YOUO)</option>
      
        <option value="CE5EF27C" >Main Canal @ Greenville, MS (Reed Road)</option>
      
        <option value="CE508084" >Main Canal @ Longwood, MS</option>
      
        <option value="MNGW2" >Mannington, WV (MANW)</option>
      
        <option value="MCHI4" >Maquoketa River at Manchester, IA</option>
      
        <option value="MAQI4" >Maquoketa River near Maquoketa, IA </option>
      
        <option value="MNCP1" >Marion Center, PA (MARP)</option>
      
        <option value="MARQ" >Mariposa Creek</option>
      
        <option value="MARP" >Mariposa Creek Reservoir Pool</option>
      
        <option value="MLDDD" >Marsh Lake Dam</option>
      
        <option value="MLDM5" >Marsh Lake Dam near Appleton, MN</option>
      
        <option value="MLD" >Marsh Lake Dam near Appleton, MN - Pool gage</option>
      
        <option value="MFLK2" >Martins Fork River at Martins Fork Dam HW, KY</option>
      
        <option value="MNLK2" >Martins Fork River at Martins Fork Dam TW, KY</option>
      
        <option value="MRTQ" >Martis Reservoir Outflow</option>
      
        <option value="MRTP" >Martis Reservoir Pool</option>
      
        <option value="03241500" >Massies Creek at Wilberforce</option>
      
        <option value="MYVN6" >Mayville, NY (STP) (MAYN)</option>
      
        <option value="COLI2" >Mazon River near Coal City,IL </option>
      
        <option value="LVLO1" >McGuire Creek below Leesville Dam near Leesville, OH (LEMOF)</option>
      
        <option value="CE5E7468" >McKinney Bayou Pumping Plant</option>
      
        <option value="MTLW2" >Meadow River near Mount Lookout, WV (MTMM7)</option>
      
        <option value="MRGP1" >Mercer, PA (MERP)</option>
      
        <option value="70900" >Mermentau River at Grand Chenieer (70900)</option>
      
        <option value="70600" >Mermentau River at Lacassine Refuge (ID 70600)</option>
      
        <option value="MYDP1" >Meyersdale, PA (MYRP)</option>
      
        <option value="KITO1" >Michael J Kirwan Dam Outflow, OH (MKOO)</option>
      
        <option value="KIRO1" >Michael J Kirwan Reservoir, OH (MJKO)</option>
      
        <option value="FM106" >Middle Fork Forked Deer Near Humboldt, TN</option>
      
        <option value="FM104" >Middle Fork Forked Deer River Near Eaton, TN (South)</option>
      
        <option value="FM111" >Middle Fork Forked Deer River Near Oakfield, TN (North)</option>
      
        <option value="03281000" >Middle Fork Kentucky River at Tallega</option>
      
        <option value="03280600" >Middle Fork Kentucky River near Hyden</option>
      
        <option value="OM111" >Middle Fork Of Obion River Near Dresden, TN (Southeast)</option>
      
        <option value="ADRW2" >Middle Fork River at Audra, WV (AUDW)</option>
      
        <option value="PANI4" >Middle Raccoon River at Panora, IA</option>
      
        <option value="BAYI4" >Middle Raccoon River near Bayard, IA</option>
      
        <option value="IDNI4" >Middle River near Indianola, IA </option>
      
        <option value="03381495" >Middle Wabash River at Carmi</option>
      
        <option value="03381500" >Middle Wabash River at Carmi (Base)</option>
      
        <option value="03341300" >Middle Wabash River at Coxville</option>
      
        <option value="03375500" >Middle Wabash River at Jasper</option>
      
        <option value="03377500" >Middle Wabash River at Mt Carmel</option>
      
        <option value="03378500" >Middle Wabash River at New Harmony</option>
      
        <option value="03374500" >Middle Wabash River at Patoka Lake TW</option>
      
        <option value="03376500" >Middle Wabash River at Princeton</option>
      
        <option value="03342000" >Middle Wabash River at Riverton</option>
      
        <option value="03345500" >Middle Wabash River at Ste Marie</option>
      
        <option value="03341500" >Middle Wabash River at Terre Haute</option>
      
        <option value="03343000" >Middle Wabash River at Vincennes</option>
      
        <option value="03380500" >Middle Wabash River at Wayne City</option>
      
        <option value="MLFK1" >Milford Lake on Republican River, KS</option>
      
        <option value="PXCK1" >Mill Creek Near Paxico,KS</option>
      
        <option value="WSHK1" >Mill Creek Near Washington, KS</option>
      
        <option value="MLNI2" >Mill Creek at Milan, IL</option>
      
        <option value="OMCI2" >Mill Creek at Old Mill Creek, IL</option>
      
        <option value="WBNT1" >Mill Creek at Thompson Ln near Woodbine</option>
      
        <option value="ANTT1" >Mill Creek near Antioch, TN</option>
      
        <option value="03359000" >Mill Creek nr Manhattan</option>
      
        <option value="MD111" >Mingo Ditch Near Fisk, MO</option>
      
        <option value="JDNM5" >Minnesota River at Jordan, MN - USGS Station No. 05330000</option>
      
        <option value="MNKM5" >Minnesota River at Mankato, MN</option>
      
        <option value="MVOM5" >Minnesota River at Montevideo, MN - USGS Station No. 05311000</option>
      
        <option value="ORTM5" >Minnesota River at Ortonville, MN - USGS Station No. 05292000</option>
      
        <option value="SAVM5" >Minnesota River at Savage, MN</option>
      
        <option value="MSSI3" >Mississinewa Lake</option>
      
        <option value="03326500" >Mississinewa River at Marion</option>
      
        <option value="03327000" >Mississinewa River at Peoria at Mississinewa Lake TW</option>
      
        <option value="WIDM5" >Mississippi River 4SE Winona Dam 5A</option>
      
        <option value="CE40EC2E" >Mississippi River @ Arkansas City, AR</option>
      
        <option value="CE40F18A" >Mississippi River @ Greenville, MS</option>
      
        <option value="CE4103F4" >Mississippi River @ Natchez, MS</option>
      
        <option value="CE40FF58" >Mississippi River @ Vicksburg, MS</option>
      
        <option value="MS117" >Mississippi River At Caruthersville, MO</option>
      
        <option value="MS133" >Mississippi River At Helena, AR</option>
      
        <option value="MS113" >Mississippi River At Hickman, KY</option>
      
        <option value="MS126" >Mississippi River At Memphis, TN (Weather Bureau Gage)</option>
      
        <option value="MS115" >Mississippi River At New Madrid, MO</option>
      
        <option value="MS130" >Mississippi River At Tunica RiverPark</option>
      
        <option value="MS121" >Mississippi River H.W. Gage 152 Near Osceola, AR (South)</option>
      
        <option value="MS116" >Mississippi River L.W. Gage 87.5 At Tiptonville, TN </option>
      
        <option value="01850" >Mississippi River South Pass at Port Eads (01850)</option>
      
        <option value="01575" >Mississippi River Southwest Pass Mile 7.5 BHP (01575)</option>
      
        <option value="01670" >Mississippi River Southwest Pass at East Jetty (01670)</option>
      
        <option value="01380" >Mississippi River at Algiers Lock (01380)</option>
      
        <option value="01390" >Mississippi River at Alliance (01390)</option>
      
        <option value="AMAW3" >Mississippi River at Alma, WI (CP5)</option>
      
        <option value="01160" >Mississippi River at Baton Rouge (01160)</option>
      
        <option value="01140" >Mississippi River at Bayou Sara (01140)</option>
      
        <option value="BETI4" >Mississippi River at Bettendorf,IA</option>
      
        <option value="01275" >Mississippi River at Bonne Carre - North of Spillway (01275)</option>
      
        <option value="01280" >Mississippi River at Bonnet Carre (01280)</option>
      
        <option value="BRLI4" >Mississippi River at Burlington,IA </option>
      
        <option value="CMMI4" >Mississippi River at Camanche,IA </option>
      
        <option value="CE401278" >Mississippi River at Cape Girardeau, MO</option>
      
        <option value="CASW3" >Mississippi River at Cassville,WI</option>
      
        <option value="CLAI4" >Mississippi River at Clayton, IA (Cp 10) - USGS Station No. 05411500</option>
      
        <option value="DKTM5" >Mississippi River at Dakota, MN (CP 7)</option>
      
        <option value="DAYM5" >Mississippi River at Days Highlanding, MN - USGS Station No. 05210000</option>
      
        <option value="01220" >Mississippi River at Donaldsonville (01220)</option>
      
        <option value="DBQI4" >Mississippi River at Dubuque,IA</option>
      
        <option value="01440" >Mississippi River at Empire (01440)</option>
      
        <option value="FMDI4" >Mississippi River at Fort Madison,IA </option>
      
        <option value="GENW3" >Mississippi River at Genoa Dam 8</option>
      
        <option value="GGYM7" >Mississippi River at Gregory Landing,MO </option>
      
        <option value="GTTI4" >Mississippi River at Guttenberg Dam 10</option>
      
        <option value="HNNM7" >Mississippi River at Hannibal,MO </option>
      
        <option value="01320" >Mississippi River at Harvey Lock (01320)</option>
      
        <option value="01545" >Mississippi River at Head of Passes (01545)</option>
      
        <option value="01340" >Mississippi River at IHNC Lock (01340)</option>
      
        <option value="KHBI2" >Mississippi River at Keithsburg,IL </option>
      
        <option value="AUEI4" >Mississippi River at Keokuk, IA (Ameren Data)</option>
      
        <option value="LCRM5" >Mississippi River at La Crescent Dam 7</option>
      
        <option value="LACW3" >Mississippi River at La Crosse, WI (CP 8)</option>
      
        <option value="LGGM7" >Mississippi River at La Grange,MO</option>
      
        <option value="LKCM5" >Mississippi River at Lake City, MN</option>
      
        <option value="LNSI4" >Mississippi River at Lansing, IA (CP 9)</option>
      
        <option value="DD1" >Mississippi River at Lock and Dam 1 (Minneapolis, MN)</option>
      
        <option value="DD10" >Mississippi River at Lock and Dam 10 (Guttenberg, IA)</option>
      
        <option value="MI11" >Mississippi River at Lock and Dam 11 (Dubuque,IA)</option>
      
        <option value="DLDI4" >Mississippi River at Lock and Dam 11 (MET Station)</option>
      
        <option value="MI12" >Mississippi River at Lock and Dam 12 (Bellevue,IA)</option>
      
        <option value="BLVI4" >Mississippi River at Lock and Dam 12 (MET Station)</option>
      
        <option value="MI13" >Mississippi River at Lock and Dam 13 (Fulton,IL)</option>
      
        <option value="FLTI2" >Mississippi River at Lock and Dam 13 (MET Station)</option>
      
        <option value="MI14" >Mississippi River at Lock and Dam 14 (LeClaire,IA)</option>
      
        <option value="LECI4" >Mississippi River at Lock and Dam 14 (MET Station)</option>
      
        <option value="RCKI2" >Mississippi River at Lock and Dam 15 (MET Station) </option>
      
        <option value="MI15" >Mississippi River at Lock and Dam 15 (Rock Island,IL)</option>
      
        <option value="MI16" >Mississippi River at Lock and Dam 16 (Illinois City,IL)</option>
      
        <option value="ILNI2" >Mississippi River at Lock and Dam 16 (MET Station)</option>
      
        <option value="NBOI2" >Mississippi River at Lock and Dam 17 (MET Station)</option>
      
        <option value="MI17" >Mississippi River at Lock and Dam 17 (New Boston,IL)</option>
      
        <option value="MI18" >Mississippi River at Lock and Dam 18 (Gladstone,IL)</option>
      
        <option value="GLDI2" >Mississippi River at Lock and Dam 18 (MET Station)</option>
      
        <option value="MI19" >Mississippi River at Lock and Dam 19 (Keokuk,IA)</option>
      
        <option value="EOKI4" >Mississippi River at Lock and Dam 19 (MET Station)</option>
      
        <option value="DD2" >Mississippi River at Lock and Dam 2 (Hastings, MN)</option>
      
        <option value="MI20" >Mississippi River at Lock and Dam 20 (Canton,MO)</option>
      
        <option value="CANM7" >Mississippi River at Lock and Dam 20 (MET Station)</option>
      
        <option value="QLDI2" >Mississippi River at Lock and Dam 21 (MET Station)</option>
      
        <option value="MI21" >Mississippi River at Lock and Dam 21 (Quincy,IL)</option>
      
        <option value="SVRM7" >Mississippi River at Lock and Dam 22 (MET Station)</option>
      
        <option value="MI22" >Mississippi River at Lock and Dam 22 (Saverton,MO)</option>
      
        <option value="DD3" >Mississippi River at Lock and Dam 3 (Welch, MN)</option>
      
        <option value="DD4" >Mississippi River at Lock and Dam 4 (Alma, WI)</option>
      
        <option value="DD5" >Mississippi River at Lock and Dam 5 (Minnesota City, MN)</option>
      
        <option value="DD5A" >Mississippi River at Lock and Dam 5A (Fountain City, WI)</option>
      
        <option value="DD6" >Mississippi River at Lock and Dam 6 (Trempealeau, WI)</option>
      
        <option value="DD7" >Mississippi River at Lock and Dam 7 (La Crescent, WI)</option>
      
        <option value="DD8" >Mississippi River at Lock and Dam 8 (Genoa, WI)</option>
      
        <option value="DD9" >Mississippi River at Lock and Dam 9 (Lynxville, WI)</option>
      
        <option value="LYNW3" >Mississippi River at Lynxville Dam 9</option>
      
        <option value="MCGI4" >Mississippi River at McGregor, IA - USGS Station No. 05389500</option>
      
        <option value="CE2256B4" >Mississippi River at Mel Price L&D (Lower)</option>
      
        <option value="MONI4" >Mississippi River at Montpelier,IA</option>
      
        <option value="MUSI4" >Mississippi River at Muscatine,IA </option>
      
        <option value="01300" >Mississippi River at New Orleans (Carrollton) (01300)</option>
      
        <option value="OQWI2" >Mississippi River at Oquawka,IL</option>
      
        <option value="PREW3" >Mississippi River at Prescott, WI (CP 3) - USGS Station No. 05344500</option>
      
        <option value="PRNI4" >Mississippi River at Princeton,IA</option>
      
        <option value="UINI2" >Mississippi River at Quincy,IL </option>
      
        <option value="01120" >Mississippi River at Red River Landing (01120)</option>
      
        <option value="RDWM5" >Mississippi River at Red Wing L/D 3</option>
      
        <option value="01260" >Mississippi River at Reserve (01260)</option>
      
        <option value="SABI4" >Mississippi River at Sabula,IA</option>
      
        <option value="SSPM5" >Mississippi River at South St. Paul (CP2)</option>
      
        <option value="STPM5" >Mississippi River at St. Paul, MN - USGS Station No. 05331000</option>
      
        <option value="01100Q" >Mississippi River at Tarbert Landing - Discharge (01100Q) </option>
      
        <option value="TREW3" >Mississippi River at Trempealeau Dam 6</option>
      
        <option value="01480" >Mississippi River at Venice (01480)</option>
      
        <option value="WABM5" >Mississippi River at Wabasha, MN (CP 4)</option>
      
        <option value="01515" >Mississippi River at West Bay (01515)</option>
      
        <option value="01400" >Mississippi River at West Pointe a la Hache (01400)</option>
      
        <option value="WNAM5" >Mississippi River at Winona, MN (CP 6) - USGS Station No. 05378500</option>
      
        <option value="ATKM5" >Mississippi River near Aitkin, MN - USGS Station No. 05227500</option>
      
        <option value="ANKM5" >Mississippi River near Anoka, MN at Coon Rapids Dam - USGS Station No. 05288500</option>
      
        <option value="BRWM5" >Mississippi River near Brownsville, MN - USGS Station No. 05386400</option>
      
        <option value="FAII4" >Mississippi River near Fairport,IA </option>
      
        <option value="FTRM5" >Mississippi River near Fort Ripley, MN - USGS Station No. 05261000</option>
      
        <option value="01080" >Mississippi River near Knox Landing (01080)</option>
      
        <option value="WILM5" >Mississippi River near Willow Beach, MN - USGS Station No. 05207600</option>
      
        <option value="01145" >Mississippi River nr St. Francisville (01145)</option>
      
        <option value="30072208" >Mississippi Sound at Grand Pass (USGS)</option>
      
        <option value="BOZM7" >Missouri River at Boonville, MO</option>
      
        <option value="GLZM7" >Missouri River at Glasgow, MO</option>
      
        <option value="JFFM7" >Missouri River at Jefferson City, MO</option>
      
        <option value="KCDM7" >Missouri River at Kansas City, MO</option>
      
        <option value="NAPM7" >Missouri River at Napoleon, MO</option>
      
        <option value="RULN1" >Missouri River at Rulo, NE</option>
      
        <option value="SJSM7" >Missouri River at St. Joseph, MO</option>
      
        <option value="WVYM7" >Missouri River at Waverly, MO</option>
      
        <option value="MHWO1" >Mohawk Lake near Nellie, OH (MKWD4)</option>
      
        <option value="MVLO1" >Mohicanville Lake near Mohicanville, OH (MOLC4)</option>
      
        <option value="BDDP1" >Monongahela River at Braddock L/D, PA (Upper) (BDDP)</option>
      
        <option value="GYLP1" >Monongahela River at Grays Landing L/D, PA (Upper) (GYLP)</option>
      
        <option value="MGTW2" >Monongahela River at Hildebrand L/D, WV (Lower) (MGTW)</option>
      
        <option value="ELZP1" >Monongahela River at L/D-3, Elizabeth, PA (Upper) (ELZP)</option>
      
        <option value="CHRP1" >Monongahela River at L/D-4, Charleroi, PA (Lower) (CHRP)</option>
      
        <option value="MAXP1" >Monongahela River at Maxwell L/D, PA (Lower) (MAXP)</option>
      
        <option value="MORW2" >Monongahela River at Morgantown L/D, WV (Lower) (MORW)</option>
      
        <option value="OPKW2" >Monongahela River at Opekiska L/D, WV (Lower) (OKKW)</option>
      
        <option value="PMRP1" >Monongahela River at Point Marion L/D, PA (Lower) (PMRP)</option>
      
        <option value="PMXP1" >Monongahela River at Point Marion L/D, PA (Upper Water Quality) (PMRX)</option>
      
        <option value="MONI3" >Monroe Lake</option>
      
        <option value="MRS" >Mormon Slough</option>
      
        <option value="MSQO1" >Mosquito Creek Lake Outflow, OH (MSOO)</option>
      
        <option value="MISO1" >Mosquito Creek Lake, OH (MOSO)</option>
      
        <option value="MTJP1" >Mount Jewett, PA (MTJP)</option>
      
        <option value="MMDN6" >Mount Morris Dam, Mt. Morris, NY</option>
      
        <option value="CE5EB176" >Muddy Bayou Control Structure (Eagle Lake Side)</option>
      
        <option value="CZ5EB176" >Muddy Bayou Control Structure (Steele Bayou Side)</option>
      
        <option value="MLBA4" >Mulberry River near Mulberry</option>
      
        <option value="MCCO1" >Muskingum River at McConnelsville, OH (MCMG5)</option>
      
        <option value="ZANO1" >Muskingum River at Zanesville, OH (ZANF5)</option>
      
        <option value="CSHO1" >Muskingum River near Coshocton, OH (COMD5)</option>
      
        <option value="DREO1" >Muskingum River near Dresden, OH (DRME4)</option>
      
        <option value="WEAM5" >Mustinka River at Wheaton, MN - USGS Station No. 05049000</option>
      
        <option value="NCMM5" >Mustinka River near Norcross, MN</option>
      
        <option value="01143" >NE Corner of Casting Yard (01143)</option>
      
        <option value="NSP" >NSP - Power Plant</option>
      
        <option value="NRAL1" >Natalbany River near Amite (USGS)</option>
      
        <option value="85390" >Natalbany River near Baptist, LA (85390)</option>
      
        <option value="NHGQ" >New Hogan Dam Outflow</option>
      
        <option value="NHGP" >New Hogan Lake Pool</option>
      
        <option value="NHGW" >New Hogan Lake Weather</option>
      
        <option value="HITO1" >New Lexington, OH (NELG4)</option>
      
        <option value="GLLV2" >New River at Glen Lyn, VA (GNNP7)</option>
      
        <option value="HINW2" >New River at Hinton, WV (HINO7)</option>
      
        <option value="GAXV2" >New River at Old Town near Galax, VA (GLXR7)</option>
      
        <option value="RDFV2" >New River at Radford, VA (RAVQ7)</option>
      
        <option value="THMW2" >New River at Thurmond, WV (THNN6)</option>
      
        <option value="ALSV2" >New River near Allisonia, VA (ALNR7)</option>
      
        <option value="BKDW" >Newaukum Creek near Black Diamond, WA</option>
      
        <option value="NHSO1" >Nimishillen Creek near North Industry, OH (NINC6)</option>
      
        <option value="GRZM7" >Nodaway River at Graham, MO</option>
      
        <option value="NOLK2" >Nolin Lake</option>
      
        <option value="03311000" >Nolin River at Kyrock</option>
      
        <option value="03310300" >Nolin River at White Mills</option>
      
        <option value="FTNO1" >North Br.Kokosing River near Fredericktown, OH (NBKD3)</option>
      
        <option value="NCC" >North Fork Cache Creek (Lower)</option>
      
        <option value="NCU" >North Fork Cache Creek (Upper)</option>
      
        <option value="NEPI4" >North Fork English River near Parnell, IA</option>
      
        <option value="FN111" >North Fork Forked Deer River At Dyersburg, TN</option>
      
        <option value="FN112" >North Fork Forked Deer River Near Tatumville, TN (South)</option>
      
        <option value="03277500" >North Fork Kentucky River at Hazard</option>
      
        <option value="03280000" >North Fork Kentucky River at Jackson</option>
      
        <option value="03277300" >North Fork Kentucky River at Whitesburg</option>
      
        <option value="03251200" >North Fork Licking River nr MT Olivet</option>
      
        <option value="FLNI4" >North Fork Maquoketa River near Fulton, IA </option>
      
        <option value="ON111" >North Fork Obion River Near Martin, TN (North)</option>
      
        <option value="ON113" >North Fork Obion River Near Palmersville, Tennessee (North)</option>
      
        <option value="CMLM5" >North Fork Rabbit River near Campbell, MN</option>
      
        <option value="NFDA4" >North Fork River at Norfork Dam - HW & TW</option>
      
        <option value="NORDO" >North Fork River below Norfork Dam - WQ</option>
      
        <option value="INNOR" >North Fork River inside Norfork Dam (WQ)</option>
      
        <option value="TNZM7" >North Fork River near Tecumseh</option>
      
        <option value="NFPV2" >North Fork of Pound River Lake (Tailwater) at Pound, VA (NFPOF)</option>
      
        <option value="POUV2" >North Fork of Pound River Lake at Pound, VA (NFPQ3)</option>
      
        <option value="EFWI4" >North Raccoon River near Jefferson, IA</option>
      
        <option value="LKCI4" >North Raccoon River near Lanesboro, IA</option>
      
        <option value="PROI4" >North Raccoon River near Perry, IA</option>
      
        <option value="SCRI4" >North Raccoon River near Sac City, IA</option>
      
        <option value="NRWI4" >North River near Norwalk, IA</option>
      
        <option value="PALM7" >North River near Palmyra,MO </option>
      
        <option value="SIGI4" >North Skunk River near Sigourney, IA</option>
      
        <option value="03255000" >OHIO RIVER AT CINCINNATI</option>
      
        <option value="OKH" >Oakhurst Weather</option>
      
        <option value="GARN6" >Oatka Creek at Garbutt, NY</option>
      
        <option value="WRSN6" >Oatka Creek at Warsaw, NY</option>
      
        <option value="OB113" >Obion River Near Bogota, TN (South)</option>
      
        <option value="OB114" >Obion River Near Mengelwood, TN (Southwest)</option>
      
        <option value="OB112" >Obion River Near Obion, TN (Southwest)</option>
      
        <option value="OB111" >Obion River Near Rives, TN (South)</option>
      
        <option value="ODDW2" >Odd, WV (ODDO6)</option>
      
        <option value="ASHK2P" >Ohio River @ Ashland</option>
      
        <option value="OH21P" >Ohio River @ Belleville L&D Pool</option>
      
        <option value="OH21" >Ohio River @ Belleville L&D TW</option>
      
        <option value="CIRI2P" >Ohio River @ Cairo</option>
      
        <option value="OH75P" >Ohio River @ Cannelton L&D Pool</option>
      
        <option value="OH75" >Ohio River @ Cannelton L&D TW</option>
      
        <option value="CCNO1P" >Ohio River @ Cincinnati</option>
      
        <option value="OH02P" >Ohio River @ Dashields L&D Pool</option>
      
        <option value="OH02" >Ohio River @ Dashields L&D TW</option>
      
        <option value="OH01P" >Ohio River @ Emsworth L&D Pool</option>
      
        <option value="OH01" >Ohio River @ Emsworth L&D TW</option>
      
        <option value="EVVI3P" >Ohio River @ Evansville</option>
      
        <option value="OH24P" >Ohio River @ Greenup L&D Pool</option>
      
        <option value="OH24" >Ohio River @ Greenup L&D TW</option>
      
        <option value="OH71P" >Ohio River @ Hannibal L&D Pool</option>
      
        <option value="OH71" >Ohio River @ Hannibal L&D TW</option>
      
        <option value="HNTW2P" >Ohio River @ Huntington</option>
      
        <option value="OH77P" >Ohio River @ J. T. Myers L&D Pool</option>
      
        <option value="OH77" >Ohio River @ J. T. Myers L&D TW</option>
      
        <option value="OH52P" >Ohio River @ L&D 52 Pool</option>
      
        <option value="OH52" >Ohio River @ L&D 52 TW</option>
      
        <option value="OH53P" >Ohio River @ L&D 53 Pool</option>
      
        <option value="OH53" >Ohio River @ L&D 53 TW</option>
      
        <option value="MRTO1P" >Ohio River @ Marietta</option>
      
        <option value="OH41P" >Ohio River @ Markland L&D Pool</option>
      
        <option value="OH41" >Ohio River @ Markland L&D TW</option>
      
        <option value="MYSK2P" >Ohio River @ Maysville</option>
      
        <option value="OH42P" >Ohio River @ McAlpine L&D Pool</option>
      
        <option value="OH42" >Ohio River @ McAlpine L&D TW</option>
      
        <option value="OH25P" >Ohio River @ Meldahl L&D Pool</option>
      
        <option value="OH25" >Ohio River @ Meldahl L&D TW</option>
      
        <option value="OH03P" >Ohio River @ Montgomery L&D Pool</option>
      
        <option value="OH03" >Ohio River @ Montgomery L&D TW</option>
      
        <option value="OH04P" >Ohio River @ New Cumberland L&D Pool</option>
      
        <option value="OH04" >Ohio River @ New Cumberland L&D TW</option>
      
        <option value="OH76P" >Ohio River @ Newburgh L&D Pool</option>
      
        <option value="OH76" >Ohio River @ Newburgh L&D TW</option>
      
        <option value="OLMI2P" >Ohio River @ Olmsted L&D</option>
      
        <option value="PAHK2P" >Ohio River @ Padukah</option>
      
        <option value="PARW2P" >Ohio River @ Parkersburg</option>
      
        <option value="OH05P" >Ohio River @ Pike Island L&D Pool</option>
      
        <option value="OH05" >Ohio River @ Pike Island L&D TW</option>
      
        <option value="POPW2P" >Ohio River @ Point Pleasant</option>
      
        <option value="OH26P" >Ohio River @ R.C. Byrd L&D Pool</option>
      
        <option value="OH26" >Ohio River @ R.C. Byrd L&D TW</option>
      
        <option value="OH22P" >Ohio River @ Racine L&D Pool</option>
      
        <option value="OH22" >Ohio River @ Racine L&D TW</option>
      
        <option value="OH78P" >Ohio River @ Smithland L&D Pool</option>
      
        <option value="OH78" >Ohio River @ Smithland L&D TW</option>
      
        <option value="OH72P" >Ohio River @ Willow Island L&D Pool</option>
      
        <option value="OH72" >Ohio River @ Willow Island L&D TW</option>
      
        <option value="OH111" >Ohio River At Cairo, IL</option>
      
        <option value="ASHK2" >Ohio River at Ashland, KY (ASOL3)</option>
      
        <option value="03303280" >Ohio River at Cannelton Lower</option>
      
        <option value="DSHP1" >Ohio River at Dashields L/D, PA (Upper) (DSHP)</option>
      
        <option value="03322000" >Ohio River at EVANSVILLE</option>
      
        <option value="EMSP1" >Ohio River at Emsworth L/D, PA (Lower) (EMSP)</option>
      
        <option value="03384500" >Ohio River at GOLCONDA</option>
      
        <option value="03612500" >Ohio River at GRAND CHAIN</option>
      
        <option value="GNUK2" >Ohio River at Greenup Lock and Dam (GROK3)</option>
      
        <option value="HANO1" >Ohio River at Hannibal L/D, OH (Lower) (HANO)</option>
      
        <option value="HNTW2" >Ohio River at Huntington, WV (HTSL3)</option>
      
        <option value="03322420" >Ohio River at JT Myers L/D lower</option>
      
        <option value="03294600" >Ohio River at Kosmosdale</option>
      
        <option value="03611500" >Ohio River at METROPOLIS</option>
      
        <option value="MRTO1" >Ohio River at Marietta, OH (MAOH6)</option>
      
        <option value="03277200" >Ohio River at Markland Dam Lower Gage</option>
      
        <option value="MYSK2" >Ohio River at Maysville, KY (MAOK1)</option>
      
        <option value="03294500" >Ohio River at McAlpine Dam Lower Gage</option>
      
        <option value="03293548" >Ohio River at McAlpine Dam Upper Gage</option>
      
        <option value="03238680" >Ohio River at Meldahl</option>
      
        <option value="MELO1" >Ohio River at Meldahl Lock and Dam (MDOJO)</option>
      
        <option value="MGYP1" >Ohio River at Montgomery L/D, PA (Lower) (MGYP)</option>
      
        <option value="MGXP1" >Ohio River at Montgomery L/D, PA (Upper Water Quality) (MGYX)</option>
      
        <option value="NCUW2" >Ohio River at New Cumberland L/D, OH (Lower) (NCUO)</option>
      
        <option value="03304300" >Ohio River at Newburgh Lower</option>
      
        <option value="03611000" >Ohio River at PADUCAH</option>
      
        <option value="PARW2" >Ohio River at Parkersburg, WV (PKRH5)</option>
      
        <option value="WHLW2" >Ohio River at Pike Island L/D, WV (Lower) (WHLW)</option>
      
        <option value="POPW2" >Ohio River at Point Pleasant, WV (PIWJ4)</option>
      
        <option value="PORO1" >Ohio River at Portsmouth, OH (PMHK3)</option>
      
        <option value="GALW2" >Ohio River at RC Byrd Lock and Dam (GPOK4)</option>
      
        <option value="RACW2" >Ohio River at Racine Lock and Dam (RAOJ5)</option>
      
        <option value="CE557912" >Ohio River at Smithland Upper</option>
      
        <option value="WLGW2" >Ohio River at Wheeling, WV (WEEW)</option>
      
        <option value="RNOO1" >Ohio River at Willow Island Lock and Dam (WIOH6)</option>
      
        <option value="ROSP1" >Oil Creek at Rouseville, PA (ROSP)</option>
      
        <option value="CE499230" >Old Coldwater River @ Birdie, MS</option>
      
        <option value="IOCI4" >Old Man's Creek near Iowa City, IA</option>
      
        <option value="49645" >Old River (FWS) at GIWW Junction (Alt Rte) (49645)</option>
      
        <option value="02200" >Old River Auxiliary Inflow near Knox Landing (02200)</option>
      
        <option value="02210" >Old River Auxiliary Outflow near Knox Landing (02210)</option>
      
        <option value="02050" >Old River LowSill Inflow Channel near Knox Landing (02050)</option>
      
        <option value="02100" >Old River Lowsill Outflow Channel near Knox Landing (02100)</option>
      
        <option value="02600Q" >Old River Outflow Channel - Total Discharge (02600Q)</option>
      
        <option value="02570" >Old River Outflow Channel below Hydropower Channel (02570)</option>
      
        <option value="DELO1" >Olentangy River (Below Dam) near Delaware, OH (DDOOF)</option>
      
        <option value="CRDO1" >Olentangy River at Claridon, OH (CLOC3)</option>
      
        <option value="WRTO1" >Olentangy River near Worthington, OH (WOOE2)</option>
      
        <option value="SC02" >Olive Creek Lake (Salt Creek Dam site #02)</option>
      
        <option value="85635" >Orleans Ave Canal 1 - ICS Lake-side (85635)</option>
      
        <option value="85636" >Orleans Ave Canal 2 - ICS Canal-side (85636)</option>
      
        <option value="85637" >Orleans Ave Canal 3 - Robert E Lee (85637)</option>
      
        <option value="85638" >Orleans Ave Canal 4 - Chapelle St. (85638)</option>
      
        <option value="85639" >Orleans Ave Canal 5 - Lane St. (85639)</option>
      
        <option value="85640" >Orleans Ave Canal 6 - Harrison Ave (85640)</option>
      
        <option value="85641" >Orleans Ave Canal 7 - Polk St. (85641)</option>
      
        <option value="85642" >Orleans Ave Canal 8 - PS7 (85642)</option>
      
        <option value="ORWDD" >Orwell Dam</option>
      
        <option value="ORWM5" >Orwell Dam near Fergus Falls, MN</option>
      
        <option value="SHNP1" >Oswayo Creek at Shinglehouse, PA (SNGP)</option>
      
        <option value="OTDIV" >Ottertail River Diversion - USGS Station No. 05046475</option>
      
        <option value="OTRM5" >Ottertail River below Orwell Dam near Fergus Falls, MN - USGS St. No. 05046000</option>
      
        <option value="CE1842E0" >Ouachita River @ Arkadelphia, AR</option>
      
        <option value="CE418B32" >Ouachita River @ Blakely Mountain Dam, AR</option>
      
        <option value="CE40BC52" >Ouachita River @ Camden, AR</option>
      
        <option value="CZ4921BE" >Ouachita River @ Columbia Lock & Dam (lower)</option>
      
        <option value="CE4921BE" >Ouachita River @ Columbia Lock & Dam (upper)</option>
      
        <option value="CE503DD8" >Ouachita River @ Felsenthal Lock & Dam (lower), AR</option>
      
        <option value="CE50459A" >Ouachita River @ Felsenthal Lock & Dam (upper), AR</option>
      
        <option value="CE40C410" >Ouachita River @ Monroe, LA</option>
      
        <option value="DDBF9588" >Ouachita River @ Mount Ida, AR</option>
      
        <option value="DD0C8038" >Ouachita River @ Remmel Dam, AR</option>
      
        <option value="D11732CA" >Ouachita River @ West Monroe, LA</option>
      
        <option value="OWNQ" >Owens Creek</option>
      
        <option value="OWNP" >Owens Reservoir Pool</option>
      
        <option value="CA05E6E0" >P1 PIEZOMETER</option>
      
        <option value="CB05E6E0" >P2 PIEZOMETER</option>
      
        <option value="CC05E6E0" >P3 PIEZOMETER</option>
      
        <option value="CD05E6E0" >P4 PIEZOMETER</option>
      
        <option value="CZ05E6E0" >P5 PIEZOMETER</option>
      
        <option value="CF05E6E0" >P6 PIEZOMETER</option>
      
        <option value="CG05E6E0" >P6B PIEZOMETER</option>
      
        <option value="CH05E6E0" >P7 PIEZOMETER</option>
      
        <option value="CI05E6E0" >P8 PIEZOMETER</option>
      
        <option value="BBRO1" >Paint Creek (below Dam) near Bainbridge, OH (PCSOF)</option>
      
        <option value="PCRO1" >Paint Creek Reservoir at Bainbridge, OH (PCSI2)</option>
      
        <option value="SFDK2" >Paint Creek below Paintsville Lake near Staffordsville, KY (PIVOF)</option>
      
        <option value="BVLO1" >Paint Creek near Bourneville, OH (BRPH2)</option>
      
        <option value="GRFO1" >Paint Creek near Greenfield, OH (GRFH2)</option>
      
        <option value="PNTK2" >Paintsville Lake near Paintsville, KY (PIVN3)</option>
      
        <option value="PSC" >Pascoes Weather</option>
      
        <option value="85420" >Pass Manchac near Pontchatoula (85420)</option>
      
        <option value="PRLI3" >Patoka Lake</option>
      
        <option value="SC14" >Pawnee Lake (Salt Creek Dam site #14)</option>
      
        <option value="17CBB7A8" >Pearl River @ Bogalusa, LA</option>
      
        <option value="177104BC" >Pearl River @ Carthage, MS</option>
      
        <option value="17CCD07A" >Pearl River @ Columbia, MS</option>
      
        <option value="1770F6C2" >Pearl River @ Edinburg, MS</option>
      
        <option value="DD3051BC" >Pearl River @ Jackson, MS</option>
      
        <option value="177364AE" >Pearl River @ Lena (Good Hope), MS</option>
      
        <option value="17CCE5E0" >Pearl River @ Monticello, MS</option>
      
        <option value="171DE4E0" >Pearl River @ Pearl River, LA</option>
      
        <option value="1770D02E" >Pearl River @ Philadelphia, MS</option>
      
        <option value="17AC1756" >Pearl River @ Pools Bluff, LA</option>
      
        <option value="16F205A8" >Pearl River @ Ross Barnett Reservoir, MS (pool)</option>
      
        <option value="16F205AZ" >Pearl River @ Ross Barnett Reservoir, MS (tailwater)</option>
      
        <option value="D116733A" >Pearl River @ Walkiah Bluff Weir Downstream</option>
      
        <option value="D116604C" >Pearl River @ Walkiah Bluff Weir Upstream</option>
      
        <option value="CE06977E" >Pearl River Lock 1 Chamber</option>
      
        <option value="CE068408" >Pearl River Lock 2 Chamber</option>
      
        <option value="CE06748C" >Pearl River Lock 3 Chamber</option>
      
        <option value="17ACA4D8" >Pearl River Navigation Canal @ L&D No. 1</option>
      
        <option value="17AC9142" >Pearl River Navigation Canal @ L&D No. 2</option>
      
        <option value="17AC8234" >Pearl River Navigation Canal @ L&D No. 3</option>
      
        <option value="DARW3" >Pecatonica River at Darlington, WI</option>
      
        <option value="FEEI2" >Pecatonica River at Freeport, IL</option>
      
        <option value="MTNW3" >Pecatonica River at Martintown, WI</option>
      
        <option value="SIRI2" >Pecatonica River near Shirland, IL</option>
      
        <option value="PRRK1" >Perry Lake near Perry, KS</option>
      
        <option value="PRY" >Perry Ranch Weather</option>
      
        <option value="BMTA4" >Petit Jean River at Blue Mtn Dam - HW</option>
      
        <option value="BMRA4" >Petit Jean River at Blue Mtn Dam - TW</option>
      
        <option value="DANA4" >Petit Jean River at Danville</option>
      
        <option value="BONA4" >Petit Jean River near Booneville</option>
      
        <option value="CNTA4" >Petit Jean River near Centerville</option>
      
        <option value="PCKW2" >Pickens, WV (PICW)</option>
      
        <option value="PIDO1" >Piedmont Lake near Piedmont, OH (PESE6)</option>
      
        <option value="PGMV2" >Pilgrim Knob near Marvin, VA (PIKP5)</option>
      
        <option value="RLFI4" >Pilot Creek near Rolfe, IA </option>
      
        <option value="CRLM5" >Pine River Dam at Crosslake, MN</option>
      
        <option value="PNVW2" >Pineville, WV (PNVO5)</option>
      
        <option value="PIST" >Pipestem Reservoir</option>
      
        <option value="PTTP1P" >Pittsburgh Point</option>
      
        <option value="PTTP1" >Pittsburgh, PA Point Gage (PTTP)</option>
      
        <option value="SSTM7" >Platte River at Sharps Station, MO</option>
      
        <option value="AGYM7" >Platte River near Agency, MO</option>
      
        <option value="RVLW3" >Platte River near Rockville, WI</option>
      
        <option value="PTHO1" >Pleasant Hill Lake near Perrysville, OH (PHCC4)</option>
      
        <option value="PKGM5" >Pokegama Dam at Grand Rapids, MN</option>
      
        <option value="POKM5" >Pokegama Lake at Grand Rapids, MN</option>
      
        <option value="APPM5" >Pomme de Terre River at Appleton, MN - USGS Station No. 05294000</option>
      
        <option value="03320500" >Pond River near Apex</option>
      
        <option value="03321060" >Pond River near Madisonville</option>
      
        <option value="CMBK2" >Poor Fork near Cumberland, KY</option>
      
        <option value="PCKI2" >Pope Creek at Keithsburg,IL </option>
      
        <option value="52415" >Port Allen Lock - Intracoastal Waterway (52415)</option>
      
        <option value="SMPP1" >Potato Creek at Smethport, PA (SMHP)</option>
      
        <option value="PICV2" >Pound River above Indian Creek near Pound, VA (PUPQ3)</option>
      
        <option value="PBCV2" >Pound River below Bold Camp Creek near Pound, VA (PLPQ3)</option>
      
        <option value="HAYV2" >Pound River below Flannagan Dam near Haysi, VA (JFPOF)</option>
      
        <option value="GFPV2" >Pound River near George's Fork, VA (GFPQ4)</option>
      
        <option value="PXTP1" >Punxsutawney, PA (STP) (PUXP)</option>
      
        <option value="KNSO1" >Pymatuning Creek at Kinsman, OH (KINO)</option>
      
        <option value="CE50330A" >Quiver River @ Doddsville, MS</option>
      
        <option value="CE5E7ABA" >Quiver River @ Sunflower, MS</option>
      
        <option value="GBTW2" >R. D. Bailey Lake near Gilbert, WV (RDBO5)</option>
      
        <option value="JAHM5" >Rabbit River near Campbell, MN</option>
      
        <option value="DMWI4" >Raccoon River at 63rd St in Des Moines, IA</option>
      
        <option value="ADMO1" >Raccoon River at Adamsville, OH (ADVJ4)</option>
      
        <option value="VNMI4" >Raccoon River at Van Meter, IA</option>
      
        <option value="WDMI4" >Raccoon River near West Des Moines, IA</option>
      
        <option value="RRF" >Railroad Flat Weather</option>
      
        <option value="CTNK2" >Rain Gage at Canton, KY</option>
      
        <option value="EKTK2" >Rain Gage at Elkton, KY</option>
      
        <option value="MNYT1" >Rain Gage at Monterey, TN</option>
      
        <option value="IRCI4" >Rapid Creek near Iowa City,IA</option>
      
        <option value="CTFO1" >Rattlesnake Creek at Centerfield, OH (CTSH2)</option>
      
        <option value="RVDW" >Ravensdale Weather Station</option>
      
        <option value="16EED5C2" >Red Chute Bayou @ Dogwood Trail</option>
      
        <option value="RRDDD" >Red Lake Dam</option>
      
        <option value="RRDM5" >Red Lake Dam near Red Lake, MN - USGS Station No. 05074000</option>
      
        <option value="CRKM5" >Red Lake River at Crookston, MN - USGS Station No. 05079000</option>
      
        <option value="HIGM5" >Red Lake River at High Landing, MN - USGS Station No. 05075000</option>
      
        <option value="WSKM5" >Red Lake at Waskish, MN - USGS Station No. 05073500</option>
      
        <option value="SAUM5" >Red Lake at mouth of Battle River near Saum, MN - USGS Station No. 05073650</option>
      
        <option value="RHWW2" >Red Oak Knob near Richwood, WV (ROKL8)</option>
      
        <option value="CE40D9B4" >Red River @ Alexandria, LA</option>
      
        <option value="CE7F29D2" >Red River @ Coushatta, LA</option>
      
        <option value="CE41E006" >Red River @ Fulton, AR</option>
      
        <option value="CE3C30A4" >Red River @ Grand Ecore, LA</option>
      
        <option value="CE7F1C48" >Red River @ Lock & Dam No. 1 (lower)</option>
      
        <option value="CE7F129A" >Red River @ Lock & Dam No. 1 (upper), LA</option>
      
        <option value="CE7F0F3E" >Red River @ Lock & Dam No. 2 (lower), LA</option>
      
        <option value="CE7F01EC" >Red River @ Lock & Dam No. 2 (upper), LA</option>
      
        <option value="CE2D35C0" >Red River @ Lock & Dam No. 3 Lower, LA</option>
      
        <option value="CE2D4350" >Red River @ Lock & Dam No. 3 Upper, LA</option>
      
        <option value="CE69D0D4" >Red River @ Lock & Dam No. 4 (Lower), LA</option>
      
        <option value="CE6A1C16" >Red River @ Lock & Dam No. 4 (upper), LA</option>
      
        <option value="CE5EBFA4" >Red River @ Lock & Dam No. 5 (lower), LA</option>
      
        <option value="CE506376" >Red River @ Lock & Dam No. 5 (upper), LA</option>
      
        <option value="CE2D5026" >Red River @ Mid Point Pool no. 3</option>
      
        <option value="CE41DB4E" >Red River @ Shreveport, LA</option>
      
        <option value="03283500" >Red River at Clay City</option>
      
        <option value="FLTA4" >Red River at Fulton</option>
      
        <option value="INGA4" >Red River at Index</option>
      
        <option value="PORT1" >Red River at Port Royal, TN</option>
      
        <option value="DRTN8" >Red River of the North at Drayton, ND - USGS Station No. 05092000</option>
      
        <option value="HILN8" >Red River of the North at Halstad, MN - USGS Station No. 05064500</option>
      
        <option value="WHNN8" >Red River of the North at Wahpeton, ND - USGS Station No. 05051500</option>
      
        <option value="BKLP1" >Redbank Creek at Brookville, PA (BRKP)</option>
      
        <option value="SNCP1" >Redbank Creek at Saint Charles, PA (SNCP)</option>
      
        <option value="WLTP1" >Redstone Creek at Waltersburg, PA (WLTP)</option>
      
        <option value="CEHT1" >Redundant Caney Fork at Center Hill Dam, TN</option>
      
        <option value="BAHK2" >Redundant Cumberland River at Barkley Dam, KY</option>
      
        <option value="CORT1" >Redundant Cumberland River at Cordell Hull Dam, TN</option>
      
        <option value="OHHT1" >Redundant Cumberland River at Old Hickory Dam, TN</option>
      
        <option value="DLHT1" >Redundant Obey River at Dale Hollow Dam, TN</option>
      
        <option value="JPHT1" >Redundant Stones River at J Percy Priest Dam, TN</option>
      
        <option value="RL111" >Reelfoot Lake Near Tiptonville, TN (Southeast)</option>
      
        <option value="CYCK1" >Republican River at Clay Center, KS</option>
      
        <option value="MILK1" >Republican River below Milford Lake, KS</option>
      
        <option value="HAVI4" >Richland Creek near Haven, IA</option>
      
        <option value="GUAW2" >Right Fork of Holly River at Guardian, WV (GARK7)</option>
      
        <option value="LR117" >Right Hand Chute of Little River At Pettyville, AR</option>
      
        <option value="LR118" >Right Hand Chute of Little River At Rivervale, AR</option>
      
        <option value="85700" >Rigolets near Lake Pontchartrain (85700)</option>
      
        <option value="GBOT1" >Roaring River above Gainesboro, TN</option>
      
        <option value="RCPW2" >Rock Camp, WV (ROCP7)</option>
      
        <option value="RCF" >Rock Creek</option>
      
        <option value="AFTW3" >Rock River at Afton, WI</option>
      
        <option value="BYRI2" >Rock River at Byron, IL</option>
      
        <option value="CMOI2" >Rock River at Como, IL </option>
      
        <option value="HCNW3" >Rock River at Horicon, WI</option>
      
        <option value="INFW3" >Rock River at Indianford, WI</option>
      
        <option value="LATI2" >Rock River at Latham Park, IL</option>
      
        <option value="MLII2" >Rock River at Moline, IL </option>
      
        <option value="FATW3" >Rock River at Robert Street at Fort Atkinson, WI</option>
      
        <option value="RABI2" >Rock River at Rockford (Auburn Street), IL</option>
      
        <option value="ROKI2" >Rock River at Rockton, IL</option>
      
        <option value="WATW3" >Rock River at Watertown, WI</option>
      
        <option value="JOSI2" >Rock River near Joslin, IL </option>
      
        <option value="BLWK2" >Rockcastle River at Billows, KY</option>
      
        <option value="BRMO1" >Rocky Fork near Barretts Mills (BMRI2)</option>
      
        <option value="AGNO" >Rogue River at Agness</option>
      
        <option value="EGLO" >Rogue River at Dodge Bridge near Eagle Point</option>
      
        <option value="GRAO" >Rogue River at Grants Pass</option>
      
        <option value="RYGO" >Rogue River at Raygold</option>
      
        <option value="PRSO" >Rogue River below Prospect</option>
      
        <option value="MCLO" >Rogue River near McLeod</option>
      
        <option value="DQDA4" >Rolling Fork River at DeQueen Dam - HW</option>
      
        <option value="DQTA4" >Rolling Fork River at DeQueen Dam - TW</option>
      
        <option value="DQNA4" >Rolling Fork River near DeQueen</option>
      
        <option value="03301500" >Rolling Fork at Boston</option>
      
        <option value="03301630" >Rolling Fork at Lebanon Junction</option>
      
        <option value="HOUM5" >Root River at Houston, MN - USGS Station No. 05385000</option>
      
        <option value="RSVO1" >Roseville, OH (ROSF4)</option>
      
        <option value="RRLK2" >Rough River Lake</option>
      
        <option value="03318500" >Rough River at Falls of Rough</option>
      
        <option value="03318010" >Rough River at Rough River Dam</option>
      
        <option value="03319000" >Rough River near Dundee</option>
      
        <option value="RWLW2" >Rowlesburg, WV (RWLW)</option>
      
        <option value="RRB11" >Running Reelfoot Bayou, TN</option>
      
        <option value="03307000" >Russell Creek near Columbia</option>
      
        <option value="BRFV2" >Russell Fork at Bartlick, VA (BLRQ4)</option>
      
        <option value="HAIV2" >Russell Fork at Haysi, VA (HARQ4)</option>
      
        <option value="ELKK2" >Russell Fork of Big Sandy River at Elkhorn City, KY (ECRP4)</option>
      
        <option value="GRN" >Russian River near Guerneville</option>
      
        <option value="HOP" >Russian River near Hopland</option>
      
        <option value="OR105" >Rutherford Fork Obion River Near Milan, TN (Northeast)</option>
      
        <option value="SMW" >SF Merced River near Wawona</option>
      
        <option value="CJ05E6E0" >SITE D for GEOTECH</option>
      
        <option value="CQ05E6E0" >SITE F for GEOTECH</option>
      
        <option value="CS05E6E0" >SITE G</option>
      
        <option value="SB106" >ST. Francis Bay at Birdeye, AR</option>
      
        <option value="01142" >SW Corner of Casting Yard (01142)</option>
      
        <option value="SLAI3" >Salamonie Lake</option>
      
        <option value="03324500" >Salamonie River at Dora at Salamonie Lake TW</option>
      
        <option value="03324300" >Salamonie River near Warren</option>
      
        <option value="SPLO1" >Salem, OH (SLMO)</option>
      
        <option value="TCSW2" >Salem, WV (SLMW)</option>
      
        <option value="17EDC018" >Saline River @ Benton, AR</option>
      
        <option value="1662D3E6" >Saline River @ Rye, AR</option>
      
        <option value="CE490980" >Saline River @ Sheridan, AR</option>
      
        <option value="CE41A30C" >Saline River @ Warren, AR</option>
      
        <option value="DIEA4" >Saline River at Dierks Dam - HW</option>
      
        <option value="DKTA4" >Saline River at Dierks Dam - TW</option>
      
        <option value="DIRA4" >Saline River near Dierks</option>
      
        <option value="LCKA4" >Saline River near Lockesburg</option>
      
        <option value="WSPI2" >Salt Creek at Western Springs, IL</option>
      
        <option value="EBRI4" >Salt Creek near Elberon, IA</option>
      
        <option value="GREI2" >Salt Creek near Greenview, IL </option>
      
        <option value="RLLI2" >Salt Creek near Rowell, IL</option>
      
        <option value="SILO1" >Salt Fork at Salt Fork Dam near North Salem, OH (SLTE5)</option>
      
        <option value="03298470" >Salt River at Floyds Fork</option>
      
        <option value="03295400" >Salt River at Glensboro</option>
      
        <option value="03298500" >Salt River at Shepherdsville</option>
      
        <option value="WANO1" >Sandy Creek at Waynesburg, OH (WAYC6)</option>
      
        <option value="SNDK2" >Sandy Hook, KY (SHLM2)</option>
      
        <option value="SNLP1" >Sandy Lake, PA (SNLP)</option>
      
        <option value="DUBP1" >Sandy Lick Creek at Dubois, PA (DUJP)</option>
      
        <option value="FISI2" >Sangamon River at Fisher, IL</option>
      
        <option value="MNTI2" >Sangamon River at Monticello,IL</option>
      
        <option value="PETI2" >Sangamon River at Petersburg, IL</option>
      
        <option value="RVTI2" >Sangamon River at Riverton, IL </option>
      
        <option value="DCRI2" >Sangamon River at Route 48 at Decatur, IL</option>
      
        <option value="CDLI2" >Sangamon River near Chandlerville, IL</option>
      
        <option value="OKFI2" >Sangamon River near Oakford, IL </option>
      
        <option value="SAYI4" >Saylorville Lake Reservoir</option>
      
        <option value="76600" >Schooner Bayou Control Structure - East (76600)</option>
      
        <option value="76680" >Schooner Bayou Control Structure - West (76680)</option>
      
        <option value="CHCO1" >Scioto River at Chillicothe, OH (CHSH3)</option>
      
        <option value="CIRO1" >Scioto River at Circleville, OH (CISG3)</option>
      
        <option value="COLO1" >Scioto River at Columbus, OH (CLSF4)</option>
      
        <option value="DBVO1" >Scioto River at Darbyville, OH (DYDG2)</option>
      
        <option value="HIGO1" >Scioto River at Higby, OH (HIGH3)</option>
      
        <option value="WEJO1" >Scioto River at West Jefferson, OH (WJEF2)</option>
      
        <option value="BLPO1" >Scioto River near Bellepoint, OH (BLPD2)</option>
      
        <option value="DUBO1" >Scioto River near Dublin, OH (DUSE2)</option>
      
        <option value="PRGO1" >Scioto River near Prospect, OH (PRSD2)</option>
      
        <option value="76060" >Seabrook Bridge - Inner Harbor Nav Canal (76060)</option>
      
        <option value="76062" >Seabrook Floodgate Closure Structure - IHNC Side (76062)</option>
      
        <option value="76065" >Seabrook Floodgate Closure Structure - Lake Side (76065)</option>
      
        <option value="82720" >Sellers Canal at Hwy 90 (Pier 90) (82720)</option>
      
        <option value="SNCO1" >Seneca Fork below Senecaville Dam near Senecaville, OH (SESOF)</option>
      
        <option value="KZUP1" >Seneca Power Upper Reservoir, PA (SURP)</option>
      
        <option value="RASP1" >Sevenmile Run near Rasselas, PA (RASP)</option>
      
        <option value="STYW2" >Sharps Knob near Slaty Fork, WV (SPKL8)</option>
      
        <option value="BOWW2" >Shavers Fork below Bowden, WV (BWDW)</option>
      
        <option value="SHR" >Sheep Ranch Weather</option>
      
        <option value="SHRI4" >Shell Rock River at Shell Rock, IA</option>
      
        <option value="RKFI4" >Shell Rock River near Rockford, IA</option>
      
        <option value="SHDP1" >Shenango Lake Outflow, PA (SHOP)</option>
      
        <option value="SHPP1" >Shenango River Lake, PA (SHNP)</option>
      
        <option value="NCSP1" >Shenango River at New Castle, PA (NCSP)</option>
      
        <option value="JMSP1" >Shenango River at Pymatuning Dam, PA (JMSP)</option>
      
        <option value="TRNP1" >Shenango River near Transfer, PA (TRNP)</option>
      
        <option value="CPRN8" >Sheyenne River at Cooperstown, ND - USGS Station No. 05057000</option>
      
        <option value="VCRN8" >Sheyenne River at Valley City, ND - USGS Station No. 05058500</option>
      
        <option value="BHTN8" >Sheyenne River below Baldhill Dam - USGS Station No. 05058000</option>
      
        <option value="WRWN8" >Sheyenne River near Warwick, ND - USGS Station No. 05056000</option>
      
        <option value="SHG" >Shirley Gulch</option>
      
        <option value="SHBO" >Shobe Creek near Heppner</option>
      
        <option value="DONO1" >Short Creek near Dillonvale, OH (DLLO)</option>
      
        <option value="SNCN6" >Sinclairville, NY (SNCN)</option>
      
        <option value="MENI2" >Sinsinawa River near Menominee, IL</option>
      
        <option value="03645" >Six Mile Lake NE of Verdunville (03645)</option>
      
        <option value="CE5E69CC" >Skuna River @ Bruce, MS</option>
      
        <option value="AGSI4" >Skunk River at Augusta, IA</option>
      
        <option value="MERI4" >Skunk River at Merrimac, IA</option>
      
        <option value="WURP1" >Slippery Rock Creek at Wurtemburg, PA (WURP)</option>
      
        <option value="SLPP1" >Slippery Rock, PA (SPPP)</option>
      
        <option value="GVST1" >Smiths Fork at Temperance Hall, TN</option>
      
        <option value="SLKM7" >Smithville Lake near Smithville, MO</option>
      
        <option value="HOLK1" >Soldier Creek Near Holton, KS</option>
      
        <option value="DELK1" >Soldier Creek near Delia, KS</option>
      
        <option value="TOPK1" >Soldier Creek near Topeka, KS</option>
      
        <option value="SMSP1" >Somerset, PA (SMRP)</option>
      
        <option value="VRNN8" >Souris River at Verendrye, ND - USGS Station No. 05120000</option>
      
        <option value="FOXN8" >Souris River near Foxholm, ND - USGS Station No. 05116000</option>
      
        <option value="SHWN8" >Souris River near Sherwood, ND - USGS Station No. 05114000</option>
      
        <option value="WSTN8" >Souris River near Westhope, ND - USGS Station No. 05124000</option>
      
        <option value="MINN8" >Souris River west of Minot, ND - USGS Station No. 05117500</option>
      
        <option value="DEKI2" >South Branch Kishwaukee River at De Kalb, IL</option>
      
        <option value="FDLI2" >South Branch Kishwaukee River near Fairdale, IL</option>
      
        <option value="WPNW3" >South Branch Rock River at Waupun, WI</option>
      
        <option value="NWKM7" >South Fabius River above Newark, MO</option>
      
        <option value="TAYM7" >South Fabius River near Taylor,MO </option>
      
        <option value="STRK2" >South Fork Cumberland River at Stearns, KY</option>
      
        <option value="FS105" >South Fork Forked Deer River At Jackson, TN</option>
      
        <option value="FS111" >South Fork Forked Deer River Near Halls, TN (North)</option>
      
        <option value="FS103" >South Fork Forked Deer River at Bells, TN</option>
      
        <option value="NPVI4" >South Fork Iowa River Northeast of New Providence, IA</option>
      
        <option value="03281500" >South Fork Kentucky River at Booneville</option>
      
        <option value="03252500" >South Fork Licking River at Cynthiana</option>
      
        <option value="BEEO1" >South Fork Licking River near Hebron, OH (HBLF3)</option>
      
        <option value="HPKK2" >South Fork Little River at Hopkinsville, KY</option>
      
        <option value="JFRN7" >South Fork New River near Jefferson, NC (JFST6)</option>
      
        <option value="OS111" >South Fork Obion River Near Kenton, TN (Northeast)</option>
      
        <option value="OS112" >South Fork Obion River Near McKenzie, TN (South)</option>
      
        <option value="HUSM5" >South Fork Root River at Houston, MN - USGS Station No. 05385500</option>
      
        <option value="ROCI2" >South Fork Sangamon River near Rochester, IL </option>
      
        <option value="HOLA4" >South Fourche LaFave River near Hollis</option>
      
        <option value="REDI4" >South Raccoon River at Redfield, IA</option>
      
        <option value="AKWI4" >South River near Ackworth, IA </option>
      
        <option value="CFXI4" >South Skunk River at Colfax, IA</option>
      
        <option value="AESI4" >South Skunk River below Squaw Creek near Ames, IA</option>
      
        <option value="AMEI4" >South Skunk River near Ames, IA</option>
      
        <option value="OOAI4" >South Skunk River near Oskaloosa, IA</option>
      
        <option value="CRKA4" >Spadra Creek at Clarksville</option>
      
        <option value="LNMI2" >Spoon River at London Mills, IL </option>
      
        <option value="SEVI2" >Spoon River at Seville, IL </option>
      
        <option value="IMBA4" >Spring River at Imboden</option>
      
        <option value="AMWI4" >Squaw Creek at Ames, IA</option>
      
        <option value="MK1" >St Johns River below McKay Pt Diversion</option>
      
        <option value="STLM5" >St. Croix River at Stillwater, MN</option>
      
        <option value="GTBW3" >St. Croix River near Grantsburg, WI</option>
      
        <option value="SF117" >St. Francis At St, Francis, AR</option>
      
        <option value="SB111" >St. Francis Bay At Riverfront, AR</option>
      
        <option value="SF114" >St. Francis River (Iron Bridge) At Wappapello, MO</option>
      
        <option value="SF136" >St. Francis River Above W.G. Huxtable Pumping Plant Near Marianna, AR </option>
      
        <option value="SF134" >St. Francis River At Cody, AR</option>
      
        <option value="SF116" >St. Francis River At Dekyns, Mo</option>
      
        <option value="SF115" >St. Francis River At Fisk, MO</option>
      
        <option value="SF123" >St. Francis River At Lake City, AR</option>
      
        <option value="SF133" >St. Francis River At Madison, AR</option>
      
        <option value="SF129" >St. Francis River At Parkin, AR</option>
      
        <option value="SF137" >St. Francis River Below W.G. Huxtable Pumping Plant Near Marianna, AR</option>
      
        <option value="SF119" >St. Francis River Near Kennett (Holly Island-West), MO </option>
      
        <option value="SF135" >St. Francis River Near Marianna, AR (Northeast)</option>
      
        <option value="SF126" >St. Francis River Near Tulot (Oak Donnick-Southeast), AR </option>
      
        <option value="SF127" >St. Francis River Siphon West Of Marked Tree, AR </option>
      
        <option value="SJ111" >St. Johns Bayou At Sikeston, MO</option>
      
        <option value="SC09" >Stagecoach Lake (Salt Creek Dam Site #09)</option>
      
        <option value="PA16" >Standing Bear Lake (Papio Creek Dam Site #16)</option>
      
        <option value="SL115" >State Line Outlet Ditch Near Pettyville, AR (West)</option>
      
        <option value="CE49572E" >Steele Bayou @ Grace, MS</option>
      
        <option value="16282F3E" >Steele Bayou @ Low Water Bridge</option>
      
        <option value="CE496C66" >Steele Bayou Control Structure (landside), MS</option>
      
        <option value="CZ496C66" >Steele Bayou Control Structure (riverside), MS</option>
      
        <option value="SBVO1" >Steubenville, OH (STBO)</option>
      
        <option value="TPPO1" >Stillwater Creek at Tippecanoe, OH (TISD6)</option>
      
        <option value="URVO1" >Stillwater Creek at Uhrichsville, OH (UHSD6)</option>
      
        <option value="PIEO1" >Stillwater Creek below Piedmont Dam near Piedmont, OH (PESOF)</option>
      
        <option value="03265000" >Stillwater River at Pleasent Hill</option>
      
        <option value="SET" >Stockton East Tunnel</option>
      
        <option value="STJW2" >Stonewall Jackson Lake Outflow, WV (SJOW)</option>
      
        <option value="JACW2" >Stonewall Jackson Lake, WV (SWJW)</option>
      
        <option value="FDLP1" >Stony Creek at Ferndale, PA (FDLP)</option>
      
        <option value="TNGK1" >Stranger Creek near Tonganoxie, KS</option>
      
        <option value="PKGA4" >Strawberry River near Poughkeepsie</option>
      
        <option value="03339500" >Sugar Creek at Crawfordsville</option>
      
        <option value="MILI2" >Sugar Creek at Milford, IL</option>
      
        <option value="BHLO1" >Sugar Creek below Beach City Dam near Beach City, OH (BCSOF)</option>
      
        <option value="SUGI2" >Sugar Creek near Springfield, IL</option>
      
        <option value="BROW3" >Sugar River near Brodhead, WI</option>
      
        <option value="SULW2" >Summersville Lake near Summersville, WV (SUGM7)</option>
      
        <option value="SUNO1" >Sunday Creek at Glouster, OH (GLSG4)</option>
      
        <option value="CE40871A" >Tallahatchie River @ Lambert, MS</option>
      
        <option value="CE485B06" >Tallahatchie River @ Locopolis, MS</option>
      
        <option value="DE167496" >Tallahatchie River @ Money, MS</option>
      
        <option value="CE40946C" >Tallahatchie River @ Swan Lake, MS</option>
      
        <option value="85402" >Tangipahoa River at Robert (85402)</option>
      
        <option value="07375430" >Tangipahoa River near Amite (USGS)</option>
      
        <option value="KENL1" >Tangipahoa River near Kentwood (USGS)</option>
      
        <option value="TAPO1" >Tappan Dam at Tappan, OH (TALD6)</option>
      
        <option value="TVLK2" >Taylorsville Lake</option>
      
        <option value="85500" >Tchefuncta River near Folsom (85500)</option>
      
        <option value="07375050" >Tchefuncte River near Covington (USGS)</option>
      
        <option value="MRAP1" >Tenmile Creek at Marianna, PA (MRAP)</option>
      
        <option value="CE3DF740" >Tensas Bayou @ Transylvania, LA</option>
      
        <option value="CE7F6AD8" >Tensas Cocodrie Pumping Plant (landside), LA</option>
      
        <option value="CE7F640A" >Tensas Cocodrie Pumping Plant (riverside), LA</option>
      
        <option value="CE69DE06" >Tensas River @ Clayton, LA</option>
      
        <option value="CE4932C8" >Tensas River @ Newlight, LA</option>
      
        <option value="CE69EB9C" >Tensas River @ Tendal, LA</option>
      
        <option value="TRMQ" >Terminus Dam Outflow (Kaweah River)</option>
      
        <option value="TRMP" >Terminus Dam Pool</option>
      
        <option value="BIGK1" >Test Station BIGK1</option>
      
        <option value="OOLO2" >Test of OOLO2</option>
      
        <option value="TFGW2" >Three Forks Creek near Grafton, WV (TFKW)</option>
      
        <option value="85302" >Tickfaw River at Holden (85302)</option>
      
        <option value="07375800" >Tickfaw River at Liverpool (USGS) </option>
      
        <option value="85300" >Tickfaw River at Springfield (85300)</option>
      
        <option value="MTWI4" >Timber Creek near Marshalltown, IA</option>
      
        <option value="LYNP1" >Tionesta Creek at Lynch, PA (LYNP)</option>
      
        <option value="TNTP1" >Tionesta Lake Outflow, PA (TNOP)</option>
      
        <option value="TIOP1" >Tionesta Lake, PA (TIOP)</option>
      
        <option value="03333050" >Tippecanoe River near Delphi</option>
      
        <option value="TTYP1" >Titusville, PA (TSVP)</option>
      
        <option value="TJLO1" >Tom Jenkins Lake near Burr Oak, OH (TJEG4)</option>
      
        <option value="LVGT1" >Town Creek at Livingston, TN</option>
      
        <option value="DDGW3" >Trempealeau River at Dodge, WI - USGS Station No. 05379500</option>
      
        <option value="TPTN7" >Triplett, NC (TRET6)</option>
      
        <option value="TRTV2" >Troutdale (Volney), VA (TRTV2)</option>
      
        <option value="WLCW2" >Tug Fork River at Welch, WV (WELP6)</option>
      
        <option value="WILW2" >Tug Fork River at Williamson, WV (WMSO4)</option>
      
        <option value="KRMW2" >Tug Fork River near Kermit, WV (KMTN4)</option>
      
        <option value="BRAP1" >Tunungwant Creek at Bradford, PA (BRFP)</option>
      
        <option value="EKDI4" >Turkey River above French Hollow Creek at Elkader, IA</option>
      
        <option value="GRBI4" >Turkey River at Garber, IA </option>
      
        <option value="SPLI4" >Turkey River at Spillville, IA</option>
      
        <option value="EDRI4" >Turkey River near Eldorado, IA</option>
      
        <option value="TRCM5" >Turtle Creek at Austin,MN</option>
      
        <option value="CLIW3" >Turtle Creek at Carvers Rock Road near Clinton, WI</option>
      
        <option value="WRDP1" >Turtle Creek at Wilmerding, PA (WILP)</option>
      
        <option value="DVLO1" >Tuscarawas River (tailwater) below Dover Dam near Dover, OH (DOTOF)</option>
      
        <option value="MLNO1" >Tuscarawas River at Massillon, OH (MATB5)</option>
      
        <option value="NWPO1" >Tuscarawas River at New Philadelphia, OH (NPTD6)</option>
      
        <option value="NCTO1" >Tuscarawas River at Newcomerstown, OH (NECD5)</option>
      
        <option value="171427A2" >Tuscolameta Creek @ Walnut Grove (South Canal)</option>
      
        <option value="1729E7AA" >Tuscolameta Creek @ Walnut Grove, MS</option>
      
        <option value="TU112" >Tuscumbia River Near Corinth, MS (West) </option>
      
        <option value="MTTK1" >Tuttle Creek Lake near Manhattan, KS</option>
      
        <option value="DUMM5" >Twelve Mile Creek near Dumont, MN</option>
      
        <option value="TMCM5" >Twelve Mile Creek near Wheaton, MN</option>
      
        <option value="LAVK2" >Twelvepole Creek at Lavalette, WV (LATL4)</option>
      
        <option value="WAYW2" >Twelvepole Creek below Wayne, WV (WAYM4)</option>
      
        <option value="SC13" >Twin Lakes (Salt Creek Dam site #13)</option>
      
        <option value="GRCP1" >Two Lick Creek at Graceton, PA. (GRCP)</option>
      
        <option value="TGOW2" >Tygart Lake Outflow, WV (TYOW)</option>
      
        <option value="TGLW2" >Tygart Lake, WV (TYGW)</option>
      
        <option value="BELW2" >Tygart River at Belington, WV (BELW)</option>
      
        <option value="CFXW2" >Tygart River at Colfax, WV (CFXW)</option>
      
        <option value="PHIW2" >Tygart River at Philippi, WV (PHIW)</option>
      
        <option value="DLYW2" >Tygart River near Dailey, WV (DATW)</option>
      
        <option value="ELKW2" >Tygart River near Elkins, WV (EKNW)</option>
      
        <option value="OLVK2" >Tygarts Creek at Olive Hill, KY (OVHL2)</option>
      
        <option value="TY113" >Tyronza River Near Twist, AR (East)</option>
      
        <option value="TY111" >Tyronza River Near Tyronza, AR (Northwest)</option>
      
        <option value="UCDP1" >Union City Dam Outflow, PA (UCOP)</option>
      
        <option value="UCTP1" >Union City Dam, PA (UCTP)</option>
      
        <option value="49570" >Upper Grand River (Flood Water Side)   (49570)</option>
      
        <option value="HINO" >Upper Hinton Creek below Kilkeeny Fork</option>
      
        <option value="DCHI4" >Upper Iowa River at Dorchester, IA - USGS Station No. 05388250</option>
      
        <option value="USAF" >Upper Saint Anthony Falls at Minneapolis, MN</option>
      
        <option value="UTL" >Upper Tyndall Weather</option>
      
        <option value="07387040" >Vermilion Bay near Cypremort Point, LA (USGS)</option>
      
        <option value="PNTI2" >Vermilion River at Pontiac, IL </option>
      
        <option value="03339000" >Vermilion River near Danville</option>
      
        <option value="LNRI2" >Vermilion River near Leonore, IL </option>
      
        <option value="VCWK1" >Vermillion Creek near LaClede, KS</option>
      
        <option value="VRGK2" >Virgie, KY (VIRP3)</option>
      
        <option value="FAYI4" >Volga River at Fayette, IA</option>
      
        <option value="VLPI4" >Volga River at Littleport, IA </option>
      
        <option value="LAWK1" >WAKARUSA R NR LAWRENCE KS</option>
      
        <option value="CR05E6E0" >WEIR</option>
      
        <option value="MCRI2P" >Wabash River @ Mount Carmel</option>
      
        <option value="03323500" >Wabash River at Huntington at JE Roush TW</option>
      
        <option value="03322900" >Wabash River at Linn Grove</option>
      
        <option value="03329000" >Wabash River at Logansport</option>
      
        <option value="03340500" >Wabash River at Montezuma</option>
      
        <option value="03327500" >Wabash River at Peru</option>
      
        <option value="03325000" >Wabash River at Wabash</option>
      
        <option value="CE7CB56C" >Wabbaseka Bayou @ Wabbaseka, AR</option>
      
        <option value="SC08" >Wagon Train Lake (Salt Creek Dam site #8)</option>
      
        <option value="FRAO1" >Wakatomika Creek near Frazeysburg, OH (FZWE4)</option>
      
        <option value="WHDO1" >Waldhonding River below Randale, OH (WALD5)</option>
      
        <option value="NLLO1" >Walhonding River (Tailwater) below Mohawk Dam at Nellie, OH (MKWOF)</option>
      
        <option value="BANV2" >Walker Creek at Bane, VA (BAWQ7)</option>
      
        <option value="85667" >Walker Drainage Structure - Flood Side (85667)</option>
      
        <option value="85666" >Walker Drainage Structure - Protected Side (85666)</option>
      
        <option value="CE02E4D4" >Walker Lake (Landside)</option>
      
        <option value="CZ02E4D4" >Walker Lake (Riverside)</option>
      
        <option value="CE41BEA8" >Wallace Lake Nr. Shreveport, LA (Pool)</option>
      
        <option value="CZ41BEA8" >Wallace Lake Nr. Shreveport, LA (tailwater)</option>
      
        <option value="DOSI4" >Walnut Creek at Des Moines, IA</option>
      
        <option value="HRTI4" >Walnut Creek near Hartwick, IA</option>
      
        <option value="SF113" >Wappapello Reservoir At Wappapello, MO</option>
      
        <option value="ANSI4" >Wapsipinicon River at Anamosa, IA</option>
      
        <option value="IDPI4" >Wapsipinicon River at Independence, IA </option>
      
        <option value="DEWI4" >Wapsipinicon River near De Witt, IA </option>
      
        <option value="TPLI4" >Wapsipinicon River near Tripoli, IA</option>
      
        <option value="HDGA4" >War Eagle Creek near Hindsville</option>
      
        <option value="SPST1" >Wartrace Creek at Springfield, TN</option>
      
        <option value="03336000" >Wasbash River at Covington</option>
      
        <option value="WCHO1" >Washington Courthouse, OH (WCHG2)</option>
      
        <option value="CE6A3428" >Wasp Lake Structure (Landside) Nr. Belzoni</option>
      
        <option value="CE6A298C" >Wasp Lake Structure (Riverside) Nr. Belzoni, MS</option>
      
        <option value="SAGDD" >Watson Sag Weir</option>
      
        <option value="SAGM5" >Watson Sag Weir and Chippewa Diversion near Watson, MN</option>
      
        <option value="76480" >Wax Lake East Drainage Area at Control Structure (76480)</option>
      
        <option value="03720" >Wax Lake Outlet at Calumet (03720)</option>
      
        <option value="PA20" >Wehrspann Lake (Papio Dam site #20)</option>
      
        <option value="01516" >West Bay Receiving Area - Outflow (01516)</option>
      
        <option value="WCXP1" >West Branch Clarion River at Wilcox, PA (WCXP)</option>
      
        <option value="NAWI2" >West Branch Du Page River near Naperville, IL</option>
      
        <option value="LVLP1" >West Branch French Creek near Lowville, PA (LOWP)</option>
      
        <option value="RVNO1" >West Branch Mahoning River at Ravenna, OH (RAVO)</option>
      
        <option value="DMTM5" >West Branch Twelve Mile Creek at Dumont, MN</option>
      
        <option value="FNHI4" >West Fork Cedar River at Finchford, IA</option>
      
        <option value="HBTI4" >West Fork Des Moines River at Humboldt, IA</option>
      
        <option value="JCKM5" >West Fork Des Moines River at Jackson, MN</option>
      
        <option value="EMTI4" >West Fork Des Moines River near Emmetsburg, IA </option>
      
        <option value="ESVI4" >West Fork Des Moines River near Estherville, IA </option>
      
        <option value="WDOM5" >West Fork Des Moines River near Windom, MN</option>
      
        <option value="03313700" >West Fork Drakes Creek nr Franklin</option>
      
        <option value="WFRO1" >West Fork Lake</option>
      
        <option value="RCKW2" >West Fork Little Kanawha River at Rocksdale, WV (ROWJ6)</option>
      
        <option value="03255500" >West Fork Mill Creek at Reading</option>
      
        <option value="ALPT1" >West Fork Obey River near Alpine, TN</option>
      
        <option value="HTVA4" >West Fork Point Remove Creek near Hattieville</option>
      
        <option value="BCVW2" >West Fork River at Butcherville, WV (BUTW)</option>
      
        <option value="CLKW2" >West Fork River at Clarksburg, WV (CLKW)</option>
      
        <option value="ENTW2" >West Fork River at Enterprise, WV (ENTW)</option>
      
        <option value="WLKW2" >West Fork River at Walkersville, WV (WLKW)</option>
      
        <option value="WTNW2" >West Fork River at Weston, WV (WTNW)</option>
      
        <option value="MUGT1" >West Fork Stones River at Murfreesboro, TN</option>
      
        <option value="WST" >Westfall Ranger St Weather</option>
      
        <option value="WTM" >Wet Meadows Weather</option>
      
        <option value="WBGK2" >Wheelersburg, KY (WHLN3)</option>
      
        <option value="WHEW2P" >Wheeling Creek @ Elm Grove</option>
      
        <option value="WHEW2" >Wheeling Creek at Elm Grove, WV (WHEW)</option>
      
        <option value="03240" >Whiskey Bay Pilot Channel Below Head (03240)</option>
      
        <option value="DLLI4" >White Breast Creek near Dallas, IA </option>
      
        <option value="WR116" >White River At Clarendon, AR</option>
      
        <option value="WR115" >White River At De Valls Bluff, AR</option>
      
        <option value="WR114" >White River At Des Arc, AR</option>
      
        <option value="WR118" >White River At St. Charles, AR</option>
      
        <option value="BAGA4" >White River at Batesville</option>
      
        <option value="BVGA4" >White River at Beaver Dam - HW & TW</option>
      
        <option value="BSGA4" >White River at Bull Shoals Dam - HW & TW</option>
      
        <option value="BULDO" >White River at Bull Shoals Dam - WQ</option>
      
        <option value="CLRA4" >White River at Calico Rock</option>
      
        <option value="GEOA4" >White River at Georgetown</option>
      
        <option value="WRNA4" >White River at Highway 341 bridge</option>
      
        <option value="03372500" >White River at Monroe Lake Tail Water</option>
      
        <option value="MPDA4" >White River at Montgomery Point Lock & Dam</option>
      
        <option value="03360500" >White River at Newberry</option>
      
        <option value="NPTA4" >White River at Newport</option>
      
        <option value="03373980" >White River at Petersburg (USGS)</option>
      
        <option value="03374000" >White River at Petersburgh</option>
      
        <option value="PSZM7" >White River at Powersite Dam</option>
      
        <option value="SOGM7" >White River at School of the Ozarks</option>
      
        <option value="03365500" >White River at Seymour</option>
      
        <option value="03373500" >White River at Shoals</option>
      
        <option value="03357000" >White River at Spencer</option>
      
        <option value="SYGA4" >White River at Sylamore</option>
      
        <option value="FORM7" >White River at Table Rock Dam - HW & TW</option>
      
        <option value="BEADO" >White River below Beaver Dam (WQ)</option>
      
        <option value="BULRB" >White River below Bull Shoals Dam on right bank - WQ</option>
      
        <option value="FARVW" >White River below Bull Shoals near Fairview - WQ</option>
      
        <option value="TBZM7" >White River below Table Rock Dam - WQ</option>
      
        <option value="INBUL" >White River inside Bull Shoals Dam (WQ)</option>
      
        <option value="AUGA4" >White River near Augusta</option>
      
        <option value="FYGA4" >White River near Fayetteville</option>
      
        <option value="03354000" >White River nr Centerton</option>
      
        <option value="WHRDD" >White Rock Dam</option>
      
        <option value="SUPW2" >White Sulphur Springs, WV (WSSN8)</option>
      
        <option value="03275000" >Whitewater River at Alpine</option>
      
        <option value="03276500" >Whitewater River at Brookville</option>
      
        <option value="WTMW2" >Whitmer, WV (WTMW)</option>
      
        <option value="WLBN7" >Wilbar, NC (WBRT6)</option>
      
        <option value="03335000" >Wildcat Creek near Lafayette</option>
      
        <option value="WLLK2" >Willard, KY (WILL3)</option>
      
        <option value="BHDO1" >William H. Harsha Lake</option>
      
        <option value="WLLV2" >Willis, VA (WILR8)</option>
      
        <option value="WIL" >Willow Creek Reservoir</option>
      
        <option value="HWLO" >Willow Creek above Lake</option>
      
        <option value="WILO" >Willow Creek at Heppner</option>
      
        <option value="WIMO" >Willow Creek at Morgan Street Bridge</option>
      
        <option value="WCLO1" >Wills Creek Lake at Wills Creek Dam near Conesville, OH (WCWE5)</option>
      
        <option value="CDIO1" >Wills Creek at Cambridge, OH (CAWE5)</option>
      
        <option value="DWTO1" >Wills Creek at Derwent, OH (DRWF5)</option>
      
        <option value="WLLO1" >Wills Creek below Wills Creek Dam near Conesville, OH (WCWOF)</option>
      
        <option value="MCWI4" >Winnebago River at Mason City, IA</option>
      
        <option value="MUSW3" >Wisconsin River at Muscoda, WI - USGS Station No. 05407000</option>
      
        <option value="DYSI4" >Wolf Creek near Dysart, IA</option>
      
        <option value="WOLV2" >Wolf Creek near Narrows, VA (NARP7)</option>
      
        <option value="WOLW2" >Wolf Pen, WV (WOPO5)</option>
      
        <option value="WF111" >Wolf River At Raleigh, TN</option>
      
        <option value="BYGT1" >Wolf River near Byrdstown TN</option>
      
        <option value="WCDP1" >Woodcock Creek Lake Outflow, PA (WCOP)</option>
      
        <option value="MEAP1" >Woodcock Creek Lake, PA (WCRP)</option>
      
        <option value="BVLP1" >Woodcock Creek at Blooming Valley, PA (BVLP)</option>
      
        <option value="WODO1" >Woodsfield, OH (WFDO)</option>
      
        <option value="CIPO1" >Wooster, OH (WOSC4)</option>
      
        <option value="49415" >Workman Canal near I-10 (49415)</option>
      
        <option value="CNZM7" >Wyaconda River near Canton,MO </option>
      
        <option value="177117CA" >Yackanookany River @ Ofahoma, MS</option>
      
        <option value="FULW3" >Yahara River near Fulton, WI</option>
      
        <option value="CE5E671E" >Yalobusha River @ Calhoun City, MS</option>
      
        <option value="CE417BB6" >Yalobusha River @ Grenada Dam (Inlet)</option>
      
        <option value="CE7F777C" >Yalobusha River @ Grenada Dam (Outlet)</option>
      
        <option value="16E7F572" >Yalobusha River @ Grenada, MS</option>
      
        <option value="CE48604E" >Yalobusha River @ Holcomb, MS</option>
      
        <option value="CE409ABE" >Yalobusha River @ Whaley, MS</option>
      
        <option value="SC10" >Yankee Hill Lake (Salt Creek Dam site #10)</option>
      
        <option value="YTUK2" >Yatesville Lake near Louisa, KY (YBCM3)</option>
      
        <option value="CE48E65A" >Yazoo River @ Alligator-Catfish Structure (landside), MS</option>
      
        <option value="CE506DA4" >Yazoo River @ Alligator-Catfish Structure (riverside), MS</option>
      
        <option value="CE48D3C0" >Yazoo River @ Belzoni, MS</option>
      
        <option value="CE502EAE" >Yazoo River @ Fort Pemberton Cutoff (downstream)</option>
      
        <option value="CE4855D4" >Yazoo River @ Fort Pemberton Cutoff (upstream)</option>
      
        <option value="CE4185E0" >Yazoo River @ Greenwood, MS</option>
      
        <option value="CE5E979A" >Yazoo River @ Shell Bluff, MS</option>
      
        <option value="CE48A550" >Yazoo River @ Yazoo City Pumping Station (landside)</option>
      
        <option value="CZ48A550" >Yazoo River @ Yazoo City Pumping Station (riverside)</option>
      
        <option value="CE69C3A2" >Yazoo River @ Yazoo City, MS</option>
      
        <option value="ODSM5" >Yellow Bank River at Odessa, MN - USGS Station No. 05293000</option>
      
        <option value="EMGT1" >Yellow Creek at Ellis Mills, TN</option>
      
        <option value="YELO1" >Yellow Creek near Hammondsville, OH (HMMO)</option>
      
        <option value="MDLK2" >Yellow Creek near Middlesboro, KY</option>
      
        <option value="KNXI3" >Yellow River at Knox, IN</option>
      
        <option value="PYMI3" >Yellow River at Plymouth, IN</option>
      
        <option value="1770B5C8" >Yockanookany River @ Kosciusko, MS</option>
      
        <option value="CE417564" >Yocona River @ Enid Dam, MS (Intake)</option>
      
        <option value="CE507000" >Yocona River @ Enid Dam, MS (Outlet)</option>
      
        <option value="CE5EFCAE" >Yocona River @ Oxford, MS</option>
      
        <option value="YKL" >Yokohl Creek</option>
      
        <option value="YGOP1" >Youghiogheny River Lake Outflow, PA (YGOP)</option>
      
        <option value="YGBP1" >Youghiogheny River Lake, PA (Buttonhook) (YGBP)</option>
      
        <option value="YOUP1" >Youghiogheny River Lake, PA (Route 40) (YOUO)</option>
      
        <option value="CLLP1" >Youghiogheny River at Connellsville, PA (CLLP)</option>
      
        <option value="FRDM2" >Youghiogheny River at Friendsville, MD (FRDM)</option>
      
        <option value="OPLP1" >Youghiogheny River at Ohiopyle State Park, PA (OHIP)</option>
      
        <option value="STSP1" >Youghiogheny River at Sutersville, PA (STSP)</option>
      
        <option value="CNFP1" >Youghiogheny River below Confluence, PA (CNFP)</option>
      
        <option value="OAKM2" >Youghiogheny River near Oakland, MD (OAKM)</option>
      
        <option value="PA18" >Zorinsky Lake (Papio Dam site #18)</option>
      
        <option value="ZUMM5" >Zumbro River at Zumbro Falls, MN - USGS Station No. 05374000</option>
      
        <option value="BIRO2" >test BIRO2</option>
      
    </select>
  </font></font></div></td>
</tr>

<tr bgcolor=#000055>
  <td bgcolor="#000055" class="style11"><div align="center"><font size="2"><font color="#FFFFFF">Choose
A Parameter<br>
<select name="fld_parameter" id="fld_parameter">
  <option value="" selected >-----</option>
  
    <option value="PC" >Cumulative Precipitation (In)</option>
  
    <option value="HP" selected>Pool Level (Ft)</option>
  
</select>
  </font></font></div></td>
</tr>

<tr bgcolor="000055">
  <td bgcolor="000055" class="style11"><div align="center"><font size="2"><font color="FFFFFF">Levels Are Between<br>
  
            <input name="fld_from" type="text" id="fld_from" value="-9000000" size="4" maxlength="7">
And <font size="2">
<input name="fld_to" type="text" id="fld_to" value="9000000" size="4" maxlength="7">
</font></font></font><br>
  </div></td>
</tr>
<tr bgcolor="000055">
<td bgcolor="000055" class="style11"> <div align="center"><font size="2"><font color="FFFFFF">Dates Are Between<br>
          <input name="fld_fromdate" type="text" id="fld_fromdate" value="1/1/2013" size="10" maxlength="10" onBlur="validateDate(document.frm_mining.fld_fromdate);">
          <!--
CF_CAL Custom Tag

Jason Bukowski
4 Brattle Circle
Cambridge, MA 02138
6/28/2000

UPDATED 7/11/2000
- Fixed Netscape bug
- Fixed Multiple Instances Bug
- Minor UI Improvment

jbukowski@dataware.com

Update 06/06/2005
 - added leap year functionality
 nick@cfconsulting.net

CF_CAL is designed to place a button that activates a popup calendar. The user may browse though the calendar and select
and date he wants by clicking on it. 
That date is then send back to a definded text field in a defined form in the format MM/DD/YYYY. 

To Use:
Paramteres-- formname target date image 

REQUIRED:
	formname - the name of the form you want the date inserted into
	target - the name of the text field in that form
OPTIONAL
	date - the date the calendar opens to. Default is current.
	image - the graphic to appear as the button. Default is [C] -- path is relative to calling page.
-->

<script language="JavaScript">

var months = new Array("January","February","March","April","May","June","July","August","September","October","November","December")



function openCalWin_fld_fromdate() { 
	stats='toolbar=no,location=no,directories=no,status=no,menubar=no,'
	stats += 'scrollbars=no,resizable=no,width=275,height=225'
	CalWin = window.open ("","Calendar",stats)
	
	
	var calMonth = 2
	var calYear = 2013
	
	
	theDate = new Date(calYear, (calMonth - 1), 1)

	buildCal_fld_fromdate(theDate)
	
}

function buildCal_fld_fromdate(theDate) {
	
	var startDay = theDate.getDay()
	var printDays = false
	var currDay = 1
	var rowsNeeded = 5
	var tstyear = theDate.getYear();
	if (isLeapYear(tstyear)){
		var totalDays = new Array(31,29,31,30,31,30,31,31,30,31,30,31)
	}
	else{
		var totalDays = new Array(31,28,31,30,31,30,31,31,30,31,30,31)
	}
	if (startDay + totalDays[theDate.getMonth()] > 35)
		rowsNeeded++
	
	CalWin.document.write('<html><head><Title>Select a Date</title>')
	CalWin.document.write('<STYLE TYPE="text/css">')
	CalWin.document.write('A { color: #000000; font-family:Arial,Helvetica;font-size:10pt; font-weight: bold; text-decoration: none}')
	CalWin.document.write('A:hover { color: red; }')
	CalWin.document.write('.dayHead { color: #FFFFFF; font-family:Arial,Helvetica;font-size:10pt; font-weight: bold}')
	CalWin.document.write('</STYLE></head>')
	CalWin.document.write('<body><a name="this"></a>')
	CalWin.document.write('<table align=center height=100% width=100% border=2 bordercolor=Black cellpadding=0 cellspacing=0>')
	CalWin.document.write('<tr><th bgcolor="#003366" colspan=7><span class="dayHead">' + months[theDate.getMonth()] + ' ' + theDate.getFullYear() + '</span></th></tr>')
	CalWin.document.write('<tr bgcolor="#999999" class="dayHead"><th>Su</th><th>Mo</th><th>Tu</th><th>We</th><th>Th</th><th>Fr</th><th>Sa</th></tr>')
	for (x=1; x<=rowsNeeded; x++){
		CalWin.document.write('<tr>')
		for (y=0; y<=6; y++){
			if (currDay == 1 && !printDays && startDay == y)
				printDays = true
			CalWin.document.write('<td align="center" width=14.28%>')
			if (printDays){
        		CalWin.document.write('<a href="javascript:opener.placeDate_fld_fromdate(' +  currDay + ',' + theDate.getMonth() + ',' + theDate.getFullYear() + ')">' + currDay++ + '</a></td>')
				if (currDay > totalDays[theDate.getMonth()])
					printDays = false
			}
			else
				CalWin.document.write('&nbsp;</td>')
		}		
		CalWin.document.write('</tr>')
	}	
	CalWin.document.write('<form><tr bgcolor="#999999"><td colspan=7 align="center"><input type="Button" size="1" name="Back" value="<<" onClick="opener.getNewCal_fld_fromdate(-1)"><font face=Arial color=white size="1"> Previous Month | Next Month </font> <input type="Button" size="1" name="Forward" value=">>" onClick="opener.getNewCal_fld_fromdate(1)"></td></tr></form>')
	CalWin.document.write('</table></body></html>')
	CalWin.document.close()
	
}

function getNewCal_fld_fromdate(newDir) {
	if (newDir == -1){
		theDate.setMonth(theDate.getMonth() - 1)
		if (theDate.getMonth() == 0){
			theDate.setMonth(12)
			theDate.setYear(theDate.getYear() - 1)
		}
	}
	else if (newDir == 1){
		theDate.setMonth(theDate.getMonth() + 1)
		if (theDate.getMonth() == 13){
			theDate.setMonth(1)
			theDate.setYear(theDate.getYear() + 1)
		}
	}
		
		
	CalWin.document.clear();
	buildCal_fld_fromdate(theDate);

}

function placeDate_fld_fromdate(dayNum, monthNum, yearNum){
	//var dateString = dayNum + '/' + (monthNum + 1) + '/' + yearNum
	var dateString = (monthNum + 1) + '/' + dayNum + '/' + yearNum
	document.frm_mining.fld_fromdate.value = dateString
		 
	CalWin.close()
}
function isLeapYear (Year) {
	if (((Year % 4)==0) && ((Year % 100)!=0) || ((Year % 400)==0)) {
		return (true);
	} 
	else { 
	return (false); 
	}
}


</script>
 

<a href="javascript:openCalWin_fld_fromdate()"><img src="/WaterControl/images/cal.gif" border=0></a>

 And
 <input name="fld_todate" type="text" id="fld_todate" value="1/15/2013" size="10" maxlength="10" onBlur="validateDate(document.frm_mining.fld_todate);">
 <!--
CF_CAL Custom Tag

Jason Bukowski
4 Brattle Circle
Cambridge, MA 02138
6/28/2000

UPDATED 7/11/2000
- Fixed Netscape bug
- Fixed Multiple Instances Bug
- Minor UI Improvment

jbukowski@dataware.com

Update 06/06/2005
 - added leap year functionality
 nick@cfconsulting.net

CF_CAL is designed to place a button that activates a popup calendar. The user may browse though the calendar and select
and date he wants by clicking on it. 
That date is then send back to a definded text field in a defined form in the format MM/DD/YYYY. 

To Use:
Paramteres-- formname target date image 

REQUIRED:
	formname - the name of the form you want the date inserted into
	target - the name of the text field in that form
OPTIONAL
	date - the date the calendar opens to. Default is current.
	image - the graphic to appear as the button. Default is [C] -- path is relative to calling page.
-->

<script language="JavaScript">

var months = new Array("January","February","March","April","May","June","July","August","September","October","November","December")



function openCalWin_fld_todate() { 
	stats='toolbar=no,location=no,directories=no,status=no,menubar=no,'
	stats += 'scrollbars=no,resizable=no,width=275,height=225'
	CalWin = window.open ("","Calendar",stats)
	
	
	var calMonth = 2
	var calYear = 2013
	
	
	theDate = new Date(calYear, (calMonth - 1), 1)

	buildCal_fld_todate(theDate)
	
}

function buildCal_fld_todate(theDate) {
	
	var startDay = theDate.getDay()
	var printDays = false
	var currDay = 1
	var rowsNeeded = 5
	var tstyear = theDate.getYear();
	if (isLeapYear(tstyear)){
		var totalDays = new Array(31,29,31,30,31,30,31,31,30,31,30,31)
	}
	else{
		var totalDays = new Array(31,28,31,30,31,30,31,31,30,31,30,31)
	}
	if (startDay + totalDays[theDate.getMonth()] > 35)
		rowsNeeded++
	
	CalWin.document.write('<html><head><Title>Select a Date</title>')
	CalWin.document.write('<STYLE TYPE="text/css">')
	CalWin.document.write('A { color: #000000; font-family:Arial,Helvetica;font-size:10pt; font-weight: bold; text-decoration: none}')
	CalWin.document.write('A:hover { color: red; }')
	CalWin.document.write('.dayHead { color: #FFFFFF; font-family:Arial,Helvetica;font-size:10pt; font-weight: bold}')
	CalWin.document.write('</STYLE></head>')
	CalWin.document.write('<body><a name="this"></a>')
	CalWin.document.write('<table align=center height=100% width=100% border=2 bordercolor=Black cellpadding=0 cellspacing=0>')
	CalWin.document.write('<tr><th bgcolor="#003366" colspan=7><span class="dayHead">' + months[theDate.getMonth()] + ' ' + theDate.getFullYear() + '</span></th></tr>')
	CalWin.document.write('<tr bgcolor="#999999" class="dayHead"><th>Su</th><th>Mo</th><th>Tu</th><th>We</th><th>Th</th><th>Fr</th><th>Sa</th></tr>')
	for (x=1; x<=rowsNeeded; x++){
		CalWin.document.write('<tr>')
		for (y=0; y<=6; y++){
			if (currDay == 1 && !printDays && startDay == y)
				printDays = true
			CalWin.document.write('<td align="center" width=14.28%>')
			if (printDays){
        		CalWin.document.write('<a href="javascript:opener.placeDate_fld_todate(' +  currDay + ',' + theDate.getMonth() + ',' + theDate.getFullYear() + ')">' + currDay++ + '</a></td>')
				if (currDay > totalDays[theDate.getMonth()])
					printDays = false
			}
			else
				CalWin.document.write('&nbsp;</td>')
		}		
		CalWin.document.write('</tr>')
	}	
	CalWin.document.write('<form><tr bgcolor="#999999"><td colspan=7 align="center"><input type="Button" size="1" name="Back" value="<<" onClick="opener.getNewCal_fld_todate(-1)"><font face=Arial color=white size="1"> Previous Month | Next Month </font> <input type="Button" size="1" name="Forward" value=">>" onClick="opener.getNewCal_fld_todate(1)"></td></tr></form>')
	CalWin.document.write('</table></body></html>')
	CalWin.document.close()
	
}

function getNewCal_fld_todate(newDir) {
	if (newDir == -1){
		theDate.setMonth(theDate.getMonth() - 1)
		if (theDate.getMonth() == 0){
			theDate.setMonth(12)
			theDate.setYear(theDate.getYear() - 1)
		}
	}
	else if (newDir == 1){
		theDate.setMonth(theDate.getMonth() + 1)
		if (theDate.getMonth() == 13){
			theDate.setMonth(1)
			theDate.setYear(theDate.getYear() + 1)
		}
	}
		
		
	CalWin.document.clear();
	buildCal_fld_todate(theDate);

}

function placeDate_fld_todate(dayNum, monthNum, yearNum){
	//var dateString = dayNum + '/' + (monthNum + 1) + '/' + yearNum
	var dateString = (monthNum + 1) + '/' + dayNum + '/' + yearNum
	document.frm_mining.fld_todate.value = dateString
		 
	CalWin.close()
}
function isLeapYear (Year) {
	if (((Year % 4)==0) && ((Year % 100)!=0) || ((Year % 400)==0)) {
		return (true);
	} 
	else { 
	return (false); 
	}
}


</script>
 

<a href="javascript:openCalWin_fld_todate()"><img src="/WaterControl/images/cal.gif" border=0></a>

 <br>
 Data Available Between 1911 And 2013<br>
</font></font></div></td>
</tr>

<tr bgcolor="#000055">
  <td bgcolor="#000055"><div align="center"><font size="2"><strong><font color="#FFFFFF">
    <input type="button" name="Button" value="Search" onClick="validate()">
  </font></strong></font></div></td>
</tr>

<tr bgcolor=#FFFFFF>
  <td><table width="640" align="center">
    <tr bgcolor=#000055 class="style11">
      <td colspan="2" bgcolor="#000055"><div align="center"><font color="#FFFFFF">Your Search Has Returned The Following Results:</font></div></td>
    </tr>
    <tr>
      <td colspan="2"><table width="640" align="center">
        <tr valign="top" class="style11">
          <td colspan="2"><div align="center"><b><strong>Data Mining For </strong>Caddo Lake Dam, LA</b></div></td>
          </tr>
        <tr valign="top" class="style11">
          <td>
      Gage Zero: 0 Ft. NGVD29<br>
      
        Record High&nbsp;
        Stage 
        : 182.59 Ft. </td>
          <td>Longitude: -93.91866300<br>
      Latitude: 32.70437900 
      <br>
      River Mile: <br>
      
        Record High&nbsp;
        Stage 
        Date: 05/05/1958 </td>
        </tr>
        <tr valign="top" class="style11">
          <td colspan="2"><div align="center">Location of Gage: <p>3 miles northeast of Mooringsport, LA.</p></div></td>
          </tr>
      </table></td>
    </tr>
    <tr>
      <td colspan="2"><table width="300" align="center">
          <tr class="style11">
            <td colspan="2"><div align="center" style="cursor:hand"><font color="#0000FF"><u onclick="document.frm_mining.hdn_excel.value = 'y'; document.frm_mining.submit()">Download Data
                        <input name="hdn_excel" type="hidden" id="hdn_excel" value="">
            </u></font></div></td>
          </tr>
          <tr class="style11">
            <td><div align="center"><strong>Date</strong></div></td>
            <td><div align="center"><strong>Value</strong></div></td>
          </tr>
          
            <tr class="style11">
              <td><div align="center">01/15/2013 08:00</div></td>
              <td><div align="center">
                       168.69 
              </div></td>
            </tr>
          
            <tr class="style11">
              <td><div align="center">01/14/2013 08:00</div></td>
              <td><div align="center">
                       168.52 
              </div></td>
            </tr>
          
            <tr class="style11">
              <td><div align="center">01/13/2013 08:00</div></td>
              <td><div align="center">
                       168.62 
              </div></td>
            </tr>
          
            <tr class="style11">
              <td><div align="center">01/12/2013 08:00</div></td>
              <td><div align="center">
                       168.51 
              </div></td>
            </tr>
          
            <tr class="style11">
              <td><div align="center">01/11/2013 08:00</div></td>
              <td><div align="center">
                       168.46 
              </div></td>
            </tr>
          
            <tr class="style11">
              <td><div align="center">01/10/2013 08:00</div></td>
              <td><div align="center">
                       168.39 
              </div></td>
            </tr>
          
            <tr class="style11">
              <td><div align="center">01/09/2013 08:00</div></td>
              <td><div align="center">
                       168.23 
              </div></td>
            </tr>
          
            <tr class="style11">
              <td><div align="center">01/08/2013 08:00</div></td>
              <td><div align="center">
                       167.81 
              </div></td>
            </tr>
          
            <tr class="style11">
              <td><div align="center">01/07/2013 08:00</div></td>
              <td><div align="center">
                       168.05 
              </div></td>
            </tr>
          
            <tr class="style11">
              <td><div align="center">01/06/2013 08:00</div></td>
              <td><div align="center">
                       167.62 
              </div></td>
            </tr>
          
            <tr class="style11">
              <td><div align="center">01/05/2013 08:00</div></td>
              <td><div align="center">
                       168.08 
              </div></td>
            </tr>
          
            <tr class="style11">
              <td><div align="center">01/04/2013 08:00</div></td>
              <td><div align="center">
                       168.10 
              </div></td>
            </tr>
          
            <tr class="style11">
              <td><div align="center">01/03/2013 08:00</div></td>
              <td><div align="center">
                       167.91 
              </div></td>
            </tr>
          
            <tr class="style11">
              <td><div align="center">01/02/2013 08:00</div></td>
              <td><div align="center">
                       167.95 
              </div></td>
            </tr>
          
            <tr class="style11">
              <td><div align="center">01/01/2013 08:00</div></td>
              <td><div align="center">
                       168.04 
              </div></td>
            </tr>
          
      </table></td>
    </tr>
  </table></td>
</tr>

</table>
</form>


</td>
</tr>
</table>
</body>
</html>
