<template>
  <v-card>
    <v-navigation-drawer
      app
      clipped
      v-if="drawerOn"
      color="#2A3F54"
      class="navBar"
    >
      <v-list nav dense dark>
        <v-list-item link to="/home">
          <v-list-item-icon>
            <v-icon>mdi-home</v-icon>
          </v-list-item-icon>
          <v-list-item-title>{{ $t("adminNav.home") }}</v-list-item-title>
        </v-list-item>

        <v-list-group
          class="white--text"
          prepend-icon="mdi-database"
          :value="false"
          no-action
        >
          <template v-slot:activator>
            <v-list-item-title class="white--text">{{
              $t("adminNav.infoBase")
            }}</v-list-item-title>
          </template>
          <v-list-item link to="/home">

            <v-list-item-title class="white--text">{{
              $t("adminNav.resp")
            }}</v-list-item-title>
          </v-list-item>
          <v-list-item link to="/home/">
            <v-list-item-title class="white--text">{{
              $t("adminNav.prof")
            }}</v-list-item-title>
          </v-list-item>
          <v-list-item link to="/home/">
            <v-list-item-title class="white--text">{{
              $t("adminNav.student")
            }}</v-list-item-title>
          </v-list-item>
          <v-list-item link to="/home">
            <v-list-item-title class="white--text">{{
              $t("adminNav.domain")
            }}</v-list-item-title>
          </v-list-item>
          <v-list-item link to="/home">
            <v-list-item-title class="white--text">{{
              $t("adminNav.questions")
            }}</v-list-item-title>
          </v-list-item>
          <v-list-item link to="/home">
            <v-list-item-title class="white--text">{{
              $t("adminNav.tests")
            }}</v-list-item-title>
          </v-list-item>
        </v-list-group>

        <v-list-group
          class="white--text"
          prepend-icon="mdi-wrench"
          :value="false"
          no-action
        >
          <template v-slot:activator>
            <v-list-item-title class="white--text">{{
              $t("adminNav.prod")
            }}</v-list-item-title>
          </template>
          <v-list-item link to="/home">
            <v-list-item-title class="white--text">{{
              $t("adminNav.domain")
            }}</v-list-item-title>
          </v-list-item>
          <v-list-item link to="/home">
            <v-list-item-title class="white--text">{{
              $t("adminNav.questions")
            }}</v-list-item-title>
          </v-list-item>
          <v-list-item link to="/tests/management">
            <v-list-item-title class="white--text">{{
              $t("adminNav.tests")
            }}</v-list-item-title>
          </v-list-item>
        </v-list-group>

        <v-list-group
          class="white--text"
          prepend-icon="mdi-check-bold"
          :value="false"
          no-action
        >
          <template v-slot:activator>
            <v-list-item-title class="white--text">{{
              $t("adminNav.ver")
            }}</v-list-item-title>
          </template>
          <!-- ROTA DA IMPORTAÇÃO  -->
          <v-list-item link to="/importacao/import">
            <v-list-item-title class="white--text">{{
              $t("adminNav.imp")
            }}</v-list-item-title>
          </v-list-item>
          <v-list-item link to="/importacao/table">
            <v-list-item-title class="white--text">{{
              $t("adminNav.verquest")
            }}</v-list-item-title>
          </v-list-item>
          <v-list-item link to="/importacao/errors">
            <v-list-item-title class="white--text">{{
              $t("adminNav.valida")
            }}</v-list-item-title>
          </v-list-item>

          <v-list-item link to="/importacao/dashboard">
            <v-list-item-title class="white--text">{{
              $t("adminNav.impdashboard")
            }}</v-list-item-title>
          </v-list-item>
          <!-- 
          <v-list-item link to="/importacao/config">
            <v-list-item-title class="white--text">{{
              $t("adminNav.conf")
            }}</v-list-item-title>
          </v-list-item>
          -->
        </v-list-group>

        <v-list-group
          class="white--text"
          prepend-icon="mdi-school"
          :value="false"
          no-action
        >
          <template v-slot:activator>
            <v-list-item-title class="white--text">{{
              $t("adminNav.av")
            }}</v-list-item-title>
          </template>
          <v-list-item link to="/tests/evaluation">
            <v-list-item-title class="white--text">{{
              $t("adminNav.test")
            }}</v-list-item-title>
          </v-list-item>
          <v-list-item link to="/home">
            <v-list-item-title class="white--text">{{
              $t("adminNav.quizz")
            }}</v-list-item-title>
          </v-list-item>
        </v-list-group>

        <v-list-group
          class="white--text"
          prepend-icon="mdi-wechat"
          :value="false"
          no-action
        >
          <template v-slot:activator>
            <v-list-item-title class="white--text">{{
              $t("adminNav.opi")
            }}</v-list-item-title>
          </template>
          <v-list-item link to="/home">
            <v-list-item-title class="white--text">{{
              $t("adminNav.inqsis")
            }}</v-list-item-title>
          </v-list-item>
          <v-list-item link to="/home">
            <v-list-item-title class="white--text">{{
              $t("adminNav.inqAnal")
            }}</v-list-item-title>
          </v-list-item>
          <v-list-item link to="/home">
            <v-list-item-title class="white--text">{{
              $t("adminNav.estPro")
            }}</v-list-item-title>
          </v-list-item>
          <v-list-item link to="/home">
            <v-list-item-title class="white--text">{{
              $t("adminNav.sentEx")
            }}</v-list-item-title>
          </v-list-item>
        </v-list-group>

        <v-list-group
          class="white--text"
          prepend-icon="mdi-trophy-variant"
          :value="false"
          no-action
        >
          <template v-slot:activator>
            <v-list-item-title class="white--text">{{
              $t("adminNav.game")
            }}</v-list-item-title>
          </template>
          <v-list-item link to="/home">
            <v-list-item-title class="white--text">{{
              $t("adminNav.domain")
            }}</v-list-item-title>
          </v-list-item>
          <v-list-item link to="/home">
            <v-list-item-title class="white--text">{{
              $t("adminNav.student")
            }}</v-list-item-title>
          </v-list-item>
        </v-list-group>

        <v-list-group
          class="white--text"
          prepend-icon="mdi-chart-bar"
          :value="false"
          no-action
        >
          <template v-slot:activator>
            <v-list-item-title class="white--text">{{
              $t("adminNav.dash")
            }}</v-list-item-title>
          </template>
          <v-list-item link to="/home">
            <v-list-item-title class="white--text">{{
              $t("adminNav.student")
            }}</v-list-item-title>
          </v-list-item>
          <v-list-item link to="/tests/results">
            <v-list-item-title class="white--text">{{
              $t("adminNav.ans")
            }}</v-list-item-title>
          </v-list-item>
          <v-list-item link to="/home">
            <v-list-item-title class="white--text">{{
              $t("adminNav.acess")
            }}</v-list-item-title>
          </v-list-item>
        </v-list-group>

        <v-list-group
          class="white--text"
          prepend-icon="mdi-account-multiple"
          :value="false"
          no-action
        >
          <template v-slot:activator>
            <v-list-item-title class="white--text">{{
              $t("adminNav.usr")
            }}</v-list-item-title>
          </template>
          <v-list-item link to="/users">
            <v-list-item-title class="white--text">{{
              $t("adminNav.ges")
            }}</v-list-item-title>
          </v-list-item>
          <v-list-item link to="/pedidos">
            <v-list-item-title class="white--text">{{
              $t("adminNav.ped")
            }}</v-list-item-title>
          </v-list-item>
          <v-list-item link to="/usersImport">
            <v-list-item-title class="white--text">{{
              $t("adminNav.import")
            }}</v-list-item-title>
          </v-list-item>
          <v-list-item link to="/uAtivos">
            <v-list-item-title class="white--text">{{
              $t("adminNav.ati")
            }}</v-list-item-title>
          </v-list-item>
          <v-list-item link to="/historico">
            <v-list-item-title class="white--text">{{
              $t("adminNav.hist")
            }}</v-list-item-title>
          </v-list-item>
        </v-list-group>

        <v-list-group
          class="white--text"
          prepend-icon="mdi-clock"
          :value="false"
          no-action
        >
          <template v-slot:activator>
            <v-list-item-title class="white--text">{{
              $t("adminNav.events")
            }}</v-list-item-title>
          </template>
          <v-list-item link to="/home">
            <v-list-item-title class="white--text">{{
              $t("adminNav.ges")
            }}</v-list-item-title>
          </v-list-item>
          <v-list-item link to="/home">
            <v-list-item-title class="white--text">{{
              $t("adminNav.agend")
            }}</v-list-item-title>
          </v-list-item>
        </v-list-group>

        <v-list-group
          class="white--text"
          prepend-icon="mdi-cog"
          :value="false"
          no-action
        >
          <template v-slot:activator>
            <v-list-item-title class="white--text">{{
              $t("adminNav.sett")
            }}</v-list-item-title>
          </template>
          <v-list-item link to="/home">
            <v-list-item-title class="white--text">{{
              $t("adminNav.confger")
            }}</v-list-item-title>
          </v-list-item>
        </v-list-group>

        <v-list-item link to="/home">
          <v-list-item-icon>
            <v-icon>mdi-text-box-multiple</v-icon>
          </v-list-item-icon>
          <v-list-item-title>{{ $t("adminNav.doc") }}</v-list-item-title>
        </v-list-item>

        <v-list-item link @click="about = true">
              <v-list-item-icon>
                <v-icon>mdi-information-outline</v-icon>
              </v-list-item-icon>
              <v-list-item-title>{{$t('adminNav.about')}}</v-list-item-title>
        </v-list-item>

        <v-dialog @keydown.esc="about = false" v-model="about" scrollable width="500">
              <v-card>
                <v-toolbar color="#2A3F54" dark>
                  <h2>{{ $t('nav.sabermais') }}</h2>
                </v-toolbar>

                <v-divider
                class="mx-4"
                horizontal
              ></v-divider>
                <v-card-text class="change-font mt-6" style="white-space: pre-line"
                  >{{ $t('nav.textoSaberMais') }}</v-card-text
                >
                <v-card-actions>
                  <v-spacer></v-spacer>
                  
                  <v-tooltip bottom> 
                    <template v-slot:activator="{ on }">
                        <v-btn depressed color="white" @click="about=false" v-on="on">
                          <v-icon large>mdi-exit-to-app</v-icon>
                        </v-btn>
                      </template>
                      <span>{{ $t('nav.Sair') }}</span>
                    </v-tooltip>

                </v-card-actions>
              </v-card>
        </v-dialog>

        <v-list-item link @click="credits = true">
              <v-list-item-icon>
                <v-icon>mdi-account-group</v-icon>
              </v-list-item-icon>
              <v-list-item-title>{{$t('navd.credits')}}</v-list-item-title>
            </v-list-item>
            <v-dialog @keydown.esc="credits = false"  v-model="credits" scrollable width="500">
              <v-card>
                <v-toolbar color="#2A3F54" dark>
                  <h2>{{ $t('nav.creditos') }}</h2>
                </v-toolbar>
                
                <v-divider
                class="mx-4"
                horizontal
                ></v-divider>
                
                <v-card-text class="change-font mt-6" style="white-space: pre-line"
                  >{{ $t('nav.textoCreditos') }}</v-card-text
                >
                <v-card-actions>
                  <v-spacer></v-spacer>
                  
                  <v-tooltip bottom> 
                    <template v-slot:activator="{ on }">
                        <v-btn depressed color="white" @click="credits=false" v-on="on">
                          <v-icon large>mdi-exit-to-app</v-icon>
                        </v-btn>
                      </template>
                      <span>{{ $t('nav.Sair') }}</span>
                    </v-tooltip>

                </v-card-actions>
              </v-card>
            </v-dialog>

        <v-list-item link @click="terms = true">
              <v-list-item-icon>
                <v-icon>mdi-book-multiple</v-icon>
              </v-list-item-icon>
              <v-list-item-title>{{$t('navd.terms')}}</v-list-item-title>
            </v-list-item>
            <v-dialog @keydown.esc="terms = false" v-model="terms" scrollable  width="500">
              <v-card>
                <v-toolbar color="#2A3F54" dark>
                  <h2>{{ $t('nav.termos') }}</h2>
                </v-toolbar>

                <v-divider
                class="mx-4"
                horizontal
              ></v-divider>

                <v-card-text class="change-font mt-6" style="white-space: pre-line"
                  >{{ $t('nav.textoTermos') }}</v-card-text
                >
                <v-card-actions>
                  <v-spacer></v-spacer>
                  
                  <v-tooltip bottom> 
                    <template v-slot:activator="{ on }">
                        <v-btn depressed color="white" @click="terms=false" v-on="on">
                          <v-icon large>mdi-exit-to-app</v-icon>
                        </v-btn>
                      </template>
                      <span>{{ $t('nav.Sair') }}</span>
                    </v-tooltip>

                </v-card-actions>
              </v-card>
          </v-dialog>

        <v-list-item link @click="priv = true">
              <v-list-item-icon>
                <v-icon>mdi-lock</v-icon>
              </v-list-item-icon>
              <v-list-item-title>{{$t('navd.priv')}}</v-list-item-title>
            </v-list-item>
            <v-dialog @keydown.esc="priv = false" v-model="priv" scrollable width="500"> 
              <v-card>
                <v-toolbar color="#2A3F54" dark>
                  <h2>{{ $t('nav.privacidade') }}</h2>
                </v-toolbar>
                <v-divider
                class="mx-4"
                horizontal
              ></v-divider>

                <v-card-text class="change-font mt-6" style="white-space: pre-line"
                  >{{ $t('nav.textoPriv') }}</v-card-text
                >
                <v-card-actions>
                  <v-spacer></v-spacer>
                  
                  <v-tooltip bottom> 
                    <template v-slot:activator="{ on }">
                        <v-btn depressed color="white" @click="priv=false" v-on="on">
                          <v-icon large>mdi-exit-to-app</v-icon>
                        </v-btn>
                      </template>
                      <span>{{ $t('nav.Sair') }}</span>
                    </v-tooltip>

                </v-card-actions>
              </v-card>
            </v-dialog>
          </v-list>
    </v-navigation-drawer>
  </v-card>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      title: "Vue",
      userPic: "",
      nome: this.$store.state.user._id,
      miniVariant: true,
      expandOnHover: true,
      drawerOn: true,
      reindexar: false,
      priv: false,
      terms: false,
      credits: false,
      about: false,
      successDialog: false,
      nDocs: 0,
      nInds: 0,
      runningDialog: false,
    };
  },
  created() {
    axios
      .get(`${process.env.VUE_APP_BACKEND}/users/foto/${this.$store.state.user._id}`, {
        responseType: "arraybuffer",
        headers: {
          Authorization: `Bearer: ${this.$store.state.jwt}`,
        },
      })
      .then((response) => {
        var image = new Buffer(response.data, "binary").toString("base64");
        this.userPic = `data:${response.headers[
          "content-type"
        ].toLowerCase()};base64,${image}`;
      })
      .catch((e) => {
        //console.log(e)
        this.errors.push(e);
      });
  },
};
</script>

<style scoped>
header {
  background: #2a3f54;
  padding: 10px;
}

h1 {
  color: white;
  text-align: center;
}
.navBar {
  text-align: left;
}
.ava {
  margin-top: 50px;
}
</style>