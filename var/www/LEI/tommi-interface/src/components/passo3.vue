<template>
    <div>
        <v-sheet
        color="white"
        tile
        >
            <v-row
            class="fill-height"
            align="center"
            justify="center"
            >
                <v-card flat width="800">
                <v-card-actions>
                    <v-img v-if="foto" :src="foto" contain aspect-ratio="2"/>
                </v-card-actions>
                </v-card>
            </v-row>
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
            foto: null
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
            if (this.folio.foto.size > 0){
                const file = this.folio.foto;
                this.foto = URL.createObjectURL(file)
            }
            else this.foto = null
        },
        reset(){
            this.$emit('cancela')
        }
    },
    created(){
        this.onUpdate()
    }
}
</script>