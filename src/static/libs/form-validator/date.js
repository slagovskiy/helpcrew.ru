/** File generated by Grunt -- do not modify
 *  JQUERY-FORM-VALIDATOR
 *
 *  @version 2.3.73
 *  @website http://formvalidator.net/
 *  @author Victor Jonsson, http://victorjonsson.se
 *  @license MIT
 */
!function(a,b){"function"==typeof define&&define.amd?define(["jquery"],function(a){return b(a)}):"object"==typeof module&&module.exports?module.exports=b(require("jquery")):b(a.jQuery)}(this,function(a){!function(a){function b(a,b,c){var d=new Date,e=new Date;return d.setYear(a),d.setMonth(b),d.setDate(c),new Date(e.getTime()-d.getTime()).getUTCFullYear()-1970}a.formUtils.registerLoadedModule("date"),a.formUtils.addValidator({name:"time",validatorFunction:function(a){if(null===a.match(/^(\d{2}):(\d{2})$/))return!1;var b=parseInt(a.split(":")[0],10),c=parseInt(a.split(":")[1],10);return!(b>23||c>59)},errorMessage:"",errorMessageKey:"badTime"}),a.formUtils.addValidator({name:"birthdate",validatorFunction:function(c,d,e){var f="yyyy-mm-dd";d.valAttr("format")?f=d.valAttr("format"):"undefined"!=typeof e.dateFormat&&(f=e.dateFormat);var g=a.formUtils.parseDate(c,f);if(!g)return!1;var h=g[0],i=g[1],j=g[2],k=b(h,i,j),l=(d.valAttr("age-range")||"0-124").split("-");if(2!==l.length||!a.isNumeric(l[0])||!a.isNumeric(l[1]))throw new Error("Date range format invalid");return k>=l[0]&&k<=l[1]},errorMessage:"",errorMessageKey:"badDate"})}(a)});