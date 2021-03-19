<template>
    <div id="indices">
        <v-sheet
        color="white"
        tile
        >
            <v-data-table
                :headers="headers"
                :items="indices"
                :sort-by="['_id','n_ocorrencias','ref']"
                :sort-desc="[false,false,true]"
                multi-sort            
            >
            </v-data-table>
            <v-tooltip bottom>
                <template v-slot:activator="{ on: tooltip }">
                    <v-btn @click.prevent="reset" v-on="{ ...tooltip}" class="ml-5"><v-icon>mdi-history</v-icon></v-btn>
                </template>
                <span>
                    {{$t('p1.reset')}}
                </span>
            </v-tooltip>
        </v-sheet>
    </div>
</template>
<script>

export default {
    data(){
        return{
            headers:[
                {
                    text: `${this.$t('ind.pal')}`,
                    align: 'start',
                    value: '_id'
                },
                {
                    text:`${this.$t('ind.oco')}`,
                    value: 'n_ocorrencias'
                },
                {
                    text:`${this.$t('ind.fol')}`,
                    value: 'ref'
                }
            ],
            indices:[],
            errors:[]
        }
    },
    props:{
        folio:{
            type:Object
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
            this.indices=this.folio.list
        },
        reset(){
            this.$emit('cancela')
        }
    },
    created() {
        this.onUpdate()
    }
}
</script>
<style scoped>
    #indices *{
            box-sizing: border-box;
    }
    #indices{
            margin: 20px auto;
            max-width: 800px;
    }
</style>