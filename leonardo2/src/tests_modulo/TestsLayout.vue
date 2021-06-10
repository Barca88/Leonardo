<template>
  <div>
    <AppHeader />
    <SideNav />
    <v-main>
      <router-view />
    </v-main>
    <Footer />
  </div>
</template>

<script>
import AppHeader from "@/tests_modulo/components/Layout/AppHeader.vue";
import SideNav from "@/tests_modulo/components/Layout/SideNav.vue";
import Footer from "@/tests_modulo/components/Layout/Footer.vue";

export default {
  name: "App",
  components: { AppHeader, SideNav, Footer },
};
</script>
