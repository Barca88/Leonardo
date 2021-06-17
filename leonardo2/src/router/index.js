import Vue from "vue";
import VueRouter from "vue-router";
import store from "../store";
import * as VueGoogleMaps from "vue2-google-maps";

import Table from "@/views/Importação/Table.vue"
import ErrorTable from "@/views/Importação/ErrorTable.vue"
import ImportMenu from '@/views/Importação/ImportMenu.vue'
import ImportDashboard from '@/views/Importação/ImportDashboard.vue'

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
    path: "/admin",
    redirect: `/admin/login`,
  },
  {
    path: "/home",
    name: "home",
    component: () => import("../views/HomeAdmin.vue"),
    beforeEnter(to, from, next) {
      if (!store.getters.isAuthenticated) {
        next(`/login`);
      } else {
        next();
      }
    },
  },
  {
    path: "/resultados",
    name: "resultados",
    component: () => import("../views/Resultados.vue"),
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
    path: "users",
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
    path: "folios/indices",
    name: "Indices",
    component: () => import("../views/Indices.vue"),
    beforeEnter(to, from, next) {
      if (!store.getters.isAuthenticated) {
        next(`/login`);
      } else {
        next();
      }
    },
  },
  {
    path: "folios/tags",
    name: "Tags",
    component: () => import("../views/Definitions.vue"),
    beforeEnter(to, from, next) {
      if (!store.getters.isAuthenticated) {
        next(`/login`);
      } else {
        next();
      }
    },
  },
  {
    path: "tagging",
    name: "ListaFolios",
    component: () => import("../views/tagging/ListaFolios.vue"),
    beforeEnter(to, from, next) {
      if (!store.getters.isAuthenticated) {
        next(`/login`);
      } else {
        next();
      }
    },
  },
  {
    path: "tagging/editor",
    name: "Editor",
    component: () => import("../views/tagging/Editor.vue"),
    beforeEnter(to, from, next) {
      if (!store.getters.isAuthenticated) {
        next(`/login`);
      } else {
        next();
      }
    },
  },
  {
    path: "tagging/modernizador",
    name: "Atualiza",
    component: () => import("../views/tagging/Atualiza.vue"),
    beforeEnter(to, from, next) {
      if (!store.getters.isAuthenticated) {
        next(`/login`);
      } else {
        next();
      }
    },
  },
  {
    path: "tagging/folioAnotado/ver/:id",
    name: "Editor",
    component: () => import("../views/tagging/VerFolio.vue"),
    beforeEnter(to, from, next) {
      if (!store.getters.isAuthenticated) {
        next(`/login`);
      } else {
        next();
      }
    },
  },
  {
    path: "tagging/folioAtualizado/ver/:id",
    name: "Editor",
    component: () => import("../views/tagging/VerAtualizado.vue"),
    beforeEnter(to, from, next) {
      if (!store.getters.isAuthenticated) {
        next(`/login`);
      } else {
        next();
      }
    },
  },
  {
    path: "tagging/tags/dicionario",
    name: "Editor",
    component: () => import("../views/tagging/DicionarioTags.vue"),
    beforeEnter(to, from, next) {
      if (!store.getters.isAuthenticated) {
        next(`/login`);
      } else {
        next();
      }
    },
  },
  {
    path: "tagging/anotaBase",
    name: "AnotaBase",
    component: () => import("../views/tagging/AnotaBase.vue"),
    beforeEnter(to, from, next) {
      if (!store.getters.isAuthenticated) {
        next(`/login`);
      } else {
        next();
      }
    },
  },
  {
    path: "tagging/tags/lista",
    name: "Editor",
    component: () => import("../views/tagging/ListaTags.vue"),
    beforeEnter(to, from, next) {
      if (!store.getters.isAuthenticated) {
        next(`/login`);
      } else {
        next();
      }
    },
  },
  {
    path: "tagging/regras/lista",
    name: "Editor",
    component: () => import("../views/tagging/ListaRegras.vue"),
    beforeEnter(to, from, next) {
      if (!store.getters.isAuthenticated) {
        next(`/login`);
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
    path: "import",
    name: "Import",
    component: () => import("../views/Import.vue"),
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
    path: "analise",
    name: "Analise",
    component: () => import("../views/AnáliseAdmin.vue"),
    beforeEnter(to, from, next) {
      if (!store.getters.isAuthenticated) {
        next(`/login`);
      } else {
        next();
      }
    },
  },
  {
    path: "resultados",
    name: "AdminResultados",
    component: () => import("../views/ResultadoAdmin.vue"),
    beforeEnter(to, from, next) {
      if (!store.getters.isAuthenticated) {
        next(`/login`);
      } else {
        next();
      }
    },
  },
  {
    path: "homeAdmin",
    name: "HomeAdmin",
    component: () => import("../views/HomeAdmin.vue"),
    beforeEnter(to, from, next) {
      if (!store.getters.isAuthenticated) {
        next(`/login`);
      } else {
        next();
      }
    },
  },
  {
    path: "documentacao",
    name: "Documentação",
    component: () => import("../views/Documentacao.vue"),
    beforeEnter(to, from, next) {
      if (!store.getters.isAuthenticated) {
        next(`/login`);
      } else {
        next();
      }
    },
  },
  {
    path: "pesquisas",
    name: "PesquisasRealizadas",
    component: () => import("../views/PesquisasRealizadas.vue"),
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
    path: "mapas",
    name: "GoogleMap",
    component: () => import("../views/GoogleMap.vue"),
    beforeEnter(to, from, next) {
      if (!store.getters.isAuthenticated) {
        next(`/login`);
      } else {
        next();
      }
    },
  },
  {
    path: "localidades",
    name: "Places",
    component: () => import("../views/PlaceList.vue"),
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
    path: "localidades/:nome",
    name: "Place",
    component: () => import("../views/GoogleMapOnePlace.vue"),
    beforeEnter(to, from, next) {
      if (!store.getters.isAuthenticated) {
        next(`/login`);
      } else {
        next();
      }
    },
  },
  {
    path: "processamento",
    name: "Processamento",
    component: () => import("../views/ProgressBar.vue"),
    beforeEnter(to, from, next) {
      if (!store.getters.isAuthenticated) {
        next(`/login`);
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
      },
      {
        path: "evaluation",
        name: "Evaluation",
        component: Evaluation,
      },
      {
        path: "evaluation/:testid",
        name: "EvaluationTest",
        component: EvaluationTest,
      },
      {
        path: "management",
        name: "Management",
        component: Management,
      },
      {
        path: "results",
        name: "results",
        component: ResultsDashboard,
      },

      /* Rotas de Importação de Questões */
      { path: '/importacao/import', component: ImportMenu },
      { path: '/importacao/table', component: Table },
      { path: '/importacao/errors', component: ErrorTable },
      { path: '/importacao/dashboard', component: ImportDashboard }

    ],
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
