import Vue from "vue";
import VueRouter from "vue-router";
import store from "../store";
import * as VueGoogleMaps from "vue2-google-maps";

Vue.use(VueRouter);

Vue.use(VueGoogleMaps, {
  load: {
    key: "AIzaSyAP-__9IVdlFFWVjAwMAlj91Bg-Aq-hUKQ",
  },
});

const originalPush = VueRouter.prototype.push;
VueRouter.prototype.push = function push(location) {
  return originalPush.call(this, location).catch((err) => err);
};

const routes = [
  {
    path: "/",
    redirect: `/home`,
  },
  {
    path: "/home",
    name: "Blank",
    component: () => import("../views/Blank.vue"),
    beforeEnter(to, from, next) {
      if (!store.getters.isAuthenticated) {
        next(`/login`);
      } else {
        next();
      }
    },
  },
  {
    path: "/domain",
    name: "Domain",
    component: () => import("../views/Dominios.vue"),
    beforeEnter(to, from, next) {
      if (!store.getters.isAuthenticated) {
        next(`/login`);
      } else {
        next();
      }
    },
  },
  {
    path: '/prodQuestao',
    name: 'ProdQuestao',
    component: () => import("../views/prodQuestao.vue"),
    beforeEnter(to, from, next) {
      if (!store.getters.isAuthenticated) {
        next(`/login`);
      } else {
        next();
      }
    }
  },
  {
    path: '/prodDominio',
    name: 'ProdDominio',
    component: () => import("../views/ProdDominio.vue"),
    beforeEnter(to, from, next) {
      if (!store.getters.isAuthenticated) {
        next(`/login`);
      } else {
        next();
      }
    }
  },
  {
    path: '/questions',
    name: 'Questions',
    component: () => import("../views/Questoes.vue"),
    beforeEnter(to, from, next) {
      if (!store.getters.isAuthenticated) {
        next(`/login`);
      } else {
        next();
      }
    }
  },
  {
    path: "/login",
    name: "Login",
    component: () => import("../views/Login.vue"),
    beforeEnter(to, from, next) {
      if (store.getters.isAuthenticated) {
        next(`/`);
      } else {
        next();
      }
    },
  },
  {
    path: "registo",
    name: "Registo",
    component: () => import("../views/Registo.vue"),
  },
  {
    path: "/users",
    name: "Utilizadores",
    component: () => import("../views/Utilizadores.vue"),
    beforeEnter(to, from, next) {
      if (!store.getters.isAuthenticated) {
        next(`/login`);
      } else if (!store.getters.isAdmin) {
        next(`/`);
      } else {
        next();
      }
    },
  },
  {
    path: "/responsible",
    name: "Responsaveis",
    component: () => import("../views/Responsaveis.vue"),
    beforeEnter(to, from, next) {
      if (!store.getters.isAuthenticated) {
        next(`/login`);
      } else if (!store.getters.isAdmin) {
        next(`/`);
      } else {
        next();
      }
    },
  },
  {
    path: "/teacher",
    name: "Professores",
    component: () => import("../views/Professores.vue"),
    beforeEnter(to, from, next) {
      if (!store.getters.isAuthenticated) {
        next(`/login`);
      } else if (!store.getters.isAdmin) {
        next(`/`);
      } else {
        next();
      }
    },
  },
  {
    path: "/student",
    name: "Alunos",
    component: () => import("../views/Alunos.vue"),
    beforeEnter(to, from, next) {
      if (!store.getters.isAuthenticated) {
        next(`/login`);
      } else if (!store.getters.isAdmin) {
        next(`/`);
      } else {
        next();
      }
    },
  },
  {
    path: "/users/ver",
    name: "Perfil",
    component: () => import("../views/Perfil.vue"),
    beforeEnter(to, from, next) {
      if (!store.getters.isAuthenticated) {
        next(`/login`);
      } else {
        next();
      }
    },
  },
  {
    path: "/historico",
    name: "HistorialAcesso",
    component: () => import("../views/HistorialAcesso.vue"),
    beforeEnter(to, from, next) {
      if (!store.getters.isAuthenticated) {
        next(`/login`);
      } else if (!store.getters.isAdmin) {
        next(`/`);
      } else {
        next();
      }
    },
  },
  {
    path: "about",
    name: "Acerca",
    component: () => import("../views/About.vue"),
    beforeEnter(to, from, next) {
      if (!store.getters.isAuthenticated) {
        next(`/login`);
      } else {
        next();
      }
    },
  },
  {
    path: "/definitions",
    name: "Definições",
    component: () => import("../views/Definitions.vue"),
    beforeEnter(to, from, next) {
      if (!store.getters.isAuthenticated) {
        next(`/login`);
      } else if (!store.getters.isAdmin) {
        next(`/`);
      } else {
        next();
      }
    },
  },
  {
    path: "/pedidos",
    name: "Pedidos",
    component: () => import("../views/PedidosAcesso.vue"),
    beforeEnter(to, from, next) {
      if (!store.getters.isAuthenticated) {
        next(`/login`);
      } else if (!store.getters.isAdmin) {
        next(`/`);
      } else {
        next();
      }
    },
  },
  {
    path: "/documentacao",
    name: "Documentação",
    component: () => import("../views/Documentacao.vue"),
    beforeEnter(to, from, next) {
      if (!store.getters.isAuthenticated) {
        next(`/login`);
      } else if (store.getters.isStudent) {
        next(`/`);
      } else {
        next();
      }
    },
  },
  {
    path: "/uAtivos",
    name: "UtilizadoresAtivos",
    component: () => import("../views/UtilizadoresAtivos.vue"),
    beforeEnter(to, from, next) {
      if (!store.getters.isAuthenticated) {
        next(`/login`);
      } else if (!store.getters.isAdmin) {
        next(`/`);
      } else {
        next();
      }
    },
  },
  {
    path: "/usersImport",
    name: "UserImportation",
    component: () => import("../views/UserImportation.vue"),
    beforeEnter(to, from, next) {
      if (!store.getters.isAuthenticated) {
        next(`/login`);
      } else if (!store.getters.isAdmin) {
        next(`/`);
      } else {
        next();
      }
    },
  },
  
      {
        path: "/preparation",
        name: "Preparation",
        component: () => import("../views/Preparation.vue"),
        beforeEnter(to, from, next) {
          if (!store.getters.isAuthenticated) {
            next(`/login`);
          } else {
            next();
          }
        },
      },
      {
        path: "/evaluation",
        name: "Evaluation",
        component: () => import("../views/Evaluation/Evaluation.vue"),
        beforeEnter(to, from, next) {
          if (!store.getters.isAuthenticated) {
            next(`/login`);
          } else {
            next();
          }
        },
      },
      {
        path: "/evaluation/:testid",
        name: "EvaluationTest",
        component: () => import("../views/Evaluation/EvaluationTest.vue"),
        beforeEnter(to, from, next) {
          if (!store.getters.isAuthenticated) {
            next(`/login`);
          } else {
            next();
          }
        },
      },
      {
        path: "/individualResult/:testid",
        name: "IndividualResult",
        component: () => import("../views/IndividualResult.vue"),
        beforeEnter(to, from, next) {
          if (!store.getters.isAuthenticated) {
            next(`/login`);
          } else {
            next();
          }
        },
      },
      {
        path: "/management",
        name: "Management",
        component: () => import("../views/Management.vue"),
        beforeEnter(to, from, next) {
          if (!store.getters.isAuthenticated) {
            next(`/login`);
          } else if (store.getters.isStudent) {
              next(`/`);
          } else {
            next();
          }
        },
      },
      {
        path: "/results",
        name: "results",
        component: () => import("../views/ResultsDashboard.vue"),
        beforeEnter(to, from, next) {
          if (!store.getters.isAuthenticated) {
            next(`/login`);
          } else if (store.getters.isStudent) {
            next(`../views/StudentResultsDashboard.vue`);
          } else {
            next();
          }
        },
      },
      {
        path: "/testresults",
        name: "testresults",
        component: () => import("../views/Results.vue"),
        beforeEnter(to, from, next) {
          if (!store.getters.isAuthenticated) {
            next(`/login`);
          } else if (store.getters.isStudent) {
            next(`/personalTestResults`);
          } else {
            next();
          }
        },
        
      },
      {
        path: "/personalTestResults",
        name: "personalTestResults",
        component: () => import("../views/StudentsResults.vue"),
        beforeEnter(to, from, next) {
          if (!store.getters.isAuthenticated) {
            next(`/login`);
          } else if (store.getters.isStudent) {
            next();
          } else {
            next();
          }
        },
        
      },


      /* Rotas de Importacao de Questões */
      { 
        path: '/importacao/import', 
        component: () => import("../views/Importacao/ImportMenu.vue"),
        beforeEnter(to, from, next) {
          if (!store.getters.isAuthenticated) {
            next(`/login`);
          } else if (!store.getters.isAdmin) {
            next(`/`);
          } else {
            next();
          }
        },
      },
      { 
        path: '/importacao/table', 
        component: () => import("../views/Importacao/Table.vue"),
        beforeEnter(to, from, next) {
          if (!store.getters.isAuthenticated) {
            next(`/login`);
          } else if (!store.getters.isAdmin) {
            next(`/`);
          } else {
            next();
          }
        },
      },
      { 
        path: '/importacao/errors', 
        component: () => import("../views/Importacao/ErrorTable.vue"),
        beforeEnter(to, from, next) {
          if (!store.getters.isAuthenticated) {
            next(`/login`);
          } else if (!store.getters.isAdmin) {
            next(`/`);
          } else {
            next();
          }
        },
      },
      {
        path: '/importacao/dashboard', 
        component: () => import("../views/Importacao/ImportDashboard.vue"),
        beforeEnter(to, from, next) {
          if (!store.getters.isAuthenticated) {
            next(`/login`);
          } else if (!store.getters.isAdmin) {
            next(`/`);
          } else {
            next();
          }
        }, 
      
      }
      /*{ path: "/*",
        name: "Pedidos",
        component: () => import("../views/PageNotFound.vue"), }*/
    
  
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
