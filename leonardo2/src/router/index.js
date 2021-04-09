import Vue from 'vue'
import VueRouter from 'vue-router'
import store from '../store'
import * as VueGoogleMaps from 'vue2-google-maps'



Vue.use(VueRouter)

Vue.use(
  VueGoogleMaps, {
    load: {
      key: 'AIzaSyAP-__9IVdlFFWVjAwMAlj91Bg-Aq-hUKQ'
    }
  }
)

const originalPush = VueRouter.prototype.push;
VueRouter.prototype.push = function push(location) {
  return originalPush.call(this, location).catch(err => err);
}

const routes = [
  {
    path: '/',
    redirect : `/home`
  },
  {
    path: '/login',
    redirect : `/admin/login`
  },
  {
    path: '/admin',
    redirect : `/admin/login`
  },
  {
    path: '/home',
    name: 'home',
    component: () => import('../views/Home.vue')
  },
  {
    path: '/resultados',
    name: 'resultados',
    component: () => import('../views/Resultados.vue')
  },
  {
    path: '/admin',
    component: {
      render(c) { return c('router-view')}
    },
    children:[
      {
        path: 'login',
        name: 'Login',
        component: () => import('../views/Login.vue')
      },
      {
        path: 'registo',
        name: 'Registo',
        component: () => import('../views/Registo.vue')
      },
      {
        path: 'users',
        name: 'Utilizadores',
        component: () => import('../views/Utilizadores.vue'),
        beforeEnter (to, from, next) {
          if (!store.getters.isAuthenticated) {
            next(`/login`)
          }
          else if (!store.getters.isAdmin) {
            next(`/homeAdmin`)
          }
          else {
            next()
          }
        }
      },
      {
        path: 'users/ver',
        name: 'Perfil',
        component: () => import('../views/Perfil.vue'),
        beforeEnter (to, from, next) {
          if (!store.getters.isAuthenticated) {
            next(`/login`)
          } else {
            next()
          }
        }
      },
      {
        path: 'folios',
        name: 'Folios',
        component: () => import('../views/Folios.vue'),
        beforeEnter (to, from, next) {
          if (!store.getters.isAuthenticated) {
            next(`/login`)
          } else {
            next()
          }
        }
      },
      {
        path: 'folios/indices',
        name: 'Indices',
        component: () => import('../views/Indices.vue'),
        beforeEnter (to, from, next) {
          if (!store.getters.isAuthenticated) {
            next(`/login`)
          } else {
            next()
          }
        }
      },
      {
        path: 'folios/tags',
        name: 'Tags',
        component: () => import('../views/Definitions.vue'),
        beforeEnter (to, from, next) {
          if (!store.getters.isAuthenticated) {
            next(`/login`)
          } else {
            next()
          }
        }
      },
      {
        path: 'tagging',
        name: 'ListaFolios',
        component: () => import('../views/tagging/ListaFolios.vue'),
        beforeEnter (to, from, next) {
          if (!store.getters.isAuthenticated) {
            next(`/login`)
          } else {
            next()
          }
        }
      },
      {
        path: 'tagging/editor',
        name: 'Editor',
        component: () => import('../views/tagging/Editor.vue'),
        beforeEnter (to, from, next) {
          if (!store.getters.isAuthenticated) {
            next(`/login`)
          } else {
            next()
          }
        }
      },
      {
        path: 'tagging/modernizador',
        name: 'Atualiza',
        component: () => import('../views/tagging/Atualiza.vue'),
        beforeEnter (to, from, next) {
          if (!store.getters.isAuthenticated) {
            next(`/login`)
          } else {
            next()
          }
        }
      },
      {
        path: 'tagging/folioAnotado/ver/:id',
        name: 'Editor',
        component: () => import('../views/tagging/VerFolio.vue'),
        beforeEnter (to, from, next) {
          if (!store.getters.isAuthenticated) {
            next(`/login`)
          } else {
            next()
          }
        }
      },
      {
        path: 'tagging/folioAtualizado/ver/:id',
        name: 'Editor',
        component: () => import('../views/tagging/VerAtualizado.vue'),
        beforeEnter (to, from, next) {
          if (!store.getters.isAuthenticated) {
            next(`/login`)
          } else {
            next()
          }
        }
      },
      {
        path: 'tagging/tags/dicionario',
        name: 'Editor',
        component: () => import('../views/tagging/DicionarioTags.vue'),
        beforeEnter (to, from, next) {
          if (!store.getters.isAuthenticated) {
            next(`/login`)
          } else {
            next()
          }
        }
      },
      {
        path: 'tagging/anotaBase',
        name: 'AnotaBase',
        component: () => import('../views/tagging/AnotaBase.vue'),
        beforeEnter (to, from, next) {
          if (!store.getters.isAuthenticated) {
            next(`/login`)
          } else {
            next()
          }
        }
      },
      {
        path: 'tagging/tags/lista',
        name: 'Editor',
        component: () => import('../views/tagging/ListaTags.vue'),
        beforeEnter (to, from, next) {
          if (!store.getters.isAuthenticated) {
            next(`/login`)
          } else {
            next()
          }
        }
      },
      {
        path: 'tagging/regras/lista',
        name: 'Editor',
        component: () => import('../views/tagging/ListaRegras.vue'),
        beforeEnter (to, from, next) {
          if (!store.getters.isAuthenticated) {
            next(`/login`)
          } else {
            next()
          }
        }
      },
      {
        path: 'about',
        name: 'Acerca',
        component: () => import('../views/About.vue'),
        beforeEnter (to, from, next) {
          if (!store.getters.isAuthenticated) {
            next(`/login`)
          } else {
            next()
          }
        }
      },
      {
        path: 'import',
        name: 'Import',
        component: () => import('../views/Import.vue'),
        beforeEnter (to, from, next) {
          if (!store.getters.isAuthenticated) {
            next(`/login`)
          }
          else if (!store.getters.isAdmin) {
            next(`/homeAdmin`)
          }
          else {
            next()
          }
        }
      },
      {
        path: 'definitions',
        name: 'Definições',
        component: () => import('../views/Definitions.vue'),
        beforeEnter (to, from, next) {
          if (!store.getters.isAuthenticated) {
            next(`/login`)
          }
          else if (!store.getters.isAdmin) {
            next(`/homeAdmin`)
          }
          else {
            next()
          }
        }
      },
      {
        path: 'pedidos',
        name: 'Pedidos',
        component: () => import('../views/PedidosAcesso.vue'),
        beforeEnter (to, from, next) {
          if (!store.getters.isAuthenticated) {
            next(`/login`)
          }
          else if (!store.getters.isAdmin) {
            next(`/homeAdmin`)
          }
          else {
            next()
          }
        }
      },
      {
        path: 'analise',
        name: 'Analise',
        component: () => import('../views/AnáliseAdmin.vue'),
        beforeEnter (to, from, next) {
          if (!store.getters.isAuthenticated) {
            next(`/login`)
          } else {
            next()
          }
        }
      },
      {
        path: 'resultados',
        name: 'AdminResultados',
        component: () => import('../views/ResultadoAdmin.vue'),
        beforeEnter (to, from, next) {
          if (!store.getters.isAuthenticated) {
            next(`/login`)
          } else {
            next()
          }
        }
      },
      {
        path: 'homeAdmin',
        name: 'HomeAdmin',
        component: () => import('../views/HomeAdmin.vue'),
        beforeEnter (to, from, next) {
          if (!store.getters.isAuthenticated) {
            next(`/login`)
          }
          else {
            next()
          }
        }
      },
      {
        path: 'compFolios',
        name: 'CompFolios',
        component: () => import('../views/CompFolios.vue'),
        beforeEnter (to, from, next) {
          if (!store.getters.isAuthenticated) {
            next(`/login`)
          } else {
            next()
          }
        }
      },
      {
        path: 'documentacao',
        name: 'Documentação',
        component: () => import('../views/Documentacao.vue'),
        beforeEnter (to, from, next) {
          if (!store.getters.isAuthenticated) {
            next(`/login`)
          }
          else {
            next()
          }
        }
      },
      {
        path: 'histAcesso',
        name: 'HistorialAcesso',
        component: () => import('../views/HistorialAcesso.vue'),
        beforeEnter (to, from, next) {
          if (!store.getters.isAuthenticated) {
            next(`/login`)
          }
          else if (!store.getters.isAdmin) {
            next(`/homeAdmin`)
          }
          else {
            next()
          }
        }
      },
      {
        path: 'pesquisas',
        name: 'PesquisasRealizadas',
        component: () => import('../views/PesquisasRealizadas.vue'),
        beforeEnter (to, from, next) {
          if (!store.getters.isAuthenticated) {
            next(`/login`)
          }
          else if (!store.getters.isAdmin) {
            next(`/homeAdmin`)
          }
          else {
            next()
          }
        }
      },
      {
        path: 'uAtivos',
        name: 'UtilizadoresAtivos',
        component: () => import('../views/UtilizadoresAtivos.vue'),
        beforeEnter (to, from, next) {
          if (!store.getters.isAuthenticated) {
            next(`/login`)
          }
          else if (!store.getters.isAdmin) {
            next(`/homeAdmin`)
          }
          else {
            next()
          }
        }
      },
      {
        path: 'mapas',
        name: 'GoogleMap',
        component: () => import('../views/GoogleMap.vue'),
        beforeEnter (to, from, next) {
          if (!store.getters.isAuthenticated) {
            next(`/login`)
          }
          else {
            next()
          }
        }
      },
      {
        path: 'localidades',
        name: 'Places',
        component: () => import('../views/PlaceList.vue'),
        beforeEnter (to, from, next) {
          if (!store.getters.isAuthenticated) {
            next(`/login`)
          }
          else if (!store.getters.isAdmin) {
            next(`/homeAdmin`)
          }
          else {
            next()
          }
        }
      },
      {
        path: 'localidades/:nome',
        name: 'Place',
        component: () => import('../views/GoogleMapOnePlace.vue'),
        beforeEnter (to, from, next) {
          if (!store.getters.isAuthenticated) {
            next(`/login`)
          }
          else {
            next()
          }
        }
      },
      {
        path: 'processamento',
        name: 'Processamento',
        component: () => import('../views/ProgressBar.vue'),
        beforeEnter (to, from, next) {
          if (!store.getters.isAuthenticated) {
            next(`/login`)
          }
          else {
            next()
          }
        }
      }
    ]
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
