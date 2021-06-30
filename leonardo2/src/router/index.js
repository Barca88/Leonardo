import Vue from "vue";
import VueRouter from "vue-router";
import store from "../store";
import * as VueGoogleMaps from "vue2-google-maps";

import Table from "@/views/Importacao/Table.vue"
import ErrorTable from "@/views/Importacao/ErrorTable.vue"
import ImportMenu from '@/views/Importacao/ImportMenu.vue'
import ImportDashboard from '@/views/Importacao/ImportDashboard.vue'

import TestsLayout from "@/tests_modulo/TestsLayout.vue";
import Preparation from "@/tests_modulo/views/Preparation.vue";
import Evaluation from "@/tests_modulo/views/Evaluation/Evaluation.vue";
import EvaluationTest from "@/tests_modulo/views/Evaluation/EvaluationTest.vue";
import Management from "@/tests_modulo/views/Management.vue";
import ResultsDashboard from "@/tests_modulo/views/ResultsDashboard.vue";

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
    path: "definitions",
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
      } else if (!store.getters.isAdmin) {
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
    path: "/tests",
    component: TestsLayout,
    children: [
      {
        path: "preparation",
        name: "Preparation",
        component: Preparation,
        beforeEnter(to, from, next) {
          if (!store.getters.isAuthenticated) {
            next(`/login`);
          } else {
            next();
          }
        },
      },
      {
        path: "evaluation",
        name: "Evaluation",
        component: Evaluation,
        beforeEnter(to, from, next) {
          if (!store.getters.isAuthenticated) {
            next(`/login`);
          } else {
            next();
          }
        },
      },
      {
        path: "evaluation/:testid",
        name: "EvaluationTest",
        component: EvaluationTest,
        beforeEnter(to, from, next) {
          if (!store.getters.isAuthenticated) {
            next(`/login`);
          } else {
            next();
          }
        },
      },
      {
        path: "management",
        name: "Management",
        component: Management,
        beforeEnter(to, from, next) {
          if (!store.getters.isAuthenticated) {
            next(`/login`);
          } else {
            next();
          }
        },
      },
      {
        path: "results",
        name: "results",
        component: ResultsDashboard,
        beforeEnter(to, from, next) {
          if (!store.getters.isAuthenticated) {
            next(`/login`);
          } else {
            next();
          }
        },
      },

      /* Rotas de Importacao de Questões */
      { 
        path: '/importacao/import', 
        component: ImportMenu,
        beforeEnter(to, from, next) {
          if (!store.getters.isAuthenticated) {
            next(`/login`);
          } else {
            next();
          }
        },
      },
      { 
        path: '/importacao/table', 
        component: Table,
        beforeEnter(to, from, next) {
          if (!store.getters.isAuthenticated) {
            next(`/login`);
          } else {
            next();
          }
        },
      },
      { 
        path: '/importacao/errors', 
        component: ErrorTable,
        beforeEnter(to, from, next) {
          if (!store.getters.isAuthenticated) {
            next(`/login`);
          } else {
            next();
          }
        },
      },
      { 
        path: '/importacao/dashboard', 
        component: ImportDashboard,
        beforeEnter(to, from, next) {
          if (!store.getters.isAuthenticated) {
            next(`/login`);
          } else {
            next();
          }
        }, 
      },
      { path: "/*",
        name: "Pedidos",
        component: () => import("../views/PageNotFound.vue"), }
    ],
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
