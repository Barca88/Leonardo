(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-62af41f9"],{"1da1":function(t,e,r){"use strict";r.d(e,"a",(function(){return a}));r("d3b7");function n(t,e,r,n,a,i,o){try{var s=t[i](o),c=s.value}catch(l){return void r(l)}s.done?e(c):Promise.resolve(c).then(n,a)}function a(t){return function(){var e=this,r=arguments;return new Promise((function(a,i){var o=t.apply(e,r);function s(t){n(o,a,i,s,c,"next",t)}function c(t){n(o,a,i,s,c,"throw",t)}s(void 0)}))}}},"51fe":function(t,e,r){"use strict";var n=r("b874"),a=r.n(n);a.a},"96cf":function(t,e,r){var n=function(t){"use strict";var e,r=Object.prototype,n=r.hasOwnProperty,a="function"===typeof Symbol?Symbol:{},i=a.iterator||"@@iterator",o=a.asyncIterator||"@@asyncIterator",s=a.toStringTag||"@@toStringTag";function c(t,e,r){return Object.defineProperty(t,e,{value:r,enumerable:!0,configurable:!0,writable:!0}),t[e]}try{c({},"")}catch(M){c=function(t,e,r){return t[e]=r}}function l(t,e,r,n){var a=e&&e.prototype instanceof v?e:v,i=Object.create(a.prototype),o=new j(n||[]);return i._invoke=S(t,r,o),i}function h(t,e,r){try{return{type:"normal",arg:t.call(e,r)}}catch(M){return{type:"throw",arg:M}}}t.wrap=l;var u="suspendedStart",d="suspendedYield",f="executing",p="completed",m={};function v(){}function g(){}function y(){}var b={};b[i]=function(){return this};var x=Object.getPrototypeOf,w=x&&x(x(k([])));w&&w!==r&&n.call(w,i)&&(b=w);var _=y.prototype=v.prototype=Object.create(b);function L(t){["next","throw","return"].forEach((function(e){c(t,e,(function(t){return this._invoke(e,t)}))}))}function E(t,e){function r(a,i,o,s){var c=h(t[a],t,i);if("throw"!==c.type){var l=c.arg,u=l.value;return u&&"object"===typeof u&&n.call(u,"__await")?e.resolve(u.__await).then((function(t){r("next",t,o,s)}),(function(t){r("throw",t,o,s)})):e.resolve(u).then((function(t){l.value=t,o(l)}),(function(t){return r("throw",t,o,s)}))}s(c.arg)}var a;function i(t,n){function i(){return new e((function(e,a){r(t,n,e,a)}))}return a=a?a.then(i,i):i()}this._invoke=i}function S(t,e,r){var n=u;return function(a,i){if(n===f)throw new Error("Generator is already running");if(n===p){if("throw"===a)throw i;return O()}r.method=a,r.arg=i;while(1){var o=r.delegate;if(o){var s=$(o,r);if(s){if(s===m)continue;return s}}if("next"===r.method)r.sent=r._sent=r.arg;else if("throw"===r.method){if(n===u)throw n=p,r.arg;r.dispatchException(r.arg)}else"return"===r.method&&r.abrupt("return",r.arg);n=f;var c=h(t,e,r);if("normal"===c.type){if(n=r.done?p:d,c.arg===m)continue;return{value:c.arg,done:r.done}}"throw"===c.type&&(n=p,r.method="throw",r.arg=c.arg)}}}function $(t,r){var n=t.iterator[r.method];if(n===e){if(r.delegate=null,"throw"===r.method){if(t.iterator["return"]&&(r.method="return",r.arg=e,$(t,r),"throw"===r.method))return m;r.method="throw",r.arg=new TypeError("The iterator does not provide a 'throw' method")}return m}var a=h(n,t.iterator,r.arg);if("throw"===a.type)return r.method="throw",r.arg=a.arg,r.delegate=null,m;var i=a.arg;return i?i.done?(r[t.resultName]=i.value,r.next=t.nextLoc,"return"!==r.method&&(r.method="next",r.arg=e),r.delegate=null,m):i:(r.method="throw",r.arg=new TypeError("iterator result is not an object"),r.delegate=null,m)}function D(t){var e={tryLoc:t[0]};1 in t&&(e.catchLoc=t[1]),2 in t&&(e.finallyLoc=t[2],e.afterLoc=t[3]),this.tryEntries.push(e)}function C(t){var e=t.completion||{};e.type="normal",delete e.arg,t.completion=e}function j(t){this.tryEntries=[{tryLoc:"root"}],t.forEach(D,this),this.reset(!0)}function k(t){if(t){var r=t[i];if(r)return r.call(t);if("function"===typeof t.next)return t;if(!isNaN(t.length)){var a=-1,o=function r(){while(++a<t.length)if(n.call(t,a))return r.value=t[a],r.done=!1,r;return r.value=e,r.done=!0,r};return o.next=o}}return{next:O}}function O(){return{value:e,done:!0}}return g.prototype=_.constructor=y,y.constructor=g,g.displayName=c(y,s,"GeneratorFunction"),t.isGeneratorFunction=function(t){var e="function"===typeof t&&t.constructor;return!!e&&(e===g||"GeneratorFunction"===(e.displayName||e.name))},t.mark=function(t){return Object.setPrototypeOf?Object.setPrototypeOf(t,y):(t.__proto__=y,c(t,s,"GeneratorFunction")),t.prototype=Object.create(_),t},t.awrap=function(t){return{__await:t}},L(E.prototype),E.prototype[o]=function(){return this},t.AsyncIterator=E,t.async=function(e,r,n,a,i){void 0===i&&(i=Promise);var o=new E(l(e,r,n,a),i);return t.isGeneratorFunction(r)?o:o.next().then((function(t){return t.done?t.value:o.next()}))},L(_),c(_,s,"Generator"),_[i]=function(){return this},_.toString=function(){return"[object Generator]"},t.keys=function(t){var e=[];for(var r in t)e.push(r);return e.reverse(),function r(){while(e.length){var n=e.pop();if(n in t)return r.value=n,r.done=!1,r}return r.done=!0,r}},t.values=k,j.prototype={constructor:j,reset:function(t){if(this.prev=0,this.next=0,this.sent=this._sent=e,this.done=!1,this.delegate=null,this.method="next",this.arg=e,this.tryEntries.forEach(C),!t)for(var r in this)"t"===r.charAt(0)&&n.call(this,r)&&!isNaN(+r.slice(1))&&(this[r]=e)},stop:function(){this.done=!0;var t=this.tryEntries[0],e=t.completion;if("throw"===e.type)throw e.arg;return this.rval},dispatchException:function(t){if(this.done)throw t;var r=this;function a(n,a){return s.type="throw",s.arg=t,r.next=n,a&&(r.method="next",r.arg=e),!!a}for(var i=this.tryEntries.length-1;i>=0;--i){var o=this.tryEntries[i],s=o.completion;if("root"===o.tryLoc)return a("end");if(o.tryLoc<=this.prev){var c=n.call(o,"catchLoc"),l=n.call(o,"finallyLoc");if(c&&l){if(this.prev<o.catchLoc)return a(o.catchLoc,!0);if(this.prev<o.finallyLoc)return a(o.finallyLoc)}else if(c){if(this.prev<o.catchLoc)return a(o.catchLoc,!0)}else{if(!l)throw new Error("try statement without catch or finally");if(this.prev<o.finallyLoc)return a(o.finallyLoc)}}}},abrupt:function(t,e){for(var r=this.tryEntries.length-1;r>=0;--r){var a=this.tryEntries[r];if(a.tryLoc<=this.prev&&n.call(a,"finallyLoc")&&this.prev<a.finallyLoc){var i=a;break}}i&&("break"===t||"continue"===t)&&i.tryLoc<=e&&e<=i.finallyLoc&&(i=null);var o=i?i.completion:{};return o.type=t,o.arg=e,i?(this.method="next",this.next=i.finallyLoc,m):this.complete(o)},complete:function(t,e){if("throw"===t.type)throw t.arg;return"break"===t.type||"continue"===t.type?this.next=t.arg:"return"===t.type?(this.rval=this.arg=t.arg,this.method="return",this.next="end"):"normal"===t.type&&e&&(this.next=e),m},finish:function(t){for(var e=this.tryEntries.length-1;e>=0;--e){var r=this.tryEntries[e];if(r.finallyLoc===t)return this.complete(r.completion,r.afterLoc),C(r),m}},catch:function(t){for(var e=this.tryEntries.length-1;e>=0;--e){var r=this.tryEntries[e];if(r.tryLoc===t){var n=r.completion;if("throw"===n.type){var a=n.arg;C(r)}return a}}throw new Error("illegal catch attempt")},delegateYield:function(t,r,n){return this.delegate={iterator:k(t),resultName:r,nextLoc:n},"next"===this.method&&(this.arg=e),m}},t}(t.exports);try{regeneratorRuntime=n}catch(a){Function("r","regeneratorRuntime = r")(n)}},b874:function(t,e,r){},ec85:function(t,e,r){"use strict";r.r(e);var n=function(){var t=this,e=t.$createElement,r=t._self._c||e;return r("div",{staticStyle:{width:"70%"},attrs:{id:"homeAdmin"}},[r("appHeader"),r("navDraw"),r("div",[r("v-toolbar",{staticStyle:{"margin-top":"2.5cm","margin-bottom":"2.5cm"},attrs:{flat:""}},[r("v-row",[r("v-col",[r("v-card",{staticClass:"text-center ml-10 mr-5"},[r("v-card-text",[r("h4",[r("v-icon",{staticClass:"mr-2"},[t._v("mdi-folder-open")]),t._v(t._s(t.$t("hAdmin.f")))],1),r("h2",{staticStyle:{color:"blue"}},[r("b",[t._v(t._s(t.nFolios))])])])],1)],1),r("v-divider",{attrs:{vertical:""}}),r("v-col",[r("v-card",{staticClass:"text-center ml-5 mr-5"},[r("v-card-text",[r("h4",[r("v-icon",{staticClass:"mr-2"},[t._v("mdi-folder-open")]),t._v(t._s(t.$t("hAdmin.doc")))],1),r("h2",{staticStyle:{color:"blue"}},[r("b",[t._v(t._s(t.nDocs))])])])],1)],1),r("v-divider",{attrs:{vertical:""}}),r("v-col",[r("v-card",{staticClass:"text-center ml-5 mr-5"},[r("v-card-text",[r("h4",[r("v-icon",{staticClass:"mr-2"},[t._v("mdi-format-list-bulleted-square")]),t._v(t._s(t.$t("hAdmin.ind")))],1),r("h2",{staticStyle:{color:"green"}},[r("b",[t._v(t._s(t.nInds))])])])],1)],1),r("v-divider",{attrs:{vertical:""}}),r("v-col",[r("v-card",{staticClass:"text-center ml-5 mr-5"},[r("v-card-text",[r("h4",[r("v-icon",{staticClass:"mr-2"},[t._v("mdi-note-multiple")]),t._v(t._s(t.$t("hAdmin.tag")))],1),r("h2",{staticStyle:{color:"green"}},[r("b",[t._v(t._s(t.nTags))])])])],1)],1),r("v-divider",{attrs:{vertical:""}}),r("v-col",[r("v-card",{staticClass:"text-center ml-5 mr-5"},[r("v-card-text",[r("h4",[r("v-icon",{staticClass:"mr-2"},[t._v("mdi-format-list-bulleted-square")]),t._v(t._s(t.$t("hAdmin.pal")))],1),r("h2",{staticStyle:{color:"green"}},[r("b",[t._v(t._s(t.nPals))])])])],1)],1),r("v-divider",{attrs:{vertical:""}}),r("v-col",[r("v-card",{staticClass:"text-center ml-5 mr-5"},[r("v-card-text",[r("h4",[r("v-icon",{staticClass:"mr-2"},[t._v("mdi-account-multiple")]),t._v(t._s(t.$t("hAdmin.users")))],1),r("h2",{staticStyle:{color:"blue"}},[r("b",[t._v(t._s(t.nUsers))])])])],1)],1)],1)],1)],1),r("div",{staticClass:"mt-12"},[r("h3",{staticClass:"ml-10 mt-6"},[t._v(t._s("Foram inseridos "+t.percent+"% dos fólios na última semana"))]),r("v-row",[r("v-col",[r("v-card",{staticClass:"text-center ml-10 mt-6 mr-10",attrs:{color:"#2A3F54",dark:""}},[r("v-card-text",[r("h2",[t._v(t._s(t.$t("hAdmin.ins")))])])],1),1==t.condition?r("v-card",{staticClass:"ml-10 mt-6 mr-10"},[r("v-card-actions",[r("v-sparkline",{attrs:{labels:t.labels,value:t.number,"label-size":"3",color:"red","line-width":"2",padding:"16"}})],1)],1):t._e()],1)],1)],1)],1)},a=[],i=(r("4160"),r("13d5"),r("ac1f"),r("1276"),r("159b"),r("96cf"),r("1da1")),o=r("bc3a"),s=r.n(o),c=r("71c2"),l=r("75ce"),h={data:function(){return{nFolios:0,nDocs:0,nInds:0,nTags:0,nPals:0,nUsers:0,value:[],labels:[],number:[],percent:0,condition:!1}},components:{appHeader:c["a"],navDraw:l["a"]},created:function(){var t=Object(i["a"])(regeneratorRuntime.mark((function t(){var e,r,n,a,i,o,c,l,h,u=this;return regeneratorRuntime.wrap((function(t){while(1)switch(t.prev=t.next){case 0:for(e=new Date,r=e.getMonth()+1+"/"+e.getDate()+"/"+e.getFullYear(),n=new Date(r).getTime(),a=-14;a<=0;a++)i=new Date(n+24*a*60*60*1e3),o=i.getDate(),o<=9&&(o="0"+o),c=i.getMonth()+1,c<=9&&(c="0"+c),l=i.getFullYear(),h=c+"/"+o+"/"+l,this.labels.push(h);return s.a.get("https://leonardo2.di.uminho.pt/api/users/users?nome=".concat(this.$store.state.user._id),{headers:{Authorization:"Bearer: ".concat(this.$store.state.jwt)}}).then((function(t){u.nUsers=t.data.users.length})).catch((function(t){u.errors.push(t)})),t.next=7,s.a.get("https://leonardo2.di.uminho.pt/api/folios/folios?nome=".concat(this.$store.state.user._id),{headers:{Authorization:"Bearer: ".concat(this.$store.state.jwt)}}).then((function(t){u.nFolios=t.data.folios.length;for(var e=0;e<t.data.folios.length;e++){var r=t.data.folios[e].data,n=r.split(/[\s-:]+/),a=n[1]+"/"+n[2]+"/"+n[0];u.value.push(a)}u.nDocs=t.data.folios.length})).catch((function(t){u.errors.push(t)}));case 7:return t.next=9,this.contains();case 9:s.a.get("https://leonardo2.di.uminho.pt/api/folios/tags?nome=".concat(this.$store.state.user._id),{headers:{Authorization:"Bearer: ".concat(this.$store.state.jwt)}}).then((function(t){u.nTags=t.data.tags.length})).catch((function(t){u.errors.push(t)})),s.a.get("https://leonardo2.di.uminho.pt/api/folios/index?nome=".concat(this.$store.state.user._id),{headers:{"Content-Type":"multipart/form-data",Authorization:"Bearer: ".concat(this.$store.state.jwt)}}).then((function(t){u.nInds=t.data.indexs.length;for(var e=0,r=0;r<t.data.indexs.length;r++)e+=t.data.indexs[r].n_ocorrencias;u.nPals=e})).catch((function(t){u.errors.push(t)}));case 11:case"end":return t.stop()}}),t,this)})));function e(){return t.apply(this,arguments)}return e}(),methods:{contains:function(){for(var t=0;t<this.labels.length;t++)this.number[t]=this.getOccurrence(this.value,this.labels[t]);this.percent=(this.number.reduce((function(t,e){return t+e}),0)/this.nFolios*100).toPrecision(4),this.condition=!0},getOccurrence:function(t,e){var r=0;return t.forEach((function(t){return t===e&&r++})),r}}},u=h,d=(r("51fe"),r("2877")),f=r("6544"),p=r.n(f),m=r("b0af"),v=r("99d9"),g=r("62ad"),y=r("ce7e"),b=r("132d"),x=r("0fd9"),w=(r("99af"),r("cb29"),r("caad"),r("d81d"),r("fb6a"),r("a9e3"),r("d3b7"),r("25f0"),r("5530")),_=r("53ca"),L=r("a9ad"),E=r("58df"),S=r("2909");function $(t,e){var r=e.minX,n=e.maxX,a=e.minY,i=e.maxY,o=t.length,s=Math.max.apply(Math,Object(S["a"])(t)),c=Math.min.apply(Math,Object(S["a"])(t)),l=(n-r)/(o-1),h=(i-a)/(s-c||1);return t.map((function(t,e){return{x:r+e*l,y:i-(t-c)*h,value:t}}))}function D(t,e){var r=e.minX,n=e.maxX,a=e.minY,i=e.maxY,o=t.length,s=Math.max.apply(Math,Object(S["a"])(t)),c=Math.min.apply(Math,Object(S["a"])(t));c>0&&(c=0),s<0&&(s=0);var l=n/o,h=(i-a)/(s-c||1),u=i-Math.abs(c*h);return t.map((function(t,e){var n=Math.abs(h*t);return{x:r+e*l,y:u-n+ +(t<0)*n,height:n,value:t}}))}r("a15b");function C(t){return parseInt(t,10)}function j(t,e,r){return C(t.x+r.x)===C(2*e.x)&&C(t.y+r.y)===C(2*e.y)}function k(t,e){return Math.sqrt(Math.pow(e.x-t.x,2)+Math.pow(e.y-t.y,2))}function O(t,e,r){var n={x:t.x-e.x,y:t.y-e.y},a=Math.sqrt(n.x*n.x+n.y*n.y),i={x:n.x/a,y:n.y/a};return{x:e.x+i.x*r,y:e.y+i.y*r}}function M(t,e){var r=arguments.length>2&&void 0!==arguments[2]&&arguments[2],n=arguments.length>3&&void 0!==arguments[3]?arguments[3]:75,a=t.shift(),i=t[t.length-1];return(r?"M".concat(a.x," ").concat(n-a.x+2," L").concat(a.x," ").concat(a.y):"M".concat(a.x," ").concat(a.y))+t.map((function(r,n){var i=t[n+1],o=t[n-1]||a,s=i&&j(i,r,o);if(!i||s)return"L".concat(r.x," ").concat(r.y);var c=Math.min(k(o,r),k(i,r)),l=c/2<e,h=l?c/2:e,u=O(o,r,h),d=O(i,r,h);return"L".concat(u.x," ").concat(u.y,"S").concat(r.x," ").concat(r.y," ").concat(d.x," ").concat(d.y)})).join("")+(r?"L".concat(i.x," ").concat(n-a.x+2," Z"):"")}var A=Object(E["a"])(L["a"]).extend({name:"VSparkline",inheritAttrs:!1,props:{autoDraw:Boolean,autoDrawDuration:{type:Number,default:2e3},autoDrawEasing:{type:String,default:"ease"},autoLineWidth:{type:Boolean,default:!1},color:{type:String,default:"primary"},fill:{type:Boolean,default:!1},gradient:{type:Array,default:function(){return[]}},gradientDirection:{type:String,validator:function(t){return["top","bottom","left","right"].includes(t)},default:"top"},height:{type:[String,Number],default:75},labels:{type:Array,default:function(){return[]}},labelSize:{type:[Number,String],default:7},lineWidth:{type:[String,Number],default:4},padding:{type:[String,Number],default:8},showLabels:Boolean,smooth:{type:[Boolean,Number,String],default:!1},type:{type:String,default:"trend",validator:function(t){return["trend","bar"].includes(t)}},value:{type:Array,default:function(){return[]}},width:{type:[Number,String],default:300}},data:function(){return{lastLength:0}},computed:{parsedPadding:function(){return Number(this.padding)},parsedWidth:function(){return Number(this.width)},parsedHeight:function(){return parseInt(this.height,10)},parsedLabelSize:function(){return parseInt(this.labelSize,10)||7},totalHeight:function(){var t=this.parsedHeight;return this.hasLabels&&(t+=1.5*parseInt(this.labelSize,10)),t},totalWidth:function(){var t=this.parsedWidth;return"bar"===this.type&&(t=Math.max(this.value.length*this._lineWidth,t)),t},totalValues:function(){return this.value.length},_lineWidth:function(){if(this.autoLineWidth&&"trend"!==this.type){var t=this.parsedPadding*(this.totalValues+1);return(this.parsedWidth-t)/this.totalValues}return parseFloat(this.lineWidth)||4},boundary:function(){if("bar"===this.type)return{minX:0,maxX:this.totalWidth,minY:0,maxY:this.parsedHeight};var t=this.parsedPadding;return{minX:t,maxX:this.totalWidth-t,minY:t,maxY:this.parsedHeight-t}},hasLabels:function(){return Boolean(this.showLabels||this.labels.length>0||this.$scopedSlots.label)},parsedLabels:function(){for(var t=[],e=this._values,r=e.length,n=0;t.length<r;n++){var a=e[n],i=this.labels[n];i||(i="object"===Object(_["a"])(a)?a.value:a),t.push({x:a.x,value:String(i)})}return t},normalizedValues:function(){return this.value.map((function(t){return"number"===typeof t?t:t.value}))},_values:function(){return"trend"===this.type?$(this.normalizedValues,this.boundary):D(this.normalizedValues,this.boundary)},textY:function(){var t=this.parsedHeight;return"trend"===this.type&&(t-=4),t},_radius:function(){return!0===this.smooth?8:Number(this.smooth)}},watch:{value:{immediate:!0,handler:function(){var t=this;this.$nextTick((function(){if(t.autoDraw&&"bar"!==t.type&&t.$refs.path){var e=t.$refs.path,r=e.getTotalLength();t.fill?(e.style.transformOrigin="bottom center",e.style.transition="none",e.style.transform="scaleY(0)",e.getBoundingClientRect(),e.style.transition="transform ".concat(t.autoDrawDuration,"ms ").concat(t.autoDrawEasing),e.style.transform="scaleY(1)"):(e.style.transition="none",e.style.strokeDasharray=r+" "+r,e.style.strokeDashoffset=Math.abs(r-(t.lastLength||0)).toString(),e.getBoundingClientRect(),e.style.transition="stroke-dashoffset ".concat(t.autoDrawDuration,"ms ").concat(t.autoDrawEasing),e.style.strokeDashoffset="0"),t.lastLength=r}}))}}},methods:{genGradient:function(){var t=this,e=this.gradientDirection,r=this.gradient.slice();r.length||r.push("");var n=Math.max(r.length-1,1),a=r.reverse().map((function(e,r){return t.$createElement("stop",{attrs:{offset:r/n,"stop-color":e||"currentColor"}})}));return this.$createElement("defs",[this.$createElement("linearGradient",{attrs:{id:this._uid,gradientUnits:"userSpaceOnUse",x1:"left"===e?"100%":"0",y1:"top"===e?"100%":"0",x2:"right"===e?"100%":"0",y2:"bottom"===e?"100%":"0"}},a)])},genG:function(t){return this.$createElement("g",{style:{fontSize:"8",textAnchor:"middle",dominantBaseline:"mathematical",fill:"currentColor"}},t)},genPath:function(){var t=$(this.normalizedValues,this.boundary);return this.$createElement("path",{attrs:{d:M(t,this._radius,this.fill,this.parsedHeight),fill:this.fill?"url(#".concat(this._uid,")"):"none",stroke:this.fill?"none":"url(#".concat(this._uid,")")},ref:"path"})},genLabels:function(t){var e=this,r=this.parsedLabels.map((function(r,n){return e.$createElement("text",{attrs:{x:r.x+t+e._lineWidth/2,y:e.textY+.75*e.parsedLabelSize,"font-size":Number(e.labelSize)||7}},[e.genLabel(r,n)])}));return this.genG(r)},genLabel:function(t,e){return this.$scopedSlots.label?this.$scopedSlots.label({index:e,value:t.value}):t.value},genBars:function(){if(this.value&&!(this.totalValues<2)){var t=D(this.normalizedValues,this.boundary),e=(Math.abs(t[0].x-t[1].x)-this._lineWidth)/2;return this.$createElement("svg",{attrs:{display:"block",viewBox:"0 0 ".concat(this.totalWidth," ").concat(this.totalHeight)}},[this.genGradient(),this.genClipPath(t,e,this._lineWidth,"sparkline-bar-"+this._uid),this.hasLabels?this.genLabels(e):void 0,this.$createElement("g",{attrs:{"clip-path":"url(#sparkline-bar-".concat(this._uid,"-clip)"),fill:"url(#".concat(this._uid,")")}},[this.$createElement("rect",{attrs:{x:0,y:0,width:this.totalWidth,height:this.height}})])])}},genClipPath:function(t,e,r,n){var a=this,i="number"===typeof this.smooth?this.smooth:this.smooth?2:0;return this.$createElement("clipPath",{attrs:{id:"".concat(n,"-clip")}},t.map((function(t){return a.$createElement("rect",{attrs:{x:t.x+e,y:t.y,width:r,height:t.height,rx:i,ry:i}},[a.autoDraw?a.$createElement("animate",{attrs:{attributeName:"height",from:0,to:t.height,dur:"".concat(a.autoDrawDuration,"ms"),fill:"freeze"}}):void 0])})))},genTrend:function(){return this.$createElement("svg",this.setTextColor(this.color,{attrs:Object(w["a"])(Object(w["a"])({},this.$attrs),{},{display:"block","stroke-width":this._lineWidth||1,viewBox:"0 0 ".concat(this.width," ").concat(this.totalHeight)})}),[this.genGradient(),this.hasLabels&&this.genLabels(-this._lineWidth/2),this.genPath()])}},render:function(t){if(!(this.totalValues<2))return"trend"===this.type?this.genTrend():this.genBars()}}),N=r("71d9"),P=Object(d["a"])(u,n,a,!1,null,"ce15819c",null);e["default"]=P.exports;p()(P,{VCard:m["a"],VCardActions:v["a"],VCardText:v["b"],VCol:g["a"],VDivider:y["a"],VIcon:b["a"],VRow:x["a"],VSparkline:A,VToolbar:N["a"]})}}]);
//# sourceMappingURL=chunk-62af41f9.e45f1116.js.map