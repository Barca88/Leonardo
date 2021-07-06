<template>
    <div>
         <navDraw></navDraw>
        <appHeader></appHeader>
        <h1 class="pa-md-4 mx-lg-auto text-center " > 404 - Página não encontrada </h1>
    </div>
</template>

<script>
import Header from '../components/header.vue'
import NavDraw from '../components/navDraw.vue'
export default {
    data() { return {}},
    components:{
            'appHeader': Header,
            'navDraw':NavDraw
    },
}
</script>
