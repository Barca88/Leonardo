(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-f56f6ff0"],{"00de":function(t,e,r){"use strict";var i=r("fc1a"),n=r.n(i);n.a},"1da1":function(t,e,r){"use strict";r.d(e,"a",(function(){return n}));r("d3b7");function i(t,e,r,i,n,a,o){try{var s=t[a](o),c=s.value}catch(l){return void r(l)}s.done?e(c):Promise.resolve(c).then(i,n)}function n(t){return function(){var e=this,r=arguments;return new Promise((function(n,a){var o=t.apply(e,r);function s(t){i(o,n,a,s,c,"next",t)}function c(t){i(o,n,a,s,c,"throw",t)}s(void 0)}))}}},"96cf":function(t,e,r){var i=function(t){"use strict";var e,r=Object.prototype,i=r.hasOwnProperty,n="function"===typeof Symbol?Symbol:{},a=n.iterator||"@@iterator",o=n.asyncIterator||"@@asyncIterator",s=n.toStringTag||"@@toStringTag";function c(t,e,r){return Object.defineProperty(t,e,{value:r,enumerable:!0,configurable:!0,writable:!0}),t[e]}try{c({},"")}catch(P){c=function(t,e,r){return t[e]=r}}function l(t,e,r,i){var n=e&&e.prototype instanceof m?e:m,a=Object.create(n.prototype),o=new S(i||[]);return a._invoke=C(t,r,o),a}function u(t,e,r){try{return{type:"normal",arg:t.call(e,r)}}catch(P){return{type:"throw",arg:P}}}t.wrap=l;var v="suspendedStart",d="suspendedYield",f="executing",p="completed",h={};function m(){}function y(){}function g(){}var _={};_[a]=function(){return this};var w=Object.getPrototypeOf,b=w&&w(w(V([])));b&&b!==r&&i.call(b,a)&&(_=b);var x=g.prototype=m.prototype=Object.create(_);function k(t){["next","throw","return"].forEach((function(e){c(t,e,(function(t){return this._invoke(e,t)}))}))}function $(t,e){function r(n,a,o,s){var c=u(t[n],t,a);if("throw"!==c.type){var l=c.arg,v=l.value;return v&&"object"===typeof v&&i.call(v,"__await")?e.resolve(v.__await).then((function(t){r("next",t,o,s)}),(function(t){r("throw",t,o,s)})):e.resolve(v).then((function(t){l.value=t,o(l)}),(function(t){return r("throw",t,o,s)}))}s(c.arg)}var n;function a(t,i){function a(){return new e((function(e,n){r(t,i,e,n)}))}return n=n?n.then(a,a):a()}this._invoke=a}function C(t,e,r){var i=v;return function(n,a){if(i===f)throw new Error("Generator is already running");if(i===p){if("throw"===n)throw a;return j()}r.method=n,r.arg=a;while(1){var o=r.delegate;if(o){var s=L(o,r);if(s){if(s===h)continue;return s}}if("next"===r.method)r.sent=r._sent=r.arg;else if("throw"===r.method){if(i===v)throw i=p,r.arg;r.dispatchException(r.arg)}else"return"===r.method&&r.abrupt("return",r.arg);i=f;var c=u(t,e,r);if("normal"===c.type){if(i=r.done?p:d,c.arg===h)continue;return{value:c.arg,done:r.done}}"throw"===c.type&&(i=p,r.method="throw",r.arg=c.arg)}}}function L(t,r){var i=t.iterator[r.method];if(i===e){if(r.delegate=null,"throw"===r.method){if(t.iterator["return"]&&(r.method="return",r.arg=e,L(t,r),"throw"===r.method))return h;r.method="throw",r.arg=new TypeError("The iterator does not provide a 'throw' method")}return h}var n=u(i,t.iterator,r.arg);if("throw"===n.type)return r.method="throw",r.arg=n.arg,r.delegate=null,h;var a=n.arg;return a?a.done?(r[t.resultName]=a.value,r.next=t.nextLoc,"return"!==r.method&&(r.method="next",r.arg=e),r.delegate=null,h):a:(r.method="throw",r.arg=new TypeError("iterator result is not an object"),r.delegate=null,h)}function E(t){var e={tryLoc:t[0]};1 in t&&(e.catchLoc=t[1]),2 in t&&(e.finallyLoc=t[2],e.afterLoc=t[3]),this.tryEntries.push(e)}function O(t){var e=t.completion||{};e.type="normal",delete e.arg,t.completion=e}function S(t){this.tryEntries=[{tryLoc:"root"}],t.forEach(E,this),this.reset(!0)}function V(t){if(t){var r=t[a];if(r)return r.call(t);if("function"===typeof t.next)return t;if(!isNaN(t.length)){var n=-1,o=function r(){while(++n<t.length)if(i.call(t,n))return r.value=t[n],r.done=!1,r;return r.value=e,r.done=!0,r};return o.next=o}}return{next:j}}function j(){return{value:e,done:!0}}return y.prototype=x.constructor=g,g.constructor=y,y.displayName=c(g,s,"GeneratorFunction"),t.isGeneratorFunction=function(t){var e="function"===typeof t&&t.constructor;return!!e&&(e===y||"GeneratorFunction"===(e.displayName||e.name))},t.mark=function(t){return Object.setPrototypeOf?Object.setPrototypeOf(t,g):(t.__proto__=g,c(t,s,"GeneratorFunction")),t.prototype=Object.create(x),t},t.awrap=function(t){return{__await:t}},k($.prototype),$.prototype[o]=function(){return this},t.AsyncIterator=$,t.async=function(e,r,i,n,a){void 0===a&&(a=Promise);var o=new $(l(e,r,i,n),a);return t.isGeneratorFunction(r)?o:o.next().then((function(t){return t.done?t.value:o.next()}))},k(x),c(x,s,"Generator"),x[a]=function(){return this},x.toString=function(){return"[object Generator]"},t.keys=function(t){var e=[];for(var r in t)e.push(r);return e.reverse(),function r(){while(e.length){var i=e.pop();if(i in t)return r.value=i,r.done=!1,r}return r.done=!0,r}},t.values=V,S.prototype={constructor:S,reset:function(t){if(this.prev=0,this.next=0,this.sent=this._sent=e,this.done=!1,this.delegate=null,this.method="next",this.arg=e,this.tryEntries.forEach(O),!t)for(var r in this)"t"===r.charAt(0)&&i.call(this,r)&&!isNaN(+r.slice(1))&&(this[r]=e)},stop:function(){this.done=!0;var t=this.tryEntries[0],e=t.completion;if("throw"===e.type)throw e.arg;return this.rval},dispatchException:function(t){if(this.done)throw t;var r=this;function n(i,n){return s.type="throw",s.arg=t,r.next=i,n&&(r.method="next",r.arg=e),!!n}for(var a=this.tryEntries.length-1;a>=0;--a){var o=this.tryEntries[a],s=o.completion;if("root"===o.tryLoc)return n("end");if(o.tryLoc<=this.prev){var c=i.call(o,"catchLoc"),l=i.call(o,"finallyLoc");if(c&&l){if(this.prev<o.catchLoc)return n(o.catchLoc,!0);if(this.prev<o.finallyLoc)return n(o.finallyLoc)}else if(c){if(this.prev<o.catchLoc)return n(o.catchLoc,!0)}else{if(!l)throw new Error("try statement without catch or finally");if(this.prev<o.finallyLoc)return n(o.finallyLoc)}}}},abrupt:function(t,e){for(var r=this.tryEntries.length-1;r>=0;--r){var n=this.tryEntries[r];if(n.tryLoc<=this.prev&&i.call(n,"finallyLoc")&&this.prev<n.finallyLoc){var a=n;break}}a&&("break"===t||"continue"===t)&&a.tryLoc<=e&&e<=a.finallyLoc&&(a=null);var o=a?a.completion:{};return o.type=t,o.arg=e,a?(this.method="next",this.next=a.finallyLoc,h):this.complete(o)},complete:function(t,e){if("throw"===t.type)throw t.arg;return"break"===t.type||"continue"===t.type?this.next=t.arg:"return"===t.type?(this.rval=this.arg=t.arg,this.method="return",this.next="end"):"normal"===t.type&&e&&(this.next=e),h},finish:function(t){for(var e=this.tryEntries.length-1;e>=0;--e){var r=this.tryEntries[e];if(r.finallyLoc===t)return this.complete(r.completion,r.afterLoc),O(r),h}},catch:function(t){for(var e=this.tryEntries.length-1;e>=0;--e){var r=this.tryEntries[e];if(r.tryLoc===t){var i=r.completion;if("throw"===i.type){var n=i.arg;O(r)}return n}}throw new Error("illegal catch attempt")},delegateYield:function(t,r,i){return this.delegate={iterator:V(t),resultName:r,nextLoc:i},"next"===this.method&&(this.arg=e),h}},t}(t.exports);try{regeneratorRuntime=i}catch(n){Function("r","regeneratorRuntime = r")(i)}},a523:function(t,e,r){"use strict";r("99af"),r("4de4"),r("b64b"),r("2ca0"),r("20f6"),r("4b85");var i=r("e8f2"),n=r("d9f7");e["a"]=Object(i["a"])("container").extend({name:"v-container",functional:!0,props:{id:String,tag:{type:String,default:"div"},fluid:{type:Boolean,default:!1}},render:function(t,e){var r,i=e.props,a=e.data,o=e.children,s=a.attrs;return s&&(a.attrs={},r=Object.keys(s).filter((function(t){if("slot"===t)return!1;var e=s[t];return t.startsWith("data-")?(a.attrs[t]=e,!1):e||"string"===typeof e}))),i.id&&(a.domProps=a.domProps||{},a.domProps.id=i.id),t(i.tag,Object(n["a"])(a,{staticClass:"container",class:Array({"container--fluid":i.fluid}).concat(r||[])}),o)}})},db6c:function(t,e,r){"use strict";(function(t){r("99af"),r("d3b7"),r("25f0");var i=r("bc3a"),n=r.n(i);e["a"]={data:function(){return{title:"Vue",userPic:"",nome:this.$store.state.user._id,miniVariant:!0,expandOnHover:!0,priv:!1,terms:!1,credits:!1,about:!1,drawerOn:!0}},created:function(){var e=this;n.a.get("https://leonardo2.di.uminho.pt/api/users/foto/".concat(this.$store.state.user._id),{responseType:"arraybuffer",headers:{Authorization:"Bearer: ".concat(this.$store.state.jwt)}}).then((function(r){var i=new t(r.data,"binary").toString("base64");e.userPic="data:".concat(r.headers["content-type"].toLowerCase(),";base64,").concat(i)})).catch((function(t){e.errors.push(t)}))},methods:{logout:function(){this.$store.commit("guardaTokenUtilizador",""),this.$store.commit("guardaNomeUtilizador",""),this.$router.push({path:"/admin/login"})},fixNav:function(){var t=this;this.expandOnHover=!this.expandOnHover,this.miniVariant=!this.miniVariant,this.drawerOn=!1,this.$nextTick((function(){return t.drawerOn=!0}))}}}}).call(this,r("b639").Buffer)},e68b:function(t,e,r){"use strict";r.r(e);var i=function(){var t=this,e=t.$createElement,r=t._self._c||e;return r("div",[r("appHeader"),"Admin"===this.$store.state.user.tipo?r("div",[r("navDraw")],1):r("div",[r("navDrawLeitor")],1),r("div",[r("progressBarComponent")],1)],1)},n=[],a=function(){var t=this,e=t.$createElement,r=t._self._c||e;return r("v-container",{attrs:{"fill-height":""}},[r("v-row",{attrs:{align:"center",justify:"center"}},[r("p",[t._v("Aguarde o processamento dos Fólios")]),r("v-col",{attrs:{cols:"12"}},[r("div",{staticStyle:{"min-height":"500px"}},[r("v-progress-linear",{attrs:{indeterminate:"",color:"blue darken-2"}})],1)])],1)],1)},o=[],s=(r("96cf"),r("1da1")),c=r("bc3a"),l=r.n(c),u="https://leonardo2.di.uminho.pt/api",v={mounted:function(){var t=Object(s["a"])(regeneratorRuntime.mark((function t(){var e;return regeneratorRuntime.wrap((function(t){while(1)switch(t.prev=t.next){case 0:return t.prev=0,t.next=3,l.a.get(u+"/process",{headers:{Authorization:"Bearer: ".concat(this.$store.state.jwt)}});case 3:e=t.sent,e.data.message&&this.$router.push("/localidades"),t.next=10;break;case 7:return t.prev=7,t.t0=t["catch"](0),t.abrupt("return",t.t0);case 10:case"end":return t.stop()}}),t,this,[[0,7]])})));function e(){return t.apply(this,arguments)}return e}()},d=v,f=r("2877"),p=r("6544"),h=r.n(p),m=r("62ad"),y=r("a523"),g=r("8e36"),_=r("0fd9"),w=Object(f["a"])(d,a,o,!1,null,null,null),b=w.exports;h()(w,{VCol:m["a"],VContainer:y["a"],VProgressLinear:g["a"],VRow:_["a"]});var x=r("71c2"),k=r("75ce"),$=r("f7af"),C={name:"Processamento",components:{appHeader:x["a"],navDraw:k["a"],navDrawLeitor:$["a"],progressBarComponent:b}},L=C,E=Object(f["a"])(L,i,n,!1,null,null,null);e["default"]=E.exports},e8f2:function(t,e,r){"use strict";r.d(e,"a",(function(){return n}));r("99af"),r("4de4"),r("a15b"),r("b64b"),r("2ca0"),r("498a");var i=r("2b0e");function n(t){return i["a"].extend({name:"v-".concat(t),functional:!0,props:{id:String,tag:{type:String,default:"div"}},render:function(e,r){var i=r.props,n=r.data,a=r.children;n.staticClass="".concat(t," ").concat(n.staticClass||"").trim();var o=n.attrs;if(o){n.attrs={};var s=Object.keys(o).filter((function(t){if("slot"===t)return!1;var e=o[t];return t.startsWith("data-")?(n.attrs[t]=e,!1):e||"string"===typeof e}));s.length&&(n.staticClass+=" ".concat(s.join(" ")))}return i.id&&(n.domProps=n.domProps||{},n.domProps.id=i.id),e(i.tag,n,a)}})}},f7af:function(t,e,r){"use strict";var i=function(){var t=this,e=t.$createElement,r=t._self._c||e;return r("v-card",[t.drawerOn?r("v-navigation-drawer",{staticClass:"navBar",attrs:{app:"",clipped:"",permanent:"","expand-on-hover":t.expandOnHover,"mini-variant":t.miniVariant,color:"#2A3F54"},scopedSlots:t._u([{key:"append",fn:function(){return[r("div",{staticClass:"pa-2"},[r("v-btn",{attrs:{dark:"",depressed:"","min-width":"60px"},on:{click:function(e){return t.fixNav()}}},[r("v-icon",[t._v("mdi-axis-arrow-lock")])],1),r("v-btn",{attrs:{dark:"",depressed:"","min-width":"60px"},on:{click:function(e){return t.logout()}}},[r("v-icon",[t._v("mdi-power")])],1)],1)]},proxy:!0}],null,!1,391888255)},[r("v-list",{attrs:{nav:"",dense:"",dark:""}},[r("v-divider",{attrs:{light:""}}),r("v-list-group",{staticClass:"white--text",attrs:{"prepend-icon":"mdi-folder-open",value:!1,"no-action":""},scopedSlots:t._u([{key:"activator",fn:function(){return[r("v-list-item-title",{staticClass:"white--text"},[t._v(t._s(t.$t("navd.documents")))])]},proxy:!0}],null,!1,237610184)},[r("v-list-item",{attrs:{link:"",to:"/admin/folios"}},[r("v-list-item-title",{staticClass:"white--text"},[t._v(t._s(t.$t("navd.folios")))])],1),r("v-list-item",{attrs:{link:"",to:"/admin/compFolios"}},[r("v-list-item-title",{staticClass:"white--text"},[t._v(t._s(t.$t("navd.cf")))])],1)],1),r("v-list-item",{attrs:{link:"",to:"/admin/folios/indices"}},[r("v-list-item-icon",[r("v-icon",[t._v("mdi-format-list-bulleted-square")])],1),r("v-list-item-title",{staticClass:"white--text"},[t._v(t._s(t.$t("navd.indexes")))])],1),r("v-list-group",{staticClass:"white--text",attrs:{"prepend-icon":"mdi-note-multiple",value:!1,"no-action":""},scopedSlots:t._u([{key:"activator",fn:function(){return[r("v-list-item-title",{staticClass:"white--text"},[t._v(t._s(t.$t("navd.annotations")))])]},proxy:!0}],null,!1,3197302848)},[r("v-list-item",{attrs:{link:"",to:"/admin/tagging"}},[r("v-list-item-title",{staticClass:"white--text"},[t._v(t._s(t.$t("navd.etags")))])],1),r("v-list-item",{attrs:{link:"",to:"/admin/folios/tags"}},[r("v-list-item-title",{staticClass:"white--text"},[t._v(t._s(t.$t("navd.eListaTags")))])],1),r("v-list-item",{attrs:{link:"",to:"/admin/folios/tags"}},[r("v-list-item-title",{staticClass:"white--text"},[t._v(t._s(t.$t("navd.tags")))])],1),r("v-list-item",{attrs:{link:"",to:"/admin/users"}},[r("v-list-item-title",{staticClass:"white--text"},[t._v(t._s(t.$t("navd.ebase")))])],1)],1),r("v-list-item",{attrs:{link:"",to:"/admin/georef"}},[r("v-list-item-icon",[r("v-icon",[t._v("mdi-map-marker")])],1),r("v-list-item-title",[t._v(t._s(t.$t("navd.georef")))])],1),r("v-list-group",{staticClass:"white--text",attrs:{"prepend-icon":"mdi-magnify",value:!1,"no-action":""},scopedSlots:t._u([{key:"activator",fn:function(){return[r("v-list-item-title",{staticClass:"white--text"},[t._v(t._s(t.$t("navd.analysis")))])]},proxy:!0}],null,!1,1866041734)},[r("v-list-item",{attrs:{link:"",to:"/admin/analise"}},[r("v-list-item-title",{staticClass:"white--text"},[t._v(t._s(t.$t("nav.barraPesquisa")))])],1),r("v-list-item",{attrs:{link:""}},[r("v-list-item-title",{staticClass:"white--text"},[t._v(t._s(t.$t("navd.estatisticas")))])],1)],1),r("v-list-item",{attrs:{link:"",to:"/admin/definitions"}},[r("v-list-item-icon",[r("v-icon",[t._v("mdi-cog")])],1),r("v-list-item-title",[t._v(t._s(t.$t("navd.definitions")))])],1),r("v-list-item",{attrs:{link:"",to:"/admin/documentacao"}},[r("v-list-item-icon",[r("v-icon",[t._v("mdi-text-box-multiple")])],1),r("v-list-item-title",[t._v(t._s(t.$t("navd.docum")))])],1),r("v-list-item",{attrs:{link:"",to:"/admin/georef"}},[r("v-list-item-icon",[r("v-icon",[t._v("mdi-map-marker")])],1),r("v-list-item-title",[t._v(t._s(t.$t("navd.georef")))])],1),r("v-list-item",{attrs:{link:""},on:{click:function(e){t.about=!0}}},[r("v-list-item-icon",[r("v-icon",[t._v("mdi-information-outline")])],1),r("v-list-item-title",[t._v(t._s(t.$t("navd.about")))])],1),r("v-dialog",{attrs:{scrollable:"",width:"500"},on:{keydown:function(e){if(!e.type.indexOf("key")&&t._k(e.keyCode,"esc",27,e.key,["Esc","Escape"]))return null;t.about=!1}},model:{value:t.about,callback:function(e){t.about=e},expression:"about"}},[r("v-card",[r("v-toolbar",{attrs:{color:"#2A3F54",dark:""}},[r("h2",[t._v(t._s(t.$t("nav.sabermais")))])]),r("v-divider",{staticClass:"mx-4",attrs:{horizontal:""}}),r("v-card-text",{staticClass:"change-font mt-6",staticStyle:{"white-space":"pre-line"}},[t._v(t._s(t.$t("nav.textoSaberMais")))]),r("v-card-actions",[r("v-spacer"),r("v-tooltip",{attrs:{bottom:""},scopedSlots:t._u([{key:"activator",fn:function(e){var i=e.on;return[r("v-btn",t._g({attrs:{depressed:"",color:"white"},on:{click:function(e){t.about=!1}}},i),[r("v-icon",{attrs:{large:""}},[t._v("mdi-exit-to-app")])],1)]}}],null,!1,1470356265)},[r("span",[t._v(t._s(t.$t("nav.Sair")))])])],1)],1)],1),r("v-list-item",{attrs:{link:""},on:{click:function(e){t.credits=!0}}},[r("v-list-item-icon",[r("v-icon",[t._v("mdi-account-group")])],1),r("v-list-item-title",[t._v(t._s(t.$t("navd.credits")))])],1),r("v-dialog",{attrs:{scrollable:"",width:"500"},on:{keydown:function(e){if(!e.type.indexOf("key")&&t._k(e.keyCode,"esc",27,e.key,["Esc","Escape"]))return null;t.credits=!1}},model:{value:t.credits,callback:function(e){t.credits=e},expression:"credits"}},[r("v-card",[r("v-toolbar",{attrs:{color:"#2A3F54",dark:""}},[r("h2",[t._v(t._s(t.$t("nav.creditos")))])]),r("v-divider",{staticClass:"mx-4",attrs:{horizontal:""}}),r("v-card-text",{staticClass:"change-font mt-6",staticStyle:{"white-space":"pre-line"}},[t._v(t._s(t.$t("nav.textoCreditos")))]),r("v-card-actions",[r("v-spacer"),r("v-tooltip",{attrs:{bottom:""},scopedSlots:t._u([{key:"activator",fn:function(e){var i=e.on;return[r("v-btn",t._g({attrs:{depressed:"",color:"white"},on:{click:function(e){t.credits=!1}}},i),[r("v-icon",{attrs:{large:""}},[t._v("mdi-exit-to-app")])],1)]}}],null,!1,123572890)},[r("span",[t._v(t._s(t.$t("nav.Sair")))])])],1)],1)],1),r("v-list-item",{attrs:{link:""},on:{click:function(e){t.terms=!0}}},[r("v-list-item-icon",[r("v-icon",[t._v("mdi-book-multiple")])],1),r("v-list-item-title",[t._v("Termos de Utilização")])],1),r("v-dialog",{attrs:{scrollable:"",width:"500"},on:{keydown:function(e){if(!e.type.indexOf("key")&&t._k(e.keyCode,"esc",27,e.key,["Esc","Escape"]))return null;t.terms=!1}},model:{value:t.terms,callback:function(e){t.terms=e},expression:"terms"}},[r("v-card",[r("v-toolbar",{attrs:{color:"#2A3F54",dark:""}},[r("h2",[t._v(t._s(t.$t("nav.termos")))])]),r("v-divider",{staticClass:"mx-4",attrs:{horizontal:""}}),r("v-card-text",{staticClass:"change-font mt-6",staticStyle:{"white-space":"pre-line"}},[t._v(t._s(t.$t("nav.textoTermos")))]),r("v-card-actions",[r("v-spacer"),r("v-tooltip",{attrs:{bottom:""},scopedSlots:t._u([{key:"activator",fn:function(e){var i=e.on;return[r("v-btn",t._g({attrs:{depressed:"",color:"white"},on:{click:function(e){t.terms=!1}}},i),[r("v-icon",{attrs:{large:""}},[t._v("mdi-exit-to-app")])],1)]}}],null,!1,873776601)},[r("span",[t._v(t._s(t.$t("nav.Sair")))])])],1)],1)],1),r("v-list-item",{attrs:{link:""},on:{click:function(e){t.priv=!0}}},[r("v-list-item-icon",[r("v-icon",[t._v("mdi-incognito")])],1),r("v-list-item-title",[t._v("Privacidade")])],1),r("v-dialog",{attrs:{scrollable:"",width:"500"},on:{keydown:function(e){if(!e.type.indexOf("key")&&t._k(e.keyCode,"esc",27,e.key,["Esc","Escape"]))return null;t.priv=!1}},model:{value:t.priv,callback:function(e){t.priv=e},expression:"priv"}},[r("v-card",[r("v-toolbar",{attrs:{color:"#2A3F54",dark:""}},[r("h2",[t._v(t._s(t.$t("nav.privacidade")))])]),r("v-divider",{staticClass:"mx-4",attrs:{horizontal:""}}),r("v-card-text",{staticClass:"change-font mt-6",staticStyle:{"white-space":"pre-line"}},[t._v(t._s(t.$t("nav.textoPriv")))]),r("v-card-actions",[r("v-spacer"),r("v-tooltip",{attrs:{bottom:""},scopedSlots:t._u([{key:"activator",fn:function(e){var i=e.on;return[r("v-btn",t._g({attrs:{depressed:"",color:"white"},on:{click:function(e){t.priv=!1}}},i),[r("v-icon",{attrs:{large:""}},[t._v("mdi-exit-to-app")])],1)]}}],null,!1,1445130681)},[r("span",[t._v(t._s(t.$t("nav.Sair")))])])],1)],1)],1)],1)],1):t._e()],1)},n=[],a=r("db6c"),o=a["a"],s=(r("00de"),r("2877")),c=r("6544"),l=r.n(c),u=r("8336"),v=r("b0af"),d=r("99d9"),f=r("169a"),p=r("ce7e"),h=r("132d"),m=r("8860"),y=r("56b0"),g=r("da13"),_=r("34c3"),w=r("5d23"),b=r("f774"),x=r("2fa4"),k=r("71d9"),$=r("3a2f"),C=Object(s["a"])(o,i,n,!1,null,"1fd84006",null);e["a"]=C.exports;l()(C,{VBtn:u["a"],VCard:v["a"],VCardActions:d["a"],VCardText:d["b"],VDialog:f["a"],VDivider:p["a"],VIcon:h["a"],VList:m["a"],VListGroup:y["a"],VListItem:g["a"],VListItemIcon:_["a"],VListItemTitle:w["c"],VNavigationDrawer:b["a"],VSpacer:x["a"],VToolbar:k["a"],VTooltip:$["a"]})},fc1a:function(t,e,r){}}]);
//# sourceMappingURL=chunk-f56f6ff0.2ab6adcc.js.map