(function(t){function e(e){for(var a,r,s=e[0],u=e[1],l=e[2],d=0,g=[];d<s.length;d++)r=s[d],Object.prototype.hasOwnProperty.call(o,r)&&o[r]&&g.push(o[r][0]),o[r]=0;for(a in u)Object.prototype.hasOwnProperty.call(u,a)&&(t[a]=u[a]);c&&c(e);while(g.length)g.shift()();return i.push.apply(i,l||[]),n()}function n(){for(var t,e=0;e<i.length;e++){for(var n=i[e],a=!0,s=1;s<n.length;s++){var u=n[s];0!==o[u]&&(a=!1)}a&&(i.splice(e--,1),t=r(r.s=n[0]))}return t}var a={},o={app:0},i=[];function r(e){if(a[e])return a[e].exports;var n=a[e]={i:e,l:!1,exports:{}};return t[e].call(n.exports,n,n.exports,r),n.l=!0,n.exports}r.m=t,r.c=a,r.d=function(t,e,n){r.o(t,e)||Object.defineProperty(t,e,{enumerable:!0,get:n})},r.r=function(t){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(t,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(t,"__esModule",{value:!0})},r.t=function(t,e){if(1&e&&(t=r(t)),8&e)return t;if(4&e&&"object"===typeof t&&t&&t.__esModule)return t;var n=Object.create(null);if(r.r(n),Object.defineProperty(n,"default",{enumerable:!0,value:t}),2&e&&"string"!=typeof t)for(var a in t)r.d(n,a,function(e){return t[e]}.bind(null,a));return n},r.n=function(t){var e=t&&t.__esModule?function(){return t["default"]}:function(){return t};return r.d(e,"a",e),e},r.o=function(t,e){return Object.prototype.hasOwnProperty.call(t,e)},r.p="/";var s=window["webpackJsonp"]=window["webpackJsonp"]||[],u=s.push.bind(s);s.push=e,s=s.slice();for(var l=0;l<s.length;l++)e(s[l]);var c=u;i.push([0,"chunk-vendors"]),n()})({0:function(t,e,n){t.exports=n("56d7")},"034f":function(t,e,n){"use strict";var a=n("85ec"),o=n.n(a);o.a},"56d7":function(t,e,n){"use strict";n.r(e);n("e260"),n("e6cf"),n("cca6"),n("a79d");var a=n("2b0e"),o=function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",{attrs:{id:"app"}},[n("navbar"),n("mainBody")],1)},i=[],r=function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",[n("b-navbar",{attrs:{toggleable:"lg",type:"dark",variant:"dark",fixed:"top"}},[n("b-navbar-brand",{attrs:{href:"#"}},[t._v("Watering System Console")]),n("b-navbar-toggle",{attrs:{target:"nav-collapse"}}),n("b-collapse",{attrs:{id:"nav-collapse","is-nav":""}},[n("b-navbar-nav",{staticClass:"ml-auto"},[n("b-navbar-nav",[n("b-nav-text",{staticClass:"mr-2"},[t._v("Current Time:")]),n("b-nav-text",[t._v(" "+t._s(t.curr_time))])],1)],1)],1)],1)],1)},s=[],u={name:"navbar",data:function(){return{curr_time:null}},created:function(){setInterval(this.getNow,1e3)},methods:{getNow:function(){var t=new Date,e=t.getFullYear()+"-"+(t.getMonth()+1)+"-"+t.getDate(),n=t.getHours()+":"+(t.getMinutes()<10?"0":"")+t.getMinutes()+":"+(t.getSeconds()<10?"0":"")+t.getSeconds();this.curr_time=e+" "+n}}},l=u,c=n("2877"),d=Object(c["a"])(l,r,s,!1,null,"c3d2386e",null),g=d.exports,m=function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("b-container",{attrs:{fluid:""}},[n("b-row",{staticClass:"pt-1"},[n("b-col",{staticStyle:{"padding-right":"2rem","border-right":"0.1rem solid #ccc"}},[n("indexStatus",{staticStyle:{"padding-bottom":"1rem","border-bottom":"0.1rem solid #ccc"}}),n("b-row",{staticStyle:{"padding-top":"1rem","border-bottom":"0.1rem solid #ccc"}},[n("humidity-chart")],1)],1),n("b-col",{staticStyle:{"padding-left":"2rem","border-left":"0.1rem solid #ccc"}},[n("indexControl",{staticStyle:{"padding-bottom":"1rem","border-bottom":"0.1rem solid #ccc"}}),n("b-row",{staticStyle:{"padding-top":"1rem","border-bottom":"0.1rem solid #ccc"}},[n("historytable")],1)],1)],1)],1)},h=[],f=function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("b-container",{attrs:{fluid:""}},[n("H4",{staticClass:"text-left"},[t._v("Status")]),n("b-row",[n("b-col",[n("b-table",{attrs:{"head-variant":"light",bordered:"",hover:"",items:t.status1}})],1),n("b-col",[n("b-table",{attrs:{"head-variant":"light",bordered:"",hover:"",items:t.status2}})],1)],1)],1)},p=[],b=(n("d3b7"),n("07ac"),{name:"status",data:function(){return{status1:[{Name:"System",Info:"Normal"},{Name:"Water",Info:"Normal"},{Name:"Pump",Info:"Normal"},{Name:"Motor",Info:"Normal"}],status2:[{Name:"Watering Mode",Info:"Loading..."},{Name:"Last Reporting",Info:"Loading..."},{Name:"Soil Humidity",Info:"Loading..."},{Name:"Sunlight",Info:"Loading..."}]}},methods:{onBtnClick:function(){this.fetchData()},fetchData:function(){var t=this,e={cmd:"getRealTime",val:1};fetch("http://521.cpp.moe/console_post.php",{method:"post",body:JSON.stringify(e)}).then((function(t){return t.json()})).then((function(e){t.genTable(e)}))},consoleOut:function(t){console.log(t)},genTable:function(t){var e=[],n=null,a=Object.values(t[0]);n="0"===a[2]?"Automatic":"Manual",e.push({Name:"Watering Mode",Info:n}),e.push({Name:"Last Reporting",Info:a[1]}),e.push({Name:"Soil Humidity",Info:a[0]}),e.push({Name:"Sunlight",Info:a[3]}),this.status2=e}},mounted:function(){var t=this;this.fetchData(),window.setInterval((function(){t.fetchData()}),2e3),console.log(123)}}),v=b,y=Object(c["a"])(v,f,p,!1,null,"5190b403",null),H=y.exports,_=function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("b-container",{attrs:{fluid:""}},[n("H4",{staticClass:"text-left"},[t._v("Control")]),n("b-row",[n("b-card-group",{attrs:{deck:""}},[n("div",{staticClass:"card"},[n("div",{staticClass:"card-body"},[n("h5",{staticClass:"card-title"},[t._v("Mode Switch")]),n("p",{staticClass:"card-text"},[t._v("Switch between automatic and manual control mode")]),n("div",[n("b-button-group",[n("b-button",{on:{click:function(e){return t.onBtnClick("mode_switch","auto")}}},[t._v("Automatic")]),n("b-button",{on:{click:function(e){return t.onBtnClick("mode_switch","manual")}}},[t._v("Manual")])],1)],1)])]),n("div",{staticClass:"card"},[n("div",{staticClass:"card-body"},[n("h5",{staticClass:"card-title"},[t._v("Real-Time Control")]),n("p",{staticClass:"card-text"},[t._v("Manually operate the water pump and motor.")]),n("b-button-group",[n("b-button",{on:{click:function(e){return t.onBtnClick("control","water_start")}}},[t._v("Watering")]),n("b-button",{on:{click:function(e){return t.onBtnClick("control","rotate_start")}}},[t._v("Rotating")])],1)],1)]),n("div",{staticClass:"card"},[n("div",{staticClass:"card-body"},[n("h5",{staticClass:"card-title"},[t._v("Target Humidity: "+t._s(t.humInp))]),n("b-col",{staticClass:"card-text mb-4"},[n("b-input-group",{staticClass:"mt-3",attrs:{prepend:"10",append:"100"}},[n("b-form-input",{attrs:{type:"range",min:"10",max:"100"},model:{value:t.humInp,callback:function(e){t.humInp=e},expression:"humInp"}})],1)],1),n("b-button",{staticClass:"btn-secondary",on:{click:function(e){return t.onBtnClick("humidity_control",t.humInp)}}},[t._v("Apply Humidity")])],1)])])],1)],1)},M=[],C={name:"control",data:function(){return{humInp:50}},methods:{onBtnClick:function(t,e){var n={cmd:t,val:e};console.log(n),fetch("http://521.cpp.moe/console_post.php",{method:"post",body:JSON.stringify(n)})}}},w=C,T=Object(c["a"])(w,_,M,!1,null,"0878cb1a",null),x=T.exports,D=function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("b-container",{attrs:{fluid:""}},[n("H4",{staticClass:"text-left"},[t._v("Humidity Last 12 Hours")]),t.alertFlag?n("div",{staticClass:"alert alert-danger",attrs:{role:"alert"}},[t._v(" Warning: In last 12 hours, humidity level is less than 30, check the system status. ")]):t._e(),n("b-row",[n("b-col",[n("b-table",{attrs:{"head-variant":"light",bordered:"",hover:"",items:t.status1}})],1),n("b-col",[n("b-table",{attrs:{"head-variant":"light",bordered:"",hover:"",items:t.status2}})],1)],1)],1)},S=[],O=n("b85c"),L={data:function(){return{status1:[{Time:"Loading",Humidity:"Loading"},{Time:"Loading",Humidity:"Loading"},{Time:"Loading",Humidity:"Loading"},{Time:"Loading",Humidity:"Loading"}],status2:[{Time:"Loading",Humidity:"Loading"},{Time:"Loading",Humidity:"Loading"},{Time:"Loading",Humidity:"Loading"},{Time:"Loading",Humidity:"Loading"}],alertFlag:0}},methods:{onBtnClick:function(){this.fetchData()},fetchData:function(){var t=this,e={cmd:"getHum12Hr",val:1};fetch("http://521.cpp.moe/console_post.php",{method:"post",body:JSON.stringify(e)}).then((function(t){return t.json()})).then((function(e){t.genTable(e)}))},consoleOut:function(t){console.log(t)},genTable:function(t){var e,n=[],a=[],o=0,i=Object(O["a"])(t);try{for(i.s();!(e=i.n()).done;){var r=e.value;r<30&&(o=1)}}catch(u){i.e(u)}finally{i.f()}this.alertFlag=1===o?1:0;var s=new Date;n.push({Time:s.getFullYear()+"-"+(s.getMonth()+1)+"-"+s.getDate()+" "+s.getHours()+":"+(s.getMinutes()<10?"0":"")+s.getMinutes(),Humidity:t[0]}),s.setHours(s.getHours()-1),n.push({Time:s.getFullYear()+"-"+(s.getMonth()+1)+"-"+s.getDate()+" "+s.getHours()+":"+(s.getMinutes()<10?"0":"")+s.getMinutes(),Humidity:t[1]}),s.setHours(s.getHours()-1),n.push({Time:s.getFullYear()+"-"+(s.getMonth()+1)+"-"+s.getDate()+" "+s.getHours()+":"+(s.getMinutes()<10?"0":"")+s.getMinutes(),Humidity:t[2]}),s.setHours(s.getHours()-1),n.push({Time:s.getFullYear()+"-"+(s.getMonth()+1)+"-"+s.getDate()+" "+s.getHours()+":"+(s.getMinutes()<10?"0":"")+s.getMinutes(),Humidity:t[3]}),s.setHours(s.getHours()-1),n.push({Time:s.getFullYear()+"-"+(s.getMonth()+1)+"-"+s.getDate()+" "+s.getHours()+":"+(s.getMinutes()<10?"0":"")+s.getMinutes(),Humidity:t[4]}),s.setHours(s.getHours()-1),n.push({Time:s.getFullYear()+"-"+(s.getMonth()+1)+"-"+s.getDate()+" "+s.getHours()+":"+(s.getMinutes()<10?"0":"")+s.getMinutes(),Humidity:t[5]}),this.status1=n,s.setHours(s.getHours()-1),a.push({Time:s.getFullYear()+"-"+(s.getMonth()+1)+"-"+s.getDate()+" "+s.getHours()+":"+(s.getMinutes()<10?"0":"")+s.getMinutes(),Humidity:t[6]}),s.setHours(s.getHours()-1),a.push({Time:s.getFullYear()+"-"+(s.getMonth()+1)+"-"+s.getDate()+" "+s.getHours()+":"+(s.getMinutes()<10?"0":"")+s.getMinutes(),Humidity:t[7]}),s.setHours(s.getHours()-1),a.push({Time:s.getFullYear()+"-"+(s.getMonth()+1)+"-"+s.getDate()+" "+s.getHours()+":"+(s.getMinutes()<10?"0":"")+s.getMinutes(),Humidity:t[8]}),s.setHours(s.getHours()-1),a.push({Time:s.getFullYear()+"-"+(s.getMonth()+1)+"-"+s.getDate()+" "+s.getHours()+":"+(s.getMinutes()<10?"0":"")+s.getMinutes(),Humidity:t[9]}),s.setHours(s.getHours()-1),a.push({Time:s.getFullYear()+"-"+(s.getMonth()+1)+"-"+s.getDate()+" "+s.getHours()+":"+(s.getMinutes()<10?"0":"")+s.getMinutes(),Humidity:t[10]}),s.setHours(s.getHours()-1),a.push({Time:s.getFullYear()+"-"+(s.getMonth()+1)+"-"+s.getDate()+" "+s.getHours()+":"+(s.getMinutes()<10?"0":"")+s.getMinutes(),Humidity:t[11]}),this.status2=a}},mounted:function(){var t=this;this.fetchData(),window.setInterval((function(){t.fetchData()}),6e4),console.log(123)}},k=L,I=Object(c["a"])(k,D,S,!1,null,"7a748400",null),j=I.exports,N=function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("b-container",{attrs:{fluid:""}},[n("H4",{staticClass:"text-left"},[t._v("Watering Last 30 Days")]),n("b-row",[n("b-table",{attrs:{"head-variant":"light",bordered:"",hover:"",items:t.status}})],1)],1)},F=[],Y={name:"historytable",data:function(){return{fields:["#","date_time","soil_humidity"],status:null,test:null}},methods:{onBtnClick:function(){this.fetchData()},fetchData:function(){var t=this,e={cmd:"getHistory",val:1};fetch("http://521.cpp.moe/console_post.php",{method:"post",body:JSON.stringify(e)}).then((function(t){return t.json()})).then((function(e){t.genTable(e)})).catch((function(t){return console.error(t)}))},consoleOut:function(t){console.log(t)},genTable:function(t){var e,n=[];for(e=1;e<=t.length;e++){var a=Object.values(t[e-1]);n.push({"#":e,date_time:a[1],soil_humidity:+a[0]})}this.status=n}},mounted:function(){var t=this;this.fetchData(),window.setInterval((function(){t.fetchData()}),2e3)}},B=Y,J=Object(c["a"])(B,N,F,!1,null,"a99b2772",null),P=J.exports,W={name:"mainBody",components:{Historytable:P,indexStatus:H,indexControl:x,humidityChart:j},data:function(){return{items:[{age:40,first_name:"Dickerson",last_name:"Macdonald"},{age:21,first_name:"Larsen",last_name:"Shaw"},{age:89,first_name:"Geneva",last_name:"Wilson"},{age:38,first_name:"Jami",last_name:"Carney"},{age:38,first_name:"Jami",last_name:"Carney"}]}}},$=W,E=Object(c["a"])($,m,h,!1,null,"5e64b9b6",null),R=E.exports,A={name:"App",components:{navbar:g,mainBody:R}},G=A,V=(n("034f"),Object(c["a"])(G,o,i,!1,null,null,null)),q=V.exports,z=n("5f5b"),K=n("b1e0");n("f9e3"),n("2dd8");a["default"].use(z["a"]),a["default"].use(K["b"]),a["default"].use(K["a"]),a["default"].config.productionTip=!1,new a["default"]({render:function(t){return t(q)},el:"#app",data:{message:"Hello Vue!"}}).$mount("#app")},"85ec":function(t,e,n){}});
//# sourceMappingURL=app.08887011.js.map