(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-d7fb1b74"],{"0e1c":function(t,a,e){},"0f79":function(t,a,e){t.exports=e.p+"img/logo_original.3f4ad9ab.png"},1091:function(t,a,e){"use strict";var n=e("2b192"),s=e.n(n);s.a},1671:function(t,a,e){"use strict";var n=e("0e1c"),s=e.n(n);s.a},"190b":function(t,a,e){"use strict";var n=e("e103"),s=e.n(n);s.a},"1a12":function(t,a,e){},"2b192":function(t,a,e){},"4b5a":function(t,a,e){},"4d63":function(t,a,e){var n=e("83ab"),s=e("da84"),o=e("94ca"),i=e("7156"),r=e("9bf2").f,c=e("241c").f,l=e("44e7"),d=e("ad6d"),u=e("9f7f"),v=e("6eeb"),p=e("d039"),f=e("69f3").set,g=e("2626"),h=e("b622"),_=h("match"),b=s.RegExp,m=b.prototype,x=/a/g,C=/a/g,k=new b(x)!==x,y=u.UNSUPPORTED_Y,w=n&&o("RegExp",!k||y||p((function(){return C[_]=!1,b(x)!=x||b(C)==C||"/a/i"!=b(x,"i")})));if(w){var S=function(t,a){var e,n=this instanceof S,s=l(t),o=void 0===a;if(!n&&s&&t.constructor===S&&o)return t;k?s&&!o&&(t=t.source):t instanceof S&&(o&&(a=d.call(t)),t=t.source),y&&(e=!!a&&a.indexOf("y")>-1,e&&(a=a.replace(/y/g,"")));var r=i(k?new b(t,a):b(t,a),n?this:m,S);return y&&e&&f(r,{sticky:e}),r},V=function(t){t in S||r(S,t,{configurable:!0,get:function(){return b[t]},set:function(a){b[t]=a}})},$=c(b),T=0;while($.length>T)V($[T++]);m.constructor=S,S.prototype=m,v(s,"RegExp",S)}g("RegExp")},"4d99":function(t,a,e){"use strict";var n=e("da04"),s=e.n(n);s.a},"553a":function(t,a,e){"use strict";e("a9e3"),e("c7cd");var n=e("5530"),s=(e("b5b6"),e("8dd9")),o=e("3a66"),i=e("d10f"),r=e("58df"),c=e("80d2");a["a"]=Object(r["a"])(s["a"],Object(o["a"])("footer",["height","inset"]),i["a"]).extend({name:"v-footer",props:{height:{default:"auto",type:[Number,String]},inset:Boolean,padless:Boolean,tag:{type:String,default:"footer"}},computed:{applicationProperty:function(){return this.inset?"insetFooter":"footer"},classes:function(){return Object(n["a"])(Object(n["a"])({},s["a"].options.computed.classes.call(this)),{},{"v-footer--absolute":this.absolute,"v-footer--fixed":!this.absolute&&(this.app||this.fixed),"v-footer--padless":this.padless,"v-footer--inset":this.inset})},computedBottom:function(){if(this.isPositioned)return this.app?this.$vuetify.application.bottom:0},computedLeft:function(){if(this.isPositioned)return this.app&&this.inset?this.$vuetify.application.left:0},computedRight:function(){if(this.isPositioned)return this.app&&this.inset?this.$vuetify.application.right:0},isPositioned:function(){return Boolean(this.absolute||this.fixed||this.app)},styles:function(){var t=parseInt(this.height);return Object(n["a"])(Object(n["a"])({},s["a"].options.computed.styles.call(this)),{},{height:isNaN(t)?t:Object(c["g"])(t),left:Object(c["g"])(this.computedLeft),right:Object(c["g"])(this.computedRight),bottom:Object(c["g"])(this.computedBottom)})}},methods:{updateApplication:function(){var t=parseInt(this.height);return isNaN(t)?this.$el?this.$el.clientHeight:0:t}},render:function(t){var a=this.setBackgroundColor(this.color,{staticClass:"v-footer",class:this.classes,style:this.styles});return t(this.tag,a,this.$slots.default)}})},5605:function(t,a,e){"use strict";var n=e("67e5"),s=e.n(n);s.a},"5dfc":function(t,a,e){"use strict";var n=e("1a12"),s=e.n(n);s.a},"67e5":function(t,a,e){},7481:function(t,a,e){"use strict";var n=e("4b5a"),s=e.n(n);s.a},"8a79":function(t,a,e){"use strict";var n=e("23e7"),s=e("06cf").f,o=e("50c4"),i=e("5a34"),r=e("1d80"),c=e("ab13"),l=e("c430"),d="".endsWith,u=Math.min,v=c("endsWith"),p=!l&&!v&&!!function(){var t=s(String.prototype,"endsWith");return t&&!t.writable}();n({target:"String",proto:!0,forced:!p&&!v},{endsWith:function(t){var a=String(r(this));i(t);var e=arguments.length>1?arguments[1]:void 0,n=o(a.length),s=void 0===e?n:u(o(e),n),c=String(t);return d?d.call(a,c,s):a.slice(s-c.length,s)===c}})},"9a46":function(t,a,e){"use strict";var n=e("c03d"),s=e.n(n);s.a},a523:function(t,a,e){"use strict";e("99af"),e("4de4"),e("b64b"),e("2ca0"),e("20f6"),e("4b85");var n=e("e8f2"),s=e("d9f7");a["a"]=Object(n["a"])("container").extend({name:"v-container",functional:!0,props:{id:String,tag:{type:String,default:"div"},fluid:{type:Boolean,default:!1}},render:function(t,a){var e,n=a.props,o=a.data,i=a.children,r=o.attrs;return r&&(o.attrs={},e=Object.keys(r).filter((function(t){if("slot"===t)return!1;var a=r[t];return t.startsWith("data-")?(o.attrs[t]=a,!1):a||"string"===typeof a}))),n.id&&(o.domProps=o.domProps||{},o.domProps.id=n.id),t(n.tag,Object(s["a"])(o,{staticClass:"container",class:Array({"container--fluid":n.fluid}).concat(e||[])}),i)}})},af16:function(t,a,e){},b5b6:function(t,a,e){},b922:function(t,a,e){"use strict";var n=e("af16"),s=e.n(n);s.a},c03d:function(t,a,e){},c3cb:function(t,a,e){"use strict";var n=e("cba7"),s=e.n(n);s.a},c54c:function(t,a,e){"use strict";e.r(a);var n=function(){var t=this,a=t.$createElement,n=t._self._c||a;return n("div",[n("Navbar"),n("v-container",[n("div",{attrs:{id:"imprimeMain"}},[n("v-row",[n("v-col",{attrs:{col:"12"}},[n("div",{staticClass:"results"},[n("v-img",{attrs:{src:e("0f79"),contain:"",width:"150px"}}),n("h2",{staticClass:"change-font black--text"},[t._v(" "+t._s(t.$t("nav.tituloProjeto"))+" ")]),n("h3",{staticClass:"font-weight-light change-font"},[t._v(" "+t._s(t.$t("nav.ResultadosAnalise"))+" ")]),n("h3",{staticClass:"font-weight-light change-font"},[t._v(" "+t._s(t.$t("nav.resultadoPara"))+" "),n("span",{staticClass:"font-weight-black change-font"},[t._v(t._s(this.pesquisa))])]),n("h3",{staticClass:"font-weight-light change-font"},[t._v(" "+t._s(t.$t("nav.Parametros"))+" "),n("span",{staticClass:"font-weight-black change-font"},[t._v(t._s(this.$route.params.selectedFolio)+", "+t._s(this.$route.params.tipo)+", "+t._s(this.$route.params.versao)+", "+t._s(this.$route.params.resultado))])]),n("h5",{staticClass:"change-font blue--text text--darken-4"},[t._v(" "+t._s(this.numResultados)+" "+t._s(t.$t("nav.resultadosEm"))+" "+t._s(this.tempoFinal)+" "+t._s(t.$t("nav.milisegundos"))+" ")]),n("v-container",{attrs:{fluid:""}},[n("v-row",[n("v-row",{attrs:{align:"start",justify:"end"}},[n("v-col",{attrs:{cols:"12",md:"1"}},[n("v-tooltip",{attrs:{bottom:""},scopedSlots:t._u([{key:"activator",fn:function(a){var e=a.on;return[n("v-btn",t._g({staticClass:"white--text change-font",attrs:{depressed:"",block:"",color:"#29b89b"},on:{click:t.goHome}},e),[n("v-icon",[t._v("mdi-magnify")])],1)]}}])},[n("span",[t._v(t._s(t.$t("nav.buttonPesquisa")))])])],1),n("v-col",{attrs:{cols:"12",md:"1"}},[n("v-dialog",{attrs:{scrollable:"",width:"500"},on:{keydown:function(a){if(!a.type.indexOf("key")&&t._k(a.keyCode,"esc",27,a.key,["Esc","Escape"]))return null;t.dialog=!1}},scopedSlots:t._u([{key:"activator",fn:function(a){var e=a.on;return[n("v-tooltip",{attrs:{bottom:""},scopedSlots:t._u([{key:"activator",fn:function(a){var s=a.on;return[n("v-btn",t._g({staticClass:"white--text change-font",attrs:{depressed:"",block:"",color:"#327ab7"}},Object.assign({},s,e)),[n("v-icon",[t._v("mdi-information")])],1)]}}],null,!0)},[n("span",[t._v(t._s(t.$t("nav.buttonAjuda")))])])]}}]),model:{value:t.dialog,callback:function(a){t.dialog=a},expression:"dialog"}},[n("v-card",[n("v-card-title",{staticClass:"headline change-font"},[t._v(t._s(t.$t("nav.buttonAjuda")))]),n("v-divider",{staticClass:"mx-4",attrs:{horizontal:""}}),n("v-card-text",{staticClass:"change-font",staticStyle:{"white-space":"pre-line"}},[t._v(t._s(t.$t("nav.textoInstrucoes")))]),n("v-card-actions",[n("v-spacer"),n("v-tooltip",{attrs:{bottom:""},scopedSlots:t._u([{key:"activator",fn:function(a){var e=a.on;return[n("v-btn",t._g({attrs:{depressed:"",color:"white"},on:{click:function(a){t.dialog=!1}}},e),[n("v-icon",{attrs:{large:""}},[t._v("mdi-door-open")])],1)]}}])},[n("span",[t._v(t._s(t.$t("nav.Sair")))])])],1)],1)],1)],1),n("v-col",{attrs:{cols:"12",md:"1"}},[n("v-tooltip",{attrs:{bottom:""},scopedSlots:t._u([{key:"activator",fn:function(a){var e=a.on;return[n("v-btn",t._g({staticClass:"white--text change-font",attrs:{depressed:"",block:"",color:"#29b89b"},on:{click:t.printSection}},e),[n("v-icon",[t._v("mdi-printer")])],1)]}}])},[n("span",[t._v(t._s(t.$t("nav.imprimir")))])])],1),n("v-col",{attrs:{cols:"12",md:"1"}})],1)],1)],1)],1),n("v-card",{staticClass:"pa-3 change-font",attrs:{text:""}},[t._l(t.pageOfItems,(function(a,e){return n("div",{key:a.idfolio+e},[a.periodo?n("h3",{staticClass:"font-weight-black change-font"},[n("a",{staticClass:"change-font",on:{click:function(e){return e.stopPropagation(),t.showFolio(a.idfolio)}}},[t._v(t._s(a.idfolio))]),t._v(" ● "+t._s(t.$t("nav.resultadoLinha"))+" "+t._s(a.linha)+" ● "+t._s(t.$t("nav.resultadoPeriodo"))+" "+t._s(a.periodo)+" ")]):n("h3",{staticClass:"font-weight-black change-font"},[n("a",{staticClass:"change-font",on:{click:function(e){return e.stopPropagation(),t.showFolio(a.idfolio)}}},[t._v(t._s(a.idfolio))]),t._v(" ● "+t._s(t.$t("nav.resultadoLinha"))+" "+t._s(a.linha)+" ")]),n("p",{staticClass:"font-weight-light change-font",domProps:{innerHTML:t._s(a.valor)}},[t._v(t._s(a.valor))]),n("br")])})),n("div",{staticClass:"card-footer text-center change-font"},[null!=t.resultados?n("jw-pagination",{attrs:{items:t.resultados},on:{changePage:t.onChangePage}}):t._e()],1)],2)],1)],1),n("v-dialog",{attrs:{persistent:"",scrollable:"","max-width":"800px"},on:{keydown:function(a){if(!a.type.indexOf("key")&&t._k(a.keyCode,"esc",27,a.key,["Esc","Escape"]))return null;t.dialogFolio=!t.dialogFolio,t.conta=[]}},model:{value:t.dialogFolio,callback:function(a){t.dialogFolio=a},expression:"dialogFolio"}},[null!=t.conta&&t.dialogFolio?n("v-card",[t.conta.length<=1?n("v-card-title",{staticClass:"headline change-font"},[n("span",{staticClass:"change-font"},[t._v(t._s(t.$t("nav.folioAnaliseHeadline")))]),t._v(" "),n("p",[n("small",{staticClass:"change-font"},[t._v(t._s(this.folioAtual)+",")]),t._v(" "),t._l(t.conta,(function(a,e){return n("small",{key:e,staticClass:"keep-spaces change-font"},[t._v(" "+t._s(a.key)+" "+t._s(t.$t("nav.com"))+" "+t._s(a.value)+" "+t._s(t.$t("nav.occur1"))+" ")])}))],2)]):n("v-card-title",{staticClass:"headline change-font"},[n("span",{staticClass:"change-font"},[t._v(" "+t._s(t.$t("nav.folioAnaliseHeadline"))+" ")]),t._v(" "),n("p",[n("small",{staticClass:"change-font"},[t._v(t._s(this.folioAtual))]),t._v(" "),t._l(t.conta,(function(a,e){return n("small",{key:e,staticClass:"keep-spaces change-font"},[t._v(", "+t._s(a.key)+" "+t._s(t.$t("nav.com"))+" "+t._s(a.value)+" "+t._s(t.$t("nav.occur2")))])}))],2)]),n("v-divider",{attrs:{horizontal:""}}),n("v-card-text",{staticClass:"change-font",domProps:{innerHTML:t._s(t.textoAtual)}},[t._v(t._s(this.textoAtual))]),n("v-card-actions",[n("v-spacer"),n("v-tooltip",{attrs:{bottom:""},scopedSlots:t._u([{key:"activator",fn:function(a){var e=a.on;return[n("v-btn",t._g({attrs:{depressed:"",color:"white"},on:{click:function(a){t.dialogFolio=!t.dialogFolio,t.conta=[]}}},e),[n("v-icon",{attrs:{large:""}},[t._v("mdi-door-open")])],1)]}}],null,!1,2147529018)},[n("span",[t._v(t._s(t.$t("nav.fechar")))])])],1)],1):t._e()],1)],1)]),n("Footer")],1)},s=[],o=(e("caad"),e("fb6a"),e("4d63"),e("ac1f"),e("25f0"),e("8a79"),e("2532"),e("466d"),e("5319"),e("1276"),e("2ca0"),e("498a"),e("bc3a")),i=e.n(o),r=e("d178"),c=e("fd2d"),l={data:function(){return{pesquisa:"",page:1,resultados:null,dialog:!1,dialogFolio:!1,folioAtual:null,textoAtual:null,pageOfItems:[],conta:[],tempoFinal:0,numResultados:0}},components:{Navbar:r["a"],Footer:c["a"]},created:function(){var t=this,a=performance.now();this.pesquisa=this.$route.params.pesquisa,this.pesquisa=this.pesquisa.trim();var e=[];i.a.get("https://leonardo2.di.uminho.pt/api/analise/pesquisa",{params:this.$route.params}).then((function(n){var s=performance.now();if(t.tempoFinal=s-a,t.numResultados=n.data.length,t.pesquisa.startsWith("+Tag")){var o="<"+t.pesquisa.split(" ")[1]+">",i="</"+t.pesquisa.split(" ")[1]+">";for(c=0;c<n.data.length;c++)n.data[c].valor=n.data[c].valor.replace(new RegExp(o,"g"),'<span class="red--text change-font">'),n.data[c].valor=n.data[c].valor.replace(new RegExp(i,"g"),"</span>")}else if(t.pesquisa.startsWith('"')&&t.pesquisa.endsWith('"')||t.$route.params.npalavras){var r=t.pesquisa;t.pesquisa.startsWith('"')&&t.pesquisa.endsWith('"')&&(r=t.pesquisa.substring(1,t.pesquisa.length-1));var c=0;for(c=0;c<n.data.length;c++)n.data[c].valor=n.data[c].valor.replace(new RegExp("<.*>","g"),""),n.data[c].valor=n.data[c].valor.replace(new RegExp("</.*>","g"),"");for(c=0;c<n.data.length;c++)n.data[c].valor=n.data[c].valor.replace(new RegExp(r,"g"),'<span class="red--text change-font">'+r+"</span>")}else{e=t.pesquisa.trim().split(" ");for(var l=0;l<e.length;l++)e[l].startsWith("+")?e[l]=e[l].split("+")[1]:e[l].startsWith('"')?e[l]=e[l].split('"')[1]:e[l].endsWith('"')&&(e[l]=e[l].slice(0,-1));var d=0;for(c=0;c<n.data.length;c++)n.data[c].valor=n.data[c].valor.replace(new RegExp("<.*>","g"),""),n.data[c].valor=n.data[c].valor.replace(new RegExp("</.*>","g"),"");for(;d<n.data.length;d++)for(l=0;l<e.length;l++)n.data[d].valor.includes(e[l])&&(n.data[d].valor=n.data[d].valor.replace(new RegExp(e[l],"g"),'<span class="red--text change-font">'+e[l]+"</span>"))}t.resultados=n.data})).catch((function(a){t.error=a.message}))},methods:{goHome:function(){this.$router.push({name:"home"})},onChangePage:function(t){this.pageOfItems=t},printSection:function(){this.$htmlToPaper("imprimeMain")},showFolio:function(t){var a=this;this.folioAtual=t;var e=[],n=0;i.a.get("https://leonardo2.di.uminho.pt/api/analise/folio/"+t).then((function(t){if(a.pesquisa.startsWith("+Tag")){var s="<"+a.pesquisa.split(" ")[1]+">",o="</"+a.pesquisa.split(" ")[1]+">";a.textoAtual=t.data.textoSTags.replace(new RegExp(s,"g"),'<span class="red--text change-font">'),a.textoAtual=a.textoAtual.replace(new RegExp(o,"g"),"</span>"),n=t.data.textoSTags.match(new RegExp(s,"g")).length,s in a.conta||a.conta.push({key:a.pesquisa.split(" ")[1],value:n}),a.dialogFolio=!0}else if(a.pesquisa.startsWith('"')&&a.pesquisa.endsWith('"')){var i=a.pesquisa.substring(1,a.pesquisa.length-1);t.data.textoSTags=t.data.textoSTags.replace(new RegExp("<.*>","g"),""),t.data.textoSTags=t.data.textoSTags.replace(new RegExp("</.*>","g"),""),t.data.textoSTags.includes(i)&&(a.textoAtual=t.data.textoSTags.replace(new RegExp(i,"g"),'<span class="red--text change-font">'+i+"</span>"),n=t.data.textoSTags.match(new RegExp(i,"g")).length,i in a.conta||a.conta.push({key:i,value:n}),a.dialogFolio=!0)}else{e=a.pesquisa.trim().split(" ");var r=0;for(t.data.textoSTags=t.data.textoSTags.replace(new RegExp("<.*>","g"),""),t.data.textoSTags=t.data.textoSTags.replace(new RegExp("</.*>","g"),""),r=0;r<e.length;r++)if(e[r].startsWith("+")){var c=e[r].substr(1);t.data.textoSTags.includes(c)&&(t.data.textoSTags=t.data.textoSTags.replace(new RegExp(c,"g"),'<span class="red--text change-font">'+c+"</span>"),n=t.data.textoSTags.match(new RegExp(c,"g")).length,c in a.conta||a.conta.push({key:c,value:n}),a.dialogFolio=!0)}else e[r].startsWith("+")||e[r].startsWith("-")||t.data.textoSTags.includes(e[r])&&(t.data.textoSTags=t.data.textoSTags.replace(new RegExp(e[r],"g"),'<span class="red--text change-font">'+e[r]+"</span>"),n=t.data.textoSTags.match(new RegExp(e[r],"g")).length,e[r]in a.conta||a.conta.push({key:e[r],value:n}),a.dialogFolio=!0);a.textoAtual=t.data.textoSTags}})).catch((function(t){a.error=t.message}))}}},d=l,u=(e("7481"),e("1091"),e("2877")),v=e("6544"),p=e.n(v),f=e("8336"),g=e("b0af"),h=e("99d9"),_=e("62ad"),b=e("a523"),m=e("169a"),x=e("ce7e"),C=e("132d"),k=e("adda"),y=e("0fd9"),w=e("2fa4"),S=e("3a2f"),V=Object(u["a"])(d,n,s,!1,null,"c5881f3a",null);a["default"]=V.exports;p()(V,{VBtn:f["a"],VCard:g["a"],VCardActions:h["a"],VCardText:h["b"],VCardTitle:h["c"],VCol:_["a"],VContainer:b["a"],VDialog:m["a"],VDivider:x["a"],VIcon:C["a"],VImg:k["a"],VRow:y["a"],VSpacer:w["a"],VTooltip:S["a"]})},cba7:function(t,a,e){},d178:function(t,a,e){"use strict";var n=function(){var t=this,a=t.$createElement,e=t._self._c||a;return e("nav",[e("v-toolbar",{attrs:{flat:"",color:"#2A3F54"}},[e("v-spacer"),e("v-tooltip",{attrs:{bottom:""},scopedSlots:t._u([{key:"activator",fn:function(a){var n=a.on;return[e("v-btn",t._g({staticClass:"white--text change-font",class:{active:"btn1"===t.activeBtn},attrs:{text:"",small:""},on:{click:function(a){t.setLocale("pt"),t.activeBtn="btn1"}}},n),[t._v("PT")])]}}])},[e("span",[t._v(t._s(t.$t("nav.LinguaPT")))])]),e("v-tooltip",{attrs:{bottom:""},scopedSlots:t._u([{key:"activator",fn:function(a){var n=a.on;return[e("v-btn",t._g({staticClass:"white--text change-font",class:{active:"btn2"===t.activeBtn},attrs:{text:"",small:""},on:{click:function(a){t.setLocale("es"),t.activeBtn="btn2"}}},n),[t._v("ES")])]}}])},[e("span",[t._v(t._s(t.$t("nav.LinguaES")))])]),e("v-tooltip",{attrs:{bottom:""},scopedSlots:t._u([{key:"activator",fn:function(a){var n=a.on;return[e("v-btn",t._g({staticClass:"white--text change-font",class:{active:"btn3"===t.activeBtn},attrs:{text:"",small:""},on:{click:function(a){t.setLocale("en"),t.activeBtn="btn3"}}},n),[t._v("UK")])]}}])},[e("span",[t._v(t._s(t.$t("nav.LinguaEN")))])])],1)],1)},s=[],o={components:{},data:function(){return{closeOnContentClick:!0,filterBtnTTip:!1,activeBtn:"btn1"}},methods:{setLocale:function(t){this.$i18n.locale=t,this.$router.push({params:{lang:t}})}}},i=o,r=(e("5dfc"),e("5605"),e("2877")),c=e("6544"),l=e.n(c),d=e("8336"),u=e("2fa4"),v=e("71d9"),p=e("3a2f"),f=Object(r["a"])(i,n,s,!1,null,"9134985c",null);a["a"]=f.exports;l()(f,{VBtn:d["a"],VSpacer:u["a"],VToolbar:v["a"],VTooltip:p["a"]})},da04:function(t,a,e){},e103:function(t,a,e){},e8f2:function(t,a,e){"use strict";e.d(a,"a",(function(){return s}));e("99af"),e("4de4"),e("a15b"),e("b64b"),e("2ca0"),e("498a");var n=e("2b0e");function s(t){return n["a"].extend({name:"v-".concat(t),functional:!0,props:{id:String,tag:{type:String,default:"div"}},render:function(a,e){var n=e.props,s=e.data,o=e.children;s.staticClass="".concat(t," ").concat(s.staticClass||"").trim();var i=s.attrs;if(i){s.attrs={};var r=Object.keys(i).filter((function(t){if("slot"===t)return!1;var a=i[t];return t.startsWith("data-")?(s.attrs[t]=a,!1):a||"string"===typeof a}));r.length&&(s.staticClass+=" ".concat(r.join(" ")))}return n.id&&(s.domProps=s.domProps||{},s.domProps.id=n.id),a(n.tag,s,o)}})}},fd2d:function(t,a,e){"use strict";var n=function(){var t=this,a=t.$createElement,e=t._self._c||a;return e("v-footer",{attrs:{color:"white"}},[e("v-row",{attrs:{justify:"center"}},[e("PopupCreditos"),e("PopupSaberMais"),e("PopupTermos"),e("PopupPrivacidade"),e("Popup"),e("v-col",{attrs:{cols:"12"}},[e("div",{staticClass:"text-center"},[e("small",{staticClass:"grey--text change-font text-none"},[t._v("©Leonardo, 2020")])])])],1)],1)},s=[],o=function(){var t=this,a=t.$createElement,e=t._self._c||a;return e("div",{staticClass:"text-center"},[e("v-dialog",{attrs:{scrollable:"",width:"500"},on:{keydown:function(a){if(!a.type.indexOf("key")&&t._k(a.keyCode,"esc",27,a.key,["Esc","Escape"]))return null;t.dialog=!1}},scopedSlots:t._u([{key:"activator",fn:function(a){var n=a.on;return[e("v-btn",t._g({staticClass:"grey--text change-font text-none",attrs:{depressed:"",text:""}},n),[e("span",{staticClass:"change-font"},[t._v(t._s(t.$t("nav.termos")))])])]}}]),model:{value:t.dialog,callback:function(a){t.dialog=a},expression:"dialog"}},[e("v-card",[e("v-card-title",{staticClass:"headline change-font"},[t._v(t._s(t.$t("nav.termos")))]),e("v-divider",{staticClass:"mx-4",attrs:{horizontal:""}}),e("v-card-text",{staticClass:"change-font",staticStyle:{"white-space":"pre-line"}},[t._v(t._s(t.$t("nav.textoTermos")))]),e("v-card-actions",[e("v-spacer"),e("v-tooltip",{attrs:{bottom:""},scopedSlots:t._u([{key:"activator",fn:function(a){var n=a.on;return[e("v-btn",t._g({attrs:{depressed:"",color:"white"},on:{click:function(a){t.dialog=!1}}},n),[e("v-icon",{attrs:{large:""}},[t._v("mdi-door-open")])],1)]}}])},[e("span",[t._v(t._s(t.$t("nav.Sair")))])])],1)],1)],1)],1)},i=[],r={data:function(){return{dialog:!1}}},c=r,l=(e("1671"),e("2877")),d=e("6544"),u=e.n(d),v=e("8336"),p=e("b0af"),f=e("99d9"),g=e("169a"),h=e("ce7e"),_=e("132d"),b=e("2fa4"),m=e("3a2f"),x=Object(l["a"])(c,o,i,!1,null,"2670c3e9",null),C=x.exports;u()(x,{VBtn:v["a"],VCard:p["a"],VCardActions:f["a"],VCardText:f["b"],VCardTitle:f["c"],VDialog:g["a"],VDivider:h["a"],VIcon:_["a"],VSpacer:b["a"],VTooltip:m["a"]});var k=function(){var t=this,a=t.$createElement,e=t._self._c||a;return e("div",{staticClass:"text-center"},[e("v-dialog",{attrs:{scrollable:"",width:"500"},on:{keydown:function(a){if(!a.type.indexOf("key")&&t._k(a.keyCode,"esc",27,a.key,["Esc","Escape"]))return null;t.dialog=!1}},scopedSlots:t._u([{key:"activator",fn:function(a){var n=a.on;return[e("v-btn",t._g({staticClass:"grey--text change-font text-none",attrs:{depressed:"",text:""}},n),[e("span",[t._v(t._s(t.$t("nav.creditos")))])])]}}]),model:{value:t.dialog,callback:function(a){t.dialog=a},expression:"dialog"}},[e("v-card",[e("v-card-title",{staticClass:"headline change-font"},[t._v(t._s(t.$t("nav.creditos")))]),e("v-divider",{staticClass:"mx-4",attrs:{horizontal:""}}),e("v-card-text",{staticClass:"change-font",staticStyle:{"white-space":"pre-line"}},[t._v(t._s(t.$t("nav.textoCreditos")))]),e("v-card-actions",[e("v-spacer"),e("v-tooltip",{attrs:{bottom:""},scopedSlots:t._u([{key:"activator",fn:function(a){var n=a.on;return[e("v-btn",t._g({attrs:{depressed:"",color:"white"},on:{click:function(a){t.dialog=!1}}},n),[e("v-icon",{attrs:{large:""}},[t._v("mdi-door-open")])],1)]}}])},[e("span",[t._v(t._s(t.$t("nav.Sair")))])])],1)],1)],1)],1)},y=[],w={data:function(){return{dialog:!1}}},S=w,V=(e("190b"),Object(l["a"])(S,k,y,!1,null,"52cb2634",null)),$=V.exports;u()(V,{VBtn:v["a"],VCard:p["a"],VCardActions:f["a"],VCardText:f["b"],VCardTitle:f["c"],VDialog:g["a"],VDivider:h["a"],VIcon:_["a"],VSpacer:b["a"],VTooltip:m["a"]});var T=function(){var t=this,a=t.$createElement,e=t._self._c||a;return e("div",{staticClass:"text-center"},[e("v-dialog",{attrs:{scrollable:"",width:"500"},on:{keydown:function(a){if(!a.type.indexOf("key")&&t._k(a.keyCode,"esc",27,a.key,["Esc","Escape"]))return null;t.dialog=!1}},scopedSlots:t._u([{key:"activator",fn:function(a){var n=a.on;return[e("v-btn",t._g({staticClass:"grey--text change-font text-none",attrs:{depressed:"",text:""}},n),[e("span",{staticClass:"change-font"},[t._v(t._s(t.$t("nav.sabermais")))])])]}}]),model:{value:t.dialog,callback:function(a){t.dialog=a},expression:"dialog"}},[e("v-card",[e("v-card-title",{staticClass:"headline change-font"},[t._v(t._s(t.$t("nav.sabermais")))]),e("v-divider",{staticClass:"mx-4",attrs:{horizontal:""}}),e("v-card-text",{staticClass:"change-font",staticStyle:{"white-space":"pre-line"}},[t._v(t._s(t.$t("nav.textoSaberMais")))]),e("v-card-actions",[e("v-spacer"),e("v-tooltip",{attrs:{bottom:""},scopedSlots:t._u([{key:"activator",fn:function(a){var n=a.on;return[e("v-btn",t._g({attrs:{depressed:"",color:"white"},on:{click:function(a){t.dialog=!1}}},n),[e("v-icon",{attrs:{large:""}},[t._v("mdi-door-open")])],1)]}}])},[e("span",[t._v(t._s(t.$t("nav.Sair")))])])],1)],1)],1)],1)},E=[],P={data:function(){return{dialog:!1}}},O=P,R=(e("4d99"),Object(l["a"])(O,T,E,!1,null,"20f04cda",null)),j=R.exports;u()(R,{VBtn:v["a"],VCard:p["a"],VCardActions:f["a"],VCardText:f["b"],VCardTitle:f["c"],VDialog:g["a"],VDivider:h["a"],VIcon:_["a"],VSpacer:b["a"],VTooltip:m["a"]});var q=function(){var t=this,a=t.$createElement,e=t._self._c||a;return e("div",{staticClass:"text-center"},[e("v-dialog",{attrs:{scrollable:"",width:"500"},on:{keydown:function(a){if(!a.type.indexOf("key")&&t._k(a.keyCode,"esc",27,a.key,["Esc","Escape"]))return null;t.dialog=!1}},scopedSlots:t._u([{key:"activator",fn:function(a){var n=a.on;return[e("v-btn",t._g({staticClass:"grey--text change-font text-none",attrs:{depressed:"",text:""}},n),[e("span",{staticClass:"change-font"},[t._v(t._s(t.$t("nav.privacidade")))])])]}}]),model:{value:t.dialog,callback:function(a){t.dialog=a},expression:"dialog"}},[e("v-card",[e("v-card-title",{staticClass:"headline change-font"},[t._v(t._s(t.$t("nav.privacidade")))]),e("v-divider",{staticClass:"mx-4",attrs:{horizontal:""}}),e("v-card-text",{staticClass:"change-font",staticStyle:{"white-space":"pre-line"}},[t._v(t._s(t.$t("nav.textoPriv")))]),e("v-card-actions",[e("v-spacer"),e("v-tooltip",{attrs:{bottom:""},scopedSlots:t._u([{key:"activator",fn:function(a){var n=a.on;return[e("v-btn",t._g({attrs:{depressed:"",color:"white"},on:{click:function(a){t.dialog=!1}}},n),[e("v-icon",{attrs:{large:""}},[t._v("mdi-door-open")])],1)]}}])},[e("span",[t._v(t._s(t.$t("nav.Sair")))])])],1)],1)],1)],1)},A=[],F={data:function(){return{dialog:!1}}},B=F,W=(e("9a46"),Object(l["a"])(B,q,A,!1,null,"16896577",null)),I=W.exports;u()(W,{VBtn:v["a"],VCard:p["a"],VCardActions:f["a"],VCardText:f["b"],VCardTitle:f["c"],VDialog:g["a"],VDivider:h["a"],VIcon:_["a"],VSpacer:b["a"],VTooltip:m["a"]});var D=function(){var t=this,a=t.$createElement,e=t._self._c||a;return e("div",{staticClass:"text-center"},[e("v-dialog",{attrs:{scrollable:"",width:"500"},on:{keydown:function(a){if(!a.type.indexOf("key")&&t._k(a.keyCode,"esc",27,a.key,["Esc","Escape"]))return null;t.dialog=!1}},scopedSlots:t._u([{key:"activator",fn:function(a){var n=a.on;return[e("v-btn",t._g({staticClass:"grey--text change-font text-none",attrs:{depressed:"",text:""}},n),[e("span",{staticClass:"change-font"},[t._v(t._s(t.$t("nav.buttonAjuda")))])])]}}]),model:{value:t.dialog,callback:function(a){t.dialog=a},expression:"dialog"}},[e("v-card",[e("v-card-title",{staticClass:"headline change-font"},[t._v(t._s(t.$t("nav.buttonAjuda")))]),e("v-divider",{staticClass:"mx-4",attrs:{horizontal:""}}),e("v-card-text",{staticClass:"change-font",staticStyle:{"white-space":"pre-line"}},[t._v(t._s(t.$t("nav.textoInstrucoes")))]),e("v-card-actions",[e("v-spacer"),e("v-tooltip",{attrs:{bottom:""},scopedSlots:t._u([{key:"activator",fn:function(a){var n=a.on;return[e("v-btn",t._g({attrs:{depressed:"",color:"white"},on:{click:function(a){t.dialog=!1}}},n),[e("v-icon",{attrs:{large:""}},[t._v("mdi-door-open")])],1)]}}])},[e("span",[t._v(t._s(t.$t("nav.Sair")))])])],1)],1)],1)],1)},L=[],N={data:function(){return{dialog:!1}}},M=N,z=(e("c3cb"),Object(l["a"])(M,D,L,!1,null,"16bcea1c",null)),H=z.exports;u()(z,{VBtn:v["a"],VCard:p["a"],VCardActions:f["a"],VCardText:f["b"],VCardTitle:f["c"],VDialog:g["a"],VDivider:h["a"],VIcon:_["a"],VSpacer:b["a"],VTooltip:m["a"]});var U={components:{PopupTermos:C,PopupCreditos:$,PopupSaberMais:j,PopupPrivacidade:I,Popup:H},data:function(){return{}}},J=U,K=(e("b922"),e("62ad")),Y=e("553a"),G=e("0fd9"),Q=Object(l["a"])(J,n,s,!1,null,"87942fe6",null);a["a"]=Q.exports;u()(Q,{VCol:K["a"],VFooter:Y["a"],VRow:G["a"]})}}]);
//# sourceMappingURL=chunk-d7fb1b74.30c31d5c.js.map