<template>
  <v-card>
    <v-navigation-drawer
      app
      clipped
      v-if="drawerOn"
      permanent
      :expand-on-hover="expandOnHover"
      :mini-variant="miniVariant"
      color="#2A3F54"
      class="navBar"
    >
      <v-list nav dense dark>
        <v-list-group
          class="white--text"
          prepend-icon="mdi-database"
          :value="false"
          no-action
        >
          <template v-slot:activator>
            <v-list-item-title class="white--text">{{
              $t("adminNav.tableBase")
            }}</v-list-item-title>
          </template>
          <v-list-item link to="/admin/folios">
            <v-list-item-title class="white--text">{{
              $t("adminNav.domains")
            }}</v-list-item-title>
          </v-list-item>
          <v-list-item link to="/admin/folios">
            <v-list-item-title class="white--text">{{
              $t("adminNav.subDomains")
            }}</v-list-item-title>
          </v-list-item>
          <v-list-item link to="/admin/compFolios">
            <v-list-item-title class="white--text">{{
              $t("adminNav.subSubDomanins")
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
          <v-list-item link to="/admin/folios">
            <v-list-item-title class="white--text">{{
              $t("adminNav.preQuestions")
            }}</v-list-item-title>
          </v-list-item>
          <v-list-item link to="/admin/folios">
            <v-list-item-title class="white--text">{{
              $t("adminNav.valQuestions")
            }}</v-list-item-title>
          </v-list-item>
          <v-list-item link to="/admin/compFolios">
            <v-list-item-title class="white--text">{{
              $t("adminNav.preModels")
            }}</v-list-item-title>
          </v-list-item>
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
          <v-list-item link to="/admin/folios">
            <v-list-item-title class="white--text">{{
              $t("adminNav.test")
            }}</v-list-item-title>
          </v-list-item>
          <v-list-item link to="/admin/folios">
            <v-list-item-title class="white--text">{{
              $t("adminNav.quizz")
            }}</v-list-item-title>
          </v-list-item>
        </v-list-group>

        <v-list-item link to="/admin/documentacao">
          <v-list-item-icon>
            <v-icon>mdi-card-account-details</v-icon>
          </v-list-item-icon>
          <v-list-item-title>{{ $t("adminNav.students") }}</v-list-item-title>
        </v-list-item>

        <v-list-group
          class="white--text"
          prepend-icon="mdi-gamepad-variant"
          :value="false"
          no-action
        >
          <template v-slot:activator>
            <v-list-item-title class="white--text">{{
              $t("adminNav.game")
            }}</v-list-item-title>
          </template>
          <v-list-item link to="/admin/folios">
            <v-list-item-title class="white--text">{{
              $t("adminNav.usr")
            }}</v-list-item-title>
          </v-list-item>
          <v-list-item link to="/admin/folios">
            <v-list-item-title class="white--text">{{
              $t("adminNav.domain")
            }}</v-list-item-title>
          </v-list-item>
          <v-list-item link to="/admin/compFolios">
            <v-list-item-title class="white--text">{{
              $t("adminNav.import")
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
              $t("adminNav.dataAnal")
            }}</v-list-item-title>
          </template>
          <v-list-item link to="/admin/folios">
            <v-list-item-title class="white--text">{{
              $t("adminNav.responseAnal")
            }}</v-list-item-title>
          </v-list-item>
          <v-list-item link to="/admin/folios">
            <v-list-item-title class="white--text">{{
              $t("adminNav.indivAnal")
            }}</v-list-item-title>
          </v-list-item>
          <v-list-item link to="/admin/folios">
            <v-list-item-title class="white--text">{{
              $t("adminNav.acessAnal")
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
              $t("adminNav.opi")
            }}</v-list-item-title>
          </template>
          <v-list-item link to="/admin/folios">
            <v-list-item-title class="white--text">{{
              $t("adminNav.inqAnal")
            }}</v-list-item-title>
          </v-list-item>
          <v-list-item link to="/admin/folios">
            <v-list-item-title class="white--text">{{
              $t("adminNav.propAnal")
            }}</v-list-item-title>
          </v-list-item>
        </v-list-group>

        <v-list-item link to="/admin/documentacao">
          <v-list-item-icon>
            <v-icon>mdi-account-multiple</v-icon>
          </v-list-item-icon>
          <v-list-item-title>{{ $t("adminNav.usr") }}</v-list-item-title>
        </v-list-item>
        
        <v-list-item link to="/admin/documentacao">
          <v-list-item-icon>
            <v-icon>mdi-format-list-numbered</v-icon>
          </v-list-item-icon>
          <v-list-item-title>{{ $t("adminNav.events") }}</v-list-item-title>
        </v-list-item>

        <v-list-item link to="/admin/documentacao">
          <v-list-item-icon>
            <v-icon>mdi-cog</v-icon>
          </v-list-item-icon>
          <v-list-item-title>{{ $t("adminNav.sett") }}</v-list-item-title>
        </v-list-item>

        <v-list-item link to="/admin/documentacao">
          <v-list-item-icon>
            <v-icon>mdi-text-box-multiple</v-icon>
          </v-list-item-icon>
          <v-list-item-title>{{ $t("adminNav.doc") }}</v-list-item-title>
        </v-list-item>

        <v-list-item link to="/admin/documentacao">
          <v-list-item-icon>
            <v-icon>mdi-information-outline</v-icon>
          </v-list-item-icon>
          <v-list-item-title>{{ $t("adminNav.about") }}</v-list-item-title>
        </v-list-item>

        <v-list-item link to="/admin/documentacao">
          <v-list-item-icon>
            <v-icon>mdi-clipboard-account-outline</v-icon>
          </v-list-item-icon>
          <v-list-item-title>{{ $t("adminNav.use") }}</v-list-item-title>
        </v-list-item>

        <v-list-item link to="/admin/documentacao">
          <v-list-item-icon>
            <v-icon>mdi-lock</v-icon>
          </v-list-item-icon>
          <v-list-item-title>{{ $t("adminNav.privacy") }}</v-list-item-title>
        </v-list-item>
      
      </v-list>
      <!-- <template v-slot:append v-if="hover == true"> -->
      <template v-slot:append>
        <div class="pa-2">
          <v-tooltip top>
            <template v-slot:activator="{ on }">
              <v-btn
                dark
                depressed
                min-width="60px"
                @click="fixNav()"
                v-on="on"
              >
                <v-icon>mdi-axis-arrow-lock</v-icon>
              </v-btn>
            </template>
            <span>{{ $t("navd.fixMenu") }}</span>
          </v-tooltip>
          <v-tooltip top>
            <template v-slot:activator="{ on }">
              <v-btn
                dark
                depressed
                min-width="60px"
                @click="logout()"
                v-on="on"
              >
                <v-icon>mdi-power</v-icon>
              </v-btn>
            </template>
            <span>{{ $t("navd.exit") }}</span>
          </v-tooltip>
        </div>
      </template>
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
      // hover:false
    };
  },
  created() {
    axios
      .get(
        `https://leonardo2.di.uminho.pt/api/users/foto/${this.$store.state.user._id}`,
        {
          responseType: "arraybuffer",
          headers: {
            Authorization: `Bearer: ${this.$store.state.jwt}`,
          },
        }
      )
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
  methods: {
    reindFunc: function () {
      axios
        .get(`https://leonardo2.di.uminho.pt/api/import/reindex/`, {
          headers: {
            Authorization: `Bearer: ${this.$store.state.jwt}`,
          },
        })
        .then((response) => {
          // JSON responses are automatically parsed.
          //console.log(response.data)
          if (response.data.message === "ok") {
            axios
              .get(
                `https://leonardo2.di.uminho.pt/api/folios/folios?nome=${this.$store.state.user._id}`,
                {
                  headers: {
                    Authorization: `Bearer: ${this.$store.state.jwt}`,
                  },
                }
              )
              .then((response) => {
                this.nDocs = response.data.folios.length;
              })
              .catch((e) => {
                this.errors.push(e);
              });
            axios
              .get(
                `https://leonardo2.di.uminho.pt/api/folios/index?nome=${this.$store.state.user._id}`,
                {
                  headers: {
                    "Content-Type": "multipart/form-data",
                    Authorization: `Bearer: ${this.$store.state.jwt}`,
                  },
                }
              )
              .then((response) => {
                this.nInds = response.data.indexs.length;
              })
              .catch((e) => {
                this.errors.push(e);
              });
            this.runningDialog = false;
            this.successDialog = true;
          } else {
            alert("Algo correu mal");
          }
        })
        .catch((e) => {
          //console.log(e)
          this.errors.push(e);
        });
    },
    logout: function () {
      //console.log("destroy token here")
      this.$store.commit("guardaTokenUtilizador", "");
      this.$store.commit("guardaNomeUtilizador", "");
      this.$router.push({ path: `/admin/login` });
    },
    fixNav: function () {
      this.expandOnHover = !this.expandOnHover;
      this.miniVariant = !this.miniVariant;
      this.drawerOn = false;
      this.$nextTick(() => (this.drawerOn = true));
    },
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
