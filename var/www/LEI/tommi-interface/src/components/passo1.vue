<template>
  <div>
    <v-sheet
      color="grey lighten-4"
      height="900"
      tile
    >
      <v-row
        class="fill-height ml-10"
        align="center"
        justify="center"
      >
        <v-col class="text-left">
          <v-form ref="form" method="post" enctype="multipart/form-data" style="width:500px">
              <v-container >
                <v-text-field
                    :label="$t('p1.id')"
                    v-model="idFolio"
                    :rules="[rules.inicioNome, rules.umHifen]"
                    required
                ></v-text-field>
                <v-text-field           
                    :label="$t('p1.desc')"
                    v-model="descricao"
                    required
                ></v-text-field>
                <v-container fluid>
                  <label>{{$t('p1.tipo')}}</label>
                  <v-radio-group v-model="tipo" row>
                      <v-radio value="rosto"></v-radio>
                      <v-radio :label="$t('p1.fre') + ' ' + $t('imp.or') + ' ' + $t('p1.v')" value="verso"></v-radio>
                  </v-radio-group>
                </v-container>
                <v-container fluid>
                  <label>{{$t('p1.ver')}}</label>
                  <v-radio-group v-model="versao" row>
                      <v-radio value="interpretativa"></v-radio>
                      <v-radio :label="$t('p1.int') + ' ' + $t('imp.or') + ' ' + $t('p1.sd')" value="semidiplomática"></v-radio>
                  </v-radio-group>
                </v-container>
                <v-container fluid>
                  <label>{{$t('p1.sum')}}</label>
                  <v-radio-group v-model="sumario" row>
                      <v-radio value="transcrição"></v-radio>
                      <v-radio :label="$t('p1.trans') + ' ' + $t('imp.or') + ' ' + $t('p1.rev')" value="revisão"></v-radio>
                  </v-radio-group>
                </v-container>
                <v-row align="center">
                    <label>{{$t('p1.foto')}}:</label>
                    <v-file-input show-size
                      accept="image/jpg, image/jpeg, image/png"
                      :label="$t('p1.f')" 
                      v-model="foto">
                    </v-file-input>
                </v-row>
                <v-row align="center">
                    <label>{{$t('p1.file')}}:</label>
                    <v-file-input show-size type="file" :label="$t('p1.tfile')" v-model="ficheiro"></v-file-input>
                </v-row>
                <v-text-field                
                    :label="$t('p1.obs')"
                    v-model="obs"
                ></v-text-field>
              </v-container>
          
          <v-container style="width:750px">
            <v-toolbar flat color="grey lighten-4">
              <v-tooltip bottom>
                <template v-slot:activator="{ on: tooltip }">
                    <v-btn @click.prevent="reset" v-on="{ ...tooltip}" class="mr-3"><v-icon>mdi-history</v-icon></v-btn>
                </template>
                <span>
                    {{$t('p1.reset')}}
                </span>
              </v-tooltip>
              <v-tooltip bottom>
                <template v-slot:activator="{ on: tooltip }">
                    <v-btn ref="submit" color="#26B99A" class="white--text mr-3" @click="save();" :disabled="disableButton" v-on="{ ...tooltip}"><v-icon>mdi-check</v-icon></v-btn>
                </template>
                <span>
                    {{$t('p1.sub')}}
                </span>
              </v-tooltip>
              <v-tooltip bottom>
                <template v-slot:activator="{ on: tooltip }">
                    <v-btn ref="skip" @click="saveSkip();" class="orange white--text" :disabled="disableButton" v-on="{ ...tooltip}"><v-icon>mdi-check-all</v-icon></v-btn>
                </template>
                <span>
                    {{$t('p1.skip')}}
                </span>
              </v-tooltip>
              <v-spacer></v-spacer>
              <v-tooltip bottom>
                <template v-slot:activator="{ on: tooltip }">
                    <v-btn @click="dialog=true" v-on="{ ...tooltip}" class="mr-5"><v-icon>mdi-help</v-icon></v-btn>
                </template>
                <span>
                    {{$t('p1.ajuda')}}
                </span>
              </v-tooltip>
              <v-dialog @keydown.esc="dialog = false"  v-model="dialog" scrollable width="500">
              <v-card>
                <v-toolbar color="#2A3F54" dark>
                  <h3>{{$t('navd.importAjuda')}}</h3>
                </v-toolbar>
                <v-divider
                class="mx-4"
                horizontal
                ></v-divider>
                
                <v-card-text class="change-font mt-6" style="white-space: pre-line"
                  >{{ $t('navd.textoImportAjuda') }}</v-card-text
                >
                <v-card-actions>
                  <v-spacer></v-spacer>
                  
                  <v-tooltip bottom> 
                    <template v-slot:activator="{ on }">
                        <v-btn depressed color="white" @click="dialog=false" v-on="on">
                          <v-icon large>mdi-exit-to-app</v-icon>
                        </v-btn>
                      </template>
                      <span>{{ $t('nav.Sair') }}</span>
                    </v-tooltip>

                </v-card-actions>
              </v-card>
            </v-dialog>
              <v-tooltip bottom>
                <template v-slot:activator="{ on: tooltip }">
                    <v-btn link to="/admin/folios" v-on="{ ...tooltip}" class="mr-12"><v-icon>mdi-exit-to-app</v-icon></v-btn>
                </template>
                <span>
                    {{$t('p1.leave')}}
                </span>
              </v-tooltip>
            </v-toolbar>
          </v-container>
          </v-form>
        </v-col>
      </v-row>
    </v-sheet>
  </div>
</template>
<script>
//depois usar para estabelecer as rules dos campos do form
//import { required, email, max } from 'vee-validate/dist/rules'
//import { extend, ValidationObserver, ValidationProvider, setInteractionMode } from 'vee-validate'
// @ is an alias to /src

export default {
  data(){
    return{
      idFolio:"",
      versao:"",
      tipo:"",
      descricao:"",
      obs:"",
      sumario:"",
      foto:{},
      ficheiro:{},
      skip:0,
      dialog:false,
      rules: {
        inicioNome: value => value.startsWith("TM-F") || 'O nome do Fólio necessita de começar com TM-F',
        umHifen: value => value.split("-").length - 1 == 1 || 'O nome do Fólio não pode ter mais hífens'
      }
    }
  },
  props:{
    folio: {
      type: Object
    }
  },
  created (){
    this.idFolio=this.folio.idFolio
    this.versao=this.folio.versao
    this.tipo=this.folio.tipo
    this.descricao=this.folio.descricao
    this.obs=this.folio.obs
    this.sumario=this.folio.sumario
    this.foto=this.folio.foto
    this.ficheiro=this.folio.ficheiro
  },
  methods: {
    reset () {
      //needs work for more resets
      this.$refs.form.reset()
      this.idFolio = "",
      this.versao = "",
      this.tipo = "",
      this.obs = "",
      this.descricao = "",
      this.sumario = "",
      this.foto = null,
      this.ficheiro = null
    },
    save (){
      this.$emit('atualizaFolio', this)
    },
    saveSkip (){
      this.skip = 1
      //console.log(this.skip)
      this.$emit('atualizaFolio', this)
    }
    
    /*
    atualizarInfo(){
      this.$emit('atualizarInfoPasso1','skip')
    }*/
  },
  computed:{
    disableButton (){
      if (this.idFolio.length > 1 && this.versao && this.tipo && this.descricao.length > 0 && this.sumario && this.ficheiro )
        return false
      else
        return true
    } 
  }
}
</script>
<style scoped>
  .v-text-field /deep/ label{
        font-size: 20px;
    }
</style>