<template>
    <div>
        <v-sheet
        color="grey lighten-4"
        height="635"
        tile
        >
            <v-row
            class="fill-height"
            align="center"
            justify="center"
            >
                <v-card flat height="633" width="400" class="scroll">
                    <strong class="title ml-5">{{$t('p2.tComTags')}}</strong>
                    <v-card-text>
                        {{textoTags}}
                    </v-card-text>
                </v-card>
                <v-card flat height="633" width="400" class="scroll">
                    <strong class="title ml-5">{{$t('p2.tSemTags')}}</strong>
                    <v-card-text>
                        {{textoSTags}}
                    </v-card-text>
                <!-- <v-tooltip bottom>
                    <template v-slot:activator="{ on: tooltip }">
                        <v-btn @click.prevent="reset" v-on="{ ...tooltip}" class="ml-5"><v-icon>mdi-history</v-icon></v-btn>
                    </template>
                    <span>
                        {{$t('p1.reset')}}
                    </span>
                </v-tooltip> -->
                </v-card>
            </v-row>
        </v-sheet>
    </div>
</template>
<script>
export default {
    data(){
        return{
            textoTags:"",
            textoSTags:""
        }
    },
    props:{
        folio: {
            type: Object
        }
    },
    watch:{
        folio: {
            immediate: true,
            deep: true,
            handler(){
                this.onUpdate()
            }
        }
    },
    methods:{
        onUpdate(){
            this.textoTags=this.folio.textoTags
            this.textoSTags=this.folio.textoSTags
        },
        reset(){
            this.$emit('cancela')
        }
    },
    created (){
        this.onUpdate()
    }
}
</script>
<style scoped>
.scroll{
    overflow-y:scroll
}

</style>