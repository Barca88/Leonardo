<template>
    <div>
        <appHeader :ajuda='ajuda'></appHeader>
        <navDraw ></navDraw> 
        <h1 class="pa-md-4 mx-lg-auto text-center " > 👷 Serviço em Desenvolvimento </h1>
    </div>
</template>

<script>
import NavDraw from '../components/navDraw.vue'
import Header from '../components/header.vue'

export default {
    data() { return {}},
    components:{
        'appHeader': Header,
        'navDraw':NavDraw
    }
}
</script>
