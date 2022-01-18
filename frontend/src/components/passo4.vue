<template>
    <div id="tags">
        <v-sheet
        color="white"
        tile
        >
            <v-data-table
                :headers="headers"
                :items="tags"
                :sort-by="['tag','n_ocorrencias','ref']"
                :sort-desc="[false,false,true]"
                multi-sort            
            ></v-data-table>
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
                    text: `${this.$t('tags.tag')}`,
                    align: 'start',
                    value: 'tag'
                },
                {
                    text:`${this.$t('tags.oco')}`,
                    value: 'n_ocorrencias'
                },
                {
                    text:`${this.$t('tags.fol')}`,
                    value: 'ref'
                }
            ],
            tags:[],
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
            this.tags=this.folio.tags
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
    #tags *{
            box-sizing: border-box;
    }
    #tags{
            margin: 20px auto;
            max-width: 800px;
    }
</style>