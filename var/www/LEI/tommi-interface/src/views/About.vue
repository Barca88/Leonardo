<template>
    <div id="aboutPage">
        <appHeader :ajuda='ajuda'></appHeader>
        <div v-if="this.$store.state.user.tipo === 'Admin'" >
            <navDraw></navDraw>
        </div>
        <div v-else>
            <navDrawLeitor></navDrawLeitor>
        </div>
        <h1>{{$t('ab.question')}}</h1>
        <article>{{blog.body}}</article>
    </div>
</template>

<script>
import Header from '../components/header.vue'
import NavDraw from '../components/navDraw.vue'
import navDrawLeitor from '../components/navDrawLeitor.vue'
export default {
    data(){
        return{
            blog:{
                body:'História do Tommi'
            },
            ajuda:'about'
        }
    },components:{
        'appHeader': Header,
        'navDrawLeitor':navDrawLeitor,
        'navDraw':NavDraw
    }
}
</script>

<style scoped>
#aboutPage{
    max-width: 960px;
    margin: 0 auto;
    margin-bottom: 50px;
}
</style>